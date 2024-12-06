#///////////////////////////////////////////////////////////////////////////////
#
# (c) 2019-2022 Toolsensing, Inc. All rights reserved.
# Unless otherwise permitted, no distribution or use is permitted.
#
#///////////////////////////////////////////////////////////////////////////////


# coding=utf-8
import os
import time         # sleep
import paramiko
import traceback
import socket
import sys
import subprocess
import logging
from abc import ABCMeta, abstractmethod, ABC


class CommandBase(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def command(self, commandline, abs_work_path, timeout_s, **kwargs):
        pass


class RemoteCommand(CommandBase):
    def __init__(self, ssh_ip, ssh_user_name, ssh_passwd, ssh_port=22, logger=None):
        self.logger = logging.getLogger(logger) if isinstance(logger, str) or logger is None else logger

        self.last_cmd_stdout = ""
        self.abs_work_path = "./"
        self.ssh_user_name = ssh_user_name
        self.ssh_ip = ssh_ip
        self.ssh_passwd = ssh_passwd
        self.ssh_port = ssh_port
        self.ssh = None
        os.system("rm -rf ~/.ssh/known_hosts")

    def __del__(self):
        self.close()
        self.logger.debug("delete RemoteCommand with ssh link to %s@%s:%s"
                        % (self.ssh_user_name, self.ssh_ip, self.ssh_port))

    def command(self, commandline, abs_work_path=None, timeout_s=None, **kwargs):
        if self.ssh is None:
            self.ssh = self.__open(self.ssh_ip, self.ssh_user_name, self.ssh_passwd, self.ssh_port)
            if self.ssh is None:
                self.logger.error("connect remote machine failed: %s@%s:%s"
                                  % (self.ssh_user_name, self.ssh_ip, self.ssh_port))
                return None

        if abs_work_path is None:  # if abs_work_path is not specified, use the last path
            abs_work_path = self.abs_work_path
        else:
            self.abs_work_path = abs_work_path

        commandline = "cd %s && %s" % (abs_work_path, commandline)
        return self.__exec_commands(self.ssh, commandline,
                                    timeout_s=timeout_s, **kwargs)

    def __open(self, ipaddress, username, password, port=22):
        self.close()
        self.ssh = self.__connect(ipaddress, username, password, port)
        self.ssh_user_name = username
        self.ssh_ip = ipaddress
        self.abs_work_path = ""
        self.last_cmd_stdout = ""
        return self.ssh

    def close(self):
        if self.ssh is not None:
            # note: we must ensure that all channel have received EOF before closing,
            # otherwise something error may happen
            time.sleep(2)
            self.ssh.close()
            self.ssh = None
            self.logger.info("closed ssh link to %s@%s:%s" % (self.ssh_user_name, self.ssh_ip, self.ssh_port))

    # multiprocess/multithread safety
    def __connect(self, host, username, password, port):
        conn = None
        i = 0
        try_times = 5
        while i < try_times:
            conn = self.__connect_once(host, username, password, port)
            if conn is None:
                i = i + 1
                time.sleep(10)
            else:
                break

        self.ssh = conn
        return conn

    # multiprocess/multithread safety
    @staticmethod
    def __connect_once(host, user, passwd, port):
        """
                __connect to the remote host machine by ssh
        :param port:
        :param host: str, ip address or hostname of remote host machine (eg. host='127.0.0.1')
        :param user:
        :param passwd:
        :return: return a __connect object if __connect the remote host successfully, otherwise return None
        """
        ssh = paramiko.SSHClient()  # create a SSHClient object
        ssh.set_log_channel(r"SSH")
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            # __connect to the remote host machine
            # note: the current remote work directory is "/home/username/" after logging in the remote host machine
            ssh.connect(hostname=host, username=user, password=passwd, allow_agent=True, port=port)
            return ssh
        except:
            # log except
            traceback.print_exc()
            return None

    @staticmethod
    def __get_output_and_error(channel):
        boutput = bytes()
        berror = bytes()

        # recv = channel.recv(len(channel.in_buffer))
        # boutput += recv
        while not channel.exit_status_ready() \
                or channel.recv_ready() \
                or channel.recv_stderr_ready():
            if channel.recv_ready():
                recv = channel.recv(1024)
                boutput += recv

            if channel.recv_stderr_ready():
                recv = channel.recv_stderr(1024)
                berror += recv

            if channel.closed:
                break

        # note: the stdout and stderr buffer of the channel can be also readable even if the channel has closed
        while channel.recv_ready():
            recv = channel.recv(1024)
            boutput += recv

        while channel.recv_stderr_ready():
            recv = channel.recv_stderr(1024)
            berror += recv

        return channel.recv_exit_status(), boutput, berror

    def __exec_commands(self, conn, cmd, timeout_s=None, **kwargs):
        """
                execute command on the remote host machine
        :param conn: a __connect object returned by __connect (eg. __connect("10.69.143.11"))
        :param cmd: str, a complete command need to be executed (eg. cmd='ls -al')
        :param timeout_s:
        :return: str, return the result of the command, if there is no result returning, it will return a blank line
        note: it will change directory to home directory of remote machine automatically after calling
        __exec_commands() function
        """
        wrap_cmd_func = None
        if "wrap_cmd_func" in kwargs:
            wrap_cmd_func = kwargs["wrap_cmd_func"]
        self.logger.debug("excute: ssh -p %s %s@%s %s"
                          % (self.ssh_port, self.ssh_user_name,
                             self.ssh_ip, cmd if wrap_cmd_func is None else wrap_cmd_func(cmd)))
        try:
            stdin, stdout, stderr = conn.exec_command(cmd, timeout=timeout_s)
        except socket.timeout:
            self.logger.error("execute command '%s' timeout!" % cmd)
            return -1, None, None
        except:
            self.logger.error("execute command '%s' error: %s" % (cmd, sys.exc_info()[0]))
            raise
        else:
            # note: stdin, stdout and stdout are from a same channel
            stdin.close()
            stdout_channel = stdout.channel

            ret, boutput, berror = self.__get_output_and_error(stdout_channel)

            results = ''.join(str(boutput, encoding="utf-8"))
            errors = ''.join(str(berror, encoding="utf-8"))
            self.last_cmd_stdout = results
            stdout.close()
            stderr.close()
        return ret, results, errors


class LocalCommand(CommandBase):
    def __init__(self, logger=None):
        self.__logger = logging.getLogger(logger) if isinstance(logger, str) or logger is None else logger
        self.__abs_work_path = "./"
        self.__host_ip = None
        self.__host_ssh_port = None

    def command(self, commandline, abs_work_path=None, timeout_s=None, **kwargs):
        if abs_work_path is None:  # if abs_work_path is not specified, use the last path
            abs_work_path = self.__abs_work_path
        else:
            self.__abs_work_path = abs_work_path

        commandline = "cd %s && %s" % (abs_work_path, commandline)
        wrap_cmd_func = None
        if "wrap_cmd_func" in kwargs:
            wrap_cmd_func = kwargs["wrap_cmd_func"]

        self.__logger.debug("local excute: %s" % commandline if wrap_cmd_func is None else wrap_cmd_func(commandline))
        return self.__get_status_output(commandline)

    @staticmethod
    def __get_status_output(*args, **kwargs):
        p = subprocess.Popen(*args, **kwargs, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        return p.returncode, str(stdout, encoding='utf-8'), str(stderr, encoding='utf-8')


def main():
    pass


if __name__ == "__main__":
    main()
