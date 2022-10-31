import argparse
import json
import os
from github import Github


'''

This script is intended to be run in conjuction with https://github.com/EnricoMi/publish-unit-test-result-action to upload trimmed
test results from the output to the checks api "text" field for further analysis.

The script takes as input the filename of the json output by the aforementioned action, trims it, and uploads it to the "text" field
of the check run provided in the json file.

Note that there is a limit of ~65k characters in the check run API text field - so we do some trimming of the json to ensure that size
is respected.

'''

# Initiate the parser
parser = argparse.ArgumentParser()

# Add long and short argument
parser.add_argument("--json", "-j", help="Path to the result json output by https://github.com/EnricoMi/publish-unit-test-result-action")

def main():
    # Read arguments from the command line
    args = parser.parse_args()

    token = os.getenv('GITHUB_TOKEN')

    f = open(args.json)
    d = json.load(f)
    out = []
    
    check_run_id = int(d["check_url"].split("/")[-1])
    for elem in d['cases']:
        if 'success' in elem['states']:
            for i in range(len(elem['states']['success'])):
                output = {
                    "test_name": elem['states']['success'][i]['test_name'],
                    "class_name": elem['states']['success'][i]['class_name'],
                    "result_file": elem['states']['success'][i]['result_file'],
                    "time": elem['states']['success'][i]['time'],
                    "state": "success",
                    "check_run_id": check_run_id,
                }
                out.append(output)
            for elem in d['cases']:
        if 'failure' in elem['states']:
            for i in range(len(elem['states']['failure'])):
                output = {
                    "test_name": elem['states']['failure'][i]['test_name'],
                    "class_name": elem['states']['failure'][i]['class_name'],
                    "result_file": elem['states']['failure'][i]['result_file'],
                    "time": elem['states']['failure'][i]['time'],
                    "state": "failure",
                    "check_run_id": check_run_id,
                }
                out.append(output)
        if 'skipped' in elem['states']:
            for i in range(len(elem['states']['skipped'])):
                output = {
                    "test_name": elem['states']['skipped'][i]['test_name'],
                    "class_name": elem['states']['skipped'][i]['class_name'],
                    "result_file": elem['states']['skipped'][i]['result_file'],
                    "time": elem['states']['skipped'][i]['time'],
                    "state": "skipped",
                    "check_run_id": check_run_id,
                }
                out.append(output)

    with open(args.json + "l", 'w') as f:
        for o in out:
            f.write(json.dumps(o), separators=(',', ':'))
            f.write('\n')

    
    z = open(args.json)
    print(z)
        


if __name__ == '__main__':
    main()