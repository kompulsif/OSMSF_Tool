# One Server More Site Finder Tool

## Usage:
* Run in terminal, `pip install -r requirements.txt`

* `python osms_finder.py --target https://subdom.exthetargetmysite.bla --notSub exthetargetmysite.bla --ipFile myIpFile.txt`

* Optional Parameter:
    - `--ipFile` : If the value is given, the contents of the file and the ip address of the target site will be used. If not given, only the ip address of the target site will be used by default.

* Mandatory Parameters:
    - `--target`
    - `--notSub`

* `--notSub` : You must write the target site without subdomain as the value for this parameter.

***

## What doest it do ?
* This tool scans the site and finds all the links. Then it finds the ip address of the sites that do not contain the --notSub value you give from these links and checks whether they are in the ip list. If there is, it will show you.