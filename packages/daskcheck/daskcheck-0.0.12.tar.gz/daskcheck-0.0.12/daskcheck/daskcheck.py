#!/usr/bin/env python3
'''

'''
from daskcheck.version import __version__
from fire import Fire
from daskcheck import config

import time
import os

import datetime as dt

import dask
from dask.distributed import Client, progress, as_completed


import platform
import time

import json
import datetime as dt

import glob
import shutil

import sys

from console import fg,bg,fx
#
# blind test: just as good as others...
from dask.utils import import_required

# I CAN SEE ALL CLIENTS
from dask.distributed import get_client
#  worker ID
from dask.distributed import get_worker


import pandas as pd
import numpy as np

# -------------------------from singlexec -----------------------
import subprocess as sp




# ---------------------------------

def get_dask_server():
    ser = ""
    print("i... DC: getting dask server ... ", end="")
    SERV=os.path.expanduser("~/.dask_server")
    if os.path.exists( SERV ):
        with open( SERV  ) as f:
            ser = f.readlines()[0].strip()
    else:
        print("\nX... file with IP address not found:", SERV )
        sys.exit(1)
    print(ser)
    return ser


#-----------------------------------

def proper_function_main( order, param):
    """
    barebone function
    """
    import subprocess as sp
    import platform
    import re
    import psutil
    import os
    import importlib
    start_time = time.perf_counter()  # Start the clock <-------------
    # -----start to collect info
    name, platf,   =  platform.node(), platform.machine()
    cwd = os.getcwd()
    #=============================================================================
    #BODY

    # sys.path.append('.') # ADD THE PATH FOR IMPORT SEARCH
    impome = "singlemod.py"
    impome = os.path.splitext(impome)[0]
    # UNLOAD FIRST
    try:
        sys.modules.pop( impome )
        #print("i... DC: unloaded successfully, loading now...")
    except:
        print(f"i... DC: {impome} not unloaded, loading now...")
    xcorefunc = importlib.import_module(f'{impome}')
    xcorefunc.tell( f"@{impome}:  call# {order}    PARAM={param} ")

    res = xcorefunc.main( order, param)
    #=============================================================================
    spent_time = time.perf_counter() - start_time # read the clock <--------


    # DEFINE WHAT IS ON RETURN+++++++++++++++++++++++++++++++++++++++++++++++++++++
    columnames=['name','t_spent','param','cwd','res']
    return order, [columnames, name,  spent_time, param, f"{cwd}", res]

#-----------------------------------

def get_cpu_info( order, param):
    """ example function to send to dask cluster cores
    """
    import subprocess as sp
    import platform
    import re
    import psutil
    import os

    start_time = time.perf_counter()  # Start the clock <-------------
    # -----start to collect info
    name, platf,   =  platform.node(), platform.machine()
    coremax = 0
    command = "cat /proc/cpuinfo"
    all_info = sp.check_output(command, shell=True).decode("utf8").strip()
    for line in all_info.split("\n"):
        if "model name" in line:
            proc = re.sub( ".*model name.*:", "", line,1)
            proc = proc.replace("     "," ")
            proc = proc.replace("    "," ")
            proc = proc.replace("   "," ")
            proc = proc.replace("  "," ")
        if "Model" in line:
            proc = re.sub( ".*Model.*:", "", line,1)
        if "processor" in line:
            coremax+=1
    corereal = psutil.cpu_count(logical = False)
    if corereal is None:  corereal = coremax

    #while len(name)<10:name=name+" "  # One lenght for names
    time.sleep(0.3)

    cwd = os.getcwd()
    arr = os.listdir()

    spent_time = time.perf_counter() - start_time # read the clock <--------
    # RETURNS LIST composed of 2 elements: order number + LIST
    # not sure if I must have STR? no...
    columnames=['name','t_spent','param','proc','cwd']
    # param can be string too
    return order, [columnames, name,  spent_time, param, f"{proc}",f"{cwd}"]
    return order, [name,  spent_time, param, f"{platf} {proc} {cwd}"]
    return order, [name,  f"{spent_time:7.1f} s", f"{platf} {proc}",f"pandas=={pd.__version__}",f"numpy=={np.__version__}"]


# ...................................................................
#-----------------------------------
def pislow(size):
    """
    calculate PI
    """
    pi = 0
    accuracy = size
    for i in range(0, accuracy):
        pi += ((4.0 * (-1)**i) / (2*i + 1))
    return pi





# ...................................................................
# ...................................................................
# ...................................................................
# ...................................................................
# ...................................................................



def cleanup_logs():
    """
    create ./OldLogs and move all dask_result*json there NOW
    """
    # cleanup log files
    cwd = os.getcwd()
    LOGBOX = os.path.expanduser("./OldLogs")
    if not os.path.exists(LOGBOX):
        os.mkdir(LOGBOX)
    #os.chdir( LOGBOX )
    #nwd = os.getcwd()

    logs = glob.glob("dask_results_log_*.json")
    for i in logs:
        print(" ... DC: moving",i,LOGBOX)
        shutil.move(i,LOGBOX)
    logs = glob.glob("dask_results_log_*.csv")
    for i in logs:
        print(" ... DC: moving",i,LOGBOX)
        shutil.move(i,LOGBOX)


# ...................................................................
# ...................................................................
# ...................................................................
# ...................................................................
# ...................................................................



# def bash_or_py(filename):
#     """
#     tell if the file is python or a bash script
#     """
#     with open(filename) as f:
#         con = f.readlines()
#     # con = con.split("\n")
#     con = [x.strip() for x in con]

#     bop = None
#     # bash:
#     if  con[0].find("#!/bin/bash")==0:
#         print(f"i... {filename} ... bash file - from shebang")
#         bop = "b"
#     elif con[0].find("#!/usr/bin/python")==0:
#         print(f"i... {filename} ... python file - from shebang")
#         bop = "p"
#     elif con[0].find("#!/usr/bin/env python")==0:
#         print(f"i... {filename} ... python file - from env in shebang")
#         bop = "p"
#     elif con[0].find("#!")==0 and con[0].find("python")>0:
#         print(f"i... {filename} ... python file - from ... some python in the shebang")
#         bop = "p"
#     elif filename.find(".py") == len(filename)-3:
#         print(f"i... {filename} ... python file - from filename")
#         bop = "p"

#     return bop





def announce(MSG, color = bg.darkslategray):
    print(color)
    print("*"*60)
    print( MSG ) #f"             {len(parameters)} jobs WERE SUBMITTED     ")
    print("*"*60, bg.default,fg.default)



#************************************************************************* KING OF FUNCTIONS
#************************************************************************* KING OF FUNCTIONS
#************************************************************************* KING OF FUNCTIONS
def submit( xcore_function,   parameters, upload = None, server=None):
    """
    general client submitter...
 1/ function_to_calculate
 2/LIST of parameters

    ... every parameter goes to one node ...
    RETURNS LIST with TWO elements:   [0]/ ORDER  [1]/  LIST of whatever results
    """
    nnodes = len(parameters)

    print(server)
    dask_server = server
    if dask_server is None:
        dask_server = get_dask_server()


    client = Client(f"{dask_server}:8786")
    announce(f"i... dask server = /{dask_server}/ \n...  client={client}")
    print( )


    spent_time2 = None
    if upload is not None:
        print(f"{bg.green}{fg.white} ..... UPLOADING -->> {upload} {fg.default}{bg.default}", flush=True, end=" ")
        start_time2 = time.perf_counter()  # Start the clock <-------------
        client.upload_file( os.path.expanduser( upload)  )
        spent_time2=time.perf_counter() - start_time2
        print(f"{bg.green}{fg.white} ..... took {spent_time2}  {fg.default}{bg.default}")

    futures = []
    # print(f"...{fg.orange} SUBMITS : {fg.default}")
    announce("SUBMITING JOBS")
    for i in range(nnodes):
        BG=f"{bg.darkmagenta}"
        if (i%2)==0:
            BG=f"{bg.darkblue}"
        print( f"{BG}{i:3d}-{parameters[i]} {bg.default}" , end=" ")
        res = client.submit( xcore_function, i , parameters[i] )
        #res = client.submit( os.system, "touch a" ) # DOID TOUCH
        #res = client.submit( os.system, "./batch_for_worker" ) # works in ~/dask_sandbox but res BAD
        #res = [1,[1]]
        futures.append( res )

    print()
    # announce(f"             {len(parameters)} jobs WERE SUBMITTED     ")
    announce(f"             WAITING TO COLLECT JOBS RESULTS......     ")

    #print(futures)
    # #li = client.gather(futures)

    my_results = {} # DICT - the key is the order of submission
    for future in as_completed(futures):
        n = future.result()   #  int,[list]
        my_results[n[0]] = n[1] # ORDER IS 1st and the DICT KEY TOO

        end="\r"  # every 10th print
        if len(my_results)%10==0: end="\n"
        # I guess for seconds:------------------------
        took = f"-1"
        try:
            took = f"{n[1][2]:6.2f}"
        except:
            took = "xxx"
        print(f"i... {fg.orange}#{n[0]:5d} has ended  ...   {len(my_results):5d}/{len(parameters):5d}     {took} s     {fg.default} ", end=end)

    #----------------maybe for debugging.....  #for k in  sorted(my_results.keys()): print(f"{k:5d}", my_results[k] )


    print("____________________________ Dataframe with results_____________")
    dic_el1=my_results[  list(my_results.keys())[0] ]
    colnames=list(dic_el1[0])

    announce(f"        PANDAS DATAFRAME   {len(colnames)} columns ")   #announce(f"        PANDAS DATAFRAME   {len(colnames)} columns  {type(colnames)} {colnames}")

    print("D... DF  .... my_results", len(my_results) , colnames, dic_el1)
    print( my_results )
    #
    df = pd.DataFrame( my_results ) #
    print(df)
    print("D...  transposing .... my_results", len(my_results) )
    df = df.transpose() # nodes are on rows
    print("D... dropping column 0 ")
    df.drop(columns=df.columns[0], axis=1,  inplace=True) # drop columnnames that came too
    df.columns=colnames # name columns for DF

    # sorting by param, if it is int, it is better
    ISINT=df.param.astype(str).str.isdecimal().all() # np.array_equal(df.param, df.param.astype(int) )
    if ISINT:
        print("i... param is integer, I sort as integer")
        df[['param' ]] = df[['param']].astype(int)
    df1 = df.sort_values( by=['param'], ascending = True)

    print("_"*60)
    print( df1   ) # sort by name ==1st member of the list)
    print("_"*60)


    if len(df1)==1:
        print(f"i... rows in df = {len(df1)} => one result")
        # print(df1.iloc[[0],[4]]) # 4 is res
        result=df1.res.iloc[0]
        print(f"i... result=={result}") # 4 is res ------------- here I have all
    # SORT BY library version.... e.g
    #print( df.sort_values(0).groupby(4, group_keys=True).apply(lambda x:x)  )


    cleanup_logs() # cleaning here


    # Write LOG file.
    now = dt.datetime.now()
    stamp = now.strftime("%Y%m%d_%H%M%S")
    fnameo= f"dask_results_log_{stamp}"
    df1.to_csv( f"{fnameo}.csv")
    with open(f"{fnameo}.json", "w") as fp:
        json.dump( my_results , fp, sort_keys=True, indent='\t', separators=(',', ': '))

    if spent_time2 is not None:
        print(f"i...    UPLOAD {upload} TOOK:  {spent_time2}")
        print(f"i...    visidata {fnameo}.csv")
    return





# ...................................................................
# ...................................................................
# ...................................................................
# ...................................................................
# ...................................................................


def prepare_params(parlist):
    """
    convert given parameter(s) (from typically commandline)  TO LIST (or STR)

    tuple to list;
    string with .. to the range;
    else remain
    """
    # ------  PREPARE PARAMETER LIST

    print(f"i... DC: parameter list= {parlist} of type {type(parlist)}")

    if type(parlist)==tuple:
        parameters = list(parlist)
    elif type(parlist) == str:
        if parlist.find("..")>0:
            rng = parlist.split("..")
            parameters = list( range( int(rng[0]),int(rng[1])+1 ) )
        else:
            parameters = parlist
    elif type(parlist) == int: # JUST ONE (integer) PARAMETER
        parameters = [parlist]
    elif type(parlist) == float: # JUST ONE (integer) PARAMETER
        parameters = [parlist]
    else: # I dont know.... if not a string... what could it be?
        print("X... HERE IT WILL COLLAPSE. Parameter type is ", type(parlist) )
        parameters = parlist
        sys.exit(1)

    print(f"i... DC; parameter list= {parameters} of type {type(parameters)}")
    return parameters





# # ...................................................................
# # ...................................................................
# # ...................................................................
# # ...................................................................


# def exec_outer_py(  order, param,  localrun = False):
#     """
#     DONOT RUN - service function to wrap your file.py for remote.

#     The py file was uploaded before to workers tmp
#     i use  /importlib/ trick for something...


#     :param order: number of the bash - used BY caller
#     :param param: filename (0) and parameters (1:) for the daughter function
#     :param lovalrun: for debugging
#     """
#     import importlib
#     #from importlib import reload

#     # always tmp
#     #import tempfile
#     #print(f" {fg.yellow} {tempfile.gettempdir()} {fg.default}")

#     # ---------------- identify the file
#     print("i... DC: outerpy received:",param)
#     pyname = param[0]
#     newpar = param[1:]


#     cwd = os.getcwd()

#     # check the python code presence - it is NOT present, it is in /tmp
#     # but still it is transported to remote and runs
#     #
#     print(f"i... DC: EOP testing ... {fx.bold}{cwd}/{pyname}{fx.default}", end="")
#     if not os.path.exists( f"{cwd}/{pyname}" ):
#         print(f" {fg.lightred} ... {cwd}/{pyname} [not exists]{fg.default}")
#         #print("X... DC: ... module for import doesnt exist ...      EXIT")
#         #sys.exit(1)
#     else:
#         print(f" {fg.green}  .... {cwd}/{pyname} [It is present! why?] {fg.default}")


#     # SANDBOX = os.path.expanduser("~/dask_sandbox")
#     # if not os.path.exists(SANDBOX):
#     #     os.mkdir(SANDBOX)
#     # os.chdir( SANDBOX )


#     # ---- import the file
#     sys.path.append('.') # ADD THE PATH FOR IMPORT SEARCH
#     impome = pyname
#     impome = os.path.splitext(pyname)[0]
#     print("i... DC: name of module=",impome)
#     print("i... DC:   newpar =",newpar)

#     # UNLOAD FIRST
#     try:
#         sys.modules.pop( impome )
#         print("i... DC: unloaded successfully, loading now...")
#     except:
#         print("X... DC: not unloaded, loading now...")

#     #import_required(f'{impome}',f"no import possible for {impome}")
#     xcorefunc = importlib.import_module(f'{impome}')

#     #print("i... name of loaded module=", xcorefunc)
#     #print("i... name of loaded module main =", xcorefunc.main)
#     return xcorefunc.main(order,newpar)




# # ...................................................................
# # ...................................................................
# # ...................................................................
# # ...................................................................



# def exec_outer_bash(  order, param,  localrun = False):
#     """
#     DONOT RUN - service function to wrap your bashscript for remote.


#     :param order: number of the bash - used BY caller
#     :param param: filename (0) and parameters (1:) for the daughter function
#     :param lovalrun: for debugging
#     """

#     # ---------------- identify the file
#     print("i... DC: execouterbash param received:",param)
#     baname = param[0]
#     CODENAME = param[0]
#     # newpar = param[1:]
#     newpar = param[1] # one parameter only


#     # # this works for a file ...
#     # print( dask.config.get("temporary_directory") )
#     # print( dask.config.get("temporary-directory") )
#     # print(  os.getcwd() )

#     # n = len(get_client().scheduler_info()['workers'])
#     # # I HAVE FOUND THE WAY TO SEE ALL WORKERS
#     # print(n)

#     # # --------------------------------------------- i can go through all temps....
#     # wks = get_client().scheduler_info()['workers']
#     # for i in wks:
#     #     print( i , "  " ,get_client().scheduler_info()['workers'][i]['local_directory'])
#     #     #print( i )
#     # # ------------ but what is my tempdict?
#     print("i.. LOCAL:",  get_worker().id )
#     print("i...LOCAL:",  get_worker().local_directory )


#     # # -  when there is python code uploaded to worker.....
#     # rundir = os.path.dirname(os.path.realpath(__file__)) # I believe, here is all running
#     # # - when in worker
#     rundir=  get_worker().local_directory
#     #print(rundir)


#     print(f"i... DC: checking # {bg.blue}{rundir}/{CODENAME}{bg.default} # presence ", end="")
#     if not os.path.exists( f"{rundir}/{CODENAME}" ):
#         print(f" {fg.red} ... [MISSING]{fg.default}")
#         print(f"X... {bg.yellow}{fg.white}SE: ... prg to run  doesnt exist ...      EXIT{fg.default}{bg.default}")
#         sys.exit(1)
#     else:
#         print(f" {fg.green}  .... [OK] {fg.default}")


#     # ENTER SANDBOX

#     SANDBOX = os.path.expanduser("~/dask_sandbox")
#     if not os.path.exists(SANDBOX):
#         os.mkdir(SANDBOX)
#     cwd = os.getcwd()
#     os.chdir( SANDBOX )
#     nwd = os.getcwd()


#     # RUN IT FROM   __________RUNDIR_______

#     if not os.access( f"{rundir}/{CODENAME}" , os.X_OK ):
#         os.chmod( f"{rundir}/{CODENAME}" , 0o777)


#     print("_"*50)
#     CMD = [f"{rundir}/{CODENAME}", str(newpar) ]
#     print("i... runnning now",CMD)
#     sp.run( CMD )
#     print("_"*50)
#     res = sorted(glob.glob("*")) # rusults are files in FOLDER
#     res = res[-1]


#     print(f"{bg.green} ... returning from signlexec  ... {bg.default}")

#     name, platf,   =  platform.node(), platform.machine()
#     return order,[name, param,  nwd, res , dt.datetime.now().strftime("%H:%M:%S")]





# ...................................................................
# ...................................................................
# ...................................................................
# ...................................................................

#------------------------------------------------------------------------ MAIN ***************
def main( pyname, parlist):
    """
    Tool to import a file's main() and execute it in DASK

    It is tested with SINGLE file. That is imported and launched.
    its main() MUST:
    - contain def main()
    - accept (order +) ONE parameter only
    - comply with the return structure of the main()


    I do 1/ Create Param_LIST     2/ call "sumbit" "exec_outer_py"
    :param pyname: your python file with def main() to launch
    :param parlist: parameters like run11  r1,r2,r3,r4,r5   1..5
    """

    # ------  PREPARE PARAMETER LIST ... why not to use prepare_params ?

    parameters = prepare_params(parlist)

    # print(f"i... DC: parameter list= {parlist} of type {type(parlist)}")

    # if type(parlist)==tuple:
    #     parameters = list(parlist)
    # elif type(parlist) == str:
    #     if parlist.find("..")>0:
    #         rng = parlist.split("..")
    #         parameters = list( range( int(rng[0]),1+int(rng[1]) ) )
    #         # included the last
    #     else:
    #         print("?... DC: I dont know what happens next")
    #         parameters = parlist # ????????????
    # elif type(parlist) == int: # JUST ONE PARAMETER, later I prepare for 1
    #         parameters = parlist
    # else:
    #     parameters = parlist
    # print(" ... DC: FINAL PARAMETER LIST:")
    # print(f"i... DC; parameter list= {parameters} of type {type(parameters)}")



    print("i... DC: testing the existence of", pyname)
    if not os.path.exists( pyname ):
        print(f"X... DC: filename {pyname} doesn exist. stop.")
        sys.exit(1)


    if bash_or_py( pyname) is None:
        print("X... I cannot tell which type is the file: ", filename," ... [EXIT] ")
        sys.exit(1)

    ISPYT = bash_or_py( pyname)=="p"



    # --------- RUN IN DASK OR LOCALY

    if type(parameters)==list and len(parameters)>1:
        print(f"i... DC: viable for {bg.red}DASK{bg.default} ....")



        newpars = [ [pyname,x] for x in parameters]  # filename to launch AND his parameter
        #newpars = [ str(x) for x in parameters]  # filename to launch AND his parameter

        cwd = os.getcwd()


        # if os.path.splitext(pyname)[-1]==".py":
        #     print()
        # else:
        #     print("X... {fg.white}{bg.red}NOT PYTHON EXTENSION IN {pyname}... EXIT {fg.default}{bg.default}")
        #     sys.exit(1)


        #
        #  I NEED to upload the python single-file itself
        #

        client = Client(f"{get_dask_server()}:8786")

        print(f"{bg.darkgreen}{fg.white} ..... MAIN uploading {cwd}/{pyname} {fg.default}{bg.default}")
        client.upload_file( f"{cwd}/{pyname}" )

        #time.sleep( 1)
        print("............................................OK")
        time.sleep(1)
        print("............................................OK")

        if ISPYT:
            #
            #  this works for python.
            #
            print(f"I... {fg.white}submitting PY ========================>{fg.default}")
            submit( exec_outer_py ,  newpars , upload = None ) # no upload here...
        else:
            #
            #  and bash?
            #
            print(f"I... {fg.white}submitting BASH ::::::::::::::::::::::>{fg.default}")
            submit( exec_outer_bash ,  newpars , upload = None ) # no upload here...


        #submit( get_cpu_info  ,  parameters )


    else:  # --------- RUN  LOCALY --------------------------------------------------
        print(f"i... {bg.red}{fg.white}this is something for local run ... too few parameters{bg.default}{fg.default}")
        #my_results = xcorefunc.main( 1 , parameters )
        newpars =  [pyname, parameters]
        my_results = exec_outer_py( 1 , newpars , localrun = True)

        # cleanup log files
        cleanup_logs()


        # Write LOG file.
        now = dt.datetime.now()
        stamp = now.strftime("%Y%m%d_%H%M%S")
        with open(f"dask_results_log_{stamp}.json", "w") as fp:
            json.dump( my_results , fp, sort_keys=True, indent='\t', separators=(',', ': '))
    return


# ...................................................................
# ...................................................................
# ...................................................................
# ...................................................................


def test(server = None):
    """
    HARDWIRED TEST - 40X get_cpu_info submited to cluster
    """
    NTASKS = 40
    submit(  get_cpu_info, [ str(x) for x in range(1,NTASKS) ] , server=server)

# ...................................................................
def proper(filename, PARAMS, server = None):
    """
    network using proper function importing/calling filename:main - 40X get_cpu_info submited to cluster
    """
    parameters = prepare_params(PARAMS)
    announce(f"module {filename};   \nparameter list: {parameters}", color = f"{bg.mediumvioletred}{fg.white}")
    #return
    #NTASKS = 40
    # submit(  proper_function_info, [ x for x in range(1,NTASKS) ] , upload="~/Downloads/beam_dump.pdf" ,server=server)
    # submit(  proper_function_main, [ x for x in parameters ] , upload="singlemod.py" ,server=server)
    submit(  proper_function_main, [ x for x in parameters ] , upload=filename ,server=server)

# ...................................................................
# ...................................................................
# ...................................................................
# ...................................................................

def loc():
    """
    Run the test get_cpu  locally.
    """
    print(  get_cpu_info( 1, "par1")  )




#==============================================================================================
if __name__=="__main__":
    print("i...  Daskcheck (DC) -  loc for get_cpu_info; test for submit job")
    # print("___________________________________________________________________________")
    # print(" ... the core function :       get_cpu_info  ")
    # print()
    # print(" ... test  :  use submit() 40x")
    # print(" ... local :  only run get_cpu_info")
    # print(" ... dask  :  import module/function and run with the list of parameters ")
    # print()
    # print()
    # print("___________________________________________________________________________")

    Fire({"net":test,
          "loc":loc,
          "file":proper
          #"bp":bash_or_py,
          #"exec_outer_py":exec_outer_py
    } )
    # Fire({"dask":main,
    #       "test":test,
    #       "test2":proper,
    #       "loc":loc,
    #       "bp":bash_or_py,
    #       "exec_outer_py":exec_outer_py
    # } )
