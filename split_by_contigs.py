#!/usr/bin/python
# -*- coding: <encoding name> -*-

#      This python script will spilt a fasta file by contigs and output several files each containing a contig
#      Moh Salim Dason
#      University of Eastern Piedmonte
#      dasonsalim@outlook.com // 20041232@studenti.uniupo.it

import os
import sys
import re
try:
  import argparse
except ImportError:
  print ("Sorry, Failure importing  *argparse*")

parser = argparse.ArgumentParser(description= 'Select a fasta file and split it into several fasta files with each containing a contig. The ouput fasta files will be stored in a directory named: Split_Contigs')
parser.add_argument('-fasta', required=True, help=' Fasta File ')

args = parser.parse_args()

fic=args.fasta


print ("The process to split your fasta file by contigs has begun!")


fic=""
redundant=""

for line in open(fic):
	line=line.strip()
	

	if line.startswith('>'):						# If the line is the name of a contig
		contig=line.split("|")[0]					# Retrieve the name of the contig by spliting from the first vertical bar and removing ">"
		contig=contig.replace(">","")
		
	if contig == fasta_file:						#If the name of the contig is the same as the file being written
		tmp.write(line+"\n")						#Add a line to the file
	else:
		redundant=redundant+"-"
		print (redundant)
		fasta_file = contig							#Else create a new file with the name of the contig
		tmp=open(contig,"w")			
		tmp.write(line+"\n")						#JAdd a new line
		
		
command="mkdir Split_Contigs"
os.system(command)
command="mv Con* Split_Contigs"
os.system(command)
	
		
print ("Successful. Your Fasta file has been split into contigs")