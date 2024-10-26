#///////////////////////////////////////////////////////////////////////////////
#
# (c) 2019-2022 Toolsensing, Inc. All rights reserved.
# Unless otherwise permitted, no distribution or use is permitted.
#
#///////////////////////////////////////////////////////////////////////////////


# coding=utf-8
import enum
import os
import uuid
import shutil
import logging

from common import file_helper


glb_log_name_placeholder_tag = r"LOG_NAME_PLACEHOLDER"


class LogHelper:
    def __init__(self, log_config_file_name, log_file_name,
                 log_name_placeholder_tag=glb_log_name_placeholder_tag):
        self.__log_config_file_name = log_config_file_name
        self.__log_file_name = log_file_name
        self.__log_name_placeholder_tag = log_name_placeholder_tag
        self.__updated_log_config_file_name = None

    def get_updated_log_config_file_name(self):
        if self.__updated_log_config_file_name is not None:
            return self.__updated_log_config_file_name

        log_config_file_dir = os.path.dirname(self.__log_config_file_name)
        log_config_file_name = os.path.basename(self.__log_config_file_name)
        updated_log_config_file_name = os.path.join(log_config_file_dir, "%s-%s" % (uuid.uuid4(), log_config_file_name))

        shutil.copyfile(self.__log_config_file_name, updated_log_config_file_name)

        file_helper.replace_file_content(updated_log_config_file_name,
                                         self.__log_name_placeholder_tag, self.__log_file_name)

        self.__updated_log_config_file_name = updated_log_config_file_name

        return updated_log_config_file_name

    def remove_updated_log_config_file(self):
        if os.path.isfile(self.__updated_log_config_file_name):
            os.remove(self.__updated_log_config_file_name)


class LogConfigGenerator:
    @enum.unique
    class LogLevel(enum.Enum):
        DEBUG = 1
        INFO = 2
        WARNING = 3
        ERROR = 4
        CRITICAL = 5
        NOTSET = 6

    def __init__(self):
        self.__logger_list = []
        self.__formatter_tag = r"Formatter"
        self.__handler_tag = r"Handler"

    # note: cloghandler must be imported in order to support process_safety function
    def add_file_logger(self, log_file_name, process_safety=False, new_log_file=True, display_process_id=False,
                        display_thread_id=False, display_logger_name=True,
                        level=LogLevel.NOTSET, name=r"root"):
        log_formatter = self.FormattterOption("%s%s" % (name, self.__formatter_tag))
        log_formatter = self.__set_log_format_style(log_formatter, display_logger_name,
                                                    display_process_id, display_thread_id)

        log_handler = self.HandlerOption("%s%s" % (name, self.__handler_tag), log_formatter, level.name)

        mode = "w" if new_log_file else "a"
        log_handler = log_handler.set_process_safety_mode(log_file_name, mode) if process_safety \
            else log_handler.set_normal_file_mode(log_file_name, mode)

        logger_opt = self.LoggerOption(name, log_handler, level.name)
        return self.__add_logger_opt(logger_opt)

    def add_stream_logger(self, display_process_id=False, display_thread_id=False,
                          display_logger_name=True, level=LogLevel.NOTSET, name=r"root"):

        log_formatter = self.FormattterOption("%s%s" % (name, self.__formatter_tag))
        log_formatter = self.__set_log_format_style(log_formatter, display_logger_name,
                                                    display_process_id, display_thread_id)

        log_handler = self.HandlerOption("%s%s" % (name, self.__handler_tag), log_formatter, level.name)
        log_handler = log_handler.set_stream_mode()

        logger_opt = self.LoggerOption(name, log_handler, level.name)
        return self.__add_logger_opt(logger_opt)

    def gen_logger_config_file(self, log_config_file_name):
        loggers_keys_content = "[loggers]\nkeys="
        handlers_keys_content = "[handlers]\nkeys="
        formatters_keys_content = "[formatters]\nkeys="

        for logger in self.__logger_list:
            loggers_keys_content += "%s, " % logger.name
            handlers_keys_content += "%s, " % logger.handler.name
            formatters_keys_content += "%s, " % logger.handler.formatter.name

        loggers_keys_content = loggers_keys_content[:loggers_keys_content.rfind(r",")]
        handlers_keys_content = handlers_keys_content[:handlers_keys_content.rfind(r",")]
        formatters_keys_content = formatters_keys_content[:formatters_keys_content.rfind(r",")]

        log_config_file_all_lines = [loggers_keys_content, "\n\n",
                                     handlers_keys_content, "\n\n",
                                     formatters_keys_content, "\n\n"]

        for logger in self.__logger_list:
            log_config_file_all_lines.append("%s" % logger)
            log_config_file_all_lines.append("\n")

        for logger in self.__logger_list:
            log_config_file_all_lines.append("%s" % logger.handler)
            log_config_file_all_lines.append("\n")

        for logger in self.__logger_list:
            log_config_file_all_lines.append("%s" % logger.handler.formatter)
            log_config_file_all_lines.append("\n")

        file_helper.write_all_lines(log_config_file_name, log_config_file_all_lines)

        return True

    @staticmethod
    def __set_log_format_style(log_formatter, display_logger_name, display_process_id, display_thread_id):
        log_formatter.add_time_info()
        log_formatter = log_formatter.add_process_id_info() if display_process_id else log_formatter
        log_formatter = log_formatter.add_thread_id_info() if display_thread_id else log_formatter
        log_formatter = log_formatter.add_logger_name_info() if display_logger_name else log_formatter
        log_formatter.add_level_info() \
            .add_message_info("", "") \
            .add_filename_info(r"(", "") \
            .add_line_num_info(":", r")")
        return log_formatter

    def __add_logger_opt(self, logger_opt):
        self.__logger_list.append(logger_opt)
        return self

    class FormattterOption:
        def __init__(self, name):
            self.__formatter_name = name
            self.__format = ""
            self.__formatter_option_template = "[formatter_%s]\nformat=%s\n"

        def __str__(self):
            if len(self.__format) == 0:
                self.add_time_info().add_level_info().add_message_info(" ", "") \
                    .add_filename_info("(", "").add_line_num_info(":", ")")
            return self.__formatter_option_template % (self.__formatter_name, self.__format)

        def reset_info(self):
            self.__format = ""

        def add_time_info(self, left_ch=r"[", right_ch=r"]"):
            self.__format += left_ch + r"%(asctime)s" + right_ch
            return self

        def add_process_id_info(self, left_ch=r"[", right_ch=r"]"):
            self.__format += left_ch + r"%(process)d" + right_ch
            return self

        def add_thread_id_info(self, left_ch=r"[", right_ch=r"]"):
            self.__format += left_ch + r"%(thread)d" + right_ch
            return self

        def add_level_info(self, left_ch=r"[", right_ch=r"]"):
            self.__format += left_ch + r"%(levelname)s" + right_ch
            return self

        def add_logger_name_info(self, left_ch=r"[", right_ch=r"]"):
            self.__format += left_ch + r"%(name)s" + right_ch
            return self

        def add_filename_info(self, left_ch=r"[", right_ch=r"]"):
            self.__format += left_ch + r"%(filename)s" + right_ch
            return self

        def add_line_num_info(self, left_ch=r"[", right_ch=r"]"):
            self.__format += left_ch + r"%(lineno)d" + right_ch
            return self

        def add_message_info(self, left_ch=r"[", right_ch=r"]"):
            self.__format += left_ch + r"%(message)s" + right_ch
            return self

        @property
        def name(self):
            return self.__formatter_name

    class HandlerOption:
        def __init__(self, handler_name, formatter, level="NOTSET"):
            self.__handler_name = handler_name
            self.__handler_class_name = ""
            self.__handler_obj_args = ""
            self.__level = level
            self.__formatter = formatter
            self.__handler_option_template = "[handler_%s]\nclass=%s\nargs=(%s)\nlevel=%s\nformatter=%s\n"
            self.__log_dir = ""
            self.__lock_file_regex_template = r"%s.*?.lock"
            self.__lock_file_name_prefix = ""
            self.set_stream_mode()

        def __del__(self):
            if len(self.__lock_file_name_prefix) > 0:
                file_helper.rm_files(self.__log_dir, self.__lock_file_regex_template % self.__lock_file_name_prefix)

        def __str__(self):
            args = ""
            for arg in self.__handler_obj_args:
                args += "%s, " % arg
            if len(self.__handler_obj_args) > 1:
                args = args[:args.rfind(r",")]

            formatter_name = self.__formatter.name

            return self.__handler_option_template % (self.__handler_name, self.__handler_class_name,
                                                     args, self.__level, formatter_name)

        def set_process_safety_mode(self, log_name, mode="a", log_max_bytes=1024 * 1024 * 10, backup_count=10):
            self.__handler_class_name = r"handlers.ConcurrentRotatingFileHandler"
            self.__handler_obj_args = [r'"%s"' % log_name, r'"%s"' % mode, log_max_bytes, backup_count]
            self.__log_dir = os.path.dirname(log_name)
            if len(self.__log_dir) == 0:
                self.__log_dir = "./"

            self.__lock_file_name_prefix = os.path.splitext(os.path.basename(log_name))[0]
            return self

        def set_normal_file_mode(self, log_name, mode="a", log_max_bytes=1024 * 1024 * 10, backup_count=10):
            self.__handler_class_name = r"logging.handlers.RotatingFileHandler"
            self.__handler_obj_args = [r'"%s"' % log_name, r'"%s"' % mode, log_max_bytes, backup_count]
            self.__log_dir = os.path.dirname(log_name)
            if len(self.__log_dir) == 0:
                self.__log_dir = "./"
            return self

        def set_stream_mode(self):
            self.__handler_class_name = r"logging.StreamHandler"
            self.__handler_obj_args = [r"sys.stdout", ]
            return self

        @property
        def log_level(self):
            return self.__level

        def set_log_level(self, level="NOTSET"):
            self.__level = level.upper()
            return self

        @property
        def formatter(self):
            return self.__formatter

        @formatter.setter
        def formatter(self, value):
            self.__formatter = value

        @property
        def name(self):
            return self.__handler_name

    class LoggerOption:
        def __init__(self, logger_name, handler, level="NOTSET", propagate=1):
            self.__logger_name = logger_name
            self.__handler = handler
            self.__propagate = propagate
            self.__level = level
            self.__logger_option_template = "[logger_%s]\nlevel=%s\nhandlers=%s\nqualname=%s\npropagate=%s\n"

        def __str__(self):
            handler_name = self.__handler.name

            return self.__logger_option_template % (self.__logger_name, self.__level,
                                                    handler_name, self.__logger_name, self.__propagate)

        @property
        def log_level(self):
            return self.__level

        def set_log_level(self, level="NOTSET"):
            self.__level = level.upper()
            return self

        @property
        def handler(self):
            return self.__handler

        @handler.setter
        def handler(self, value):
            self.__handler = value

        @property
        def name(self):
            return self.__logger_name

        @property
        def propagate(self):
            return self.__propagate

        def set_propagate(self, value=0):
            self.__propagate = value
            return self

class LogerHelper:
    def __init__(self, log_output_path, log_level=logging.INFO, out):
        logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)
        return logger


def main():
    pass


if __name__ == "__main__":
    main()
