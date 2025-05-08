#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from tm_slack_reporter.crew import TmSlackReporter

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    """
    Run the crew.
    """
    inputs = {
        "slack_channel_name": "#tm-slack-reporter-test",
        "time_period": "last 30 days",
        "slack_user_name": "echo",
    }

    try:
        TmSlackReporter().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "slack_channel_name": "#tm-slack-reporter-test",
        "time_period": "last 30 days",
        "slack_user_name": "echo",
    }
    try:
        TmSlackReporter().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        TmSlackReporter().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "slack_channel_name": "#tm-slack-reporter-test",
        "time_period": "last 30 days",
        "slack_user_name": "echo",
    }

    try:
        TmSlackReporter().crew().test(
            n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
