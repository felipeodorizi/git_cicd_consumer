#!/usr/bin/env python3

import sys
import pathlib
from ecflow import Defs

if __name__ == '__main__':
    # sys.argv[0] is the script name itself.
    # sys.argv[1] should be suite file name

    base = pathlib.Path.cwd()

    if len(sys.argv) > 1:
        try:
            suite_file = sys.argv[1]
            print(f"[1] Load suite definition from file {suite_file}")
            defs = Defs(str(base / suite_file))
            #print(defs)
            print("[2] Validating job creation: .ecf -> .job0")
            defs.check_job_creation(throw_on_error=True, verbose=True)

        except RuntimeError as e:
            print("Failed:", e)
            sys.exit(1)   # retorna código de erro para o bash


    else:
        print("Provide a suite definition file as argument. Ex: ./validade.py suite.def")
