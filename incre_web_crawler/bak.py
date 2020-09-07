# # coding:utf-8
# import os
# import sys
# import time
# import json
#
# import requests
# from selenium import webdriver
# from ghost import Ghost, Session
# from lxml import etree
#
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, os.path.dirname(BASE_DIR))
#
# from incre_web_crawler.logger import Logger
# from incre_web_crawler import constants
#
# class HardwareSpider:
#     """硬件部分爬虫"""
#
#     def __init__(self):
#         # self.ghost = Ghost()
#         self.session = Session(Ghost())
#
#     def get_single_page_data(self, url, filename):
#         """获取单页数据"""
#         headers = {
#             "User-Agent": constants.USER_AGENT,
#         }
#         try:
#             response = self.session.open(url, headers=headers)
#             page, resources = self.session.wait_for_page_loaded()
#
#             wb_data = response.text
#             html = etree.HTML(wb_data)
#             need_data = html.xpath('//*[@id="nr-search-all"]/article')
#             logger.info("first element:{element}".format(element=need_data[0]))
#             if need_data:
#                 with open(filename, "w", encoding="utf-8", errors="ignore") as fp:
#                     for data in need_data:
#                         fp.write(data)
#         except Exception as e:
#             logger.error(e)


# query_params = {
#     'redhat_client': 'ecosystem-catalog',
#     'start': 0,
#     'rows': 15,
#     'q': '*:*',
#     'sort': '',
#     'facet': 'true',
#     'facet.mincount': 1,
#     'f.c_catalog_vendor.facet.limit': -1,
#     'f.c_version.facet.limit': -1,
#     'facet.sort': 'index',
#     'fl': 'id,portal_thumbnail,allTitle,c_catalog_vendor,view_uri,publishedAbstract,ch_architecture,c_catalog_channel',
#     'facet.field': '{!ex=c_catalog_channel_tag}c_catalog_channel',
#     'facet.field': '{!ex=ch_architecture_tag}ch_architecture',
#     'facet.field': '{!ex=c_catalog_vendor_tag}c_catalog_vendor',
#     'facet.field': '{!ex=c_version_tag}c_version',
#     'facet.field': '{!ex=granularity_category_network}granularity_category_network',
#     'facet.field': '{!ex=granularity_category_management}granularity_category_management',
#     'facet.field': '{!ex=granularity_category_compute}granularity_category_compute',
#     'facet.field': '{!ex=granularity_category_storage}granularity_category_storage',
#     'facet.field': '{!ex=c_format_tag}c_format',
#     'fq': 'c_certification:*',
#     'fq': 'documentKind:"CertifiedHardware"',
#     'fq': '{!tag=c_catalog_channel_tag}c_catalog_channel:"Server"',
#     'fq': '!c_catalog_channel:"Cloud Instance Type"'
# }
# URI = urlencode(query_params)

from urllib.parse import quote, unquote, urlencode
from lxml import etree