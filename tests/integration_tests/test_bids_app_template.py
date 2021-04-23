import logging
from pathlib import Path
from unittest import TestCase

import flywheel_gear_toolkit

import run

log = logging.getLogger(__name__)


def test_run_works(
    caplog, install_gear, un_install_gear, search_caplog_contains, search_caplog
):

    caplog.set_level(logging.DEBUG)

    user_json = Path(Path.home() / ".config/flywheel/user.json")
    if not user_json.exists():
        TestCase.skipTest("", f"No API key available in {str(user_json)}")

    FWV0 = Path.cwd()

    install_gear("bids_app_template.zip")

    with flywheel_gear_toolkit.GearToolkitContext(input_args=[]) as gtk_context:

        status = run.main(gtk_context)

    assert status == 0
    assert search_caplog(
        caplog, "Not launching bids-fmriprep, running bids-app-template instead"
    )

    un_install_gear()
