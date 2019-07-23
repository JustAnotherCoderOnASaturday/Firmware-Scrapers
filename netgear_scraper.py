from requests import get
from bs4 import BeautifulSoup
import json
import re
import os

dwnld_dict = dict()

def get_models_request():
    site = "https://www.netgear.com/system/supportModels.json"
    print("[\] Getting Support Models Site")
    try:
        response = get(site)
        soup = BeautifulSoup(response.text, "html.parser")
        json_format = json.loads(soup.text)
        for item in json_format:
            dwnld_dict[item.get('title')] = item['url']
        print("[+] Successfully Acquired Models & Sites")
    except:
        print("[-] Failed to Get Support Models Site")

def formatName(firmware):
    reverse = firmware[::-1]
    cut = reverse.find("/")
    bkwd = reverse[:cut]
    return bkwd[::-1]

def _download(firmware):
    try:
        name = formatName(firmware)
        print("[\] Downloading: " + name)
        if(os.path.exists('netgear/' + name)):
            print("Already Downloaded")
            return None
        r = get(firmware)
        file = open("netgear/" + name, "wb")
        file.write(r.content)
        r.close()
        print("[+] Sccessfully Downloaded as: " + name)
    except:
        print("[-] Download went wrong")


# def downloadFromSite():
#     #site = 'https://www.netgear.com/support/product/DM200.aspx'
#     site ='https://www.netgear.com/support/product/DGFV338.aspx'
#     response = get(site)
#     soup = BeautifulSoup(response.text, "html.parser")
#     allbtn = soup.find_all(href=re.compile("\W*(zip)"))
#     for btn in allbtn:
#         #print(btn['href'])
#         ## Device name will be put
#         _download(btn['href'])
#     print("over")


def downloadFromSite():
    site = 'https://www.netgear.com'
    for item in dwnld_dict:
        if (dwnld_dict[item][0] == '/'): # Ensures none are https, since the others are supported
            try:
                formatted_site = site + dwnld_dict[item]

                response = get(formatted_site)
                soup = BeautifulSoup(response.text, "html.parser")

                allbtn = soup.find_all(href=re.compile("\W*(Firmware)(.*)(.zip)"))   # Download Firmware Zip files
                # allbtn = soup.find_all(href=re.compile("\W*(zip)"))               # Download ALL FILES
                num_downloaded = 0
                for btn in allbtn:
                    _download(btn['href'])
                    num_downloaded += 1
                    if num_downloaded == 3:     # A Max of 3 versions to download
                        break
            except:
                print("[-] Error In Getting the Site: " + formatted_site)


get_models_request()
downloadFromSite()
