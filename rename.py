#!/usr/bin/python

import os
import sys

def main():
	if not len(sys.argv)==2:
		print "Error : Directory name missing."
		sys.exit(1)
	if not os.path.isdir(sys.argv[1]):
		print "Error :",sys.argv[1],"is not a Directory."
		sys.exit(2)
	dirname = sys.argv[1]
	files = os.listdir(dirname)
	for i in range(len(files)):
		complete_filename = dirname+'/'+files[i]
		filename,ext = os.path.splitext(complete_filename)
		os.rename(complete_filename,dirname+"/"+dirname+"_"+str(i+1)+ext)

if __name__ == "__main__":
	main()