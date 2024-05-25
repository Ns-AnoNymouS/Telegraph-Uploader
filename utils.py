"""
Module: progress_utils

This module provides utilities for displaying progress while downloading.
"""

import logging
import time
import math

logger = logging.getLogger(__name__)


async def progress(done, total, message, start_time):
    """Display progress while downloading."""

    present = time.time()
    percentage = done * 100 / total
    progressbar = f"[{'▪️' * math.floor(percentage/10)}{'▫️' * (10 - math.floor(percentage/10))}]"
    text = progressbar + f"\n{human_redable(done)} of {human_redable(total)}"
    if round((present - start_time) % 3) == 0 or done == total:
        try:
            await message.edit(text)
        except Exception as e: # pylint: disable=broad-exception-caught
            logger.warning(e)


def human_redable(size):
    """Convert bytes to human-readable format."""

    size_units = ["B", "KB", "MB", "GB", "TB"]
    for unit in size_units:
        formatted_size = f"{round(size, 2)} {unit}"
        size /= 1024
        if size < 1:
            break
    return formatted_size
