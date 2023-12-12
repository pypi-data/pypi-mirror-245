#!/usr/bin/env python3
# v1945
from fire import Fire
import time
import platform
import datetime as dt
import os
import tempfile
from console import fg,bg
import subprocess as sp
import glob

import sys
import shutil # for copy

#
#2023-05-11
# we run   ./daskcheck.py dask singlexec.py 1..100
#
#   we want:    ./daskcheck.py dask  batch_for_worker  1..100
#
#



def main( order, param):
    """
    test to RUN BASH  on remote. Must exist 1st

    It creates a file in ~/dask_sendbox - the name changes with param. Try
with ./daskcheck.py dask temod.py 1,3

    :param order: just the number returned back
    :param param: list or number, only first element taken
    """
    #time.sleep(1)
    #print("i... param===", param)
    if type(param) is list:
        pp = param[0]
    elif type(param) is tuple:
        pp = param[0]
    else:
        pp = param

    #pi = pislow(pp*1000000)
    ###print(f" {fg.yellow} {tempfile.gettempdir()} {fg.default}")
    ###cwd = tempfile.gettempdir()
    # CHECK EXISTENCE OF RUNME


    CODENAME = "batch_for_worker"

    rundir = os.path.dirname(os.path.realpath(__file__)) # I believe, here is all running
    print(rundir)
    # time.sleep(1)
    #res = glob.glob("*") # this finds files in the current folder. Not enough for me
    #res = glob.glob(rundir) # this finds files in the current folder. Not enough for me
    #print(res)

    print(f"i... SE: checking # {bg.blue}{rundir}/{CODENAME}{bg.default} # presence ", end="")
    if not os.path.exists( f"{rundir}/{CODENAME}" ):
        print(f" {fg.red} ... [MISSING]{fg.default}")
        print(f"X... {bg.yellow}{fg.white}SE: ... prg to run  doesnt exist ...      EXIT{fg.default}{bg.default}")
        sys.exit(1)
    else:
        print(f" {fg.green}  .... [OK] {fg.default}")



    # ENTER SANDBOX

    SANDBOX = os.path.expanduser("~/dask_sandbox")
    if not os.path.exists(SANDBOX):
        os.mkdir(SANDBOX)
    cwd = os.getcwd()
    os.chdir( SANDBOX )
    nwd = os.getcwd()



    # RUN IT FROM   __________RUNDIR_______

    if not os.access( f"{rundir}/{CODENAME}" , os.X_OK ):
        os.chmod( f"{rundir}/{CODENAME}" , 0o777)


    print("_"*50)
    CMD = [f"{rundir}/{CODENAME}", str(param[0]) ]
    print("i... runnning now",CMD)
    sp.run( CMD )
    print("_"*50)
    res = sorted(glob.glob("*")) # rusults are files in FOLDER
    res = res[-1]


    # # COPY CODENAME TO SANDBOX
    # try:
    #     shutil.copyfile( f"{rundir}/{CODENAME}", f"{SANDBOX}/{CODENAME}")
    #     if not os.access( f"{SANDBOX}/{CODENAME}" , os.X_OK ):
    #         os.chmod( f"{SANDBOX}/{CODENAME}" , 0o777)
    # except:
    #     print("X... not copied, file is busy")


    # CHANGE TO SANDBOX


    # print(f"i... SE: checking # {bg.cyan}{cwd}/{CODENAME}{bg.default} # presence ", end="")
    # if not os.path.exists( f"{nwd}/{CODENAME}" ):
    #     print(f" {fg.red} ... [MISSING]{fg.default}")
    #     print(f"X... {bg.red}{fg.white}SE: ... prg to run  doesnt exist ...      EXIT{fg.default}{bg.default}")
    #     sys.exit(1)
    # else:
    #     print(f" {fg.green}  .... [OK] {fg.default}")

    # RUN AND GLOB THE RESULTS

    #print(res)

    #with open(f"aaaa{pp}","w") as f:
    #    f.write(" ")


    print(f"{bg.green} ... returning from signlexec  ... {bg.default}")


    name, platf,   =  platform.node(), platform.machine()
    return order,[name, param,  nwd, res , dt.datetime.now().strftime("%H:%M:%S")]

if __name__=="__main__":
    Fire(main)
