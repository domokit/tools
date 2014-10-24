#!/usr/bin/env python

import os
import shutil
import subprocess

def system(command):
    return subprocess.check_call(command)

home = os.environ["HOME"]
shutil.copy("/tmp/jenkins_config.xml", os.path.join(home, "config.xml"))
dest = os.path.join(home, "jobs", "mojo_continuous_builder")
system(["mkdir", "-p", dest])
shutil.copy("/var/mojo/tools/jenkins/mojo_continuous_builder_config.xml", dest)

plugin_dir = os.path.join(home, "plugins")
system(["mkdir", "-p", plugin_dir])

plugins = [
    "credentials",
    "git",
    "git-client",
    "github-api",
    "github-oauth",
    "scm-api",
    "ssh-credentials"]

os.chdir(plugin_dir)
for p in plugins:
    system(["wget", "-q", "http://updates.jenkins-ci.org/latest/" + p + ".hpi"])
