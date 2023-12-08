from io import StringIO
from pathlib import Path
from typing import List, Tuple, Dict, Union

import configured_mail_sender
from configured_mail_sender import create_sender, MailSender, known_domains
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from breeze_chms_api.profile_helper import ProfileHelper, join_dicts, profile_compare
from breeze_chms_api import breeze

import logging
import sys
import json
import gzip
import argparse
import os
import platformdirs
import datetime

from breeze_email_reports.table_format import ColSpec, _HTMLFormatter, _CSVFormatter, _TextFormatter

DEFAULT_DATA_DIR = platformdirs.user_data_dir('BreezeProfiles')
DEFAULT_COLUMN_WIDTHS = '30,20,20'

APPLICATION_NAME = 'email_profile_report'
DEFAULT_LOG_FILE = os.path.join(platformdirs.user_log_dir(), APPLICATION_NAME + '.log')


class ProfileData:
    def __init__(self):
        self.datetime_str = 'Unknown'
        self.fields_map = {}
        self.profiles = {}

    def get_datetime(self) -> str:
        """
        Get time of this data dump
        :return: Date time in iso format
        """
        return self.datetime_str

    def get_fields_map(self) -> Dict[str, Dict[str, Union[str, List[str]]]]:
        """
        Get mapping from field id to name
        :return: The mapping
        """
        return self.fields_map

    def get_profile_fields(self) -> Dict[str, Dict[str, Union[str, List[str]]]]:
        """
        Return profile field values as list of tuples. First item in each tuple
        is the profile id. Second is a mapping from field id to Value(s) of
        the field.
        :return: List of profiles with their field values
        """
        return self.profiles

    def save_data(self) -> None:
        """
        Save current data to a new file in the given directory,
        if this was freshly loaded from Breeze.
        :return: None
        """
        return


class ProfileFromBreeze(ProfileData):
    """
    Profile data fetched directly from Breeze.
    """

    def __init__(self,
                 args,
                 breeze_api: breeze.BreezeApi = None,
                 do_save: bool = True):
        """
        Get current data from breeze
        :param args: Command line arguments
        :param breeze_api: Pre-existing Breeze API
        :param do_save: Save results on completion
        """
        ProfileData.__init__(self)
        self.do_save = do_save
        self.args = args
        ProfileData.__init__(self)
        breeze_api = breeze_api if breeze_api \
            else breeze.breeze_api(overrides=args.breeze_creds)
        profile_helper = ProfileHelper(breeze_api.get_profile_fields())
        self.fields_map = profile_helper.get_field_id_to_name()
        people = breeze_api.list_people(details=True)
        self.profiles = profile_helper.process_profiles(people)
        curtime = datetime.datetime.now()
        self.save_file_name = (datetime.datetime.isoformat(curtime)
                               + '.json.gz')
        self.datetime_str = curtime.strftime("%b %d %Y %I:%M%p")

    def save_data(self) -> None:
        if self.do_save:
            new_file = os.path.join(self.args.data, self.save_file_name)
            with gzip.open(new_file, 'w') as outfile:
                towrite = json.dumps((self.fields_map, self.profiles), indent=2)
                outfile.write(bytes(towrite, 'utf8'))
            if self.args.retain_days > 0:
                # We need to clean up old files
                oldest_allowed = (datetime.datetime.now()
                                  - datetime.timedelta(days=self.args.retain_days)
                                  ).isoformat()
                now_files = _get_previous_files(self.args)
                too_old = [f for f in now_files
                           if f < oldest_allowed]
                for file in too_old:
                    path = os.path.join(self.args.data, file)
                    logging.info(f'Removing old data: {file}')
                    os.remove(path)


class ProfileFromFile(ProfileData):
    """
    Profile data loaded from a file.
    """

    def __init__(self, filepath: str):
        """
        Load profile fields from a file
        :param filepath:
        """
        ProfileData.__init__(self)
        directory, file = os.path.split(filepath)
        if filepath.endswith('.gz'):
            date_part = file[:-8]
            with gzip.open(filepath, 'r') as prfile:
                data = json.loads(prfile.read())
        else:
            date_part = file[:-5]
            with open(filepath, 'r') as prfile:
                data = json.loads(prfile.read())
        if data:
            (self.fields_map, self.profiles) = data
            try:
                dtime = datetime.datetime.fromisoformat(date_part)
                self.datetime_str = dtime.strftime("%b %d %Y %I:%M%p")
            except ValueError:
                self.datetime_str = 'Unknown'


class EmptyProfile(ProfileData):
    """
    Used when there isn't actually any profile data.
    """

    def __init__(self):
        ProfileData.__init__(self)


class Results:
    def __init__(self,
                 reference_data: ProfileData,
                 current_data: ProfileData):
        """
        Save results of compare and method to save data after successful delivery
        :param reference_data: Previous data
        :param current_data: Current data
        """
        self.reference_data: ProfileData = reference_data
        self.current_data: ProfileData = current_data

    def get_diffs(self) -> List[Tuple[str, List[Tuple[str, List[str], List[str]]]]]:
        """
        Return result of compare
        :return: The list of profile differences
        """
        all_fields = dict(self.reference_data.get_fields_map())
        all_fields.update(self.current_data.get_fields_map())
        joined_values = join_dicts(self.reference_data.get_profile_fields(),
                                   self.current_data.get_profile_fields())

        diffs = profile_compare(joined_values, all_fields)
        # If there are multiple values in a bucket they're in random order
        # Sort them. Alpha order is nice for the report, but mostly
        # this makes repeatable unit test possible.
        for person, fields in diffs:
            for field in fields:
                if field[1]:
                    field[1].sort()
                if field[2]:
                    field[2].sort()
        return diffs

    def save_data(self) -> None:
        """
        Save recent data on successful send of email.
        :return: None
        """
        self.current_data.save_data()

    @property
    def header(self) -> str:
        """
        Return date range of differences as string.
        :return:
        """
        return (f'{self.reference_data.get_datetime()} thru '
                f'{self.current_data.get_datetime()}')


def _get_previous_files(args: argparse.Namespace) -> List[str]:
    if os.path.exists(args.data):
        return [f for f in os.listdir(args.data)
                if f.endswith(('.json', '.json.gz'))]
    else:
        return []


def _generate_diffs(args,
                    breeze_api: breeze.BreezeApi = None) -> Results:
    if args.reference_data:
        # Special case. Run current data against an existing reference
        # and don't save the results
        reference_data = ProfileFromFile(args.reference_data)
        current_data = ProfileFromBreeze(args, breeze_api, do_save=False)
    else:
        prev_saved = _get_previous_files(args)
        prev_saved.sort(reverse=True)
        if args.replay:
            # Generate report from the two previous runs
            if len(prev_saved) < 2:
                # Need two files for replay
                sys.exit(f'Need at two previous runs in {args.data} for replay')
            reference_data = ProfileFromFile(os.path.join(args.data,
                                                          prev_saved[1]))
            current_data = ProfileFromFile(os.path.join(args.data,
                                                        prev_saved[0]))
        else:
            if not prev_saved:
                logging.warning('No previous data found. This will be big!')
                reference_data = EmptyProfile()
            else:
                reference_data = ProfileFromFile(os.path.join(args.data,
                                                              prev_saved[0]))
            current_data = ProfileFromBreeze(args, breeze_api)

    return Results(reference_data, current_data)


def _verify_directory(args: argparse.Namespace, create=False):
    if os.path.isdir(args.data):
        if os.access(args.data, os.W_OK | os.R_OK):
            return
        msg = f'{args.data} exists but isn\'t writable'
    elif create:
        Path(args.data).mkdir(exist_ok=True, parents=True)
        logging.info(f'Creating directory {args.data}')
        return
    else:
        msg = f'Directory {args.data} doesn\'t exist'

    logging.error(msg)
    sys.exit(msg)


def _list_domains(args):
    domains = known_domains(overrides=args.email_servers)
    print("Known email domains:")
    for domain, text in domains.items():
        print(f'   {domain}: {text}')


def main(breeze_api: breeze.BreezeApi = None,
         email_sender: MailSender = None):
    """
    Email a report of Breeze profile changes
    :param breeze_api: (For testing) pre-made Breeze API
    :param email_sender: (For testing) email sender
    :return: None
    """

    # First, figure out what we'll be doing
    parser = argparse.ArgumentParser('Generate report of recent Breeze changes')
    parser.add_argument('--from',
                        '-f',
                        dest='sender',
                        metavar='sender',
                        help='sending email address (required in most cases)')
    parser.add_argument('--to',
                        '-t',
                        metavar='recipient(s)',
                        help='public recipients, comma separated')
    parser.add_argument('--cc',
                        '-c',
                        metavar='copy recipient(s)',
                        help='copy recipients, comma separated')
    parser.add_argument('--bcc',
                        '-b',
                        metavar='<blind recipient(s)>',
                        help='hidden recipients, comma separated')
    parser.add_argument('--data',
                        '-d',
                        metavar='<data directory>',
                        help=f'directory with history, default: {DEFAULT_DATA_DIR}',
                        default=DEFAULT_DATA_DIR)
    parser.add_argument('--reference_data',
                        metavar='<reference data file>',
                        help='explicit previous data file to compare against')
    parser.add_argument('--format',
                        metavar='<report format>',
                        help='form of report (html, text, or csv)',
                        choices=['html', 'text', 'csv'],
                        default='html')
    parser.add_argument('--columns',
                        metavar='<column widths>',
                        help='column widths for format=text, default: ' +
                             DEFAULT_COLUMN_WIDTHS,
                        default=DEFAULT_COLUMN_WIDTHS)
    parser.add_argument('--breeze_creds',
                        metavar='<Breeze credential file>',
                        help='file with Breeze credentials if not standard',
                        default=None)
    parser.add_argument('--email_creds',
                        metavar='<email credential file>',
                        help='file with email passwords if not standard')
    parser.add_argument('--email_servers',
                        metavar='<email domain specification file>',
                        help='file with email domain configuration if not standard')
    parser.add_argument('--replay',
                        help='send differences between last two snapshots',
                        default=False,
                        action='store_true')
    parser.add_argument('--list_directories',
                        default=False,
                        action='store_true',
                        help='list data and configuration directories and exit')
    parser.add_argument('--initialize',
                        default=False,
                        action='store_true',
                        help="initialize from Breeze before first use "
                             "without sending report")
    parser.add_argument('--list_domains',
                        default=False,
                        action='store_true',
                        help='Print known email domains and exit')
    parser.add_argument('--retain_days',
                        type=int,
                        metavar='<days to retain>',
                        default=0,
                        help='<Number of days to retain old data')
    parser.add_argument('--logfile',
                        default=DEFAULT_LOG_FILE,
                        metavar='Log file',
                        help='File for application logs')
    parser.add_argument('--log_level',
                        default='info',
                        metavar='Log level',
                        help='Logging level, default=info')

    args = parser.parse_args()

    if args.logfile == 'stdout':
        out = {'stream': sys.stdout}
    elif args.logfile == 'stderr':
        out = {'stream': sys.stderr}
    else:
        out = {'filename': args.logfile}
        directory, file = os.path.split(args.logfile)
        Path(directory).mkdir(exist_ok=True, parents=True)

    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        level=getattr(logging, args.log_level.upper()),
        **out
    )

    logging.info(f'Running {" ".join(sys.argv)}')

    if args.list_domains:
        _list_domains(args)
        sys.exit(0)

    if args.list_directories:
        # Making it easy to note where users should look for files on this platform.
        mailsender_configs = configured_mail_sender.config_file_list()
        print('configured_mail_sender configuration files:')
        for f in mailsender_configs:
            print(f'\t{f}')
        breeze_config = breeze.config_file_list(overrides=args.breeze_creds)
        print('breeze_chms_api configuration files:')
        for f in breeze_config:
            print(f'\t{f}')
        print(f'{APPLICATION_NAME} data directory:\n\t{args.data}')
        print(f'log output\n\t{args.logfile}')
        sys.exit(0)

    if args.initialize:
        _verify_directory(args, create=True)
        if _get_previous_files(args):
            # Shouldn't initialize if there's already data
            sys.exit(f'Remove files from {args.data} before initializing')
        # Create first-time reference data to prevent monster first report
        current_data = ProfileFromBreeze(args, breeze_api)
        current_data.save_data()
        msg = f'Initial data saved to {current_data.save_file_name}'
        logging.info(msg)
        print(msg)
        sys.exit(0)

    if not args.sender:
        sys.exit('--from=sender is required')

    if not (args.to or args.bcc or args.cc):
        sys.exit('At least one of -t, -c, or -b is required')

    _verify_directory(args)

    results = _generate_diffs(args, breeze_api)

    widths = [int(w) for w in args.columns.split(',')]
    names = ['Field', 'Old', 'New']
    column_specs = [ColSpec(names[i], width=widths[i]) for i in range(3)]
    msg = MIMEMultipart()
    msg['Subject'] = 'Breeze profile change report'
    if args.to:
        msg['to'] = args.to
    if args.bcc:
        msg['bcc'] = args.bcc
    if args.cc:
        msg['cc'] = args.cc
    diffs = results.get_diffs()
    if diffs:
        msg.attach(MIMEText(f'Breeze changes for {results.header}'))
        if args.format == 'html':
            formatter = _HTMLFormatter(column_specs)
        elif args.format == 'csv':
            formatter = _CSVFormatter(column_specs)
        else:
            args.format = 'plain'
            formatter = _TextFormatter(column_specs)
        output = StringIO()
        formatter.format_table(diffs, output)
        output.seek(0)
        txt = output.read()
        if args.format == 'csv':
            part = MIMEText(txt, 'csv', 'utf-8')
            # part.set_payload(txt)
            part.add_header('Content-Disposition',
                            "attachment; filename=profile_changes.csv")
            msg.attach(part)
        else:
            msg.attach(MIMEText(txt, args.format))
    else:
        msg.attach(MIMEText(f'No changes found between {results.header}'))

    sender = email_sender if email_sender else \
        create_sender(args.sender,
                      creds_file=args.email_creds,
                      overrides=args.email_servers)
    sender.send_message(msg)

    results.save_data()


if __name__ == "__main__":
    main()
