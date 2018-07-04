#!/usr/bin/env python

"""
This module iniializes the weekly scan by finding out the list of images
on the registry and initializing the scan tasks scan-worker.
"""

import datetime
import json
import logging
import os
import random
import string

from scanning.lib.queue import JobQueue
from scanning.lib.log import load_logger
from scanning.lib import settings
from scanning.lib.run_saasherder import run_saasherder
from config import GITREPO
import inpect_registry



import beanstalkc
import container_pipeline.lib.dj
from container_pipeline.models.pipeline import Project, Build, BuildPhase
from django.utils import timezone
import glob
import json
import os
import subprocess
import sys
import uuid
import yaml


# Logs base URL
LOGS_DIR_BASE = "/srv/pipeline-logs/"

# REGISTRY end point to process weekly scan against
REGISTRY_ENDPOINT = "{}:5000".format(JENKINS_SLAVE)
SECURE=False


class WeeklyScan(object):
    """
    Class for aggregating operations needed to perform weekly scan
    """

    def __init__(self, sub=None, pub=None):
        self.inspect_registry = inspect_registry.InspectRegistry(
                REGISTRY_ENDPOINT, SECURE)
        # configure logger
        self.logger = logging.getLogger('weeklyscan')
        # initialize beanstalkd queue connection for scan trigger
        self.queue = JobQueue(host=settings.BEANSTALKD_HOST,
                              port=settings.BEANSTALKD_PORT,
                              sub=sub, pub=pub, logger=self.logger)
        self.gitrepo = GITREPO


    def split_repo_name(self, repo_name):
        """
        Given a fully qualified repository name returns a dict
        with parts of repo_name as
        {  "registry": "r.c.o"
           "image": "foo/bar:tag1",
           "tag": "tag1",
           "image_name": "foo/bar"  #name without tag
        }

        """
        if not repo_name:
            return {}

        parts = repo_name.split("/")

        if len(parts) == 1:
            # case for foo:latest
            registry = None
            image = repo_name
        elif len(parts) == 2:
            # check if part[0] is a registry
            if "." in parts[0] or ":" in parts[0]:
                # case for r.c.o/foo:latest
                registry = parts[0]
                image = parts[1]
            else:
                # case for foo/bar:latest
                registry = None
                image = repo_name

        # for cases where len(parts) > 2
        else:
            # check if part[0] is a registry
            if "." in parts[0] or ":" in parts[0]:
                # case for r.c.o/foo/bar:latest
                registry = parts[0]
                image = "/".join(parts[1:])
            else:
                # case for prod/foo/bar:latest
                registry = None
                image = repo_name

        # now process tags
        image_parts = image.split(":")
        if len(image_parts) == 2:
            # case for foo:tag1, foo/bar:tag1, prod/foo/bar:latest
            image_name = image_parts[0]
            tag = image_parts[1]
        else:
            # cases for foo , foo/bar, prod/foo/bar
            image_name = image
            # use default tag
            tag = "latest"

        return {"registry": registry, "image": image,
                "image_name": image_name, "tag": tag}

    def generate_test_tag(self):
        """
        Returns a unique random chars to be used for test_tag
        """
        # test_tag generation, unique per project
        task = subprocess.Popen(
            "date +%s%N | md5sum | base64 | head -c 14",
            shell=True,
            stdout=subprocess.PIPE)
        return task.stdout.read()

    def new_logs_dir(self, test_tag=None):
        """
        Creates a scan dir under LOGS_DIR_BASE with given
        name of test_tag
        """
        if not test_tag:
            test_tag = self.generate_test_tag()

        LOGS_DIR = os.path.join(LOGS_DIR_BASE, test_tag)

        # Create the logs directory
        try:
            if not os.path.exists(LOGS_DIR):
                os.makedirs(LOGS_DIR)
        except OSError as e:
            self.logger.warning(
                "Failing to create {} dir for scanner results. {}".format(
                    LOGS_DIR, e))
            return None
        else:
            return LOGS_DIR


    def run(self):
        """
        Finds all the containers on given registry using REST API calls,
        and puts the containers for scanning
        """
        self.logger.info("Starting weekly scan..")
        self.logger.debug("Finding images in registry {}".format(
            REGISTRY_ENDPOINT))

        # run the inspect registry and list all images
        all_images = self.inspect_registry.list_all_images()

        if not all_images:
            self.logger.critical("No image is found in registry. ")
            return

        self.logger.info("{} no of images found in registry".format(
            len(all_images)))

        for image in all_images:
            split_image_name = self.split_repo_name(image)
            # returns split_image_name as
            # {"registry": registry,
            #  "image": appid/jobid:desiredtag,
            #  "image_name": appid/job,
            #  "tag": tag }

            # handle the libary image case where image_name r.c.o/centos
            if len(split_image_name["image_name"].split("/")) == 1:
                appid = "libary"
                jobid = split_image_name["image_name"]
            # normal case where say image_name = r.c.o/centos/etherpad
            elif len(split_image_name["image_name"].split("/")) > 1:
                appid = split_image_name["image_name"].split("/")[0]
                jobid = split_image_name["image_name"].split("/")[1]

            # desired tag of the image as present in the registry
            desired_tag = split_image_name["tag"]

            # generate project_name
            project_name = "{}-{}-{}".format(appid, jobid, desired_tag)

            # check if project exists in database
            project = Projects.objects.get(name=project_name)

            if not project:
                self.logger.info("{} is not present in database."
                                 "Skipping scan for it".format(project))

            # create a new logs dir for the image's scanning result
            logs_dir = self.new_logs_dir()



            self.put_image_for_scanning(
                    project_name=project_name,
                    desired_tag=desired_tag,
                    namespace=project_name,
                    image_under_test=image,
                    output_image="registry.centos.org/{}".format(
                        split_image_name["image"]),



                    )

        # put every container found to scan
        # create logs dir
        # queue up for scan, split the repo name

        for image in images:
            # create logs dir
            resultdir = self.new_logs_dir()
            if not resultdir:
                # retry once more
                resultdir = self.new_logs_dir()
                if not resultdir:
                    self.logger.warning(
                        "Can't create result dir for repo {}."
                        "Failed to run weekly scan for it.".format(image[2]))
                    continue

            # image = [git-url, git-hash, image]
            self.put_image_for_scanning(
                image[2], resultdir, image[0], image[1], scan_gitpath)
            self.logger.info("Queued weekly scanning for {}.".format(image))
        return "Queued containers for weekly scan."

    def put_image_for_scanning(self, image, logs_dir,
                               giturl, gitsha, scan_gitpath):
        """
        Put the image for scanning on beanstalkd tube
        """
        self.logger.info("Putting {} for scan..".format(image))
        # now put image for scan
        self.queue.put(json.dumps(job), "master_tube")

        # ====================================
        # Scan an image only if it exists in the catalog!
        # if entry_short_name in json_catalog:
        job_uuid = str(uuid.uuid4())
        project_name = str.format(
            "{app_id}-{job_id}-{desired_tag}",
            app_id=str(app_id),
            job_id=str(job_id),
            desired_tag=str(desired_tag)
        )
        data = {
            "action": "start_scan",
            "tag": desired_tag,
            "project_name": project_name,
            "namespace": project_name,
            "image_under_test": "registry.centos.org/%s/%s:%s" %
                                (app_id, job_id, desired_tag),
            "output_image": "registry.centos.org/%s/%s:%s" %
                            (app_id, job_id, desired_tag),
            "notify_email": email,
            "weekly": True,
            "logs_dir": LOGS_DIR,
            "test_tag": test_tag,
            "job_name": job_id,
            "uuid": job_uuid
        }

        job = bs.put(json.dumps(data))
        # Initializing Database entries
        project = Project.objects.get(
            name=project_name
        )
        if not project:
            print(
                str.format(
                    "Skipping {}, as project object was not found",
                    project_name
                )
            )
            continue
        build = Build.objects.create(
            uuid=job_uuid,
            project=project,
            status='queued',
            start_time=timezone.now(),
            weekly_scan=True
        )
        scan_phase, created = BuildPhase.objects.get_or_create(
            build=build,
            phase='scan'
        )
        scan_phase.status = 'queued'
        scan_phase.save()

        print "Image %s sent for weekly scan with data %s" % \
              (entry_short_name, data)







if __name__ == "__main__":
    load_logger()
    ws = WeeklyScan(sub="master_tube", pub="master_tube")
    print(ws.run())



















# connect to beanstalkd tube
bs = beanstalkc.Connection("BEANSTALK_SERVER")
bs.use("master_tube")

# index dir will always have yml files only; but just in case
for f in files:
    with open(os.path.join(os.environ.get("CWD"), "index.d", f)) as stream:
        try:
            yaml_parse = yaml.load(stream)
        except yaml.YAMLError as e:
            print e

    # all entries in a yml file in list of dictionaries format
    entries = yaml_parse.values()[0]

    for entry in entries:
        app_id = entry["app-id"]
        job_id = entry["job-id"]
        desired_tag = entry["desired-tag"]
        email = entry["notify-email"]

        entry_short_name = str(app_id) + "/" + str(job_id)

        # test_tag generation, unique per project
        task = subprocess.Popen(
            "date +%s%N | md5sum | base64 | head -c 14",
            shell=True,
            stdout=subprocess.PIPE)
        test_tag = task.stdout.read()

        LOGS_DIR = os.path.join(LOGS_DIR_BASE, test_tag)

        # Create the logs directory
        if not os.path.exists(LOGS_DIR):
            os.makedirs(LOGS_DIR)

        # Scan an image only if it exists in the catalog!
        # if entry_short_name in json_catalog:
        job_uuid = str(uuid.uuid4())
        project_name = str.format(
            "{app_id}-{job_id}-{desired_tag}",
            app_id=str(app_id),
            job_id=str(job_id),
            desired_tag=str(desired_tag)
        )
        data = {
            "action": "start_scan",
            "tag": desired_tag,
            "project_name": project_name,
            "namespace": project_name,
            "image_under_test": "registry.centos.org/%s/%s:%s" %
                                (app_id, job_id, desired_tag),
            "output_image": "registry.centos.org/%s/%s:%s" %
                            (app_id, job_id, desired_tag),
            "notify_email": email,
            "weekly": True,
            "logs_dir": LOGS_DIR,
            "test_tag": test_tag,
            "job_name": job_id,
            "uuid": job_uuid
        }

        job = bs.put(json.dumps(data))
        # Initializing Database entries
        project = Project.objects.get(
            name=project_name
        )
        if not project:
            print(
                str.format(
                    "Skipping {}, as project object was not found",
                    project_name
                )
            )
            continue
        build = Build.objects.create(
            uuid=job_uuid,
            project=project,
            status='queued',
            start_time=timezone.now(),
            weekly_scan=True
        )
        scan_phase, created = BuildPhase.objects.get_or_create(
            build=build,
            phase='scan'
        )
        scan_phase.status = 'queued'
        scan_phase.save()

        print "Image %s sent for weekly scan with data %s" % \
              (entry_short_name, data)
