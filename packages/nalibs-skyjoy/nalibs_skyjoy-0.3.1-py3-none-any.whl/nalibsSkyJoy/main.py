#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from nalibsAWS import Exit
from nalibsAWS.x0_cli_cicd import main_cicd_aws_sm


def run_cicd_aws_sm():
    try:
        main_cicd_aws_sm()
    except KeyboardInterrupt:
        print("Quit.")
        sys.exit(Exit.KEYBOARD_INTERRUPT)
    except Exit as e:
        sys.exit(e.exitcode)


if __name__ == "__main__":
    run_cicd_aws_sm()
