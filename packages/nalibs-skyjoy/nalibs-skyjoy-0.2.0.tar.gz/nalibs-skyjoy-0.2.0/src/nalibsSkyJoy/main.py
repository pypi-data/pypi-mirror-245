#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from nalibsAWS.x0_cli_cicd import main_cicd_case2


def run_cicd_case2():
    try:
        main_cicd_case2()
    except KeyboardInterrupt:
        print("Quit.")
        sys.exit(Exit.KEYBOARD_INTERRUPT)
    except Exit as e:
        sys.exit(e.exitcode)


if __name__ == "__main__":
    run_cicd_case2()
