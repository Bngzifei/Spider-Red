# coding:utf-8
import time

import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

RHEL8_URL = "https://access.redhat.com/downloads/content/rhel---8.1/x86_64/9180/kernel/4.18.0-193.6.3.el8_2/x86_64/fd431d51/package-changelog"
RHEL7_URL = "https://access.redhat.com/downloads/content/rhel---7.4/x86_64/4118/kernel/3.10.0-1062.26.1.el7/src/fd431d51/package-changelog"
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0"
ACCOUNT = "rd.sangfor@gmail.com"
PASSWORD = "@Sangfor123"
LOGIN_URL = "https://access.redhat.com/login"



cookie = "_redhat_downloads_session=%2B9TnbKguWLKn0wIBhIM1pELpx9MgUMcupufmkY%2BL0zztsHnRsGLCxSVjJZ0lxWF36ICh40mwVNTJp0QmxMDXLbe9xfaCaNsMho%2FPKLT4XBp7TMfrCb86P91RX51POrWznqm2boLX%2FKkUSllP82nxDhZgVcgSEBNsPynZlbL0o4nRdcle7BAQDU5OfX29jx6EwcJJ8eVGyhzikbgmlhI%3D--WQ%2F8jIvt3ZE8xfT5--dH4%2BPK8RPJvnrFBviIDWZQ%3D%3D; 687975abb031448267d67b8718cb78ea=5db550249405237d15d480fbe17d7b94; AMCV_945D02BE532957400A490D4C%40AdobeOrg=1075005958%7CMCIDTS%7C18441%7CMCMID%7C43282633681557953170651032718080681416%7CMCAAMLH-1593856104%7C11%7CMCAAMB-1593856104%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1593258504s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-18448%7CvVersion%7C4.4.1%7CMCCIDH%7C-1362207722; check=true; mbox=session#eb60295b0bfa4f3c98cd30bb9fe081a1#1593253132|PC#eb60295b0bfa4f3c98cd30bb9fe081a1.38_0#1656495984; AMCVS_945D02BE532957400A490D4C%40AdobeOrg=1; rh_omni_tc=701f2000001Css0AAC; dtm_prevURL=https%3A%2F%2Fsso.redhat.com%2Fauth%2Frealms%2Fredhat-external%2Fprotocol%2Fsaml%3FSAMLRequest%3DfVJBbsIwEPxKbj4ZhzQkYCWRIlAlJFpV0PbQS2WSjbDk2KnXKbSvrxNESy8cd3dmdnbsDEWrOl727qC38NEDuqBEBOuk0UujsW%252FB7sB%252BygpetpucHJzrkDMmqgoQJxbqg3CTyrSsNketjKiRDZqskVoo%252BQ0kWHlRXwyKf3xEc00W3gCzIFSL7NymcHJgvQbrrHGmMmrUJcF6lZP3eJrWYQoxhXgONJ7NUjqfJXta1fumScNoPr9beChiD2uNTmiXkyiMQhomNEqfwwWPEz5N3kjwChZHZ9EkJMGpVRr5sCgnvdXcCJTItWgBuav4rnzYcA%252Fk4pLRNaW7zbncQYpsQPPRnS16LRsJNf3NL2PX4%252Bz8Qo9ebr16MkpWX0GplDkufVwOcuJs70O%252BN7YV7raBoSNr2oxQ3g2HowPtCCvOO%252F9%252FhOIH%26RelayState%3Dhttps%253A%252F%252Faccess.redhat.com%252Fdownloads%252Fcontent%252Frhel---7.4%252Fx86_64%252F4118%252Fkernel%252F3.10.0-693.39.1.el7%252Fsrc%252Ffd431d51%252Fpackage-changelog%26SigAlg%3Dhttp%253A%252F%252Fwww.w3.org%252F2000%252F09%252Fxmldsig%2523rsa-sha1%26Signature%3DeHhvK58EK6G949b5UqzgdA1gSia7FpgYvecjBdGm2TSI603mOeu8deSdJLGteBTPu8ZuXp7%252FXC%252BKrY63awnt902kdNlemkyJSIzM3jS3BXBT5OfVrCGduvOX05a8rhPVgimuZ%252Fv3M4g5IZ9lORvIpqRnDevs4ZKqjDXqjtrwxOdijHNE%252BWlhFKLXi83rf%252F%252BNjmA%252FAejTNrmkdjYM4Syme7VrZJwevt7wRXxR9b0aeuCfbWsHoxpQTDRmHCtg8DqMHIbE1THdSEh98pVPsZNEYFqZ4EPAdo5yGKi0niMQsaoMwV%252BPZK1m85vmj1gSyJnj1axmwYR5DQLFDeBL%252B81XwRci0jbrtBxA0dDlrqZMsvb%252FOnpYynox4ZIYcHHn08odhaR1Fa%252Bk8BAbJtr%252BDY%252BCsgGmOyHBHzYz7M0fNw8%252FCVLjuwpiYpgeuALITkzaFsM8v7ObOCjdPzN9eurv9Ebi4f%252BG5Cx4znhDe4yrBbRE%252FaiB%252FGOHv8BnO5x%252F%252BnmrD1QwWZ1KzbNoHDvvvtrVZuqtWdRHDP04SZMobZ0JXpRsfTUUCle4Jy0DGifIgw9yhI%252ByDGGoEhdTUfOJhDcxpu2oiO99i6%252BwIETfIn9gIiq3vDbUaWxe28s9EUz3j3Lb5oken%252FfUo4quS9zL6MEBYeyJLG9oxRY%252FtjAWAeelnEPhoDo%253D; sat_prevInternalCampaign=; sat_prevExtCmp=no%20value; sat_prevUrl=https%3A%2F%2Fsso.redhat.com%2Fauth%2Frealms%2Fredhat-external%2Fprotocol%2Fsaml%3FSAMLRequest%3DfVJBbsIwEPxKbj4ZhzQkYCWRIlAlJFpV0PbQS2WSjbDk2KnXKbSvrxNESy8cd3dmdnbsDEWrOl727qC38NEDuqBEBOuk0UujsW%252FB7sB%252BygpetpucHJzrkDMmqgoQJxbqg3CTyrSsNketjKiRDZqskVoo%252BQ0kWHlRXwyKf3xEc00W3gCzIFSL7NymcHJgvQbrrHGmMmrUJcF6lZP3eJrWYQoxhXgONJ7NUjqfJXta1fumScNoPr9beChiD2uNTmiXkyiMQhomNEqfwwWPEz5N3kjwChZHZ9EkJMGpVRr5sCgnvdXcCJTItWgBuav4rnzYcA%252Fk4pLRNaW7zbncQYpsQPPRnS16LRsJNf3NL2PX4%252Bz8Qo9ebr16MkpWX0GplDkufVwOcuJs70O%252BN7YV7raBoSNr2oxQ3g2HowPtCCvOO%252F9%252FhOIH%26RelayState%3Dhttps%253A%252F%252Faccess.redhat.com%252Fdownloads%252Fcontent%252Frhel---7.4%252Fx86_64%252F4118%252Fkernel%252F3.10.0-693.39.1.el7%252Fsrc%252Ffd431d51%252Fpackage-changelog%26SigAlg%3Dhttp%253A%252F%252Fwww.w3.org%252F2000%252F09%252Fxmldsig%2523rsa-sha1%26Signature%3DeHhvK58EK6G949b5UqzgdA1gSia7FpgYvecjBdGm2TSI603mOeu8deSdJLGteBTPu8ZuXp7%252FXC%252BKrY63awnt902kdNlemkyJSIzM3jS3BXBT5OfVrCGduvOX05a8rhPVgimuZ%252Fv3M4g5IZ9lORvIpqRnDevs4ZKqjDXqjtrwxOdijHNE%252BWlhFKLXi83rf%252F%252BNjmA%252FAejTNrmkdjYM4Syme7VrZJwevt7wRXxR9b0aeuCfbWsHoxpQTDRmHCtg8DqMHIbE1THdSEh98pVPsZNEYFqZ4EPAdo5yGKi0niMQsaoMwV%252BPZK1m85vmj1gSyJnj1axmwYR5DQLFDeBL%252B81XwRci0jbrtBxA0dDlrqZMsvb%252FOnpYynox4ZIYcHHn08odhaR1Fa%252Bk8BAbJtr%252BDY%252BCsgGmOyHBHzYz7M0fNw8%252FCVLjuwpiYpgeuALITkzaFsM8v7ObOCjdPzN9eurv9Ebi4f%252BG5Cx4znhDe4yrBbRE%252FaiB%252FGOHv8BnO5x%252F%252BnmrD1QwWZ1KzbNoHDvvvtrVZuqtWdRHDP04SZMobZ0JXpRsfTUUCle4Jy0DGifIgw9yhI%252ByDGGoEhdTUfOJhDcxpu2oiO99i6%252BwIETfIn9gIiq3vDbUaWxe28s9EUz3j3Lb5oken%252FfUo4quS9zL6MEBYeyJLG9oxRY%252FtjAWAeelnEPhoDo%253D; sat_prevPage=SSO%7Cauth%7Crealms%7Credhat-external%7Cprotocol%7Csaml; scCidHist=701f2000001Css0AAC; s_cc=true; sat_ppv=89; s_sq=%5B%5BB%5D%5D; rh_user=rd.sangfor|rd|P|; rh_locale=zh_CN; rh_user_id=51768269; rh_sso_session=1; BIGipServer~prod~kcs-webapp-http=276497674.20480.0000; BIGipServer~prod~staticweb-webapp-http=795084042.20480.0000; rh_jwt=eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICItNGVsY19WZE5fV3NPVVlmMkc0UXhyOEdjd0l4X0t0WFVDaXRhdExLbEx3In0.eyJqdGkiOiJmODhkNDg3Ny1jYTI0LTQzYzAtYjIxNi00Y2U2OTFhZTRiNDIiLCJleHAiOjE1OTMyNTIxNTIsIm5iZiI6MCwiaWF0IjoxNTkzMjUxMjUyLCJpc3MiOiJodHRwczovL3Nzby5yZWRoYXQuY29tL2F1dGgvcmVhbG1zL3JlZGhhdC1leHRlcm5hbCIsImF1ZCI6ImN1c3RvbWVyLXBvcnRhbCIsInN1YiI6ImY6NTI4ZDc2ZmYtZjcwOC00M2VkLThjZDUtZmUxNmY0ZmUwY2U2OnJkLnNhbmdmb3IiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJjdXN0b21lci1wb3J0YWwiLCJub25jZSI6ImMwZGJkNjIxLTI3ZWQtNDkzOC05OGI5LWQwZjczNTNmNWU5MiIsImF1dGhfdGltZSI6MTU5MzI1MTIxNywic2Vzc2lvbl9zdGF0ZSI6ImM1NjUzNjI2LTY2ZmYtNDY3My05MjQ3LWY4NWM3MTI1NjJlZCIsImFjciI6IjAiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly9wcm9kLmZvby5yZWRoYXQuY29tOjEzMzciLCJodHRwczovL3d3dy5yZWRoYXQuY29tIiwiaHR0cHM6Ly9hY2Nlc3MucmVkaGF0LmNvbSJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiYXV0aGVudGljYXRlZCIsImNhbmRsZXBpbl9zeXN0ZW1fYWNjZXNzX3ZpZXdfZWRpdF9wZXJzb25hbCIsImlkcF9hdXRoZW50aWNhdGVkIiwicG9ydGFsX21hbmFnZV9zdWJzY3JpcHRpb25zIiwiZXJyYXRhOm5vdGlmaWNhdGlvbl9zdGF0dXNfZW5hYmxlZCIsImVycmF0YTpub3RpZmljYXRpb25fZGVsaXZlcnlfd2Vla2x5IiwicG9ydGFsX21hbmFnZV9jYXNlcyIsImVycmF0YTpub3RpZmljYXRpb246c2VjdXJpdHkiLCJlcnJhdGE6bm90aWZpY2F0aW9uX2xldmVsX3N5c3RlbS12aXNpYmxlIiwiZXJyYXRhOm5vdGlmaWNhdGlvbjpidWdmaXgiLCJhZG1pbjpvcmc6YWxsIiwidW1hX2F1dGhvcml6YXRpb24iLCJwb3J0YWxfc3lzdGVtX21hbmFnZW1lbnQiLCJyaGRfYWNjZXNzX21pZGRsZXdhcmUiLCJwb3J0YWxfZG93bmxvYWQiXX0sInJlc291cmNlX2FjY2VzcyI6eyJyaGQtZG0iOnsicm9sZXMiOlsicmh1c2VyIl19LCJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJSRURIQVRfTE9HSU4iOiJyZC5zYW5nZm9yIiwibGFzdE5hbWUiOiJzYW5nZm9yIiwiY291bnRyeSI6IkNOIiwiYWNjb3VudF9udW1iZXIiOiI2MDgwMjc3IiwicHJlZmVycmVkX3VzZXJuYW1lIjoicmQuc2FuZ2ZvciIsImZpcnN0TmFtZSI6InJkIiwiYWNjb3VudF9pZCI6IjExNzI4MTc4IiwidXNlcl9pZCI6IjUxNzY4MjY5Iiwib3JnYW5pemF0aW9uX2lkIjoiMDBEbTAwMDAwMDAxMTZDIiwic2l0ZUlkIjoicmVkaGF0Iiwic2l0ZUlEIjoicmVkaGF0IiwicG9ydGFsX2lkIjoiMDYwNjAwMDAwMDBEMGFmIiwibGFuZyI6InpoX0NOIiwicmVnaW9uIjoiQ04iLCJlbWFpbCI6InJkLnNhbmdmb3JAZ21haWwuY29tIiwiUkhBVF9MT0dJTiI6InJkLnNhbmdmb3IiLCJ1c2VybmFtZSI6InJkLnNhbmdmb3IifQ.SAd0MkCBhn3QRq12oijQqHSc2t5YyEKvdmdg4Kq14aMpTePVmLdaO6zArPCTfxb1yO_8DSNg0tXuCc2anoZirS1EO4tHkvVpqxGLNPq_neLBD1qb5pYWeIaSn0EWbtXVu0SQvQ6QYQZ4_U07KdmMhm1Oit4YtqAj7RVhd0lfRvZ5okRw9a_Ah0Sy0uYRR0b2JlHE_gpBzcSD2o5GMSCgXd0Cmt4Fifu3SX6GYUpoSPbbtYkTirx0ZX28LT0xKYxViQKcX7MoS-Ob7dRVzDPv6kL7Y-BmR5CTA_iSvzt6B-MrsZdbe4agKb-qKPqXeFYbtHb4rp7zDU19nQVGjQDA4g6zkEgaXuxGJtgVxLgxV3XvG5wFzn_deLXp-KAZf2QxgFUpqgHQNAirvXUpi0gWF9l64IXUghq5nqwKUuAebJFL8ZmT_K0QVdG7_DkshoKFIESD_M1dCcKtbyQh92_GdDy0-sdQ7jRHJCC8YoaFa-OwWtmF3Pl6i9vz0ciuZsteOrP3OhZ4-JTJDgNGjhwIZ1-5lS7YbN51oFj4B5DKaT3Q7003QzJQx1POHUkGUxKiBuQDaiNpH59o09v2W-TEx4KtHsPWrI2HoXFtnVXjteS9qyUj8vSXeCtPahku8L4OI341XMOpBqyoREX5M_GkM5KC3yDUR0YbOVihve1dIg8; chrome_session_id=824183|1593251264298; SESSe82ddad2d63e5504fdf78cf492d69542=4pTvqK6bVWjvUOHh95Wjl8UMrH28VS10cuCwUPkmMDw; redhat_www_eu_cookie=true; dtm_cpReg=yes"
cookie1 = "rh_user=rd.sangfor|rd|P|;rh_locale=zh_CN;rh_user_id=51768269;rh_sso_session=1;rh_jwt=eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICItNGVsY19WZE5fV3NPVVlmMkc0UXhyOEdjd0l4X0t0WFVDaXRhdExLbEx3In0.eyJqdGkiOiIwYjJmNGQxOC00ODViLTRmYmYtYjFlYS04ZDMzZGM3ZjVlZGUiLCJleHAiOjE1OTMzMzg0MzUsIm5iZiI6MCwiaWF0IjoxNTkzMzM3NTM1LCJpc3MiOiJodHRwczovL3Nzby5yZWRoYXQuY29tL2F1dGgvcmVhbG1zL3JlZGhhdC1leHRlcm5hbCIsImF1ZCI6ImN1c3RvbWVyLXBvcnRhbCIsInN1YiI6ImY6NTI4ZDc2ZmYtZjcwOC00M2VkLThjZDUtZmUxNmY0ZmUwY2U2OnJkLnNhbmdmb3IiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJjdXN0b21lci1wb3J0YWwiLCJub25jZSI6Ijc3NzExMmJhLTY3ZmUtNDNiZS05NzRjLTg5MTZlODBmOTE1YiIsImF1dGhfdGltZSI6MTU5MzMzNzE4OSwic2Vzc2lvbl9zdGF0ZSI6IjZkM2UwZTQ1LTFmODYtNDk0MC04ZmQ2LTRlNGZlMGY1M2JhOCIsImFjciI6IjAiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly9wcm9kLmZvby5yZWRoYXQuY29tOjEzMzciLCJodHRwczovL3d3dy5yZWRoYXQuY29tIiwiaHR0cHM6Ly9hY2Nlc3MucmVkaGF0LmNvbSJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiYXV0aGVudGljYXRlZCIsImNhbmRsZXBpbl9zeXN0ZW1fYWNjZXNzX3ZpZXdfZWRpdF9wZXJzb25hbCIsImlkcF9hdXRoZW50aWNhdGVkIiwicG9ydGFsX21hbmFnZV9zdWJzY3JpcHRpb25zIiwiZXJyYXRhOm5vdGlmaWNhdGlvbl9zdGF0dXNfZW5hYmxlZCIsImVycmF0YTpub3RpZmljYXRpb25fZGVsaXZlcnlfd2Vla2x5IiwicG9ydGFsX21hbmFnZV9jYXNlcyIsImVycmF0YTpub3RpZmljYXRpb246c2VjdXJpdHkiLCJlcnJhdGE6bm90aWZpY2F0aW9uX2xldmVsX3N5c3RlbS12aXNpYmxlIiwiZXJyYXRhOm5vdGlmaWNhdGlvbjpidWdmaXgiLCJhZG1pbjpvcmc6YWxsIiwidW1hX2F1dGhvcml6YXRpb24iLCJwb3J0YWxfc3lzdGVtX21hbmFnZW1lbnQiLCJyaGRfYWNjZXNzX21pZGRsZXdhcmUiLCJwb3J0YWxfZG93bmxvYWQiXX0sInJlc291cmNlX2FjY2VzcyI6eyJyaGQtZG0iOnsicm9sZXMiOlsicmh1c2VyIl19LCJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJSRURIQVRfTE9HSU4iOiJyZC5zYW5nZm9yIiwibGFzdE5hbWUiOiJzYW5nZm9yIiwiY291bnRyeSI6IkNOIiwiYWNjb3VudF9udW1iZXIiOiI2MDgwMjc3IiwicHJlZmVycmVkX3VzZXJuYW1lIjoicmQuc2FuZ2ZvciIsImZpcnN0TmFtZSI6InJkIiwiYWNjb3VudF9pZCI6IjExNzI4MTc4IiwidXNlcl9pZCI6IjUxNzY4MjY5Iiwib3JnYW5pemF0aW9uX2lkIjoiMDBEbTAwMDAwMDAxMTZDIiwic2l0ZUlkIjoicmVkaGF0Iiwic2l0ZUlEIjoicmVkaGF0IiwicG9ydGFsX2lkIjoiMDYwNjAwMDAwMDBEMGFmIiwibGFuZyI6InpoX0NOIiwicmVnaW9uIjoiQ04iLCJlbWFpbCI6InJkLnNhbmdmb3JAZ21haWwuY29tIiwiUkhBVF9MT0dJTiI6InJkLnNhbmdmb3IiLCJ1c2VybmFtZSI6InJkLnNhbmdmb3IifQ.CpUNAy8RrPemybbp0oagAg1APRD7FEvYId3JFHdIiB0kzMvfqBTQM4cdiimj7Gr1nuwN5z6uIol2Ehf0grdJK4CCU0LoA3Maa7W9Yu_V199dXm7sBvVmy0YItGqtk4flW0dgO0Pjne0TgN62DBpBuTpnhzAtKP9ytTbKTVkTsmMafMcADQVfJIK8AMDm5fNyOeJPWnlluZ_TcwmJtGhSwbuKPQF00O86zc75LroC1SFUsCJv-q1TjAnx0oYLYLO2aSt0AQmD7b4IuDKi-3C0k51hAN3I8mRBM_F4Lj7VjW2eWGYKdEkbVENNGLrapW6yn60Ir4nmDNkSR93NtYtCBdzGAzKDHgtZWxcdmWAKK2AQ932DNBUcTbwB2IdRD9AcIxWzrJUJUA9w4VDT2RbZ14q_Z3jdcRNu4_vu2S5nD6oEHAfv7E0G6HMIIJsG1Y9MgKf__7sACSOWsu9Y4hIvo38Oi9vJWZsA1lho7sTuPNbz39lFJHBLeY8RHUMZ7sMLbSp9GFT7jLp2Jg8I3WE7tXCp53wBKPQRrKRbjmxALPotbKuXO1vyuoRmCoxmyfJj3Bxnu4Ph2bEIfpESI1u-THHXOnzzwfYMkqKx_abVRyoQ_wSDjc0pH6fRa3cCpKJA6pL4focxiY_YCDMFHuAacNXWVDgo_ycR13INw7PnwKs;_redhat_downloads_session=JjxeTyhOZ1lAeLqmXTN23HGX7IZVAVgHPClGpemA0Hlr%2FhbHKzwsAlz17LmMl9aROkCFEdMLteIxy36CkT7EVMr4tV6sNmxbBnTwhhQq1SDnUZHyl51zOkmGEHbdPdsOj78ZgYtp8ZtMPEu3ipxr1%2FN3%2BcwpP6QakNGEt8%2FZwNoLXNe2KMYFVsP%2FNHeKb9bN8lPx0T%2FQ44mX2S%2BlL0U%3D--jhs2MpDQsjKSzJFA--0PaAJD464sUlgZITyaxTBQ%3D%3D;"
headers = {
    "User-Agent": USER_AGENT,
    "Cookie": cookie1,
}

LOGIN_AUTH_URL = "https://sso.redhat.com/auth/realms/redhat-external/login-actions/authenticate?code=X0DzXNyqnXu-kL5ZluyrJF0v3zia8an9GJAdcss_JxQ&execution=42ab36f8-26fd-4425-9aba-7792a9f08f59&client_id=customer-portal&tab_id=7zcHPatNctI"

data = {
    "username": ACCOUNT,
    "password": PASSWORD
}
# response = session_obj.post(LOGIN_AUTH_URL, data=data)
# print(response.text)

headers1 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'Connection': 'keep-alive'
}
# //使用copy()防止修改原代码定义dict
cap = DesiredCapabilities.PHANTOMJS.copy()
for key, value in headers1.items():
    cap['phantomjs.page.customHeaders.{}'.format(key)] = value
# browser = webdriver.PhantomJS(desired_capabilities=cap)

# driver = webdriver.PhantomJS(executable_path=r"C:\Python3\phantomjs-2.1.1-windows\bin\phantomjs.exe",desired_capabilities=cap)
driver = webdriver.PhantomJS(executable_path=r"C:\Python3\phantomjs-2.1.1-windows\bin\phantomjs.exe",
                             desired_capabilities=cap)
driver.set_window_size(1366, 768)
# driver = webdriver.PhantomJS()
# driver.set_page_load_timeout(5)
# chrome_options = Options()
# 无头模式启动
# chrome_options.add_argument('--headless')
# 谷歌文档提到需要加上这个属性来规避bug
# chrome_options.add_argument('--disable-gpu')
# driver = webdriver.Chrome(options=chrome_options)
# time.sleep(5)
url = "https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/auth?client_id=customer-portal&redirect_uri=https%3A%2F%2Faccess.redhat.com%2Fwebassets%2Favalon%2Fj%2Fincludes%2Fsession%2Fscribe%2F%3FredirectTo%3Dhttps%253A%252F%252Faccess.redhat.com&state=ee983228-b950-4e69-82f8-1d201d73b885&nonce=38f73164-a3bb-49bb-8b7b-9f7d64103b61&response_mode=fragment&response_type=code&scope=openid"
# url = "https://access.redhat.com/login"
driver.get(url)
print(driver.title)
# 睡眠2秒
time.sleep(2)

# 输入用户名
user = driver.find_element_by_xpath("//div[@class='field']/input[@id='username']")
user.send_keys(ACCOUNT)
# 找到下一步按钮点击进去
driver.find_element_by_xpath('//div[@class="centered form-buttons"]/button[@class="centered button heavy-cta"]').click()
time.sleep(2)

# 输入密码
driver.find_element_by_xpath("//div[@id='passwordWrapper']/input[@id='password']").send_keys(PASSWORD)
# pwd.send_keys(PASSWORD)
# 点击登录按钮实现登录
driver.find_element_by_xpath("//div[@id='kc-form-buttons']//input[@id='kc-login']").click()
# 登录成功后跳转首页，进行加载，休眠10秒加载页面
time.sleep(10)
# 点击进入发帖页面
# driver.switch_to_default_content()
cookies_list = driver.get_cookies()
print(cookies_list)
print()

driver.get(RHEL8_URL)
time.sleep(8)
# WebDriverWait(driver, 10, poll_frequency=5).until(lambda x:x.find_element_by_xpath('//div[@class="chosen-container chosen-container-single"]/a[@class="chosen-single"]'))
rh_jwt = driver.get_cookie("rh_jwt")
rh_jwt_value = rh_jwt["value"]
print(rh_jwt_value)
_redhat_downloads_session = driver.get_cookie("_redhat_downloads_session")
_redhat_downloads_session_value = _redhat_downloads_session["value"]
cookie2 = "rh_user=rd.sangfor|rd|P|;rh_locale=zh_CN;rh_user_id=51768269;rh_sso_session=1;" + "rh_jwt="+rh_jwt_value +";redhat_downloads_session"+_redhat_downloads_session_value
headers2 = {
    "User-Agent": USER_AGENT,
    "Cookie": cookie2,
}
# print(rh_jwt)
# print(_redhat_downloads_session)
# source_codes = driver.page_source
# print("===>>>",source_codes)
session_obj = requests.Session()
response = session_obj.get(RHEL8_URL, headers=headers2)
wb_data = response.text
print(wb_data)
html = etree.HTML(wb_data)
need_data = html.xpath('//div[@class="changelog"]//text()')

if need_data:
    with open("red16.txt", "w", encoding="utf-8", errors="ignore") as fp:
        for data in need_data:
            fp.write(data)

# html = etree.HTML(source_codes)
# time.sleep(3)
# need_data = html.xpath('//div[@class="changelog"]//text()')
# print("===>>>not match data", need_data)
# # # time.sleep(2)
# # # res_objs = driver.find_element_by_xpath('//div[@class="changelog"]//text()')
# #
# # # if response.status_code == 200:
# with open("red19.txt", "w", encoding="utf-8", errors="ignore") as fp:
#     for data in need_data:
#         fp.write(data)

driver.quit()
