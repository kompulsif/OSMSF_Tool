from argparse import ArgumentParser
from urllib.parse import urlparse
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


def linkFinder(site: str) -> set:
    r = requests.get(site).text
    d = BeautifulSoup(r, 'html.parser')
    all_links = d.find_all('a')
    all_links = [i.attrs['href'] for i in all_links]
    checked_links = set()

    for i in all_links:
        if i.startswith(('https://', 'http://')):
            i = urlparse(i)
            i = i.scheme + '://' + i.netloc
            if notSub not in i: checked_links.add(i)

    return checked_links


def showLinks(fLinks: dict) -> None:
    for (link, ip) in fLinks.items():
        print(link.ljust(50) + " | " + ip)


def scanner(links: set, ips: list) -> None:
    sameServerLinks = {}

    for siteaddr in links:
        try:
            tIp = socket.gethostbyname(urlparse(siteaddr).netloc)

        except socket.error:
            print(f'[*]-> I can\'t connect to site {siteaddr}')
            continue

        if tIp in ips:
            sameServerLinks[siteaddr] = tIp

    if len(sameServerLinks.keys()) == 0:
        print('\n[!]-> No other site found on the same server!! <-[!]\n')
    else:
        showLinks(sameServerLinks)


def main() -> None:
    global notSub, ip_list
    args = getArguments()
    target = args.target
    notSub = args.notSub.strip('/')

    if target:
        if (notSub and (notSub in target)) and (target.startswith(('https://', 'http://'))):
            try:
                ip_list = [socket.gethostbyname(urlparse(target).netloc)]

            except socket.error:
                print('[!]-> Check the given site or your internet connection <-[!]')
                quit()

            if args.ipFile:
                ip_list.extend(ipLister(args.ipFile))

            scanner(linkFinder(target), ip_list)

        else:
            print('\n[!]-> Please, check the notSub parameter value! <-[!]\n')

    else:
        print(
            '\n[!]-> Please enter a valid site address, Ex: https://www.exsitemysite.com\n')


if __name__ == '__main__':
    main()
