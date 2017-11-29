#!/usr/bin/env python

# Python 3 required. A virtualenv is recommended. Install requirements.txt.

import csv
import datetime
import json
import sys

import requests


# If the file settings_secret.py isn't detected, exit with a nasty message.
try:
    import settings_secret as settings
except:
    print("Could not find settings_secret.py. I don't know what to do!", file=sys.stderr)
    sys.exit(1)

if settings.SSL_CHECKS is False:
    print("WARNING: Disabling insecure SSL request warnings! NOT FOR PROD!", file=sys.stderr)
    requests.packages.urllib3.disable_warnings(
        requests.packages.urllib3.exceptions.InsecureRequestWarning)


# Application entry point for command line execution mode.
def main(argv):

    start_time = datetime.datetime.now()
    print("\nStarting at %s\n" % start_time, file=sys.stderr)

    results = do_force_submit(settings.ENDPOINT, settings.CLIENT_NAME)

    end_time = datetime.datetime.now()
    deltasecs = (end_time - start_time).total_seconds()
    print("\nSubmitted %d Exams. Completed at %s, Elapsed %s" % (len(results), end_time, deltasecs), file=sys.stderr)
    print_results(results)


def do_force_submit(endpoint, client):
    bearer_token = get_bearer_token(
        settings.AUTH_PAYLOAD.get('username', None),
        settings.AUTH_PAYLOAD.get('password', None))
    print("Received bearer token '%s'" % bearer_token, file=sys.stderr)

    results = []
    while True:
        response = post(endpoint, client, bearer_token)
        if response.status_code == 200:
            exams, more = process_success_response(response)
            results.extend(exams)
            if not more:
                break
        else:
            raise RuntimeError("Proctor Exam Expire API call failed with code: %d, %s: %s" % (
                response.status_code, response.reason, response.content))
    return results


# Parses and prints a successful response from server.
# Returns True if there are more records to fetch, else False
def process_success_response(response):
    content = json.loads(response.content.decode("utf-8"))
    exams = content.get('expiredExams')
    print("POST exported %d Exams." % len(exams), file=sys.stderr)
    return exams, content.get('additionalExamsToExpire')


def print_results(results):
    print("CSV for the processed exams now being printed to STDOUT.\n", file=sys.stderr)
    writer = csv.DictWriter(sys.stdout, ['assessmentKey', 'assessmentId', 'examId', 'studentId'])
    writer.writeheader()
    writer.writerows(results)


def post(endpoint, client, bearer_token):
    headers = {"Content-Type": "application/json", "Authorization": "Bearer %s" % bearer_token}
    print("POST '%s'..." % (endpoint + client), file=sys.stderr)
    return requests.post(endpoint + client, headers=headers, data=json.dumps(''), verify=settings.SSL_CHECKS)


def get_bearer_token(username, password):
    endpoint = settings.AUTH_ENDPOINT
    payload = settings.AUTH_PAYLOAD
    if username:
        payload['username'] = username
    if password:
        payload['password'] = password
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(endpoint, headers=headers, data=payload)
    content = json.loads(response.content.decode("utf-8"))
    if response.status_code == 200:
        return content["access_token"]
    else:
        raise RuntimeError("Error retrieving access token from '%s'" % endpoint)


if __name__ == "__main__":
    main(sys.argv[1:])
