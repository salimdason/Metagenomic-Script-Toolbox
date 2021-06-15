

#!/usr/bin/python
# -*- coding: <encoding name> -*-

#                                                 Script to automate metagenomic workflow
#                                                   Written by: Mohammed Salim Dason 
#                                                   Universita del Piemonte Orientale
#                                             dasonsalim@outlook.com // 20041232@studenti.uniupo.it





import argparse
import subprocess
import os



print("Before you begin, please make sure your forward and reverse reads are named forward.fq and reverse.fq respectively!\n Please wait while your files are being copied. The Assembly will begin shortly after it's done!")

parser = argparse.ArgumentParser(description="Metagenomic Script")

parser.add_argument('forward', metavar="forward_read", type=str, help="Please select your forward read")
parser.add_argument('reverse', metavar="reverse_read", type=str, help="Please select your reverse read")

args = parser.parse_args()

forward = args.forward
reverse = args.reverse


#                                          Creating Directory and copying read files which would be used later by bowtie2 for local alignment


os.mkdir("Script_Output")
subprocess.call("cp forward.fq reverse.fq ./Script_Output", shell=True)

def pipeline():
    #Running MetaSpades to assembly reads

    subprocess.call('metaspades.py -t 100 -m 30 -1 forward.fq -2 reverse.fq -o Script_Output', shell = True)
    os.chdir("Script_Output")

    #Once in output folder containing assemblies from previous step, reads <1000nt will be discarded using the seqtk tool

    subprocess.call("seqtk seq -L 1000 contigs.fasta > contigs.filtered.fasta", shell=True)

    #Once seqtk tool is done running, bowtie2 will now proceed

    subprocess.call("bowtie2-build --threads 30 contigs.filtered.fasta contigs.filtered.fasta", shell=True)

    #Bowtie 2 will now align reads locally, and output a sam files

    subprocess.call("bowtie2 --threads 60 --no-unal --very-sensitive-local -x contigs.filtered.fasta -1 forward.fq -2 reverse.fq -S aligned.contigs.sam", shell=True)

    #SAMTOOLS will convert sam file output into a bam file

    subprocess.call("samtools view -Sb aligned.contigs.sam > aligned.contigs.bam", shell=True)

    #Bam file will now be sorted by samtools

    subprocess.call("samtools sort aligned.contigs.bam > aligned.contigs.sorted.bam", shell=True)

    #Now we will get a contig depth summary

    subprocess.call("jgi_summarize_bam_contig_depths --outputDepth depth.txt aligned.sorted.bam", shell=True)

    #Metabat2 will now reconstruct genomes

    subprocess.call("metabat2 -m 1500 -i contigs.filtered.fasta -a depth.txt -o Reconstructed", shell=True)
    

    print("Congrats, You've reached the end of the pipline. Your files are located in the Script_Ouput Folder")


pipeline()
