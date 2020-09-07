# coding:utf-8
import time
import requests
from lxml import etree
from selenium import webdriver

RHEL8_URL = "https://access.redhat.com/downloads/content/rhel---8.1/x86_64/9180/kernel/4.18.0-193.6.3.el8_2/x86_64/fd431d51/package-changelog"
RHEL7_URL = "https://access.redhat.com/downloads/content/rhel---7.4/x86_64/4118/kernel/3.10.0-1062.26.1.el7/src/fd431d51/package-changelog"
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0"
USERNAME = "rd.sangfor@gmail.com"
PASSWORD = "@Sangfor123"
LOGIN_URL = "https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/auth?client_id=customer-portal&redirect_uri=https%3A%2F%2Faccess.redhat.com%2Fwebassets%2Favalon%2Fj%2Fincludes%2Fsession%2Fscribe%2F%3FredirectTo%3Dhttps%253A%252F%252Faccess.redhat.com&state=ee983228-b950-4e69-82f8-1d201d73b885&nonce=38f73164-a3bb-49bb-8b7b-9f7d64103b61&response_mode=fragment&response_type=code&scope=openid"

from requests.exceptions import ConnectionError


def retry(**kw):
    def wrapper(func):
        def _wrapper(*args, **kwargs):
            raise_ex = None
            for num in range(kw['reNum']):
                print(num)
                try:
                    return func(*args, **kwargs)
                except ConnectionError as ex:
                    raise_ex = ex

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

@retry(reNum=5)
def get_rehl_cookie(login_url, username, password):
    """获取red_hat网站登陆后的cookie"""
    driver = webdriver.Chrome()
    try:
        driver.get(login_url)
    except Exception as e:
        print(e)
    print("login_title", driver.title)
    time.sleep(5)

    # 输入用户名
    driver.find_element_by_xpath("//div[@class='field']/input[@id='username']").send_keys(username)
    driver.find_element_by_xpath(
        '//div[@class="centered form-buttons"]/button[@class="centered button heavy-cta"]').click()
    time.sleep(2)

    # 输入密码
    driver.find_element_by_xpath("//div[@id='passwordWrapper']/input[@id='password']").send_keys(password)
    driver.find_element_by_xpath("//div[@id='kc-form-buttons']//input[@id='kc-login']").click()
    time.sleep(5)

    # 目标地址
    try:
        driver.get(RHEL8_URL)
    except Exception as e:
        print(e)
    time.sleep(8)
    rh_jwt = driver.get_cookie("rh_jwt")
    session = driver.get_cookie("_redhat_downloads_session")
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
    element_str = dict2str(cookies)
    return element_str

@retry(reNum=5)
def red_spider(cookie, target_url):
    """爬取rehl目标网站的数据"""
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
        print(need_data)
        if need_data:
            with open("red129.txt", "w", encoding="utf-8", errors="ignore") as fp:
                for data in need_data:
                    fp.write(data)
    except Exception as e:
        print(e)


def main():
    cookie = get_rehl_cookie(LOGIN_URL, USERNAME, PASSWORD)
    red_spider(cookie, RHEL8_URL)


if __name__ == '__main__':
    main()
