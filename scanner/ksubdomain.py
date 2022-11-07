import os
from loguru import logger


def run_ksubdomain(target):
    logger.info("ksubdomain start!")
    ksubdomain_file = f'{target}_ksubdomain.txt'
    ksubdomains = list()
    os.system('sudo -S ksubdomain e -d {} -o {} >/dev/null'.format(target, ksubdomain_file))
    try:
        with open(ksubdomain_file, 'rt') as f:
            for each_line in f.readlines():
                each_line_split = each_line.split('=>')
                subdomain = each_line_split[0].strip()  # 子域名
                ksubdomains.append(subdomain)

        os.remove(ksubdomain_file)  # 删除临时文件
        logger.info("ksubdomain done!")
    except Exception:
        logger.error('ksubdomain run error')
    return ksubdomains
