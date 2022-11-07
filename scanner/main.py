import os

import init
import OneForAll
import Shuize
import fire
import ksubdomain
from loguru import logger
import threading
import utils
import AltDNS

class Scanner:
    def __init__(self, target=None, file=None):
        self.target = target
        self.file = file
        self.is_wildcard = None
        self.subdomains = list()

    def runb(self):
        with open(self.file, 'r') as f:
            for line in f:
                self.target = line.strip()
                self.run()

    def run(self):
        self.prepare()
        self.run_step1()
        self.run_step2()
        self.run_step3()
        self.run_step4()
        OneForAll.export.export_data(self.target, alive=False, fmt="csv", path=os.getcwd() + "/results/")

    def prepare(self):
        OneForAll.utils.init_table(self.target)
        Shuize.ShuiZe.set_domain(self.target)
        self.is_wildcard = OneForAll.wildcard.to_detect_wildcard(self.target)
        logger.log('ALERT', f'{self.target} {"存在泛解析将不会爆破子域名" if self.is_wildcard else "不存在泛解析"}')

    def run_step1(self):
        """
        调用OneForAll核心部分收集子域名
        """
        threads = [
            threading.Thread(target=OneForAll.Collect(self.target).run),
            # 核心 'certificates', 'check', 'datasets','dnsquery', 'intelligence', 'search'
            threading.Thread(target=OneForAll.BruteSRV(self.target).run),
            # 枚举常见的子域
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        OneForAll.utils.deal_data(self.target)

    def run_step2(self):
        """
        调用ksubdomain爆破子域名
        """
        result = list()
        if not self.is_wildcard:
            data = ksubdomain.run_ksubdomain(self.target)
            for subdomain in data:
                result.append(utils.gen_result(subdomain=subdomain, module='ksubdomain', source='ksubdomain'))
        utils.add_to_db(self.target, result, 'ksubdomain')

    def run_step3(self):
        """
        调用Shuize的子域名爬虫
        """
        result = list()
        bdSubdomains, _ = Shuize.Plugins.infoGather.subdomain.Spider.Baidu.baidu.BaiduSpider().run_subdomain(
            self.target)
        bingSubdomains, _ = Shuize.Plugins.infoGather.subdomain.Spider.Bing.bing.BingSpider().run_subdomain(self.target)
        for subdomain in list(set(bdSubdomains + bingSubdomains)):
            result.append(utils.gen_result(subdomain=subdomain, module='shuize', source='spider'))
        utils.add_to_db(self.target, result, 'spider')

    def run_step4(self):
        data = OneForAll.utils.get_data(self.target)
        OneForAll.utils.clear_data(self.target)
        data = OneForAll.resolve.run_resolve(self.target, data)
        OneForAll.resolve.save_db(self.target, data)
        if self.is_wildcard:
            data = OneForAll.wildcard.deal_wildcard(data)
        AltDNS.Altdns(self.target).run(data)
        OneForAll.utils.deal_data(self.target)
        OneForAll.Enrich(self.target).run()

if __name__ == '__main__':
    fire.Fire(Scanner)
