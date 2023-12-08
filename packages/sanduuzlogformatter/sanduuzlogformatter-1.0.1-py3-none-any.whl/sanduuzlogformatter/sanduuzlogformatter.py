#!/usr/bin/env python3

from logging import Formatter


class SLF(Formatter):
    def __init__(self, datefmt="%Y-%m-%d %H:%M:%S", info_section_max_length=50):
        super(SLF, self).__init__(datefmt=datefmt)
        self.info_section_max_length = info_section_max_length

    def formatTime(self, record, datefmt=None):
        """ Override the formatTime method to use the specified datefmt. """
        if datefmt:
            self.datefmt = datefmt

        return super(SLF, self).formatTime(record, self.datefmt)

    def format(self, record):
        """ Add custom formatting with info section truncation if max limit is exceeded. """
        info_section_max_length = self.info_section_max_length

        # Info section max length - module name length - length of linenumber - 3 dots - 2 separators (':').
        max_funcname_length = info_section_max_length - len(record.module) - len(str(record.lineno)) - 3 - 2

        info_section = f"{record.module}:{record.funcName}:{record.lineno}"
        if len(info_section) > info_section_max_length:
            new_info_section = f"{record.module}:{record.funcName[:max_funcname_length]}...:{record.lineno}"
        else:
            new_info_section = f"{record.module}:{record.funcName}:{record.lineno}"

        msg = '%s - %-8s | %s | %s' % (
            self.formatTime(record),
            record.levelname,
            new_info_section.ljust(info_section_max_length),
            record.msg
        )
        record.msg = msg

        return super(SLF, self).format(record)
