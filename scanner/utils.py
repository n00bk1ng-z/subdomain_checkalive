from OneForAll.common.module import lock
from OneForAll.common.database import Database
import OneForAll

__result = {'id': None, 'alive': None, 'request': None, 'resolve': None, 'url': None, 'subdomain': None, 'port': None,
            'level': None, 'cname': None, 'ip': None, 'public': None, 'cdn': None, 'status': None, 'reason': None,
            'title': None, 'banner': None, 'header': None, 'history': None, 'response': None, 'ip_times': None,
            'cname_times': None, 'ttl': None, 'cidr': None, 'asn': None, 'org': None, 'addr': None, 'isp': None,
            'resolver': None, 'module': None, 'source': None, 'elapse': None, 'find': None}


def gen_result(**kwargs):
    result = __result.copy()
    for key, value in kwargs.items():
        if key == "subdomain":
            result["level"] = len(value.split(".")) - 1
        result[key] = value
    return result


def add_to_db(domain, results, source):
    lock.acquire()
    db = Database()
    db.create_table(domain)
    db.save_db(domain, results, source)
    db.close()
    lock.release()
    OneForAll.utils.deal_data(domain)

def save_json(domain, results, source):
    path = OneForAll.settings.result_save_dir.joinpath(domain, self.module)
    path.mkdir(parents=True, exist_ok=True)
    name = self.source + '.json'
    path = path.joinpath(name)
    with open(path, mode='w', errors='ignore') as file:
        result = {'domain': self.domain,
                  'name': self.module,
                  'source': self.source,
                  'elapse': self.elapse,
                  'find': len(self.subdomains),
                  'subdomains': list(self.subdomains),
                  'infos': self.infos}
        json.dump(result, file, ensure_ascii=False, indent=4)
    return True
