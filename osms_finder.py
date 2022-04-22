from argparse import ArgumentParser
from bs4 import BeautifulSoup
import requests
import socket


def getArguments():
    parser = ArgumentParser()
    parser.add_argument('--target', help='Enter a target site address')
    parser.add_argument('--ipFile', help='Ip address file')
    parser.add_argument('--notSub', help='Enter the site without a subdomain')
    return parser.parse_args()


def ipLister(file: str) -> list:
    try:
        with open(file, 'r') as f:
            ips = [i.strip() for i in f.readlines()
                   if i not in ('', '\n') and not i.isspace()]

        return ips

    except FileNotFoundError:
        print('[!]-> File not found! <-[!]')
        quit()


def linkFinder(site: str) -> list:
    r = requests.get(site).text
    d = BeautifulSoup(r, 'html.parser')
    all_links = d.find_all('a')
    all_links = [i.attrs['href'] for i in all_links]
    links = []

    for i in all_links:
        if (i.startswith('https://') or i.startswith('http://')):
            links.append(i)

    return addressStriper(links)


def scanner(links: str, ips: list, wosub: str) -> None:
    links = set(links)
    found = False

    for siteaddr in links:
        if (wosub not in siteaddr):
            try:
                tIp = socket.gethostbyname(siteaddr)

            except socket.error:
                print(f'[*]-> I can\'t connect to site {siteaddr}')
                continue

            if (tIp in ips):
                found = True

    if (not found):
        print('\n[!]-> No other site found on the same server!! <-[!]\n')


def addressStriper(links: list) -> list:
    l = []
    
    for i in links:
        i = http_s_striper(i)
        slash_index = i.find('/')
        if (slash_index == -1):
            l.append(i)

        else:
            l.append(i[:slash_index])

    return l


def http_s_striper(site: str) -> str:
    if (site.startswith('http://')):
        return site[7:].strip('/')

    elif (site.startswith('https://')):
        return site[8:].strip('/')

    else:
        return site.strip('/')


def main() -> None:

    args = getArguments()
    target = args.target
    notSub = args.notSub

    if (target):

        if ((notSub) and (notSub in target)) and \
                (target.startswith('https://') or target.startswith('http://')):

            try:
                ip_list = [socket.gethostbyname(http_s_striper(target))]

            except socket.error:
                print('[!]-> Check the given site or your internet connection <-[!]')
                quit()

            if (args.ipFile):
                ip_list.extend(ipLister(args.ipFile))

            scanner(linkFinder(target), ip_list, notSub.strip('/'))

        else:
            print('\n[!]-> Please, check the notSub parameter value! <-[!]\n')

    else:
        print(
            '\n[!]-> Please enter a valid site address, Ex: https://www.exsitemysite.com\n')


if __name__ == '__main__':
    main()
