

#!/usr/bin/python
# -*- coding: <encoding name> -*-

#                                                 Script to automate metagenomic workflow
#                                                   Written by: Mohammed Salim Dason 
#                                                   Universita del Piemonte Orientale
#                                             dasonsalim@outlook.com // 20041232@studenti.uniupo.it

import subprocess
import os
import sys
from shutil import copy

os.mkdir("Output")
files = os.listdir('.')
pdf_files = []

for filename in files:
        if filename.endswith(".fq"):
            pdf_files.append(filename)
           

print(f"Your directory contains these fastq files: {pdf_files}\nThese will now be copied into the Script Directory. Please wait...")

destination = os.getcwd()
final=os.path.join(destination, "Output")

#A progress bar so you can see your files are actually being copied

def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), j, count))
        file.flush()        
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()

#Copying files

for i in progressbar(range(2), "Copying Files: ", 60):
    copy(pdf_files[0], final)
    copy(pdf_files[1], final)

print("Files successfully copied. Sequence Assembly will now start..")

#Renaming files to forward.fq and reverse.fq

def file_rename():
    os.chdir(final)
    os.rename(pdf_files[0], "forward.fq")
    os.rename(pdf_files[1], "reverse.fq")


file_rename()


def pipeline():
    
    #Running MetaSpades to assembly reads

    subprocess.call('metaspades.py -t 100 -m 30 -1 forward.fq -2 reverse.fq -o Output', shell = True)
    os.chdir("Output")

    #Reads <1000nt will be discarded using the seqtk tool

    print("Metaspades done, Seqtk will now start...")

    subprocess.call("seqtk seq -L 1000 contigs.fasta > contigs.filtered.fasta", shell=True)

    print("Seqtk done...\n Bowtie2 will now run.")

    #Once seqtk tool is done running, bowtie2 will now proceed

    subprocess.call("bowtie2-build --threads 30 contigs.filtered.fasta contigs.filtered.fasta", shell=True)

    print("Bowtie2 now done.")

    print("Bowtie 2 will now align reads locally, and output a sam files")

    subprocess.call("bowtie2 --threads 60 --no-unal --very-sensitive-local -x contigs.filtered.fasta -1 forward.fq -2 reverse.fq -S aligned.contigs.sam", shell=True)

    print("Alignment done...")

    #SAMTOOLS will convert sam file output into a bam file

    print("Sam tools will now convert sam file to a bam file...")
    subprocess.call("samtools view -Sb aligned.contigs.sam > aligned.contigs.bam", shell=True)

    print("Conversion done...")

    #Bam file will now be sorted by samtools
    
    print("Sorting bam file now...")

    subprocess.call("samtools sort aligned.contigs.bam > aligned.contigs.sorted.bam", shell=True)

    #Now we will get a contig depth summary
    print("Sorting done.\n Depth summary will begin... ")
  
    subprocess.call("jgi_summarize_bam_contig_depths --outputDepth depth.txt aligned.sorted.bam", shell=True)
    
    #Metabat2 will now reconstruct genomes
    print("Genome reconstruction with metabat will now begin...")

    subprocess.call("metabat2 -m 1500 -i contigs.filtered.fasta -a depth.txt -o Reconstructed", shell=True)
    
    print("Congrats, You've reached the end of the pipline. Your files are located in the Script_Ouput Folder")


pipeline()
