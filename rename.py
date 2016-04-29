#!/usr/bin/python

import os
#will get the file names
dirname = raw_input("Dir name : ")
files = os.listdir(dirname)
for i in range(len(files)):
	os.rename(dirname+"/"+files[i],dirname+"/"+dirname+"_"+str(i+1)+".gif")