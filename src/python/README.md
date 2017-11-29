# Force Submit Proctor Utility
## Instruction Manual

### Description
This command line utility calls Proctor's 'expire exams' endpoint repeatedly until there are no more exams to expire. It will then print a csv data table to standard out containing details about all the exams that were expired during the session. All diagnostic output is written to standard error.

The endpoint for force submit in Proctor is currently https://PROCTOR_URL/proctor/Services/exams/expire/CLIENT_NAME. You will need to replace PROCTOR_URL to point to whatever Proctor you have deployed, and CLIENT_NAME with your client name.

#### force_submit.py
This is the utility script to run. It takes no arguments and is meant to be run from crontab. Because only the csv data goes to standard out, you can run it like this to create a csv file containing all the expired exam details:
```
$ ./force_submit.py > recently_expired_exams.csv
```

#### settings_secret.py
This file contains the settings used by the utility to connect to proctor and the authentication endpoint. It's recommended to copy settings_default.py to this file and modify as needed. Adjust permissions to prevent unauthorized users from reading the contents. Due to its sensitive nature, this file is not distributed with the utilities and is not in source control.

### Installation and setup
The loader requires Python 3.4 or better. It's been tested against Python 3.4 and 3.6. No other Python versions are supported. The package requirements are in the customary requirements.txt file.

Python environment setup is detailed below for CentOS, Ubuntu, and MacOS. It should run fine on Windows and many other platforms if Python 3.6 and the requirements are properly set up.

#### CentOS 6.9
```
-- become root or use sudo for all `'`#`'` commands, regular user for `'`$`'
-- base setup
# yum -y update
# yum -y install yum-utils
# yum -y groupinstall development
-- set up python 3, using ius packages --
# yum -y install https://centos6.iuscommunity.org/ius-release.rpm
# yum -y install python36u
# yum -y install python36u-pip
# yum -y install python36u-devel
-- set up virtual environment for an isolated python
$ cd <loader-script-directory>
$ mkdir environments
$ python3.6 -m venv fs36  # can change fs36 to whatever you like
$ source environments/fs36/bin/activate  # enter the fs36 env. should show a nice env prompt.
-- now all regular python and pip commands will use your art python 3.6 environment
$ python -V  # show python version. can also run pip -V to see that pip is OK
$ pip install -r requirements.txt  # run from within the loader script directory

-- If you prefer epel or Python 3.4, don't install ius-release and adjust the commands accordingly (changing 36u to 34):
# yum install -y epel-release
# yum install -y python34-pip ..., etc.
```
You're all set! Make sure to always enter the correct python environment before running the script or you may start up the wrong python version or encounter missing packages.

It's been reported that on some CentOS installations it's necessary to manually install these packages (enter your fs36 env first):
$ pip install pyopenssl ndg-httpsclient pyasn1 "requests[security]"

#### Ubuntu 14.04
```
Become root or use sudo for all '#' commands, be regular user for '$' commands.
-- base setup
# apt update && apt upgrade
-- set up python 3
# apt install python3
# apt install python3-pip
# apt install build-essential libssl-dev libffi-dev python3-dev  # for paramiko/ssl
-- set up virtual environment for an isolated python
# apt-get install python3.4-venv
$ cd <loader-script-directory>
$ mkdir environments
$ python3.4 -m venv fs34
$ source environments/fs34/bin/activate  # enter the fs34 env. should show a nice env prompt.
-- now all regular python and pip commands will use your art python 3.4 environment
$ python -V  # show python version. can also run pip -V to see that pip is OK
$ pip install -r requirements.txt
```
You're all set! Make sure to always enter the correct python environment before running the loader scripts, or you may start up the wrong python version or encounter missing packages.

#### MacOS Sierra (OSX 10.12)
```
-- base setup - install Homebrew (https://brew.sh/)
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
-- set up python 3
$ brew install python3
-- set up virtual environment for an isolated python
$ cd <loader-script-directory>
$ mkdir environments
$ python3 -m venv fs36
$ source environments/fs36/bin/activate  # enter the fs36 env. should show a nice env prompt.
-- now all regular python and pip commands will use your art python 3.6 environment
$ python -V  # show python version. can also run pip -V to see that pip is OK
$ pip install -r requirements.txt
```
You're all set! Make sure to always enter the correct python environment before running the script, or you may start up the wrong python version or encounter missing packages.
