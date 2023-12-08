import glob
import json
import logging
import os
from datetime import datetime

import pytest

test_results: list = []
logger = logging.getLogger(__name__)


def pytest_configure(config) -> None:
    logging.basicConfig(level=logging.INFO)
    if hasattr(config, "workerinput"):
        # Unique file for each worker in parallel execution
        worker_id = config.workerinput.get("workerid", "master")
        config.worker_output_file = (
            f"test_report_{worker_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        )
    else:
        # Default file name for non-parallel execution
        config.worker_output_file = (
            f"test_report_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        )


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call) -> None:
    if call.when == "call":
        test_result = {
            "name": item.nodeid,
            "outcome": "passed" if call.excinfo is None else "failed",
            "duration": call.stop - call.start
            if hasattr(call, "stop") and hasattr(call, "start")
            else None,
            "longrepr": str(call.excinfo) if call.excinfo else None,
        }
        test_results.append(test_result)
        logging.info(f"Test result appended: {test_result}")


@pytest.hookimpl(hookwrapper=True)
def pytest_sessionfinish(session, exitstatus) -> None:
    yield
    report_file = session.config.worker_output_file
    try:
        with open(report_file, "w") as f:
            json.dump(test_results, f, indent=4)
        logging.info(f"Test results written to {report_file}.")
    except Exception as e:
        logging.error(f"Error writing to file: {e}")


def pytest_terminal_summary(terminalreporter, exitstatus, config) -> None:
    report_files = glob.glob("test_report_*.json")
    aggregated_results = []

    for file in report_files:
        with open(file, "r") as f:
            results = json.load(f)
            aggregated_results.extend(results)
        os.remove(file)

    if aggregated_results:
        with open("aggregated_test_report.json", "w") as f:
            json.dump(aggregated_results, f, indent=4)
        logger.info(f"Aggregated results written to aggregated_test_report.json.")
    else:
        logger.warning("No results found to aggregate.")
