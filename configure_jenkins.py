#!/usr/bin/env python

import os
import shutil
import subprocess

def system(command):
    return subprocess.check_call(command)

home = os.environ["HOME"]
dest = os.path.join(home, "jobs", "mojo_continuous_builder")
system(["mkdir", "-p", dest])
shutil.copy("tools/jenkins/config.xml", dest)

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

for p in plugins:
    system(["curl", "http://updates.jenkins-ci.org/latest/" + p + ".hpi", "-o",
            os.path.join(plugin_dir, p + ".hpi")])
