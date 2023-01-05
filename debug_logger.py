import os
import time
import logging
import asyncio

logging.basicConfig(level=logging.INFO, filename=None, filemode="w",
                    format="%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

def setup_debug_logger():
    # Create the debug directory if it doesn't exist
    if not os.path.exists("debug"):
        os.makedirs("debug")

    # Get current year, month, and day
    current_time = time.gmtime()
    year = current_time.tm_year
    month = current_time.tm_mon
    day = current_time.tm_mday

    # Create the year, month, and day directories if they don't exist
    year_path = f"debug/{year}"
    month_path = f"{year_path}/{month}"
    day_path = f"{month_path}/{day}"
    if not os.path.exists(year_path):
        os.makedirs(year_path)
    if not os.path.exists(month_path):
        os.makedirs(month_path)
    if not os.path.exists(day_path):
        os.makedirs(day_path)

    # Get the current hour
    hour = current_time.tm_hour

    # Determine which file to log to based on the current hour
    if hour // 6 == 0:
        filename = "debug.log"
    elif hour // 6 == 1:
        filename = "debug1.log"
    elif hour // 6 == 2:
        filename = "debug2.log"
    else:
        filename = "debug3.log"

    # Set the file to log to
    file_path = f"{day_path}/{filename}"
    logging.basicConfig(filename=file_path, filemode="w",
                        format="%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    # Check if the log file exists
    if not os.path.exists(file_path):
        # If the log file doesn't exist, create it
        open(file_path, "w+").close()

    logging.basicConfig(filename=file_path, filemode="a",
                        format="%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

async def log_command(command: str, output: str):
    # Check if the log file exists
    if isinstance(logging.root.handlers[0], logging.FileHandler):
        # If the handler is a FileHandler, use the 'baseFilename' attribute
        if not os.path.exists(logging.root.handlers[0].baseFilename):
            # If the log file doesn't exist, create it
            await setup_debug_logger()
    elif isinstance(logging.root.handlers[0], logging.StreamHandler):
        # If the handler is a StreamHandler, use the 'stream' attribute
        if not logging.root.handlers[0].stream.writable():
            # If the log stream is not writable, create a new log file
            await setup_debug_logger()
    logger = logging.getLogger()
    with logging.root.handlers[0].stream as log_file:
        log_file.write(f"{command}: {output}\n")
    return True
