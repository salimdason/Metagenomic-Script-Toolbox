# Metagenomic-Script-Toolbox
A collection of scripts for metagenomic analysis


Pipeline_Script.py assumes you already have the following installed:
1.metaspades, 2.bowtie2, 3.seqtk, 4.samtools, 5.jgi_summarize_bam_contig_depths, 6.metabat 2, already insatlled and added to your path variable. 


PIPELINE SCRIPT USAGE

Make sure the only files present in the directory are your paired-end reads, and the script.

This version of the script searches the directory for paired-end fastq files. It automatically copies and renames the files to "reverse.fq" and "forward.fq".

The files are then copied to a folder named "Output" and parsed into the script.


To run:

1. Place script in directory containing fastq files (Paired end)
2. Open terminal in direcory and run: Python Pipeline_Script_v2.0.py
