#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Bootloader.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Bootloader or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with Bootloader.
#
# BOOTLOADER MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE
# SUITABILITY OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR
# A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.  BOOTLOADER SHALL NOT BE
# LIABLE FOR ANY LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF
# USING, MODIFYING OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

import argparse
import logging
import os
import sys
from collections import defaultdict
from os import PathLike
from pathlib import Path

from majormode.perseus.constant.logging import LOGGING_LEVEL_LITERAL_STRINGS
from majormode.perseus.constant.logging import LoggingLevelLiteral
from majormode.perseus.utils import cast
from majormode.perseus.utils.logging import DEFAULT_LOGGING_FORMATTER
from majormode.perseus.utils.logging import cast_string_to_logging_level
from majormode.perseus.utils.logging import set_up_logger

from bootloader.utils.plasticscm import reporting, utility
from bootloader.utils.plasticscm.model import Changeset, UserStats


def cast_string_to_path(path: str) -> PathLike:
    return Path(path)


def parse_arguments() -> argparse.Namespace:
    """
    Convert argument strings to objects and assign them as attributes of
    the namespace.


    @return: An instance `Namespace` corresponding to the populated
        namespace.
    """
    parser = argparse.ArgumentParser(description="Plastic SCM repository activities reporting")

    parser.add_argument(
        '--end-time',
        dest='end_time',
        metavar='ISO8601',
        required=False,
        type=cast.string_to_timestamp,
        help="specify the latest date of changesets to return.  This date is "
             "exclusive, so changesets that were made at this date are not "
             "returned."
    )

    parser.add_argument(
        '--logging-level',
        dest='logging_level',
        metavar='LEVEL',
        required=False,
        default=str(LoggingLevelLiteral.info),
        type=cast_string_to_logging_level,
        help=f"specify the logging level ({', '.join(LOGGING_LEVEL_LITERAL_STRINGS)})"
    )

    parser.add_argument(
        '--server',
        dest='plasticscm_server_address',
        metavar='NAME',
        required=False,
        help="specify the Plastic SCM server to connect to"
    )

    parser.add_argument(
        '-o', '--output-file',
        dest='stats_output_file_path_name',
        metavar='PATH',
        required=False,
        type=cast_string_to_path,
        help="specify the path and name of the file to write in the activity "
             "statistics of the Plastic SCM repositories"
    )

    parser.add_argument(
        '--start-time',
        dest='start_time',
        metavar='ISO8601',
        required=False,
        type=cast.string_to_timestamp,
        help="specify the earliest date of changesets to return.  This date "
             "is inclusive, so changesets that were made at this date are "
             "returned."
    )

    return parser.parse_args()


def run():
    arguments = parse_arguments()

    set_up_logger(
        logging_formatter=DEFAULT_LOGGING_FORMATTER,
        logging_level=arguments.logging_level
    )

    plastic_scm_version = reporting.get_cm_version()
    logging.debug(f"Plastic SCM command line v{plastic_scm_version}")

    # Determine the list of Plastic SCM repositories available on the
    # specified server.
    available_repositories = reporting.fetch_available_repositories(
        server_address=arguments.plasticscm_server_address
    )

    # Calculate the activity statistics of the Plastic SCM repositories per
    # user.
    users_stats: dict[str, UserStats] = {}

    for repository_name in available_repositories:
        changesets = reporting.fetch_changeset_history(
            repository_name,
            include_details=True,
            end_date=arguments.end_time,
            start_date=arguments.start_time
        )

        for changeset in changesets:
            user_stats = users_stats.get(changeset.owner)
            if user_stats is None:
                user_stats = UserStats(changeset.owner)
                users_stats[changeset.owner] = user_stats
            user_stats.add_changeset(changeset)

    # Aggregate all the users' activity statistics.
    stats_report = [
        user_stats.generate_stats_report()
        for user_stats in users_stats.values()
    ]

    # Write the stats report into the specified file if any defined,
    # otherwise print the stats report onto the standard output.
    stringified_stats_report = "Plastic SCM users activities report for the period"
    if arguments.start_time:
        stringified_stats_report += f" from {utility.convert_to_plastics_scm_timestamp(arguments.start_time)}"
    if arguments.end_time:
        stringified_stats_report += f" to {utility.convert_to_plastics_scm_timestamp(arguments.end_time)}"

    stringified_stats_report += os.linesep * 2
    stringified_stats_report += os.linesep.join(stats_report)

    if arguments.stats_output_file_path_name is not None:
        with open(arguments.stats_output_file_path_name, 'wt') as fd:
            fd.writelines(stringified_stats_report)
    else:
        print(stringified_stats_report)


