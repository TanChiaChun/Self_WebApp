# Import from packages
import os
import argparse
import logging
from sys import stdout, exit
import sqlite3
import csv

# Initialise project
CURR_DIR, CURR_FILE = os.path.split(__file__)
PROJ_NAME = CURR_FILE.split('.')[0]
logger = logging.getLogger("my_logger")

# Get command line arguments
my_arg_parser = argparse.ArgumentParser(description=f"{PROJ_NAME}")
my_arg_parser.add_argument("input", help="File path of SQLite DB")
my_arg_parser.add_argument("output", help="File path of CSV output")
my_arg_parser.add_argument("--log", help="DEBUG to enter debug mode")
args = my_arg_parser.parse_args()

# # Get environment variables
# env_var1 = os.getenv("env_var1")
# env_var2 = os.getenv("env_var2")

##################################################
# Variables
##################################################
LOG_END = "\n-------------------------"
productivity = []

##################################################
# Functions
##################################################
def handle_exception(log_message):
    logger.error(log_message, exc_info=True)
    logger.error("App run fail!" + LOG_END)
    exit()

def initialise_app():
    # # Check environment variables
    # if env_var1 == None or env_var2 == None:
    #     handle_exception("Missing environment variables!")
    
    # Create directories
    os.makedirs("data", exist_ok=True)
    os.makedirs("data/app", exist_ok=True)

    # Logger
    if args.log == "DEBUG":
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    my_log_format = logging.Formatter("[%(asctime)s] %(message)s")
    my_log_stream = logging.StreamHandler(stdout)
    my_log_stream.setFormatter(my_log_format)
    logger.addHandler(my_log_stream)
    my_log_file = logging.FileHandler("data/app/" + PROJ_NAME + ".log")
    my_log_file.setFormatter(my_log_format)
    logger.addHandler(my_log_file)

def finalise_app(log_message=""):
    if log_message != "":
        logger.info(log_message)
    logger.info("App complete running successfully" + LOG_END)
    exit()

##################################################
# Main
##################################################
initialise_app()

# Read from DB
con = sqlite3.connect(args.input)
cur = con.cursor()
for row in cur.execute("SELECT * FROM Productivity"):
    productivity.append(row)
con.close()
logger.info(f"Complete reading from {args.input}")

# Write to CSV
with open(args.output, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["id", "item", "last_check", "last_check_previous", "category"])
    writer.writerows(productivity)
logger.info(f"Output to {args.output}")

finalise_app()