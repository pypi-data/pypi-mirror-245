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

from majormode.perseus.model.date import ISO8601DateTime


def convert_to_plastics_scm_timestamp(timestamp: ISO8601DateTime) -> str:
    """
    Convert a timestamp to a string representation with the date and time
    only.


    :param timestamp: A timestamp.


    :return: The string representation with the date and time only.
    """
    plastic_scm_timestamp = f'{timestamp.year:>04}-{timestamp.month:>02}-{timestamp.day:>02}'

    if hasattr(plastic_scm_timestamp, 'hour'):
        plastic_scm_timestamp += f' {timestamp.hour:>02}:{timestamp.minute:>02}:{timestamp.second:>02}'
    else:
        plastic_scm_timestamp += ' 00:00:00'

    return plastic_scm_timestamp
