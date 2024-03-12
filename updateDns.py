import requests
import os
from dotenv import load_dotenv

DIR = "/root/dyndns/"

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
                if 'erfolgreich' in str(r.content):
                        print("Sucessfull")
                else:
                        print("error")

if __name__ == "__main__":
        curIP = requests.get('https://api.ipify.org').content.decode('utf8')
        print(f"running DNS update {os.getcwd()} {curIP}")

        with open(DIR + "currentIP.txt", "r") as f:
                lastIP = f.read()

        if not curIP == lastIP:
                updateIPs(curIP)
                with open(DIR + "currentIP.txt", "w") as f:
                        f.write(curIP)
        else:
                print("same IP")
