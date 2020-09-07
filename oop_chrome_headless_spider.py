# coding:utf-8
import functools
import time
import requests
from datetime import datetime
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotInteractableException

RHEL8_URL = "https://access.redhat.com/downloads/content/rhel---8.1/x86_64/9180/kernel/4.18.0-80.el8/x86_64/fd431d51/package-changelog"
RHEL7_URL = "https://access.redhat.com/downloads/content/rhel---7.4/x86_64/4118/kernel/3.10.0-123.el7/src/fd431d51/package-changelog"
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0"
USERNAME = "rd.sangfor@gmail.com"
PASSWORD = "@Sangfor123"
LOGIN_URL = "https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/auth?client_id=customer-portal&redirect_uri=https%3A%2F%2Faccess.redhat.com%2Fwebassets%2Favalon%2Fj%2Fincludes%2Fsession%2Fscribe%2F%3FredirectTo%3Dhttps%253A%252F%252Faccess.redhat.com&state=ee983228-b950-4e69-82f8-1d201d73b885&nonce=38f73164-a3bb-49bb-8b7b-9f7d64103b61&response_mode=fragment&response_type=code&scope=openid"
BASE_URL = "downloads/content/rhel---8.1/x86_64/9180/kernel/4.18.0-80.el8/x86_64/fd431d51/package-changelog"
REDHAT_DOMAIN = "https://access.redhat.com"

TODAY = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
RHEL7_STORAGE_DIR = r"D:\git_pro\Spiders\Spider-Red\rhel7_changelog\changelog-"
RHEL8_STORAGE_DIR = r"D:\git_pro\Spiders\Spider-Red\rhel8_changelog\changelog-"


def time_it(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        start = time.time()
        fn(*args, **kwargs)
        end = time.time()
        print("Time cost for function `{}`: {}".format(fn.__name__, (end - start)))

    return inner


def retry(**kw):
    def wrapper(func):
        def _wrapper(*args, **kwargs):
            raise_ex = None
            for num in range(kw['reNum']):
                print("This is the {number}-time of requests".format(number=str(num + 1)))
                try:
                    return func(*args, **kwargs)
                except Exception as ex:
                    raise_ex = ex
            print(raise_ex)

        return _wrapper

    return wrapper


def dict2str(dict_obj):
    """字典格式转成字符串格式"""
    assert isinstance(dict_obj, dict)
    cookie_elements = list()
    for k, v in dict_obj.items():
        each_obj = "=".join([k, v])
        cookie_elements.append(each_obj)

    element_str = ";".join(cookie_elements)
    return element_str


class RedSpiderHandler(object):

    def __init__(self, login_url, username, password):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('blink-settings=imagesEnabled=false')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('user-agent={useragent}'.format(useragent=USER_AGENT))
        self.driver = webdriver.Chrome(options=chrome_options)
        self.rhel7_base_url = RHEL7_URL
        self.rhel8_base_url = RHEL8_URL
        self.login_url = login_url
        self.username = username
        self.password = password
        self.failed_urls = list()

    @retry(reNum=5)
    def login_red_website(self):
        """登录red网站"""
        try:
            self.driver.get(self.login_url)
        except Exception as e:
            raise e
        print("login_title", self.driver.title)
        time.sleep(5)
        try:
            # 输入用户名
            self.driver.find_element_by_xpath("//div[@class='field']/input[@id='username']").send_keys(self.username)
            self.driver.find_element_by_xpath(
                '//div[@class="centered form-buttons"]/button[@class="centered button heavy-cta"]').click()
            time.sleep(2)

            # 输入密码
            self.driver.find_element_by_xpath("//div[@id='passwordWrapper']/input[@id='password']").send_keys(
                self.password)
            self.driver.find_element_by_xpath("//div[@id='kc-form-buttons']//input[@id='kc-login']").click()
            time.sleep(5)
        except ElementNotInteractableException as e:
            raise e

    @retry(reNum=5)
    def get_all_rehl_urls(self, rehl_url):
        """获取所有下载链接"""
        try:
            self.driver.get(rehl_url)
        except Exception as e:
            print(e)
        time.sleep(8)
        target_objs = self.driver.find_elements_by_xpath('//div[@class="option pull-left"][2]/select[@id="evr"]/option')
        version2urls = [{obj.get_attribute("text"): obj.get_attribute("value")} for obj in target_objs]
        return version2urls

    @retry(reNum=5)
    def get_target_page_cookie(self, rehl_url):
        """获取目标网页的cookie"""
        try:
            self.driver.get(rehl_url)
        except Exception as e:
            print(e)
        rh_jwt = self.driver.get_cookie("rh_jwt")
        session = self.driver.get_cookie("_redhat_downloads_session")
        if all([rh_jwt, session]):
            print("jwt:", rh_jwt)
            print("session", session)
            rh_jwt_value = rh_jwt["value"]
            session_value = session["value"]
            time.sleep(5)
            cookies = {
                "rh_user": "rd.sangfor|rd|P|",
                "rh_locale": "zh_CN",
                "rh_user_id": "51768269",
                "rh_sso_session": "1",
                "rh_jwt": rh_jwt_value,
                "_redhat_downloads_session": session_value
            }
            cookie_str = dict2str(cookies)
            return cookie_str
        else:
            print("{rehl_url}链接获取cookie失败,请重新获取")
            self.failed_urls.append(rehl_url)

    @retry(reNum=5)
    def save_target_data(self, cookie, target_url, filename):
        """保存数据"""
        headers = {
            "User-Agent": USER_AGENT,
            "Cookie": cookie,
        }
        session_obj = requests.Session()
        try:
            response = session_obj.get(target_url, headers=headers)
            wb_data = response.text
            html = etree.HTML(wb_data)
            need_data = html.xpath('//div[@class="changelog"]//text()')
            print("first element:{element}".format(element=need_data[0]))
            if need_data:
                with open(filename, "w", encoding="utf-8", errors="ignore") as fp:
                    for data in need_data:
                        fp.write(data)
        except Exception as e:
            print(e)

    def get_all_rehl8_data(self):
        """爬取所有rehl8的数据"""
        # 先登录
        self.login_red_website()
        # 后获取链接
        # 获取cookie
        version2urls = self.get_all_rehl_urls(self.rhel8_base_url)

        for item in version2urls:
            url_suffix = [i for i in item.values()][0]
            url = "".join([REDHAT_DOMAIN, url_suffix])
            ver_no = [i for i in item.keys()][0]
            print("===>>>开始爬取{ver_no}...".format(ver_no=ver_no))
            cookie = self.get_target_page_cookie(url)
            filename = "".join([RHEL8_STORAGE_DIR, str(TODAY), "-", ver_no, ".txt"])
            self.save_target_data(cookie, url, filename)
            print("===>>>{ver_no}更新日志已保存".format(ver_no=ver_no))
            time.sleep(5)
        self.driver.quit()

        if self.failed_urls:
            self.get_lost_data()

    def get_rehl8_latest_data(self):
        """爬取最新的rehl8"""

        # 先登录
        self.login_red_website()

        version2urls = self.get_all_rehl_urls(self.rhel8_base_url)
        url_suffix = [i for i in version2urls[0].values()][0]
        url = "".join([REDHAT_DOMAIN, url_suffix])
        ver_no = [i for i in version2urls[0].keys()][0]
        print("===>>>开始爬取{ver_no}...".format(ver_no=ver_no))
        cookie = self.get_target_page_cookie(url)
        filename = "".join([RHEL8_STORAGE_DIR, str(TODAY), "-", ver_no, ".txt"])
        self.save_target_data(cookie, url, filename)
        print("===>>>{ver_no}更新日志已保存".format(ver_no=ver_no))
        self.driver.quit()

    def get_rehl7_latest_data(self):
        """爬取最新的rehl7"""

        # 先登录
        self.login_red_website()

        version2urls = self.get_all_rehl_urls(self.rhel7_base_url)
        url_suffix = [i for i in version2urls[0].values()][0]
        url = "".join([REDHAT_DOMAIN, url_suffix])
        ver_no = [i for i in version2urls[0].keys()][0]
        print("===>>>开始爬取{ver_no}...".format(ver_no=ver_no))
        cookie = self.get_target_page_cookie(url)
        filename = "".join([RHEL7_STORAGE_DIR, str(TODAY), "-", ver_no, ".txt"])
        self.save_target_data(cookie, url, filename)
        print("===>>>{ver_no}更新日志已保存".format(ver_no=ver_no))
        self.driver.quit()

    def get_all_rehl7_data(self):
        """爬取所有rehl7的数据"""

        # 先登录
        self.login_red_website()
        version2urls = self.get_all_rehl_urls(self.rhel7_base_url)

        for item in version2urls:
            url_suffix = [i for i in item.values()][0]
            url = "".join([REDHAT_DOMAIN, url_suffix])
            ver_no = [i for i in item.keys()][0]
            print("===>>>开始爬取{ver_no}...".format(ver_no=ver_no))
            cookie = self.get_target_page_cookie(url)
            filename = "".join([RHEL7_STORAGE_DIR, str(TODAY), "-", ver_no, ".txt"])
            self.save_target_data(cookie, url, filename)
            print("===>>>{ver_no}更新日志已保存".format(ver_no=ver_no))
            time.sleep(5)
        self.driver.quit()
        print("============开始爬取失败的url==========================")
        if self.failed_urls:
            self.get_lost_data()

    def get_lost_data(self):
        """爬取丢失的数据"""
        # self.failed_urls = [
        #     "https://access.redhat.com/downloads/content/rhel---7.4/x86_64/4118/kernel/3.10.0-957.38.2.el7/src/fd431d51/package-changelog",
        #     "https://access.redhat.com/downloads/content/rhel---7.4/x86_64/4118/kernel/3.10.0-862.34.1.el7/src/fd431d51/package-changelog",
        #     "https://access.redhat.com/downloads/content/rhel---7.4/x86_64/4118/kernel/3.10.0-514.55.4.el7/src/fd431d51/package-changelog",
        #     "https://access.redhat.com/downloads/content/rhel---7.4/x86_64/4118/kernel/3.10.0-514.53.1.el7/src/fd431d51/package-changelog",
        #     "https://access.redhat.com/downloads/content/rhel---7.4/x86_64/4118/kernel/3.10.0-327.28.2.el7/src/fd431d51/package-changelog",
        # ]
        if self.failed_urls:
            self.login_red_website()
            for url in self.failed_urls:
                ver_no = url.split("/")[-4]
                print("===>>>开始爬取{ver_no}...".format(ver_no=ver_no))
                cookie = self.get_target_page_cookie(url)
                filename = "".join([RHEL7_STORAGE_DIR, str(TODAY), "-", ver_no, ".txt"])
                self.save_target_data(cookie, url, filename)
                print("===>>>{ver_no}更新日志已保存".format(ver_no=ver_no))
                time.sleep(5)
            self.driver.quit()
        else:
            pass


@time_it
def main():
    red_spider = RedSpiderHandler(LOGIN_URL, USERNAME, PASSWORD)
    red_spider.get_all_rehl7_data()
    # red_spider.get_lost_data()


if __name__ == '__main__':
    main()

# urllib3.exceptions.MaxRetryError
# urllib3.exceptions.NewConnectionError
# ConnectionRefusedError: [WinError 10061] 由于目标计算机积极拒绝，无法连接
