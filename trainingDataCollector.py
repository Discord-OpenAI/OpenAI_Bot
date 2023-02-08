"""
trainingDataCollecter.py
Made by CoCFire#1111
Training data collection module for OpenAI model fine-tuning
I'm making it cuz I really need a better way to record the prompts used than the console log files lol
I've improved it quite a bit so far. Since I'm kinda lazy, I just copied a bit of code from debug_logger since
it saves me a lot of time. Anyway, even though it's not yet implemented into the actual bot, it's still something
"""
# trainingDataCollector.py
# Made by CoCFire#1111

# Importing modules
import os, asyncio, discord, openai, requests, json, time, datetime, debug_logger


async def getFile(name: str):

    """

    Creates a new file to log prompts for manual review, then returns the file
    use "default" for name to automatically generate a name
    
    """

    # Making sure everything exists
    if not os.path.exists("training_data"):
        os.makedirs("training_data")
    if not os.path.exists("training_data/raw"):
        os.makedirs("training_data/raw")
    if not os.path.exists("training_data/processed"):
        os.makedirs("training_data/processed")
    if not os.path.exists("training_data/partial"):
        os.makedirs("training_data/partial")

    if name == 'default':
        # Basically makes a file using a generic filename based on the time
        current_time = time.gmtime()
        year = current_time.tm_year
        month = current_time.tm_mon
        day = current_time.tm_mday
        hour = current_time.tm_hour
        form = f'{year}_{month}_{day}_{hour}'
        filename = f"{form}.jsonl"
    else:
        filename = f'{name}.jsonl'

    return filename
    
async def logPrompt(filename: str, formatted: bool, prompt: str, output: str):
    
    """

    Logs a prompt to a given file for later review
    filename: string, name of the file to log to, meant for use with the getFile function
    formatted: boolean, whether or not to preformat the prompts. If they are preformatted, outputs will not be logged.
    prompt: string, the prompt to log

    """

    # Checking to see if the file exists
    if not os.path.exists(f"training_data/raw/{filename}"):
        filename = getFile("default")

    # Setting the filepath as a variable
    filepath = f'training_data/raw/{filename}'

    # Checkinig the value of "formatted" then formatting respectively
    if formatted == True:
        with open(filepath, 'a') as f:
            f.write('\n{"prompt": "'+f'{prompt}'+'", "completion": ""}')
    elif output == 'null':
        with open(filepath, 'a') as f:
            f.write(f'\n[PROMPT: {prompt}] [OUTPUT: NULL]')
    else:
        with open(filepath, 'a') as f:
            f.write(f'\n[PROMPT: {prompt}] [OUTPUT: {output}]')
