# coding:utf-8
import os
from datetime import datetime

REDHAT_DOMAIN = "https://access.redhat.com"
BASE_URL = "downloads/content/rhel---8.1/x86_64/9180/kernel/4.18.0-80.el8/x86_64/fd431d51/package-changelog"
BASE_PREFIX = os.path.join(REDHAT_DOMAIN, BASE_URL)

RHEL8_URL = "https://access.redhat.com/downloads/content/rhel---8.1/x86_64/9180/kernel/4.18.0-80.el8/x86_64/fd431d51/package-changelog"
RHEL7_URL = "https://access.redhat.com/downloads/content/rhel---7.4/x86_64/4118/kernel/3.10.0-123.el7/src/fd431d51/package-changelog"
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0"
USERNAME = "rd.sangfor@gmail.com"
PASSWORD = "@Sangfor123"
LOGIN_URL = "https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/auth?client_id=customer-portal&redirect_uri=https%3A%2F%2Faccess.redhat.com%2Fwebassets%2Favalon%2Fj%2Fincludes%2Fsession%2Fscribe%2F%3FredirectTo%3Dhttps%253A%252F%252Faccess.redhat.com&state=ee983228-b950-4e69-82f8-1d201d73b885&nonce=38f73164-a3bb-49bb-8b7b-9f7d64103b61&response_mode=fragment&response_type=code&scope=openid"

TODAY = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
RHEL7_STORAGE_DIR = r"D:\git_pro\Spiders\Spider-Red\changelog\rhel7\changelog-"
RHEL8_STORAGE_DIR = r"D:\git_pro\Spiders\Spider-Red\changelog\rhel8\changelog-"
