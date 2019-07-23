from requests import get
from bs4 import BeautifulSoup

from contextlib import closing
import urllib.request as request
import shutil

dwnld_lst = []
site = 'https://www.tp-link.com/us/support/download/'

def getTPLinkDevices():
    global site
    response = get(site)
    soup = BeautifulSoup(response.text, "html.parser")

    #print(soup)
    #spans = soup.find_all()
    global dwnld_lst
    dwnld_lst = []

    for span in soup.find_all('a'):
        #print(span)
        try:
            if( span['class'] == ['ga-click'] ):
                #print(span['href'])
                dwnld_lst.append((span["href"]))
        except:
            pass


def formatName(firmware):
    reverse = firmware[::-1]
    cut = reverse.find("/")
    bkwd = reverse[:cut]
    return bkwd[::-1]


def _download(firmware):
    try:
        print("[\] Downloading: " + firmware)
        r = get(firmware)
        name = formatName(firmware)
        tst = open("tplink/" + name, "wb")
        tst.write(r.content)
        tst.close()

        print("[+] Successfully Downloaded as: " + name)
    except:
        print("[-] Download went wrong")

def downloadFromSite():
    for raw in dwnld_lst:
        formatted_site = "https://www.tp-link.com" + raw + "#Firmware"
        try:
            response = get(formatted_site)
            soup = BeautifulSoup(response.text, "html.parser")

            #print(formatted_site)
            for span in soup.find_all('a'):
                try:
                    if( span["data-ga"][:8] == "Firmware"):
                        firmware = span['href']
                        _download(firmware)
                except:
                    pass
        except:
            print("[-] Failed to get From: " + firmware)


getTPLinkDevices()
downloadFromSite()