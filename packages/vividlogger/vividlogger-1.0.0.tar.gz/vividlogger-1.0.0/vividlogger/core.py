#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ File Name      :  core.py
@ Time           :  2023/11/27 11:17:37
@ Author         :  keyork
@ Version        :  0.1
@ Contact        :  chengky18@icloud.com
@ Description    :  None
@ History        :  0.1(2023/11/27) - None(keyork)
"""


def log_warn(data: str) -> None:
    """print warning

    Args:
        data (str): warning
    """
    print(f"[Warn] {data}")


def log_info(data: str) -> None:
    """print info

    Args:
        data (str): info
    """
    print(f"[Info] {data}")


def log_error(data: str) -> None:
    """print error

    Args:
        data (str): error
    """
    print(f"[Error] {data}")
