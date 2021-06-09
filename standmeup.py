import argparse
import os
import subprocess
import json
import sys
import datetime
import calendar
from datetime import date
from datetime import datetime, timedelta

def load_json(jsonfile):
    """Read the "Daily" app json export file."""
    try:
        with open(os.path.join(sys.path[0], jsonfile), "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                raise json.JSONDecodeError(f"{jsonfile} is not valid JSON")
    except IOError:
        raise IOError(f"{jsonfile} does not exist. Please export it from the 'Daily' app.")

def sort_day(day):

    daynames = [n.lower() for n in calendar.day_name]
    day_index = daynames.index(day.lower())
    today_index = datetime.today().weekday()

    print(f"{today_index} has an int of {day_index}")

    if today_index > day_index:
	    days_removed = today_index - day_index
    elif today_index < day_index:
        days_removed = today_index + (7-day_index)
    else:
        days_removed = 7

    print(f"days removed is {days_removed}")
    newdate = datetime.today() - timedelta(days_removed)
    print(f"new date is {newdate}")
    return newdate, days_removed

# Fetches the json from the Daily App, and saves it in a directory
def get_daily_json(sorted_date, days_removed):
    # Need to get the date for dumping the daily json file
    today = date.strftime(sorted_date, '%d-%m-%Y')

    # This gets the path of the script and creates the name of the file to be dumped
    filepath = os.path.realpath(__file__)
    file = f"{os.path.dirname(filepath)}/daily_jsons/standup-{today}.json"

    # This makes the directory for the json dumps if not already existing
    if not os.path.exists(f"{os.path.dirname(filepath)}/daily_jsons"):
        os.mkdir(f"{os.path.dirname(filepath)}/daily_jsons")

    # this executes an `applescript` to get the json data from the Daily App https://dailytimetracking.com/support?utm_source=app#faq-applescript-export
    os.system(f"osascript {os.path.dirname(filepath)}/applescript {days_removed} > {file}")
    return file

def write_standup_file(standup, sorted_date, output_file):
    # This wipes the output file if it has data in it already
    output_file.truncate(0)

    # Gets the current day
    day = f"{date.strftime(sorted_date, '%A')}:\n"

    # Adds the day to the top
    output_file.write(day)

    # Iterates over the JSON items, and adds each as an entry for the standup
    for item in range(len(standup)):
        if (standup[item]['activity']).lower() not in ["break", "lunch"]:
            duration = round(standup[item]['duration'], 2)
            activity = standup[item]['activity']
            entry = f"- [{duration}] {activity} \n"
            output_file.write(entry)

    # Goes back to the first line of the file for printing, and prints
    output_file.seek(0)
    print(output_file.read())

def main(output_file, day):

    sorted_date, days_removed = sort_day(day)
    # Get the files
    file = get_daily_json(sorted_date, days_removed)
    standup = load_json(file)
    output_file = open(os.path.join(sys.path[0], 'output.txt'), 'a+')

    # Build and output the standup
    write_standup_file(standup, sorted_date, output_file)
    output_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generates my standups file from json export from "Daily" app')
    parser.add_argument('--output', '-o', required=False, default='output.txt',
                        help='The desired output location of the generated YAML manifest')
    parser.add_argument('--day', '-d', required=False, default=f"{date.today().strftime('%A')}",
                        help='The day that you wish to create a standup for')
    args = parser.parse_args()
    main(args.output, args.day)
