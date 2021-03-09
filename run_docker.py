# coding=UTF-8

import docker
import os
from os.path import abspath, join, dirname


def main():
    run()


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
                                          tty=True
                                          )

    print("Container id:{}".format(ros_container.short_id))


if __name__ == '__main__':
    main()
