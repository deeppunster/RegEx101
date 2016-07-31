"""
PlayParse - explore how to parse lines
"""

from logging import getLogger, debug, error, info, DEBUG, basicConfig
from re import match, findall, fullmatch, search, VERBOSE, compile
from io import SEEK_SET, SEEK_END

__author__ = 'Travis Risner'
__project__ = "play_parse"
__creation_date__ = "7/21/2016"
# "${CopyRight.py}".

log = getLogger(__name__)

sample_file_name = 'play_firewall_config.txt'


class PlayParseClass:
    """
    Explore how to parse components of a complex file.

    **The core of the processing**

    The variable self.identify_conponent is a regular expression to
    determine the kind of line that was found.  Each expression
    component identifies a line beginning with a particular header and
    tags it with a "group" name.

    The group name is found in the dictionary variable named
    self.group_action.  The entry for the group is a function to use to
    parse the line.

    **The wrapper around the core**

    (Not needed to explore the parsing technique)
    """

    def __init__(self):
        """
        Setup for this class.
        """
        # input file
        self.input_name = sample_file_name
        """
        The variable self.identify_conponent is a regular expression to
        determine the kind of line that was found.  Each expression
        component identifies a line beginning with a particular header and
        tags it with a "group" name.

        The group name is found in the dictionary variable named
        self.group_action.  The entry for the group is a function to use to
        parse the line.
        """
        self.identify_component = compile(r"""
            (?P<interface>^interface .*$) # interface definition
            |                     # or
            (?P<emptyline>^\s*$)  # empty line
            |                     # or
            (?P<continuation>^\s.+$) # continuation - not a primary line
            |                     # or
            (?P<comment>^!.*$)    # comment - an exclamation point at beginning
            |                     # or
            (?P<other>^.*$)       # other - anything not match the above
            """, flags=VERBOSE)

        # table to drive parsing once the kind of line has been identified
        self.group_action = {
            'interface': self.interface_function,
            'continuation': self.continue_function,
            'comment': self.comment_function,
            'other': self.other_function,
            'emptyline': self.empty_line_function,
        }

    def input_token_generator(self):
        """
        Create a generator to yield lines from the firewall config file.

        :yields: each line of the firewall config file in turn
        :return:
        """
        firewall_line = ''
        with open(self.input_name, mode='r') as fc:  # encoding='utf-8'
            fc.seek(0, SEEK_END)
            end_marker = fc.tell()
            fc.seek(0, SEEK_SET)
            while fc.tell() < end_marker:
                firewall_line = fc.readline()
                yield firewall_line
        return


    def parse_lines(self):
        """
        Identify the type of each line read in.

        :return: (nothing)
        """
        info('Start parsing')
        for line in self.input_token_generator():
            debug('Line to be parsed is ==>{}<=='.format(line))
            result = match(self.identify_component, line)
            debug('Result of match was {}'.format(result.groupdict()))
            debug('Group identifier of the match was {} '.format(
                result.lastgroup))
            try:
                function_to_execute = self.group_action[result.lastgroup]
                debug(
                    'Function to be executed is {}'.format(
                        function_to_execute.__name__))
                function_to_execute(line)
            except KeyError as xcp:
                debug('##### {}, invalid group identifier #####'.format(xcp))
        info("End of parsing")


    def interface_function(self, line: str):
        debug('Reached interface_function with line {}'.format(line))
        return


    def continue_function(self, line: str):
        debug('Reached continue_function with line {}'.format(line))
        return


    def comment_function(self, line: str):
        debug('Reached comment_function with line {}'.format(line))
        return


    def other_function(self, line: str):
        debug('Reached other_function with line {}'.format(line))
        return


    def empty_line_function(self, line: str):
        debug('Reached empty_line_function with line {}'.format(line))


if __name__ == '__main__':
    # use simple logger
    debugfilename = 'debuginfo.txt'
    logformat = '%(levelname)-8s - %(name)-30s - %(funcName)-20s ' \
                '(%(lineno)5d) - %(message)-s'
    loglevel = DEBUG
    # Python-based logging
    basicConfig(
        filename=debugfilename,
        filemode='w',
        format=logformat,
        level=loglevel
    )

    ppc = PlayParseClass()
    ppc.parse_lines()

# EOF
