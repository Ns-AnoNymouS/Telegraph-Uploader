import logging
logger = logging.getLogger(__name__)

import time
import math


async def progress(done, total, message, start_time):
    """ Progress while Downloading """

    present = time.time()
    percentage = done * 100 / total
    progressbar = "[{0}{1}]".format(
        ''.join(["▪️" for i in range(math.floor(percentage / 10))]),
        ''.join(["▫️" for i in range(10 - math.floor(percentage / 10))])
    )
    text = progressbar + f"\n{human_redable(done)} of {human_redable(total)}"
    if round((present - start_time) % 3) == 0 or done == total:
        try:
            await message.edit(text)
        except Exception as e:
            pass


def human_redable(size):
    """ Converting bytes to human readable bytes"""

    size_units = ['B', 'KB', 'MB', 'GB', 'TB']
    for unit in size_units:
        formatted_size = f'{round(size, 2)} {unit}'
        size /= 1024
        if size < 1:
            break     
    return formatted_size
