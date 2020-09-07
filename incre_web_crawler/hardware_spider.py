# coding:utf-8
import os
import sys
import json
import time

import requests
from selenium import webdriver

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(BASE_DIR))

from incre_web_crawler.logger import Logger

logger = Logger(log_name=r".\log\HardwareSpider.log", log_level=1, logger="HardwareSpider").get_log()

HARDWARE_URI = "https://access.redhat.com/rs/search?redhat_client=ecosystem-catalog&start=0&rows=4947&q=*%3A*&sort=&facet=true&facet.mincount=1&f.c_catalog_vendor.facet.limit=-1&f.c_version.facet.limit=-1&facet.sort=index&fl=id%2Cportal_thumbnail%2CallTitle%2Cc_catalog_vendor%2Cview_uri%2CpublishedAbstract%2Cch_architecture%2Cc_catalog_channel&facet.field=%7B!ex%3Dc_catalog_channel_tag%7Dc_catalog_channel&facet.field=%7B!ex%3Dch_architecture_tag%7Dch_architecture&facet.field=%7B!ex%3Dc_catalog_vendor_tag%7Dc_catalog_vendor&facet.field=%7B!ex%3Dc_version_tag%7Dc_version&facet.field=%7B!ex%3Dgranularity_category_network%7Dgranularity_category_network&facet.field=%7B!ex%3Dgranularity_category_management%7Dgranularity_category_management&facet.field=%7B!ex%3Dgranularity_category_compute%7Dgranularity_category_compute&facet.field=%7B!ex%3Dgranularity_category_storage%7Dgranularity_category_storage&facet.field=%7B!ex%3Dc_format_tag%7Dc_format&fq=c_certification%3A*&fq=documentKind%3A%22CertifiedHardware%22&fq=%7B!tag%3Dc_catalog_channel_tag%7Dc_catalog_channel%3A%22Server%22&fq=!c_catalog_channel%3A%22Cloud%20Instance%20Type%22"

COMPONENTS_URI = "https://access.redhat.com/rs/search?redhat_client=ecosystem-catalog&start=0&rows=375&q=*%3A*&sort=&facet=true&facet.mincount=1&f.c_catalog_vendor.facet.limit=-1&f.c_version.facet.limit=-1&facet.sort=index&fl=id%2Cportal_thumbnail%2CallTitle%2Cc_catalog_vendor%2Cview_uri%2CpublishedAbstract%2Cch_architecture%2Cc_catalog_channel&facet.field=%7B!ex%3Dc_catalog_channel_tag%7Dc_catalog_channel&facet.field=%7B!ex%3Dch_architecture_tag%7Dch_architecture&facet.field=%7B!ex%3Dc_catalog_vendor_tag%7Dc_catalog_vendor&facet.field=%7B!ex%3Dc_version_tag%7Dc_version&facet.field=%7B!ex%3Dgranularity_category_network%7Dgranularity_category_network&facet.field=%7B!ex%3Dgranularity_category_management%7Dgranularity_category_management&facet.field=%7B!ex%3Dgranularity_category_compute%7Dgranularity_category_compute&facet.field=%7B!ex%3Dgranularity_category_storage%7Dgranularity_category_storage&facet.field=%7B!ex%3Dc_format_tag%7Dc_format&fq=c_certification%3A*&fq=documentKind%3A%22CertifiedHardware%22&fq=%7B!tag%3Dc_catalog_channel_tag%7Dc_catalog_channel%3A%22Component%22&fq=!c_catalog_channel%3A%22Cloud%20Instance%20Type%22"

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0"


class HardwareSpider:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        # 静默模式
        chrome_options.add_argument('--headless')
        # 解决 ERROR:browser_switcher_service.cc(238) 报错,添加下面的试用选项
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--hide-scrollbars')
        chrome_options.add_argument('user-agent={useragent}'.format(useragent=USER_AGENT))
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_all_pages_data(self, url, filename):
        """获取所有数据"""
        headers = {
            "Host": "access.redhat.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0",
            "Accept": "application/vnd.redhat.solr+json",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://catalog.redhat.com/hardware/components/search",
            "Origin": "https://catalog.redhat.com",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0, no-cache",
            "Pragma": "no-cache"
        }
        try:
            session_obj = requests.Session()
            response = session_obj.get(url, headers=headers)
            wb_data = response.text
            ret = json.loads(wb_data)
            doc_data = ret["response"]["docs"]
            with open(filename, "w", encoding="utf-8", errors="ignore") as fp:
                json.dump(doc_data, fp)
        except Exception as e:
            logger.error(e)

    def get_detail_page_data(self, filename1, filename2):
        """获取详情页的数据"""
        with open(filename1, "r", encoding="utf-8", errors="ignore") as fp:
            datas = json.load(fp)

        all_datas = list()
        for data in datas:
            print(f"{data['id']}开始...")
            url = data["view_uri"]
            # import pdb;pdb.set_trace()
            try:
                self.driver.get(url)
            except Exception as e:
                logger.error(e)
                time.sleep(3)

            infos = self.driver.find_elements_by_xpath('//*[@id="product-cert-table"]/table/tbody/tr')
            counts = len(infos)
            detail_infos = list()
            for i in range(1, counts + 1):
                products = self.driver.find_elements_by_xpath(f'//*[@id="product-cert-table"]/table/tbody/tr[{i}]/th[@headers="th-products"]')
                versions = self.driver.find_elements_by_xpath(f'//*[@id="product-cert-table"]/table/tbody/tr[{i}]/td[@headers="th-person1 th-version"]')
                archs = self.driver.find_elements_by_xpath(f'//*[@id="product-cert-table"]/table/tbody/tr[{i}]/td[@headers="th-person1 th-arch"]')
                labels = self.driver.find_elements_by_xpath(f'//*[@id="product-cert-table"]/table/tbody/tr[{i}]/td[@headers="th-person1 th-level"]')
                product = ""
                version = ""
                arch = ""
                label = ""
                if len(products) == 1:
                    product = products[0].text
                if len(products) == 0:
                    product = " "
                if len(versions) == 1:
                    version = versions[0].text
                if len(versions) == 0:
                    version = " "
                if len(archs) == 1:
                    arch = archs[0].text
                if len(archs) == 0:
                    arch = " "
                if len(labels) == 1:
                    label = labels[0].text
                if len(labels) == 0:
                    label = " "

                info = {
                    "product": product,
                    "version": version,
                    "arch": arch,
                    "label": label
                }
                detail_infos.append(info)

            data["detail"] = detail_infos
            all_datas.append(data)

        with open(filename2, "w", encoding="utf-8", errors="ignore") as fp:
            json.dump(all_datas, fp)


def main():
    """主函数"""
    spider = HardwareSpider()
    filename1 = r".\hardware.json"
    filename2 = r".\hardware_result.json"
    spider.get_detail_page_data(filename1, filename2)


if __name__ == '__main__':
    main()
