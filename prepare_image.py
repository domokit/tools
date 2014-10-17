#!/usr/bin/env python

import os
import subprocess

def system(command):
    return subprocess.check_call(command)

def root(command):
    return system(["sudo", "-n"] + command)

root(["mkdir", "/ssd"])
root(["mount", "-t", "ext4", "/dev/sdb", "/ssd"])
root(["ln", "-s", "/ssd/docker", "/var/lib/docker"])

subprocess.check_call("wget -q -O - https://jenkins-ci.org/debian/jenkins-ci.org.key | sudo -n apt-key add -", shell=True)
subprocess.check_call("sudo -n sh -c 'echo deb http://pkg.jenkins-ci.org/debian binary/ > /etc/apt/sources.list.d/jenkins.list'", shell=True)
subprocess.check_call("curl -sSL https://get.docker.com/ | sh", shell=True)


root(["apt-get", "update"])
root(["apt-get", "install", "-y", "git", "jenkins"])
# TODO: add user 'jenkins' to the sudo without password list
root(["usermod", "-G", "sudo", "jenkins"])

system(["git", "clone", "https://github.com/domokit/tools.git"])

root(["sudo", "-u", "jenkins", "./tools/configure_jenkins.py"])

root(["/etc/init.d/jenkins", "restart"])
