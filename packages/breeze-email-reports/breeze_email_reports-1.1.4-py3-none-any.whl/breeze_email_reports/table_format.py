import csv
import html
from abc import abstractmethod
from io import IOBase
from typing import List, Tuple, Union

# Pad string to length, e.g. f'{a<15}' will pad to 15 chars.


class ColSpec:
    def __init__(self,
                 title: str,
                 header_attrs: str = '',
                 row_attrs: str = '',
                 width: int = 0):
        """
        Column specifications for table formatter
        :param title: Column title
        :param header_attrs: HTML attributes for header (if appropriate)
        :param row_attrs: HTML attributes for data rows (if appropriate)
        """
        self.title_val = title
        self.header_attrs_val = header_attrs if header_attrs else row_attrs
        self.row_attrs_val = row_attrs if row_attrs else header_attrs
        self.width_val = width

    @property
    def title(self):
        return self.title_val

    @property
    def header_attrs(self):
        return self.header_attrs_val

    @property
    def row_attributes(self):
        return self.row_attrs_val

    @property
    def width(self):
        return self.width_val


class _ReportFormatter:
    def __init__(self,
                 column_specs: List[ColSpec]):
        self.column_specs = column_specs
        self.columns = len(column_specs)

    @abstractmethod
    def format_table(self,
                     data: List[Tuple],
                     output: IOBase):
        """
        Format the data in appropriate format and write to output
        :param data: Data for the table
        :param output: Output stream to write to.
        :return: None
        The input data is a list of tuples. The first value is a group header
        that divides subsequent data. (A member name in this context.) The second
        value is a list of tuples, each with label for the tuple followed by values
        for columns in the row. Each column value can be None, a string, or a list
        of strings.
        """
        pass


def _escape_html_value(val: Union[str, List[str]]) -> str:
    if val:
        if isinstance(val, list):
            # For lists in HTML break each item on semicolons (for addresses).
            # But we have to do that before the html.escape() because that
            # introduces semicolons.
            return '<br/>'.join([html.escape(i) for elt in val
                                 for i in elt.split(';')])
        else:
            return html.escape(val)
    else:
        return ' '


class _HTMLFormatter(_ReportFormatter):
    def __init__(self, *args, **kwargs):
        _ReportFormatter.__init__(self, *args, **kwargs)
        self.table_header = ('<table border="1" style="border:1px solid #000000;'
                             'border-collapse:collapse" cellpadding="4">\n')

    def format_table(self,
                     data: List[Tuple],
                     output: IOBase):
        """
        Format as an HTML table
        :param data:
        :param output:
        :return:
        """
        output.write('<table border="1" style="border:1px solid #000000;'
                     'border-collapse:collapse" cellpadding="4">')
        nl = '\n'
        row = '\n'.join([f'  <th {c.header_attrs}>{c.title}</th>'
                         for c in self.column_specs])
        output.write(f'{nl} <tr>{nl}{row}{nl} </tr>{nl}')

        for name, values in data:
            output.write(f'<tr><td colspan="{self.columns}" '
                         f'bgcolor="LightBlue"><b>{html.escape(name)}</b></td></tr>')
            for row in values:
                output.write(' <tr>\n')
                for i in range(len(row)):
                    cs = self.column_specs[i]
                    colval = row[i]
                    output.write(f'  <td {cs.row_attributes}>'
                                 f'{_escape_html_value(colval)}</td>' '\n')
                output.write(' </tr>\n')

        output.write('</table>\n')


def _splitval(val: str, cs: ColSpec, splits: str = ';: ') \
        -> Tuple[str, Union[str, None]]:
    """
    Split a string if too long
    :param val: Value to split
    :param cs: ColSpec with desired length
    :return: Tuple, parts of val before and after the split
    """
    # use .strip() to remove pre and post whitespace
    if not val:
        return '', None
    if len(val) <= cs.width:
        return val, ''
    last_found = cs.width - 1
    found_char = None
    for c in splits:
        end = cs.width if c == ' ' else cs.width - 1
        found = val.rfind(c, 0, end)
        if found > 0:
            last_found = found
            found_char = c
            break

    first = val[:last_found] if found_char == ' ' else val[:last_found + 1]
    second = val[last_found + 1:]
    return first, second


class _ToFileFormatter(_ReportFormatter):
    def __init__(self, *args, **kwargs):
        _ReportFormatter.__init__(self, *args, **kwargs)
        # self.line_mark = '   |'
        # self.row_prefix = self.line_mark
        # for cs in self.column_specs:
        #     self.line_mark += ''.rjust(cs.width, '-') + '|'

    def format_table(self,
                     data: List[Tuple],
                     output: IOBase):
        """
        Format as an HTML table
        :param data:
        :param output:
        :return:
        """
        for section in data:
            name, values = section
            self.start_section(name, output)
            for row in values:
                more = True
                self.start_group(output)
                # print(self.line_mark, file=output)
                while more:
                    # print(self.row_prefix, end='', file=output)
                    more = False
                    next_values = []
                    this_row = []
                    for i in range(min(len(row), self.columns)):
                        cs = self.column_specs[i]
                        colval = row[i]
                        nextval = []
                        if colval:
                            if isinstance(colval, list):
                                curval = colval[0]
                                nextval = colval[1:]
                                if nextval:
                                    more = True
                            else:
                                curval = colval
                                nextval = []
                            curval, overflow = self.splitval(curval, cs)
                            if overflow:
                                nextval = [overflow] + nextval
                                more = True
                        else:
                            curval = ''
                        this_row.append(curval if curval else '')
                        next_values.append(nextval)

                    self.emit_row(this_row, output)
                    row = next_values

            # print(self.line_mark, file=output)
            self.end_section(output)
        self.finish_output(output)

    @abstractmethod
    def start_section(self, name: str, output: IOBase):
        pass

    def end_section(self, output: IOBase):
        pass

    def start_group(self, output):
        pass

    def splitval(self, val: str, cs: ColSpec) -> Tuple[str, Union[str, None]]:
        return val, None

    def emit_row(self, values: List[str], output: IOBase):
        # print(self.row_prefix, end='', file=output)
        # for i in range(len(values)):
        #     v = values[i]
        #     cs = self.column_specs[i]
        #     v = v.ljust(cs.width)
        #     print(v + '|',
        #           end='',
        #           file=output)
        #     output.flush()
        # print('', file=output)
        pass

    def finish_output(self, output: IOBase):
        pass


class _TextFormatter(_ToFileFormatter):
    def __init__(self, *args, **kwargs):
        _ToFileFormatter.__init__(self, *args, **kwargs)
        self.line_mark = '   |'
        self.row_prefix = self.line_mark
        for cs in self.column_specs:
            self.line_mark += ''.rjust(cs.width, '-') + '|'

    def start_section(self, name: str, output: IOBase):
        print('', file=output)
        print(name, file=output)

    def start_group(self, output):
        print(self.line_mark, file=output)

    def splitval(self, val: str, cs: ColSpec) -> Tuple[str, str]:
        ret_val, overflow = _splitval(val, cs)
        return ret_val.replace('\n', ';'), ('+' + overflow) if overflow else None

    def emit_row(self, values: List[str], output: IOBase):
        print(self.row_prefix, end='', file=output)
        for i in range(len(values)):
            v = values[i]
            cs = self.column_specs[i]
            v = v.ljust(cs.width)
            print(v + '|',
                  end='',
                  file=output)
            output.flush()
        print('', file=output)

    def end_section(self, output: IOBase):
        print(self.line_mark, file=output)


class _CSVFormatter(_ToFileFormatter):
    def __init__(self, *args, **kwargs):
        _ToFileFormatter.__init__(self, *args, **kwargs)
        self.writer = None

    def start_section(self, name: str, output: IOBase):
        if not self.writer:
            self.writer = csv.writer(output)
        self.writer.writerow([name])

    def emit_row(self, values: List[str], output: IOBase):
        self.writer.writerow([''] + values)
