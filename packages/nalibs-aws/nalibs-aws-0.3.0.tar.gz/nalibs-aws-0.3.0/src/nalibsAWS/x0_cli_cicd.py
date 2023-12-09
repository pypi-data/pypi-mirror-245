#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json

from nalibsUtils import json_writer, yaml_writer

# from .__base import init_logging
try:
    from .__base import init_logging
except ImportError:
    from __base import init_logging

# from .__version import __version__
try:
    from .__version import __version__
except ImportError:
    from __version import __version__

# from .common import NotFoundError, Exit, export_dotenv_config
try:
    from .common import NotFoundError, Exit, export_dotenv_config
except ImportError:
    from common import NotFoundError, Exit, export_dotenv_config

# from .aws_sm_func import get_secret
try:
    from .aws_sm_func import get_secret
except ImportError:
    from aws_sm_func import get_secret


class OutputFormat:
    def __init__(self, cmdargs: argparse.Namespace, secrets_values, output_filepath):
        self.secrets_values = secrets_values
        self.cmdargs = cmdargs
        self.output_filepath = output_filepath

    def output(self):
        pass


class HumanOutputFormat(OutputFormat):
    def output(self):
        sys.stdout.write(self.secrets_values)
        # for k, v in self.secrets_values.items():
        #     print("{key}={value}".format(key=k,value=v))


class JSONOutputFormat(OutputFormat):
    def output(self):
        json_writer(self.output_filepath, self.secrets_values)


class YAMLOutputFormat(OutputFormat):
    def output(self):
        yaml_writer(self.output_filepath, self.secrets_values)


class DOTENVOutputFormat(OutputFormat):
    def output(self):
        export_dotenv_config(self.output_filepath, self.secrets_values)


# From https://bugs.python.org/msg323681
class ConvertChoices(argparse.Action):
    """
    Argparse action that interprets the `choices` argument as a dict
    mapping the user-specified choices values to the resulting option
    values.
    """

    def __init__(self, *args, choices, **kwargs):
        super().__init__(*args, choices=choices.keys(), **kwargs)
        self.mapping = choices

    def __call__(self, parser, namespace, value, option_string=None):
        setattr(namespace, self.dest, self.mapping[value])


## ==================================================
## CASE: GET / MERGE AWS SECRETS ==> EXPORT TO FILE
## ==================================================

def parse_sys_args_cicd_aws_sm() -> argparse.Namespace:
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(
        description="nalibs - tiny tools"
    )

    parser.add_argument(
        "--secret-override",
        action="store",
        help="AWS Secret Name - override env",
    )
    parser.add_argument(
        "--secret-app",
        action="store",
        help="AWS Secret Name - app env",
    )
    parser.add_argument(
        "--output-file",
        action="store",
        default="/tmp/output_example",
        help="AWS Secret Name - output filename",
    )
    parser.add_argument(
        "-r",
        "--region",
        action="store",
        default="ap-southeast-1",
        help="AWS Region",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity level. Warning on -vv (highest level) user input will be printed on screen",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=__version__,
        help="Check version",
    )

    ## [BEGIN] OUTPUT FORMAT ================
    format_choices = {
        "dotenv": DOTENVOutputFormat,
        "json": JSONOutputFormat,
        "yaml": YAMLOutputFormat,
    }
    parser.add_argument(
        "-f",
        "--format",
        action=ConvertChoices,
        choices=format_choices,
        default=DOTENVOutputFormat,
        help="Format for the output",
    )
    ## [END] OUTPUT FORMAT ==================

    args = parser.parse_args()

    return args


def main_cicd_aws_sm() -> None:
    """Main entry point"""
    args = parse_sys_args_cicd_aws_sm()

    if args.verbose == 1:
        log_level = 1
    elif args.verbose >= 2:
        log_level = 2
    else:
        log_level = 0

    global logger

    logger = init_logging(log_level)

    # testLog()
    logger.info("Running version: %s", __version__)
    logger.debug("Parsed commandline arguments: %s", args)
    
    ## Get Secrets
    secret_app  = args.secret_app
    secret_override = args.secret_override
    region = args.region
    output_filename = args.output_file
    logger.info("GET DATA [%s]: %s / %s", region, secret_app, secret_override)
    logger.info("OUTPUT FILENAME: %s", output_filename)

    if secret_override == None:
        kv_override = dict()
    else:
        kv_override = json.loads(get_secret(secret_override, region))
    
    kv_app = json.loads(get_secret(secret_app, region))
    kv_merge_output =  kv_app | kv_override
    logger.debug(kv_app)
    logger.debug(kv_override)
    logger.info(kv_merge_output)

    ## Export passwords into one of many formats
    formatter = args.format(args, kv_merge_output, output_filename)
    formatter.output()


def run_cicd_aws_sm():
    try:
        main_cicd_aws_sm()
    except KeyboardInterrupt:
        print("Quit.")
        sys.exit(Exit.KEYBOARD_INTERRUPT)
    except Exit as e:
        sys.exit(e.exitcode)

## ==================================================
## [END] ============================================
## ==================================================

if __name__ == "__main__":
    run_cicd_aws_sm()

