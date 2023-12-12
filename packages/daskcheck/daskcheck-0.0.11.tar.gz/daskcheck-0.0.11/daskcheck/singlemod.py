#!/usr/bin/env python3
"""
 This function is imported
then
 TELL is called with anounced parameter and
 MAIN is called !!!

whatever is returned from MAIN is included to json and csv later
"""
from fire import Fire
import time
import platform
import datetime as dt
import os
import tempfile
from console import fg,bg
import sys


def tell(word):
    print(bg.midnightblue)
    print("*"*60)
    print(word)
    print("*"*60  ,bg.default)

#-----------------------------------
def pislow(size):
    """
    calculate PI
    """
    pi = 0
    accuracy = size
    for i in range(0, accuracy):
        pi += ((4.0 * (-1)**i) / (2*i + 1))
    return float(pi)



def main( order, param,  localrun = False):
    """
    test to write to a directory on remote

    It creates a file in ~/dask_sendbox - the name changes with param. Try with ./daskcheck.py dask temod.py 1,3

    :param order: just the number returned back
    :param param: list or number, only first element taken
    """
    import math
    #---------------------------------- treat params: can be list, tuple, int
    #print("i... param===", param)
    if type(param) is list:
        pp = param[0]
        print("X.. parameter must be one element")
        sys.exit(1)
    elif type(param) is tuple:
        pp = param[0]
        print("X.. parameter must be one element")
        sys.exit(1)
    else:
        pp = param

    if type(pp) is not int:
        print(f"X.. {bg.red}parameter must be one integer {type(pp)} {bg.default}" )
        sys.exit(1)


    pi = pislow(pp* param*param*param*100)
    pi2 = pi - 3.141592853589
    pi2=abs(pi2)
    pi2 = math.log10(pi)

    # #---------------------------------- go to sandbox
    # SANDBOX = os.path.expanduser("~/dask_sandbox")
    # if not os.path.exists(SANDBOX):
    #     os.mkdir(SANDBOX)
    # os.chdir( SANDBOX )
    # cwd = os.getcwd()

    # fname = f"aaaa{pp:04d}"
    # with open(fname,"w") as f:
    #     f.write(" ")

    # print(f"{bg.green} ... I created the file {fname} in sandbox ... {bg.default}")

    #---------------------------------- retrun information
    name   =  platform.node()
    # name, platf   =  platform.node(), platform.machine()
    print(f"i... {fg.lightyellow}# {order:3d}. - returning  {pi} {fg.default}")

    if localrun:
        import json
        # data = {'another_dict': {'a': 0, 'b': 1}, 'a_list': [0, 1, 2, 3]}
        # e.g. file = './data.json'
        print(f"i... {fg.lightyellow}# {order:3d}. - local save  {fg.default}")
        with open(f"P{param:04d}_{order}_output.json", 'w') as f:
            json.dump( {'pi':pi} , f)
        return True
    #return pi2 # [ pi for x in range(10) ]
    return [pi,pi2] # i can return list or whatever reasonable that goes to dataframe
    return order,[name, param, pi,  pp*0.999, dt.datetime.now().strftime("%H:%M:%S")]

if __name__=="__main__":
    Fire(main)
