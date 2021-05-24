#!/usr/bin/env python3
"""Run BIDS fMRIPrep on all subjects in the project."""

from datetime import datetime
import logging
import sys

import flywheel_gear_toolkit

log = logging.getLogger(__name__)

GEAR = "all-subject-bids-fmriprep"
REPO = "flywheel-apps"
CONTAINER = f"{REPO}/{GEAR}]"


def main(gtk_context):

    gtk_context.log_config()

    return_code = 0

    fw = gtk_context.client

    gear_to_launch = gtk_context.config.get("gear-gear-to-run")

    if "gear-test-override-gear" in gtk_context.config:
        old_gear_to_launch = gear_to_launch
        gear_to_launch = gtk_context.config.get("gear-test-override-gear")
        log.info("Not launching %s, running %s instead", old_gear_to_launch, gear_to_launch)

    gear = fw.lookup(f"gears/{gear_to_launch}")
    log.info(f"{gear_to_launch} version = {gear.gear.version}")

    destination = fw.get(gtk_context.destination["id"])
    job_id = destination.reload().job.id
    project = fw.get_project(destination.parents.project)

    for subject in project.subjects.iter():

        inputs = {}

        config = gtk_context.config

        now = datetime.now()
        analysis_label = f'{gear.gear.name} {now.strftime("%m-%d-%Y %H:%M:%S")} launched by {GEAR} job.id={job_id}'

        analysis_id = gear.run(
            analysis_label=analysis_label,
            config=config,
            inputs=inputs,
            destination=subject,
        )
        log.info("Launched analysis id: %s", analysis_id)

    log.info("%s Gear is done.  Returning %s", CONTAINER, return_code)

    return return_code


if __name__ == "__main__":

    gtk_context = flywheel_gear_toolkit.GearToolkitContext()

    # Setup basic logging and log the configuration for this job
    if gtk_context.config["gear-log-level"] == "INFO":
        gtk_context.init_logging("info")
    else:
        gtk_context.init_logging("debug")

    sys.exit(main(gtk_context))
