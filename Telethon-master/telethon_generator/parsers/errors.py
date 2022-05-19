import csv
import re

from ..utils import snake_to_camel_case

# Core base classes depending on the integer error code
KNOWN_BASE_CLASSES = {
    303: 'InvalidDCError',
    400: 'BadRequestError',
    401: 'UnauthorizedError',
    403: 'ForbiddenError',
    404: 'NotFoundError',
    406: 'AuthKeyError',
    420: 'FloodError',
    500: 'ServerError',
    503: 'TimedOutError'
}


def _get_canonical_name(error_code):
    """
    Gets the corresponding canonical name for the given error code.
    """
    # This code should match that of the library itself.
    name = re.sub(r'[-_\d]', '', error_code).lower()
    while name.endswith('error'):
        name = name[:-len('error')]

    return name


class Error:
    def __init__(self, codes, name, description):
        # TODO Some errors have the same name but different integer codes
        # Should these be split into different files or doesn't really matter?
        # Telegram isn't exactly consistent with returned errors anyway.
        self.int_code = codes[0]
        self.str_code = name
        self.canonical_name = _get_canonical_name(name)
        self.description = description

        has_captures = '0' in name
        if has_captures:
            self.capture_name = re.search(r'{(\w+)}', description).group(1)
        else:
            self.capture_name = None


def parse_errors(csv_file):
    """
    Parses the input CSV file with columns (name, error codes, description)
    and yields `Error` instances as a result.
    """
    with csv_file.open(newline='') as f:
        f = csv.reader(f)
        next(f, None)  # header
        for line, tup in enumerate(f, start=2):
            try:
                name, codes, description = tup
            except ValueError:
                raise ValueError('Columns count mismatch, unquoted comma in '
                                 'desc? (line {})'.format(line)) from None

            try:
                codes = [int(x) for x in codes.split()] or [400]
            except ValueError:
                raise ValueError('Not all codes are integers '
                                 '(line {})'.format(line)) from None

            yield Error([int(x) for x in codes], name, description)