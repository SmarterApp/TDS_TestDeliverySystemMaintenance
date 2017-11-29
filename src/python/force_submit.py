#!/usr/bin/env python

# Python 3 required. A virtualenv is recommended. Install requirements.txt.

import datetime
import getopt
import json
import sys

import requests


# If the file settings_secret.py isn't detected, exit with a nasty message.
try:
    import settings_secret as settings
except:
    print("Could not find settings_secret.py file. I don't know what to do!")
    sys.exit(1)

if settings.SSL_CHECKS is False:
    print("WARNING: Disabling insecure SSL request warnings! NOT FOR PROD!")
    requests.packages.urllib3.disable_warnings(
        requests.packages.urllib3.exceptions.InsecureRequestWarning)


# This is an overridable callback method for reporting progress.
def progress(message):
    print(message)


# Application entry point for command line execution mode.
def main(argv):

    endpoint = settings.ENDPOINT
    client = settings.CLIENT

    try:
        opts, _ = getopt.getopt(argv, "he:c:", ["help", "endpoint", "client", ])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-e", "--endpoint"):
            endpoint = arg
            print("Command line set endpoint to '%s'" % endpoint)
        elif opt in ("-c", "--client"):
            client = arg
            print("Command line set client to '%s'" % client)

    start_time = datetime.datetime.now()
    print("\nStarting at %s\n" % start_time)

    count = do_force_submit(endpoint, client, progress)

    end_time = datetime.datetime.now()
    deltasecs = (end_time - start_time).total_seconds()
    print("\nSubmitted %d Exams. Completed at %s, Elapsed %s" % (count, end_time, deltasecs))


def do_force_submit(endpoint, client, progress):
    bearer_token = get_bearer_token(
        settings.AUTH_PAYLOAD.get('username', None),
        settings.AUTH_PAYLOAD.get('password', None))
    print("Received bearer token '%s'" % bearer_token)

    count = 0
    while True:
        response = post(endpoint, client, bearer_token, progress)
        if response.status_code == 200:
            processed, more = process_success_response(response)
            count += processed
            if not more:
                break
        else:
            raise RuntimeError("Proctor Exam Expire API call failed with code: %d, %s: %s" % (
                response.status_code, response.reason, response.content))
    return count


# Parses and prints a successful response from server.
# Returns True if there are more records to fetch, else False
def process_success_response(response):
    content = json.loads(response.content.decode("utf-8"))
    more = content.get('additionalExamsToExpire')
    exams = content.get('expiredExams')
    processed = len(exams)
    print("Expired %d Exams." % processed)
    print("All done!" if not more else "Fetching more...")
    return processed, more


def post(endpoint, client, bearer_token, progress):
    headers = {"Content-Type": "application/json", "Authorization": "Bearer %s" % bearer_token}
    progress("POSTing to '%s'" % (endpoint + client))
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


def usage():
    print("Hit proctor force_submit endpoint with correct auth.")
    print("\nSee README.md for details and configuration instructions.")
    print("  To modify those settings, copy settings_default.py to settings_secret.py and edit the copy.")
    print("\nHelp/usage details:")
    print("  -h, --help               : this help screen")
    print("  -e, --endpoiont          : override the endpoint to hit")
    print()


if __name__ == "__main__":
    main(sys.argv[1:])
