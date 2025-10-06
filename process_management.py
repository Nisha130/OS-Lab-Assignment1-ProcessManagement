#!/usr/bin/env python3
# """
# process_management.py
# Operating Systems Lab Assignment 1
# Author: Nisha Sangwan
# Roll No: 2301010068
# College: K.R. Mangalam University

# Tasks Implemented:
# 1. Process creation using os.fork()
# 2. Executing Linux commands using execvp
# 3. Simulating zombie and orphan processes
# 4. Reading process information from /proc/[pid]
# 5. Demonstrating priority (nice) values
# """

import os
import sys
import time
import subprocess

def task1_create_children(n):
    print(f"[Task 1] Creating {n} child processes...")
    pids = []
    for i in range(n):
        pid = os.fork()
        if pid == 0:
            print(f"Child {i+1}: PID={os.getpid()}, PPID={os.getppid()} - Hello!")
            os._exit(0)
        else:
            pids.append(pid)
    for _ in pids:
        pid, _ = os.wait()
        print(f"[Parent] Reaped child PID={pid}")
    print("[Task 1 Completed]")

def task2_exec_command(command):
    print(f"[Task 2] Executing command: {command}")
    pid = os.fork()
    if pid == 0:
        os.execvp(command[0], command)
    else:
        os.wait()
        print("[Task 2 Completed]")

def task3_zombie():
    print("[Task 3] Zombie Process Demonstration")
    pid = os.fork()
    if pid == 0:
        print(f"Child PID={os.getpid()} exiting immediately (becomes zombie).")
        os._exit(0)
    else:
        print(f"Parent PID={os.getpid()} sleeping 5s — child will be zombie.")
        time.sleep(5)
        os.wait()
        print("[Zombie cleared]")

def task3_orphan():
    print("[Task 3] Orphan Process Demonstration")
    pid = os.fork()
    if pid == 0:
        print(f"Child PID={os.getpid()} running, initial PPID={os.getppid()}")
        time.sleep(5)
        print(f"After parent exit, new PPID={os.getppid()}")
        os._exit(0)
    else:
        print(f"Parent PID={os.getpid()} exiting immediately...")
        os._exit(0)

def task4_proc_info(pid):
    base = f"/proc/{pid}"
    print(f"[Task 4] Reading /proc/{pid} info...")
    try:
        with open(f"{base}/status") as f:
            print(f.read())
        exe = os.readlink(f"{base}/exe")
        print(f"Executable Path: {exe}")
    except Exception as e:
        print(f"Error reading process info: {e}")

def task5_priority(n):
    print(f"[Task 5] Running {n} CPU-intensive child processes with different nice values.")
    for i in range(n):
        pid = os.fork()
        if pid == 0:
            os.nice(i * 5)
            print(f"Child {os.getpid()} with nice={i*5} started.")
            start = time.time()
            for _ in range(10**6):  # CPU work
                pass
            end = time.time()
            print(f"Child {os.getpid()} finished in {end-start:.2f}s")
            os._exit(0)
    for _ in range(n):
        os.wait()
    print("[Task 5 Completed]")

if __name__ == "__main__":
    print("=== Process Management Lab ===")
    task1_create_children(2)
    task2_exec_command(["date"])
    task3_zombie()
    # task3_orphan()   # Uncomment to see orphan example
    task4_proc_info(os.getpid())
    task5_priority(3)
    print("=== All Tasks Completed ===")
