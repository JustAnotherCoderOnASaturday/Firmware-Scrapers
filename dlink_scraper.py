from requests import get
from requests import post
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

import shutil
import urllib.request as request
from contextlib import closing

listOfAllDevices = []
websiteOfProducts = 'https://support.dlink.com/ProductInfo.aspx?m='
allProductsSite = 'https://dlinkmea.com/index.php/site/allproducts?page='
pages = 35

# def isAsciiChar(c):
#     if ord(c)==45 or 47<ord(c)<58 or 64<ord(c)<91:
#         return True
#     return False
#
# def getAllPossibleDevices(file):
#     '''Will get all possible devices from the all products size'''
#     f = open(file, "w+")
#     for x in range(1, pages):
#         response = get( allProductsSite + str(x) )
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         for em in soup.find_all('em'):
#             em_str = str(em)
#             item = ''
#             for c in em_str[4:]:
#                 if not (isAsciiChar(c) ):
#                     break
#                 item += c
#
#             f.write(item + '\n')
#     f.close()

def getDevicesImproved():
    site = 'https://support.dlink.com/AllPro.aspx'
    f = open('all_products.txt', 'w')
    try:
        response = get(site)
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find('table')
        table_rows = table.find_all('tr')

        for tr in table_rows:
            td = tr.find_all('td')
            row = [i.text for i in td]
            f.write(row[0] + '\n')
    except:
        pass
    finally:
        f.close()

def putFileItemsToList(file):
    f = open(file, 'r')
    for l in f.readlines():
        listOfAllDevices.append(l[:-1])
    f.close()

def checkIfSiteExists():
    '''Checks if the Website of the product exists'''
    f = open('working_site.txt', 'w')
    for device in listOfAllDevices:
        site = websiteOfProducts + device
        try:
            response = get( site )
            if response.request.url == 'https://support.dlink.com/ErrorPage.htm':
                print('[-] Item Failed: ' + device)
                continue
        except RequestException:
            print('[-] Item Failed: ' + device)
            continue
        else:
            f.write(device + '\n')
            print("[+] Item Works: " + device)
    f.close()

def getValues(device):
    try:
        site = get('https://support.dlink.com/ProductInfo.aspx?m=' + device)
        soup = BeautifulSoup(site.text, 'html.parser')
        ver = []
        for num in soup.find_all('option'):
            if num['value'] != '':
                ver.append(num['value'])

        print('[+] Success: Device: ' + str(ver) )
        return ver
    except:
        return []

def _download(json, value_ver, device):
    MAX = 2   # Can adjust this number
    try:
        for i in range(0, len(json['item'][0]['file']) ):
            if json['item'][0]['file'][i]['filetypename'] == 'Firmware':

                dwnld = json['item'][0]['file'][i]['url']
                print("[\] Downloading: "+ dwnld)

                with closing(request.urlopen(dwnld)) as r:
                    with open('firmwares/' + device + "__" + value_ver+ '__' + json['item'][0]['file'][i]['name']+ '.zip' , 'wb') as f:
                        shutil.copyfileobj(r, f)

                MAX -= 1
                print("[+] Successfully Downloaded: " + dwnld)
                if MAX==0:
                    break
                continue
    except:
        print("[-] Download went wrong")

def downloadFromSite(value, device):
    try:
        url = 'https://support.dlink.com/ajax/ajax.ashx?action=productfile&lang=en-US&ver={}&ac_id=1'\
            .format( str(value) )
        response = post(url)
        _download(response.json(), value, device)
    except:
        print("[-] Failed to Load Site")



if __name__ == '__main__':
    print("[+] Running Program")
    # getDevicesImproved()  # Use This function to get the devices
    # putFileItemsToList('all_products.txt')
    # print(len(listOfAllDevices))

    # checkIfSiteExists()
    putFileItemsToList('working_site.txt')

    for device in listOfAllDevices:
        for value in getValues(device):
            downloadFromSite(value, device)

    print("[+] Finished Running")