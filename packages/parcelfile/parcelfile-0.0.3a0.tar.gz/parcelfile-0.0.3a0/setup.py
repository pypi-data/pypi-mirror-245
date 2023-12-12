from setuptools import setup, find_packages

long_description = open("parcelfile/README.md","r").read()

setup(
  name="parcelfile",
  
  install_requires=[], #Installs the packages that are required to run the module
  
  packages=find_packages(), #Finds all the packages in the directory
  
  version="v0.0.3-alpha", #Module version

  description="parcel is a created for manipulating file's funtions within python", #Short description of the module
  
  license="MIT", #The MIT license is free and its the best to use (https://choosealicense.com/licenses/mit/)
  
  long_description=long_description, #Sets the long_description
  
  long_description_content_type='text/markdown', #Sets the long_description to be read as markdown (*.md)
  author="@malachi196", #The author of the module
  
  author_email="malachiaaronwilson@gmail.com", #The author email of the module
  
  url="https://github.com/malachi196/parcel", #The url of the module #If you want to post it on github then its best to put the github repo here but if not you can remove this
) 