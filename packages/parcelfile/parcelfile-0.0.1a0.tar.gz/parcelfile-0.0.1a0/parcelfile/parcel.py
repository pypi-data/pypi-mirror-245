'''Welcome to parcel.py! this project was made to "package programs properly".
The contents of this file are original. Creation rights go to @malachi196 on github'''

'''for any items with kwargs, input a variable name, and its value'''

import sys
import os
from zipfile import ZipFile
import P_Requirments as pr #personal module for unnamed functions

class colors:
  red = '\033[91m'
  green = '\033[92m'
  yellow = '\033[93m'
  blue = '\033[94m'
  magenta = '\033[95m'
  cyan = '\033[96m'
  white = '\033[97m'
  end = '\033[0m'

#=====logo=====
print(f"""This project was made with {colors.cyan}Parcel{colors.end}, the:
      {colors.red}P{colors.end}|{colors.red}ython file
      {colors.green}A{colors.end}|{colors.green}rranger with
      {colors.yellow}R{colors.end}|{colors.yellow}endering
      {colors.magenta}C{colors.end}|{colors.magenta}omplex
      {colors.red}E{colors.end}|{colors.red}lement
      {colors.green}L{colors.end}|{colors.green}eafs
      {colors.end}""")

#=====literals=====
ZIPPED = pr.mode['zipped']
STR = pr.type['str']
INT = pr.type['int']
BOOL = pr.type['bool']
FLOAT = pr.type["float"]
MULTI = pr.type['other']

#=====functions=====
def Parcel(*args):
  pass

def measure(filename): # measures length of contents
  with open(filename,'r') as f: 
    fileno = f.fileno()
    print(fileno)

def package(filenames,mode:pr.mode): # packages files
  if mode == pr.mode['zipped'] or ZIPPED:
    pr.modesliteralZIPPED(filepassname=filenames)
    print(f"packaged {filenames}")

def unpackage(filenames): # unpackages files
  print(f"unpackaged {filenames}")

def wrap(type,spacing,**kwargs): # wraps items
  results = ""
  try:
    if type == STR: #str
      if spacing == True:
        for arg in kwargs.values():
          results += arg + " "
          return results
      else:
        for arg in kwargs.values():
          results += arg 
      return results
    elif type == INT: # int
      if spacing == True:
        for arg in kwargs.values():
          results += str(arg) + " "
        return results
      else:
        for arg in kwargs.values():
          results += arg 
    elif type == BOOL: # bool
      if spacing == True:
        for arg in kwargs.values():
          results += str(arg).lower() + " "
        return results.lower()
      else:
        for arg in kwargs.values():
          results += str(arg).lower()
        return results.lower()
    elif type == FLOAT: # float
      if spacing == True:
        for arg in kwargs.values():
          results += str(arg) + " "
        return results
      else:
        for arg in kwargs.values():
          results += str(arg)
    elif type == MULTI: # other
      if spacing == True:
        for arg in kwargs.values():
          results += str(arg).lower() + " "
        return results
      else:
        for arg in kwargs.values():
          results += str(arg).lower()
        return results
  except Exception as e:
    raise RuntimeError(f"An error occoured with kwargs. Exception: {e}")

def box(file,start_line,end_line): # boxes items
  directory = os.getcwd()
  log = []
  try:
    with open(file, 'r') as f:
      contents = f.read()
      if contents.count(str(start_line),str(end_line)) >= start_line and contents.count(str(start_line),str(end_line)) <= end_line:
        for item in contents.count(str(start_line), str(end_line)):
          log.append(item)
        with open(f"boxed_{file}", "w") as fle:
          fle.write(log)
  except OSError as e:
    raise OSError(f"error with OS. Exception: {e}")
  except Exception as e:
    raise RuntimeError(f"error with system. Exception: {e}")