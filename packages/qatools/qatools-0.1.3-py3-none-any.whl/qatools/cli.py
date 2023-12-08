#!/usr/bin/python
"""
@Author  :  Lijiawei
@Date    :  2023/11/6 7:29 PM
@Desc    :  main line.
"""
import argparse
import sys

from qatools import __description__
from qatools import __version__
import base64
import os
import platform
import socket
import stat

import psutil

STATICPATH = os.path.dirname(os.path.realpath(__file__))
DEFAULT_ADB_PATH = {
    "Windows": os.path.join(STATICPATH, "adb", "windows", "adb.exe"),
    "Darwin": os.path.join(STATICPATH, "adb", "mac", "adb"),
    "Linux": os.path.join(STATICPATH, "adb", "linux", "adb"),
    "Linux-x86_64": os.path.join(STATICPATH, "adb", "linux", "adb"),
    "Linux-armv7l": os.path.join(STATICPATH, "adb", "linux_arm", "adb"),
}


def make_file_executable(file_path):
    """
    If the path does not have executable permissions, execute chmod +x
    :param file_path:
    :return:
    """
    if os.path.isfile(file_path):
        mode = os.lstat(file_path)[stat.ST_MODE]
        executable = True if mode & stat.S_IXUSR else False
        if not executable:
            os.chmod(file_path, mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        return True
    return False


def builtin_adb_path():
    system = platform.system()
    machine = platform.machine()
    adb_path = DEFAULT_ADB_PATH.get(f"{system}-{machine}")
    if not adb_path:
        adb_path = DEFAULT_ADB_PATH.get(system)
    if not adb_path:
        raise RuntimeError(
            f"No adb executable supports this platform({system}-{machine})."
        )

    if system != "Windows":
        # chmod +x adb
        make_file_executable(adb_path)
    return adb_path


def get_adb_path():
    if platform.system() == "Windows":
        ADB_NAME = "adb.exe"
    else:
        ADB_NAME = "adb"

    # Check if adb process is already running
    for process in psutil.process_iter(["name", "exe"]):
        if process.info["name"] == ADB_NAME:
            return process.info["exe"]

    # Check if ANDROID_HOME environment variable exists
    android_home = os.environ.get("ANDROID_HOME")
    if android_home:
        adb_path = os.path.join(android_home, "platform-tools", ADB_NAME)
        if os.path.exists(adb_path):
            return adb_path

    # Use qatools builtin adb path
    adb_path = builtin_adb_path()
    return adb_path


def get_host_ip():
    """
    Query the local ip address
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def encryption(value):
    """
    encryption
    :param value:
    :return:
    """
    bytes_url = value.encode("utf-8")
    str_url = base64.b64encode(bytes_url)
    return str_url


def decryption(value):
    """
    decryption
    :param value:
    :return:
    """
    str_url = base64.b64decode(value).decode("utf-8")
    return str_url


def main():
    adb = get_adb_path()
    parser = argparse.ArgumentParser(description=__description__)

    parser.add_argument(
        "-v", "--version", dest="version", action="store_true", help="show version"
    )
    subparsers = parser.add_subparsers(help="sub-command help")
    subparsers.add_parser("clear", help="clear app cache data.")
    subparsers.add_parser("info", help="show app setting page.")
    subparsers.add_parser("adb", help="complete adb debugging capability.")
    subparsers.add_parser(
        "remote", help="open Android device remote debugging port(5555)."
    )
    subparsers.add_parser(
        "proxy", help=f"enable device global proxy({get_host_ip()}:8888)."
    )
    subparsers.add_parser("unproxy", help=f"disable device global proxy.")

    if len(sys.argv) == 1:
        # qa
        parser.print_help()
        sys.exit(0)
    elif len(sys.argv) == 2:
        # print help for sub-commands
        if sys.argv[1] in ["-v", "--version"]:
            # qa -v
            print(f"{__version__}")

        elif sys.argv[1] == "remote":
            # qa remote
            ret = os.system(f"{adb} tcpip 5555")
            if ret == 0:
                print("已经开启端口5555远程调试，请检查是否开启成功。")
            sys.exit(0)
        elif sys.argv[1] == "proxy":
            # qa proxy
            ret = os.system(
                f'{adb} {decryption(b"c2hlbGwgc2V0dGluZ3MgcHV0IGdsb2JhbCBodHRwX3Byb3h5")} {get_host_ip()}:8888'
            )
            if ret == 0:
                print(f"已经开启代理，请检查是否开启成功。{get_host_ip()}:8888")
            sys.exit(0)
        elif sys.argv[1] == "unproxy":
            # qa proxy
            ret = os.system(
                f'{adb} {decryption(b"c2hlbGwgc2V0dGluZ3MgcHV0IGdsb2JhbCBodHRwX3Byb3h5IDow")}'
            )
            if ret == 0:
                print("已经关闭代理，请检查是否关闭成功。")  # line:63
            sys.exit(0)

        elif sys.argv[1] == "adb":
            # qa adb
            os.system(f"{adb}")
            sys.exit(0)

        elif sys.argv[1] == "clear":
            os.system(f"{adb} shell pm clear {decryption(b'Y29tLnltdDM2MC5hcHAubWFzcw==')}")
        elif sys.argv[1] == "info":
            os.system(
                f"{adb} shell am start -a android.settings.APPLICATION_DETAILS_SETTINGS -d package:{decryption(b'Y29tLnltdDM2MC5hcHAubWFzcw==')}")

        elif sys.argv[1] in ["-h", "--help"]:
            # qa -h
            parser.print_help()
        else:
            parser.print_help()
        sys.exit(0)

    elif sys.argv[1] == "adb":
        del sys.argv[0:2]
        args = " ".join([str(i) for i in sys.argv])
        os.system(f"{adb} {args}")
        sys.exit(0)

    elif len(sys.argv) == 3:
        if sys.argv[1] == "clear":
            os.system(f"{adb} shell pm clear {sys.argv[2]}")
        elif sys.argv[1] == "info":
            os.system(
                f"{adb} shell am start -a android.settings.APPLICATION_DETAILS_SETTINGS -d package:{sys.argv[2]}")  # line:84

        elif sys.argv[1] == "proxy":
            ret = os.system(
                f'{adb} {decryption(b"c2hlbGwgc2V0dGluZ3MgcHV0IGdsb2JhbCBodHRwX3Byb3h5")} {get_host_ip()}:{sys.argv[2]}'
            )  # line:55
            if ret == 0:
                print(f"已经开启代理，请检查是否开启成功。{get_host_ip()}:{sys.argv[2]}")
            sys.exit(0)
        sys.exit(0)

    args = parser.parse_args()

    if args.version:
        print(f"{__version__}")
        sys.exit(0)
