import base64
import json
import os
import pickle
import shutil
import sqlite3
import tarfile
import uuid
from subprocess import CalledProcessError
from urllib.parse import urlparse, parse_qsl, ParseResult

import urllib3
from PyQt5.QtCore import QProcess, QSettings

# http = urllib3.PoolManager()
import db_params

http = urllib3.ProxyManager('https://localhost:12333')


def b64decode(b64, encoding='utf-8'):
    if isinstance(b64, bytes):
        as_bytes = b64
    else:
        as_bytes = bytes(b64, encoding)

    padded = as_bytes + (b'=' * (-len(as_bytes) % 4))
    return base64.urlsafe_b64decode(padded).decode(encoding)


def read_ssr_urls(subscription_url: str):
    resp: urllib3.HTTPResponse = http.request('GET', subscription_url)
    urls = b64decode(resp.data).split('\n')
    return urls


def decode_ssr_url(ssr_url: str):
    idx = ssr_url.find("//") + 2
    decoded = ssr_url[:idx] + b64decode(ssr_url[idx:])
    parsed: ParseResult = urlparse(decoded)
    keys = ["server", "server_port", "protocol", "method", "obfs", "password"]
    res = dict(zip(keys, parsed.netloc.split(':')))
    params = parse_qsl(parsed.query)
    for (k, v) in params:
        res[k] = b64decode(v)
    res['password'] = b64decode(res['password'])
    return res


def read_test_configs():
    with open('test_configs.pkl', 'rb') as f:
        res = pickle.load(f)

    return res


def read_ssr_config(subscription_url: str):
    urls = read_ssr_urls(subscription_url)
    return list(map(decode_ssr_url, urls))


def make_config_old(config: dict, path=None, local_addr="127.0.0.1", local_port=1080, **kwargs):
    config_dict = {"protocol_param": config.get('protocolparam', ''), "method": config['method'],
                   "protocol": config['protocol'],
                   "server": config['server'], "password": config['password'], "local_address": local_addr,
                   "server_port": config['server_port'], "local_port": local_port,
                   "obfs_param": config.get('obfsparam', ''),
                   "obfs": config['obfs']}

    config_dict.update(kwargs)

    if not path:
        return json.dumps(config_dict)
    else:
        with open(path, 'w') as fp:
            json.dump(config_dict, fp)
        return None


def make_config_file(config: dict, path=None, local_addr="127.0.0.1", local_port=1080, use_udp=False, timeout=2000):
    config_dict = {
        "password": config['password'],
        "method": config['method'],
        "protocol": config['protocol'],
        "protocol_param": config.get('protocolparam', ''),
        "obfs": config['obfs'],
        "obfs_param": config.get('obfsparam', ''),

        "udp": use_udp,
        "timeout": timeout,

        "client_settings": {
            "server": config['server'],
            "server_port": config['server_port'],
            "listen_address": local_addr,
            "listen_port": local_port
        }
    }

    if not path:
        return json.dumps(config_dict)
    else:
        with open(path, 'w') as fp:
            json.dump(config_dict, fp)
        return None


def make_config_files(configs: [dict], path, old_format=False, *args, **kwargs, ):
    for config in configs:
        group_path = os.path.join(path, config.get('group', ''))
        if not os.path.isdir(group_path):
            os.mkdir(group_path)
        file_path = os.path.join(group_path, config.get('remarks', str(uuid.uuid4())) + '.json')
        assert not os.path.exists(file_path)
        f = make_config_old if old_format else make_config_file
        f(config, file_path, *args, **kwargs)


def init_ssr_at(path, signals):
    root = os.path.join(path, 'qt-ssr')
    # remove existing folder
    if os.path.isdir(root):
        signals.stdout.emit('Removing existing directory %s ... \n' % root)
        shutil.rmtree(root)

    # make directory $path/qt-ssr
    signals.stdout.emit('Making directory %s ...\n' % root)
    os.mkdir(root)

    # TODO: acquire version automatically
    version = '2.5.3'
    dir_name = 'shadowsocksr-libev-%s' % version
    url = "https://github.com/shadowsocksrr/shadowsocksr-libev/archive/2.5.3.tar.gz"
    ssr_dir = os.path.join(root, dir_name)

    signals.stdout.emit('Downloading and extracting from %s ...\n' % url)
    with http.request('GET', url, preload_content=False) as resp:
        with tarfile.open(mode='r:gz', fileobj=resp) as zip_fp:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(zip_fp, root, numeric_owner="True")

    bin_dir = os.path.join(ssr_dir, 'src')
    bin_path = os.path.join(bin_dir, 'ss-local')

    # remove -Werrors
    # TODO: remove shell dependencies
    os.chdir(bin_dir)
    p = QProcess()

    def read_stderr():
        qb_arr = p.readAllStandardError()
        signals.stderr.emit(str(qb_arr.data(), 'utf-8'))

    def read_stdout():
        qb_arr = p.readAllStandardOutput()
        signals.stdout.emit(str(qb_arr.data(), 'utf-8'))

    p.readyReadStandardError.connect(read_stderr)
    p.readyReadStandardOutput.connect(read_stdout)

    signals.stdout.emit('Removing -Werror from makefiles ...\n')

    p.start('/usr/bin/bash', ['-c', r"/usr/bin/sed -i 's/-Werror//g' Makefile*"])
    p.waitForFinished()
    if p.exitStatus() != QProcess.NormalExit:
        raise CalledProcessError(p.exitCode(), p.program())

    signals.stdout.emit('Configuring and Making Binaries ... \n')

    os.chdir(ssr_dir)
    p.start('/usr/bin/bash', ['-c', r"./configure && make -j$(nproc)"])
    p.waitForFinished()

    if p.exitStatus() != QProcess.NormalExit:
        raise CalledProcessError(p.exitCode(), p.program())

    os.mkdir(os.path.join(root, 'server-configs'))
    db_path = os.path.join(root, 'server-configs', 'servers.db')

    signals.stdout.emit('Configuring database...')
    setting = QSettings()
    setting.sync()
    setting.beginGroup('SSR')
    setting.setValue('root_dir', root)
    setting.setValue('bin_path', bin_path)
    setting.setValue('db_path', db_path)
    setting.endGroup()
    setting.sync()

    db_params.path = db_path

    signals.stdout.emit('Done! \n')
