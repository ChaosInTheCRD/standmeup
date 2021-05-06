import argparse
import os
import subprocess
import json
import sys
import datetime
from datetime import date

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

def get_daily_json():
    today = date.today()
    today = date.strftime(today, '%d-%m-%Y')
    cmd = "osascript applescript"
    file = f"daily_jsons/standup-{today}.json"
    if not os.path.exists('daily_jsons'):
        os.mkdir("daily_jsons")
    os.system(f"osascript applescript > {file}")
    return file

def write_standup_file(standup, output_file):
    output_file.truncate(0)
    day = f"{date.today().strftime('%A')}:\n"
    output_file.write(day)
    for item in range(len(standup)):
        duration = round(standup[item]['duration'], 2)
        activity = standup[item]['activity']
        entry = f"- [{duration}] {activity} \n"
        output_file.write(entry)
    output_file.seek(0)
    print(output_file.read())

def main(standup_json, output_file):

    file = get_daily_json()
    # Get the files
    standup = load_json(file)
    output_file = open(os.path.join(sys.path[0], 'output.txt'), 'a+')

    # Build the standup
    write_standup_file(standup, output_file)
    output_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generates my standups file from json export from "Daily" app')
    parser.add_argument('--standup', '-c', required=False, default="hello",
                        help='The location of the Platform Components YAML file')
    parser.add_argument('--output', '-o', required=False, default='output.txt',
                        help='The desired output location of the generated YAML manifest')
    args = parser.parse_args()
    main(args.standup, args.output)
