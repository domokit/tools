#!/usr/bin/env python

import subprocess
import tempfile
import time

instance_name = "mojo-builder-1"
disk_name = "mojo-builder-ssd-1"
address = "130.211.144.95"
machine_type = "n1-highcpu-16"
zone = "us-central1-f"

def gcompute(command):
    return subprocess.check_call(["gcloud", "compute"] + command)

def delete_instance():
    try:
        gcompute(["instances", "delete",
                  instance_name,
                  "--zone", zone,
                  "--quiet"])
    except:
        print "Failed to delete instance; might already have been deleted."

    try:
        gcompute(["disks", "delete",
                  instance_name,
                  "--zone", zone,
                  "--quiet"])
    except:
        print "Failed to delete disk; might already have been deleted."

delete_instance()

gcompute(["instances", "create",
          instance_name,
          "--address", address,
          "--boot-disk-type", "pd-standard",
          "--disk", "name=" + disk_name,
          "--image", "debian-7-backports",
          "--machine-type", machine_type,
          "--project", "google.com:webkit",
          "--zone", zone,
          "--quiet"])

try:
    # Give the instance a bit of time to spin up or the ssh will fail.
    while subprocess.call(["gcloud", "compute", "ssh",
                           instance_name,
                           "--command", "true",
                           "--quiet",
                           "--zone", zone]) != 0:
        print "waiting for instance to allow ssh..."
        time.sleep(5)

    gcompute(["copy-files",
              "prepare_image.py",
              instance_name + ":~/prepare_image.py",
              "--quiet",
              "--zone", zone])

    with tempfile.NamedTemporaryFile() as temp:
        subprocess.check_call(["gsutil", "cp", "gs://mojo_infra/jenkins_config.xml", temp.name])
        gcompute(["copy-files",
                  temp.name,
                  instance_name + ":/tmp/jenkins_config.xml",
                  "--quiet",
                  "--zone", zone])

    gcompute(["ssh",
              instance_name,
              "--command", "~/prepare_image.py",
              "--quiet",
              "--zone", zone])

except:
    delete_instance()
