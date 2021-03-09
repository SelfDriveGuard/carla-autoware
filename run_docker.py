# coding=UTF-8

import docker
import os
import requests
from os.path import abspath, join, dirname
import sys


def main():
    if not os.path.exists("third-party"):
        os.makedirs("third-party")

    if not os.path.exists("third-party/autoware-contents"):
        print("开始下载第三方依赖")
        url = "https://guard-strike.oss-cn-shanghai.aliyuncs.com/ADTest/autoware-contents.tar.gz"
        path = "third-party/autoware-contents.tar.gz"
        download(url, path)
        unzip(path)
        delete(path)
    else:
        print("第三方依赖已存在")

    run()


def download(url, path):
    with open(path, "wb") as f:
        print("正在下载：{}".format(path))
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:  # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
                sys.stdout.flush()
        print("")


def unzip(path):
    print("正在解压缩:{}".format(path))
    os.system("tar -xzf {} -C third-party/".format(path))


def delete(path):
    os.system("rm {}".format(path))


def run():
    client = docker.from_env()

    ROOT_PATH = abspath(dirname(__file__))
    CONTENTS_PATH = join(ROOT_PATH, "autoware-contents")
    SCRIPTS_PATH = join(ROOT_PATH, "scripts")

    ros_container = client.containers.run("carla-autoware:latest",
                                          detach=True,
                                          volumes={CONTENTS_PATH: {'bind': '/home/autoware/autoware-contents', 'mode': 'ro'},
                                                   SCRIPTS_PATH: {'bind': '/home/autoware/my_scripts', 'mode': 'rw'}},
                                          runtime='nvidia',
                                          network='host',
                                          privileged=True,
                                          environment=["DISPLAY={}".format(
                                              os.getenv('DISPLAY'))],
                                          tty=True  # 防止容器暴毙
                                          )

    print("容器ID为:{}".format(ros_container.short_id))


if __name__ == '__main__':
    main()
