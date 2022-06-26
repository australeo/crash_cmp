#!/usr/bin/python3
"""
Example lldb python script, currently targetting MacOS ARM64
"""

import os
from os.path import isfile, join
import sys
# Make sure this points to installed LLDB python module
sys.path.append(!!!LLDB Python path here)
import lldb

# Set to target arch
TARGET_ARCH = !!!Your arch here
DEBUG = False

def debug_print(s):
    if(DEBUG):
        print(s)

def get_files(path):
    return [f for f in os.listdir(path) if isfile(join(path, f))]

def main(path):
    if len(sys.argv) < 3:
        print("Usage:\tcrash_cmp.py <program> <path_to_testcases>")
        return

    program = sys.argv[1]
    path = sys.argv[2]

    print(f"[*] Using \'{path}\' as testcase directory.")
    files = get_files(path)
    if len(files) == 0:
        print("[!] No testcases found!")
        return

    crashes = {}

    for f in files:
        fp = join(path, f)
        debug_print(f"Running testcase \'{str(fp)}\'")
        crash = run_testcase(program, str(fp))
        crashes.setdefault(crash,[]).append(fp)

    for c in crashes.keys():
        print(f"Crash occurs at: {c}\nTestcases:")
        for v in crashes[c]:
            print(f"\t{v}")


def run_testcase(program, argpath):
    crashline = None

    # Create a new debugger instance
    debugger = lldb.SBDebugger.Create()

    # Set arch
    target = debugger.CreateTargetWithFileAndArch(program, TARGET_ARCH)

    # Run program until end/failure
    debugger.SetAsync(False)

    if target:

        # Build argv[...]
        args = [argpath]

        # Launch target in debugger
        process = target.LaunchSimple(args, None, os.getcwd())

        if process:
            
            state = process.GetState()
            if state == lldb.eStateStopped:

                # Assume only one thread for now
                thread = process.GetThreadAtIndex(0)
                if thread.stop_reason == lldb.eStopReasonException:
                    debug_print("Crash detected!")
                    frame = thread.GetSelectedFrame()

                    # Get the line the crash occurred on
                    crashline = str(frame.line_entry).split('/')[-1]
                    debug_print(frame)

            else:
                debug_print(f"Process didn't crash!")
                process.Kill()

    debug_print("")
    return crashline

if __name__ == '__main__':
    main(sys.argv[1])
