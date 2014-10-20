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
root(["usermod", "-G", "sudo", "jenkins"])
subprocess.check_call("echo \"%sudo ALL=NOPASSWD: ALL\" | " +
                      "sudo tee -a /etc/sudoers", shell=True)

root(["mkdir", "/var/mojo"])
root(["chmod", "777", "/var/mojo"])
system(["git", "clone", "https://github.com/domokit/tools.git", "/var/mojo/tools"])

root(["docker", "build", "-t", "mojo-image", "/var/mojo/tools/docker"])
root(["sudo", "-u", "jenkins", "/var/mojo/tools/configure_jenkins.py"])

root(["/etc/init.d/jenkins", "restart"])
