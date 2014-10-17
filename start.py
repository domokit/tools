#!/usr/bin/env python

import os
import subprocess

job_name = os.environ['JOB_NAME']

retval = subprocess.call(["sudo", "docker", "run", "--name=%s" % job_name, "e0516f09bd70", "/mojo/build.py"])
subprocess.check_call(["sudo", "docker", "rm", job_name])

os.exit(retval)
