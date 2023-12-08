import base64
import gzip
import json
import os
import shutil
import unittest
import tempfile
from datetime import datetime, timedelta
from io import StringIO
from typing import Tuple, List
import sys
from breeze_email_reports.EmailProfileReport import main

TEST_REFERENCE_WRONG_NAME = '2023-09-16T23:00:24.211429.json'
TEST_REFERENCE_NAME = '2023-09-17T23:00:24.211429.json'
TEST_REPLAY_NAME = '2023-10-17T23:00:24.211429.json'

TEST_FILES_DIR = os.path.join(os.path.split(__file__)[0], 'test_files')

# Data from previous run
TEST_PREVIOUS_DATA = os.path.join(TEST_FILES_DIR, 'ReferenceData.json')

# Returned by Breeze for "current" data
CURRENT_DATA_BREEZE = os.path.join(TEST_FILES_DIR, 'CurrentDataBreeze.json')
# Output from command, processed CURRENT_DATA_BREEZE. (Though this is uncompressed.)
TEST_CURRENT_DATA = os.path.join(TEST_FILES_DIR, 'ExpectedCurrentData.json')

# Expected results in email
EXPECTED_TABLE = os.path.join(TEST_FILES_DIR, 'ExpectedHtml.txt')
EXPECTED_CSV = os.path.join(TEST_FILES_DIR, 'ExpectedCSV.csv')
EXPECTED_TEXT = os.path.join(TEST_FILES_DIR, 'ExpectedText.txt')

TO_ADDRESS = 'to@test.com'
BCC_ADDRESS = 'bcc1@bcc.com, bcc2@bcc.com'
CC_ADDRESS = 'cc@cc.com'


class MockBreezeAPI:
    def __init__(self, fields, profiles):
        self.fields = fields
        self.profiles = profiles

    def list_people(self, **kwargs):
        return self.profiles

    def get_profile_fields(self):
        return self.fields


class MockSender:
    def __init__(self):
        self.result = None

    def send_message(self, msg):
        self.result = msg


class TestSender(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.mock_sender = MockSender()
        self.saved_argv = sys.argv
        self.saved_stdout = None

    def runTest(self,
                report_format: str = 'text',
                do_gz: bool = True,
                do_reference: bool = True,
                previous_data: str = TEST_PREVIOUS_DATA,
                extra_params: List[str] = []) -> Tuple[str, int]:
        """
        Run BreezeProfile report. Return emitted event.
        :param report_format:
        :param do_gz:
        :param do_reference:
        :param previous_data:
        :param extra_params:
        :return:
        :raises: ParamException, IOException
        """

        with open(previous_data, 'r') as f:
            previous_data = f.read()

        test_file_name = os.path.join(self.test_dir.name, TEST_REFERENCE_NAME)
        if do_reference:
            if do_gz:
                with gzip.open(f'{test_file_name}.gz', 'w') as outfile:
                    outfile.write(bytes(previous_data, 'utf8'))
            else:
                with open(test_file_name, 'w') as f:
                    f.write(previous_data)
            with open(os.path.join(self.test_dir.name, TEST_REFERENCE_WRONG_NAME),
                      'w') as f:
                f.write('This is bad data')

        with open(CURRENT_DATA_BREEZE, 'r') as f:
            fields, profiles = json.load(f)

        api_mock = MockBreezeAPI(fields, profiles)

        sys.argv = ['test', '-f', 'from@test.com', '-t', TO_ADDRESS,
                    '-b', BCC_ADDRESS,
                    '--cc', CC_ADDRESS,
                    '--data', self.test_dir.name,
                    '--log_level=critical',
                    f'--logfile={os.path.join(self.test_dir.name, "test.log")}',
                    '--format', report_format] + extra_params

        ret = main(breeze_api=api_mock, email_sender=self.mock_sender)
        self.assertEqual(None, ret)
        # files = os.listdir(self.test_dir.name)
        # newfile = files[-1]
        # with open(os.path.join(self.test_dir.name, newfile), 'r') as f:
        #     expect_out = f.read()
        #
        # with open(TEST_CURRENT_DATA, 'w') as f:
        #     f.write(expect_out)

    def test_html(self):
        self.runTest('html',
                     extra_params=['--reference_data', TEST_PREVIOUS_DATA])

        sent_message = self.mock_sender.result
        # daw30410@yahoo.com
        # bcc1@foo,bcc2@foo
        # Breeze profile change report
        # [<email.mime.text.MIMEText object at 0x10e514cd0>, <email.mime.text.MIMEText object at 0x10edb8390>]
        # ['Content-Type', 'MIME-Version', 'Content-Transfer-Encoding']
        # ['text/plain; charset="us-ascii"', '1.0', '7bit']
        # ['Content-Type', 'MIME-Version', 'Content-Transfer-Encoding']
        # ['text/html; charset="us-ascii"', '1.0', '7bit']
        # Breeze changes since Sep 17 2023 11:00PM (Payload one get_payload()
        self.assertEqual('Breeze profile change report',
                         str(sent_message.get('Subject')))
        self.assertEqual(TO_ADDRESS, sent_message.get('to'))
        self.assertEqual(BCC_ADDRESS, sent_message.get('bcc'))
        self.assertEqual(CC_ADDRESS, sent_message.get('cc'))

        sent_message = self.mock_sender.result
        payloads = sent_message.get_payload()
        pl0 = payloads[0]
        pl1 = payloads[1]
        self.assertEqual(pl0.get_content_subtype(), 'plain')
        self.assertTrue(str(pl0.get_payload()).
                        startswith('Breeze changes for Unknown thru'))
        self.assertEqual(pl1.get_content_subtype(), 'html')
        got = str(pl1.get_payload())
        # with open(EXPECTED_TABLE, 'w') as f:
        #     f.write(got)
        with open(EXPECTED_TABLE, 'r') as f:
            ref = f.read()
        self.assertEqual(got, ref)

    def test_csv(self):
        self.runTest('csv', do_gz=True)
        sent_message = self.mock_sender.result
        self.assertEqual('Breeze profile change report',
                         str(sent_message.get('Subject')))
        self.assertEqual(TO_ADDRESS, sent_message.get('To'))
        self.assertEqual(BCC_ADDRESS, sent_message.get('Bcc'))

        sent_message = self.mock_sender.result
        payloads = sent_message.get_payload()
        pl0 = payloads[0]
        pl1 = payloads[1]
        self.assertEqual(pl0.get_content_subtype(), 'plain')
        self.assertTrue(
            str(pl0.get_payload().
                startswith('Breeze changes since Sep 17 2023 11:00PM thru')))
        self.assertEqual(pl1.get_content_subtype(), 'csv')
        got_bytes = base64.b64decode(pl1.get_payload())
        got = got_bytes.decode('utf-8)')
        # with open(EXPECTED_CSV, 'w', newline='') as f:
        #     f.write(got)
        with open(EXPECTED_CSV, 'r', newline='') as f:
            ref = f.read()
        self.assertEqual(got, ref)

    def test_replay(self):
        shutil.copyfile(TEST_CURRENT_DATA,
                        os.path.join(self.test_dir.name, TEST_REPLAY_NAME))
        self.runTest('html', extra_params=['--replay'], do_gz=False)
        sent_message = self.mock_sender.result
        self.assertEqual('Breeze profile change report',
                         str(sent_message.get('Subject')))
        self.assertEqual(TO_ADDRESS, sent_message.get('To'))
        self.assertEqual(BCC_ADDRESS, sent_message.get('Bcc'))

        payloads = sent_message.get_payload()
        pl0 = payloads[0]
        pl1 = payloads[1]
        self.assertEqual(pl0.get_content_subtype(), 'plain')
        self.assertEqual(
            'Breeze changes for Sep 17 2023 11:00PM thru Oct 17 2023 11:00PM',
            str(pl0.get_payload()))
        # self.assertTrue(str(pl0.get_payload()).
        #                 startswith('Breeze changes for Unknown thru'))
        self.assertEqual(pl1.get_content_subtype(), 'html')
        got = str(pl1.get_payload())
        # with open(EXPECTED_TABLE, 'w') as f:
        #     f.write(got)
        with open(EXPECTED_TABLE, 'r') as f:
            ref = f.read()
        self.assertEqual(got, ref)

    def test_no_change(self):
        self.runTest('csv', previous_data=TEST_CURRENT_DATA)
        sent_message = self.mock_sender.result
        self.assertEqual('Breeze profile change report',
                         str(sent_message.get('Subject')))
        self.assertEqual(TO_ADDRESS, sent_message.get('To'))
        self.assertEqual(BCC_ADDRESS, sent_message.get('Bcc'))
        payloads = sent_message.get_payload()
        self.assertEqual(len(payloads), 1)
        pl0 = payloads[0]
        self.assertEqual(pl0.get_content_subtype(), 'plain')
        self.assertTrue(
            str(pl0.get_payload().
                startswith('No changes found between Sep 17 2023 11:00PM thru ')))

    def test_text(self):
        self.runTest('text')
        sent_message = self.mock_sender.result
        self.assertEqual('Breeze profile change report',
                         str(sent_message.get('Subject')))
        self.assertEqual(TO_ADDRESS, sent_message.get('To'))
        self.assertEqual(BCC_ADDRESS, sent_message.get('Bcc'))

        sent_message = self.mock_sender.result
        payloads = sent_message.get_payload()
        pl0 = payloads[0]
        pl1 = payloads[1]
        self.assertEqual(pl0.get_content_subtype(), 'plain')
        self.assertTrue(
            str(pl0.get_payload().
                startswith('Breeze changes for Sep 17 2023 11:00PM')))
        self.assertEqual(pl1.get_content_subtype(), 'plain')
        got = str(pl1.get_payload())
        # with open(EXPECTED_TEXT, 'w') as f:
        #     f.write(got)
        with open(EXPECTED_TEXT, 'r') as f:
            ref = f.read()
        self.assertEqual(got, ref)

    def test_bad_params(self):
        # Exception if no "to"
        sys.argv = ['test', '-b', 'foo@bar']
        with self.assertRaises(SystemExit) as se:
            main()
        self.assertEqual('--from=sender is required', se.exception.code)

    def test_no_to(self):
        sys.argv = ['test', '-f', 'from@foobar', ]
        with self.assertRaises(SystemExit) as se:
            main()
        self.assertEqual('At least one of -t, -c, or -b is required', se.exception.code)

    def test_bad_data(self):
        sys.argv = ['test', '-f', 'from@foobar', '-t', 'to@foobar',
                    '--logfile=stdout',
                    '--log_level=critical',
                    '--data', '/no/such/dir']
        with self.assertRaises(SystemExit) as e:
            main(email_sender=self.mock_sender)
        self.assertEqual('Directory /no/such/dir doesn\'t exist',
                         e.exception.code)

    def test_no_previous(self):
        self.runTest(report_format='text', do_reference=False)
        sent_message = self.mock_sender.result
        self.assertEqual('Breeze profile change report',
                         str(sent_message.get('Subject')))
        self.assertEqual(TO_ADDRESS, sent_message.get('To'))
        self.assertEqual(BCC_ADDRESS, sent_message.get('Bcc'))

        # sent_message = self.mock_sender.result
        payloads = sent_message.get_payload()
        pl0 = payloads[0]
        pl1 = payloads[1]
        self.assertEqual(pl0.get_content_subtype(), 'plain')
        self.assertTrue(
            str(pl0.get_payload().
                startswith('Breeze changes for Unknown thru')))
        self.assertEqual(pl1.get_content_subtype(), 'plain')
        # got = str(pl1.get_payload())
        # print(got)
        # with open(EXPECTED_TEXT, 'w') as f:
        #     f.write(got)

    def test_retain(self):
        now = datetime.now()
        days = 7
        files = [datetime.isoformat(now - timedelta(days=days + d)) + '.json'
                 for d in [5, 1, -1, -2]]
        for f in files:
            shutil.copyfile(TEST_CURRENT_DATA, os.path.join(self.test_dir.name, f))

        self.runTest(report_format='text',
                     do_reference=False,
                     extra_params=['--retain_days', str(days)])
        retained_files = os.listdir(self.test_dir.name)
        self.assertEqual(3, len(retained_files))
        self.assertFalse(files[1] in retained_files)
        self.assertTrue(files[3] in retained_files)

    def test_list_directories(self):
        sys.argv = ['test', '--list_directories', '--log_level=critical']
        self.saved_stdout = sys.stdout
        capture_out = StringIO()
        sys.stdout = capture_out
        with self.assertRaises(SystemExit) as e:
            main(email_sender=self.mock_sender)
        self.assertEqual(e.exception.code, 0,
                         "List directories shouldn't cause error")
        sys.stdout = self.saved_stdout
        capture_out.seek(0)
        output = capture_out.read()
        lines = output.split('\n')
        self.assertEqual('configured_mail_sender configuration files:',
                         lines[0])

    def test_known_domains(self):
        sys.argv = ['test', '--list_domains', '--log_level=critical']
        capture_out = StringIO()
        self.saved_stdout = sys.stdout
        sys.stdout = capture_out
        with self.assertRaises(SystemExit) as e:
            main()
        self.assertEqual(e.exception.code, 0,
                         "List domains shouldn't cause error")
        sys.stout = self.saved_stdout
        capture_out.seek(0)
        captured = capture_out.read()
        # lines = captured.split('\n')
        domains = {}
        for line in captured.split('\n')[1:]:
            line = line.replace(' ', '')
            if line:
                entry = line.split(':')
                key = entry[0]
                domains[key] = entry[1]
        self.assertEqual('smtp.mail.yahoo.com', domains.get('yahoo.com'))

    def test_initialize(self):
        os.removedirs(self.test_dir.name)
        with self.assertRaises(SystemExit) as e:
            self.runTest(extra_params=['--initialize'],
                         do_reference=False)
        self.assertEqual(0, e.exception.code)
        self.assertIsNone(self.mock_sender.result)
        # Should get same result
        files = os.listdir(self.test_dir.name)
        self.assertEqual(1, len(files))
        result = files[0]
        path = os.path.join(self.test_dir.name, result)
        with gzip.open(path, 'r') as f:
            saved_data = f.read()
        with open(TEST_CURRENT_DATA, 'r') as f:
            expected = bytes(f.read(), 'utf-8')
        self.assertEqual(expected, saved_data)

    def tearDown(self):
        if self.saved_stdout:
            sys.stdout = self.saved_stdout
        self.test_dir.cleanup()
        sys.argv = self.saved_argv
