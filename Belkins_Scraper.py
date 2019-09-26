## Required Libraries: requests, BeautifulSoup4, re
import requests
from bs4 import BeautifulSoup
import re
import os  ## To create a Directory for Downloading

router_url = 'https://www.belkin.com/us/support-search?text=router&fbclid=IwAR17hbM2JBsLRpLvuIt0vF9-WVkMC8X7tpY7gE4f-B8G2w97ZuAQFJ4Ugzo'
base_site = 'https://www.belkin.com/us/'  # Used for Getting Product Sites
base_site2 = 'https://www.belkin.com'    # Used for Getting Direct Download Sites


def directory_setup():
    '''The Directory that the firmware will be downloaded to'''
    if not os.path.exists("BelkinsFirmware"):
        os.makedirs("BelkinsFirmware")


def get_all_product_sites():
    '''This Function Gets All the Products and return its website
        in a list'''
    product_sites = []
    site = requests.get(router_url)
    soup = BeautifulSoup(site.text, "lxml")
    for product in soup.find_all("a", class_="btn-pill-primary grey-pill prodPageLink"):
        product_sites.append(product['href'])
    print("[+] Acquired Product Sites")
    return product_sites


def get_download_site(dir):
    ''' Returns the href that contains the direct site
    with the download'''
    url = base_site + dir
    site = requests.get(url)
    soup = BeautifulSoup(site.text, "lxml")
    a = soup.find(title="Downloads / Firmware")
    print("[+] Acquired Download Site: " + a["href"])
    return a["href"]


def _formatName(firmware):
    '''Simply Formats the Downloadble's name for easier file names'''
    reverse = firmware[::-1]
    cut = reverse.find("/")
    bkwd = reverse[:cut]
    return bkwd[::-1]


def _download(firmware):
    '''The Actual Downloading Part, So modify it if u want the files
    to have a certain name, or to a certain file directory'''
    name = _formatName(firmware)
    print("[/] Downloading: " + name)

    file = open("BelkinsFirmware/" + name, "wb")
    try:
        response = requests.get(firmware)
        file.write(response.content)
        response.close()
        file.close()
        print("[+] Successfully Downloaded")
    except:
        print("[-] Failed to Complete Download")


def _locate_html_dwnld(soup):
    '''Quick and Easy Way to get the Direct Download Link - checks for bin in href'''
    dwnld_list = []
    for dwnld in soup.find_all(href=re.compile("bin$")):
        dwnld_list.append(dwnld['href'])
    return dwnld_list


def download(dir):
    '''Acquires the direct url and calls the download helper function'''
    url = base_site2 + dir
    site = requests.get(url)
    soup = BeautifulSoup(site.text, "lxml")
    for firmware in _locate_html_dwnld(soup):
        _download(firmware)


if __name__=='__main__':
    directory_setup()
    product_list = get_all_product_sites()

    # Test Code
    # y = get_download_site(product_list[1])
    # download(y)

    for product in product_list:
        try:
            site = get_download_site(product)
            download(site)
        except:
            print("[-] Failed to Get Download Site: " + product)
