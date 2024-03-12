import requests
import os
from dotenv import load_dotenv

IPFILE = os.path.join(os.getcwd(), 'currentIP.txt')
load_dotenv()


def getLoginCookies():
    payload = {'FORM_SUBMIT': 'tl_login',
               'username': os.getenv('username'), 'password': os.getenv('password')}

    r = requests.post(
        'https://mein.domainssaubillig.de/interface.html', data=payload)
    return r.cookies


def updateDomain(auth, ipv4='', ipv6=''):

    payload = {
        'uid': os.getenv('uid'),
        'did': '140014',
        'formf': '919',
        'ipv4': ipv4,
        'ipv6': ipv6
    }

    r = requests.post(
        'https://mein.domainssaubillig.de/editdns.php', data=payload, cookies=auth)

    return r


def updateSubdomain(auth, ipv4='', ipv6=''):
    payload = {
        'uid': os.getenv('uid'),
        'sdid': '198516',
        'formf': '919',
        'ipv4': ipv4,
        'ipv6': ipv6
    }

    r = requests.post(
        'https://mein.domainssaubillig.de/sub_editdns.php', data=payload, cookies=auth)

    return r


def updateIPs(ip):
    auth = getLoginCookies()
    requestsresults = [updateDomain(auth=auth, ipv4=ip),
                       updateSubdomain(auth=auth, ipv4=ip)]
    for r in requestsresults:
        if not 'erfolgreich' in str(r.content):
            print("error")


if __name__ == "__main__":
    curIP = requests.get('https://api.ipify.org').content.decode('utf8')
    if "TEST" in os.environ:
        print(f"TEST IP: {curIP}")
        exit()
    print(f"running DNS update {os.getcwd()} {curIP}")

    if os.path.isfile(IPFILE):
        with open(IPFILE, "r") as f:
            lastIP = f.read()
    else:
        lastIP = None
        print(os.path.abspath(__file__))
        print(f"IP-file {IPFILE}")
        print("Keine letzte IP gefunfen!")

    if not curIP == lastIP:
        updateIPs(curIP)
        with open(IPFILE, "w") as f:
            f.write(curIP)
