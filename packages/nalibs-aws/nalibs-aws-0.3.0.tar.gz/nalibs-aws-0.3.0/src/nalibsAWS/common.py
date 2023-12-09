#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from jinja2 import Template
from pathlib import Path


class NotFoundError(Exception):
    """Exception to handle situations where a credentials file is not found"""
    pass


class Exit(Exception):
    """Exception to allow a clean exit from any point in execution"""
    CLEAN = 0
    ERROR = 1
    MISSING_PROFILEINI = 2
    MISSING_SECRETS = 3
    BAD_PROFILEINI = 4
    LOCATION_NO_DIRECTORY = 5
    BAD_SECRETS = 6
    BAD_LOCALE = 7

    FAIL_LOCATE_NSS = 10
    FAIL_LOAD_NSS = 11
    FAIL_INIT_NSS = 12
    FAIL_NSS_KEYSLOT = 13
    FAIL_SHUTDOWN_NSS = 14
    BAD_PRIMARY_PASSWORD = 15
    NEED_PRIMARY_PASSWORD = 16
    DECRYPTION_FAILED = 17

    PASSSTORE_NOT_INIT = 20
    PASSSTORE_MISSING = 21
    PASSSTORE_ERROR = 22

    READ_GOT_EOF = 30
    MISSING_CHOICE = 31
    NO_SUCH_PROFILE = 32

    UNKNOWN_ERROR = 100
    KEYBOARD_INTERRUPT = 102

    def __init__(self, exitcode):
        self.exitcode = exitcode

    def __unicode__(self):
        return f"Premature program exit with exit code {self.exitcode}"


def get_template_dotenv_config():
    src_location = Path(__file__).absolute().parent
    template_location =  "{}/tmpl.dotenv_config.j2".format(src_location)
    with open(template_location, 'r', encoding='UTF-8') as file:
        return file.read()


def export_dotenv_config(filepath, data):
    template_dotenv_config = get_template_dotenv_config()
    jinja2_template = Template(template_dotenv_config)
    # content = jinja2_template.render(**input_data)
    content = jinja2_template.render(list_env=data)
    with open(filepath, 'w', encoding='UTF-8') as file:
        file.write(content)

