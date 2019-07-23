from scrapy import Spider
from scrapy.http import FormRequest

#from firmware.items import FirmwareImage
#from firmware.loader import FirmwareLoader
from FirmwareLoader import FirmwareLoader
from FirmwareImage import FirmwareImage

import urllib.parse as urlparse


class NetgearSpider(Spider):
    name = "netgear"
    allowed_domains = ["netgear.com"]
    # "http://downloadcenter.netgear.com/fr/", "http://downloadcenter.netgear.com/de/", "http://downloadcenter.netgear.com/it/", "http://downloadcenter.netgear.com/ru/", "http://downloadcenter.netgear.com/other/"]
    start_urls = ["http://downloadcenter.netgear.com"]

    visited = []

    # grab the first argument from e.g.
    # javascript:__doPostBack('ctl00$ctl00$ctl00$mainContent$localizedContent$bodyCenter$BasicSearchPanel$btnAdvancedSearch','')
    @staticmethod
    def strip_js(url):
        return url.split('\'')[1]

    def parse(self, response):
        # choose the "Product Drilldown" button
        # if response.xpath(
        #         "//a[@id='ctl00_ctl00_ctl00_mainContent_localizedContent_bodyCenter_BasicSearchPanel_btnAdvancedSearch']"):
        #     href = NetgearSpider.strip_js(response.xpath(
        #         "//a[@id='ctl00_ctl00_ctl00_mainContent_localizedContent_bodyCenter_BasicSearchPanel_btnAdvancedSearch']/@href").extract()[0])
        #
        #     yield FormRequest.from_response(response,
        #                                     formname="aspnetForm",
        #                                     formdata={"__EVENTTARGET": href},
        #                                     headers={"Referer": response.url},
        #                                     callback=self.parse)
        #
        # # continue iterating through product/model/os selector
        if True:
            print("AAAAAAAAAAAA")
            if response.xpath("//div[@id='LargeFirmware']//a"):
                print("BBBBBBBBBBBBBBBBb")
                mib = None

            elif "" not in response.xpath("//select[@name='ctl00$ctl00$ctl00$mainContent$localizedContent$bodyCenter$adsPanel$lbProduct']/option/@value").extract():
                print("DDDDDDDDD")
                for entry in response.xpath(
                        "//select[@name='ctl00$ctl00$ctl00$mainContent$localizedContent$bodyCenter$adsPanel$lbProduct']/option"):
                    rsrc = entry.xpath("./@value").extract()[0]
                    text = entry.xpath(".//text()").extract()
                    print("ITERATING THROUGH THE ENTRYYYYY")
                    if text and (response.url, rsrc) not in self.visited:
                        self.visited.append((response.url, rsrc))
                        print("ABOUT TO YIELDDDDDDDDDDDDDDDDDDDDDDDDDDD")
                        yield FormRequest.from_response(response,
                                                        formname="aspnetForm",
                                                        formdata={"__EVENTTARGET": "ctl00$ctl00$ctl00$mainContent$localizedContent$bodyCenter$adsPanel$lbProduct",
                                                                  "ctl00$ctl00$ctl00$mainContent$localizedContent$bodyCenter$adsPanel$lbProduct": rsrc, "__ASYNCPOST:": "true"},
                                                        meta={
                                                            "product": text[0]},
                                                        headers={
                                                            "Referer": response.url},
                                                        callback=self.parse)

            elif "" not in response.xpath("//select[@name='ctl00$ctl00$ctl00$mainContent$localizedContent$bodyCenter$adsPanel$lbProductFamily']/option/@value").extract():
                print("EEEEEEEEEEEEEEEEEE")
                for entry in response.xpath(
                        "//select[@name='ctl00$ctl00$ctl00$mainContent$localizedContent$bodyCenter$adsPanel$lbProductFamily']/option"):
                    rsrc = entry.xpath("./@value").extract()[0]
                    text = entry.xpath(".//text()").extract()

                    if text and (response.url, rsrc) not in self.visited:
                        self.visited.append((response.url, rsrc))

                        yield FormRequest.from_response(response,
                                                        formname="aspnetForm",
                                                        formdata={"__EVENTTARGET": "ctl00$ctl00$ctl00$mainContent$localizedContent$bodyCenter$adsPanel$lbProductFamily",
                                                                  "ctl00$ctl00$ctl00$mainContent$localizedContent$bodyCenter$adsPanel$lbProductFamily": rsrc, "__ASYNCPOST:": "true"},
                                                        headers={
                                                            "Referer": response.url},
                                                        callback=self.parse)

            elif "" not in response.xpath("//select[@name='ctl00$ctl00$ctl00$mainContent$localizedContent$bodyCenter$adsPanel$lbProductCategory']/option/@value").extract():
                print("FFFFFFFFFFFF")
                for entry in response.xpath(
                        "//select[@name='ctl00$ctl00$ctl00$mainContent$localizedContent$bodyCenter$adsPanel$lbProductCategory']/option"):
                    rsrc = entry.xpath("./@value").extract()[0]
                    text = entry.xpath(".//text()").extract()

                    if text and (response.url, rsrc) not in self.visited:
                        self.visited.append((response.url, rsrc))

                        yield FormRequest.from_response(response,
                                                        formname="aspnetForm",
                                                        formdata={"__EVENTTARGET": "ctl00$ctl00$ctl00$mainContent$localizedContent$bodyCenter$adsPanel$lbProductCategory",
                                                                  "ctl00$ctl00$ctl00$mainContent$localizedContent$bodyCenter$adsPanel$lbProductCategory": rsrc, "__ASYNCPOST:": "true"},
                                                        headers={
                                                            "Referer": response.url},
                                                        callback=self.parse)