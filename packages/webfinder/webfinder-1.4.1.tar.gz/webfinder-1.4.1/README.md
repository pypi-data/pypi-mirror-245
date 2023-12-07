finder-py
=======

It is only a tool for 'LAN file Share', support [win, mac, linux]

### Use help

~~~bash
~  finder -h
usage: finder [-h] [-i IP] [-p PORT] [-d DIR] [-q] [-u] [-m] [-z] [-r]
              [--hidden] [--user USER] [--password PASSWORD] [--start]
              [--stop] [--pid_file PID_FILE] [--log_file LOG_FILE]

LAN file sharing 1.3.3

optional arguments:
  -h, --help            show this help message and exit
  -i IP, --ip IP        Local IP
  -p PORT, --port PORT  Local port
  -d DIR, --dir DIR     Shared directory path
  -q, --qr              Show QRCode
  -u, --upload          Support upload
  -m, --mkdir           Support mkdir
  -z, --zip             Support zip
  -r, --rm              Support rm
  --hidden              Show hidden
  --user USER           Basic Auth User
  --password PASSWORD   Basic Auth Password
  --start               daemon start
  --stop                daemon stop
  --pid_file PID_FILE   pid_file
  --log_file LOG_FILE   log_file

make it easy
~~~

### Install

~~~bash
~ sudo pip install finder-py
~~~

or 

~~~bash
~ sudo pip install finder-py -i https://pypi.tuna.tsinghua.edu.cn/simple/
~~~

Install the latest version with Github

~~~bash
~ sudo pip install git+https://github.com/hyxf/finder-py.git@main
~~~

---------

### Uninstall

~~~bash
~ sudo pip uninstall finder-py
~~~

### Upgrade

~~~bash
~ sudo pip install --upgrade finder-py
~~~

or

~~~bash
~ sudo pip install -U finder-py
~~~