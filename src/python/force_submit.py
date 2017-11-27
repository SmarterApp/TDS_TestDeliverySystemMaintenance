#!/usr/bin/env python

# Python 3 required. A virtualenv is recommended. Install requirements.txt.

import datetime
import getopt
import json
import sys

import requests


# SETTINGS:
# Put your own version of these values in settings_secret.py and they'll be overridden.
# Don't use the dict, use the key names as top level variables. For example, your file
# could contain (uncommented, of course):
# ENDPOINT = "http://example.com"
# SSL_CHECKS = True
# ... etc.

settings = {}
# The client (e.g. 'SBAC_PT') will be appended to this URL - please end URLs with a forward slash.
settings['ENDPOINT'] = "http://localhost:8080/proctor/exams/expire/"
settings['CLIENT'] = "SBAC_PT"
settings['SSL_CHECKS'] = True  # Should be False for production.

# SUPER SENSITIVE AUTH INFO (these are fake - put yours in settings_secret.py)
settings['AUTH_ENDPOINT'] = "https://localhost/auth/oauth2/access_token?realm=/sbac"
settings['AUTH_PAYLOAD'] = {
    "client_id": "me",
    "client_secret": "secret",
    "grant_type": "password",
    "password": "password",
    "username": "me@example.com"
}

# END SETTINGS SECTION - now we override them if settings_secret.py is present.
try:
    import settings_secret as settings
except:
    print("*** USING INTERNAL SETTINGS.")
    print("*** Please create a settings_secret.py and add your settings there!")

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

    bearer_token = get_bearer_token(
        settings.AUTH_PAYLOAD.get('username', None),
        settings.AUTH_PAYLOAD.get('password', None))
    print("Received bearer token '%s'" % bearer_token)

    success = post(endpoint, client, bearer_token, progress)

    end_time = datetime.datetime.now()
    deltasecs = (end_time - start_time).total_seconds()
    print("\nRequest %s at %s, Elapsed %s" % ("succeeded" if success else "failed", end_time, deltasecs))


def post(endpoint, client, bearer_token, progress):
    headers = {"Content-Type": "application/json", "Authorization": "Bearer %s" % bearer_token}
    progress("POSTing to '%s'" % (endpoint + client))
    response = requests.post(endpoint + client, headers=headers, data=json.dumps(''), verify=settings.SSL_CHECKS)
    if response.status_code == 200:
        return True
    else:
        raise RuntimeError("Proctor Exam Expire API call failed with code: %d, %s: %s" % (
            response.status_code, response.reason, response.content))
    return False


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
