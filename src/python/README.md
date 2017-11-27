# Force Submit Proctor Utility
## Instruction Manual

### Description
TODO

#### force_submit.py
This is the main executable script. Run with -h or --help for a usage summary. This script performs the following main functions:

1. TODO
  - TODO
  - TODO
2. TODO
3. TODO
  - TODO
  - TODO


#### settings_secret.py
This file is a settings override file the user will create and modify, then prevent unauthorized users from reading via permissions, etc. Copy settings_default.py to this file and modify to taste.
This file should contain all the sensitive passwords and URL's, etc, the utilities read to connect to ART and the sFTP server where the sensitive data is stored. Due to its nature, this file is not distributed with the utilities and is not in source control.

### Usage
```
Paste usage here.
```
### Examples
The script is designed to be run with no arguments, with all settings coming from settings_secret.py. For example, to expire all partially completed exams for the configured envorionment:
> $ ./force_submit.py

Or to do the same with an overridden proctor URL:
> $ ./force_submit.py -u TODO

##### Usage notes
TODO

If TODO:

*   TODO
*   TODO

When in doubt, TODO.

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

### Configuration

#### Settings, overrides, and security

The script is configured by reading a settings file. This way you can run the scripts with no arguments and they'll do what you want every time.

The script contains sensible, but public default settings. To provide your own values, create a file called settings_secret.py** and add your own versions of the settings found in the SETTINGS section of the main script. It's easier to copy all the lines over then adjust as desired. If settings_secret.py is not found at runtime, the script will complain, as this is probably not what you want.

If you put any sensitive values in settings_secret.py it's advised to **set the permissions on settings_secret.py so nobody but you can read it**. It also shouldn't be put into source control or emailed around.

### Troubleshooting

#### Runtime issues

TODO

#### Performance

TODO
