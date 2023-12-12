#!/usr/bin/env python3
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import
import os
import subprocess
import sys


# import colemen_utils as c
import colemen_mint_setup.settings as _settings




def execute_cmd(cmd):
    cmd = cmd.replace("//","/")
    subprocess.call(["/bin/bash", "-c", cmd])

def set_gsetting(path,name,value,logMessage=None):
    path = path.replace("/",".")
    cmd = f"gsettings set {path} {name} '{value}'"
    if isinstance(value,(int)):
        cmd = f"gsettings set {path} {name} {value}"

    if isinstance(value,(bool)):
        if value is True:
            cmd = f"gsettings set {path} {name} true"
        if value is False:
            cmd = f"gsettings set {path} {name} false"


    if logMessage is not None:
        logMessage = logMessage.replace("$value",value)
        print(logMessage)
    else:
        print(f"    {path} {name} = {value}")
    subprocess.call(["/bin/bash", "-c", cmd])

def dconf_write(path:str,value):
    path = path.replace(".","/")

    if path.startswith("/") is False:
        path = f"/{path}"

    cmd = f"dconf write {path} '{value}'"
    if isinstance(value,(int)):
        cmd = f"dconf write {path} {value}"
    if isinstance(value,(list)):
        sval = []
        for x in value:
            if isinstance(x,(str)):
                sval.append(f"'{x}'")
            if isinstance(x,(int)):
                sval.append(f"{x}")
        value = ','.join(sval)
        cmd = f'dconf write {path} "[{value}]"'
        if len(sval) == 0:
            cmd = f'dconf write {path} "[]"'


    if isinstance(value,(bool)):
        if value is True:
            cmd = f"dconf write {path} true"
        if value is False:
            cmd = f"dconf write {path} false"


    # print(cmd)
    print(f"    {path} = {value}")

    subprocess.call(["/bin/bash", "-c", cmd])

def install_app(name,ppa:str=None):
    if ppa is not None:
        if ppa.startswith("ppa") is False:
            ppa = f"ppa:{ppa}"
        execute_cmd(f"sudo DEBIAN_FRONTEND=noninteractive add-apt-repository --assume-yes {ppa}")
        execute_cmd("sudo apt-get update")
    execute_cmd("sudo DEBIAN_FRONTEND=noninteractive apt-get --assume-yes install -y {name}")
