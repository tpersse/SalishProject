#!/bin/bash

#SBATCH -p bgmp

#SBATCH --cpus-per-task=8
#SBATCH --job-name=fastqc_filtered
#SBATCH -o %j.out
#SBATCH -e %j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --account=bgmp
#SBATCH --time=0-24:00:00

conda activate Salish 

#generate QC reports for unfiltered raw R1 and R2 files: 
fastqc -t 2 /projects/bgmp/shared/2021_projects/Salish/Project-35_S1_L001_R1_001.fastq /projects/bgmp/shared/2021_projects/Salish/Project-35_S1_L001_R2_001.fastq 

#generate QC reports for filtered R1 and R2 files: 
fastqc --outdir /projects/bgmp/shared/2021_projects/Salish/fastqc --format fastq --threads 4 /projects/bgmp/shared/2021_projects/Salish/fastqc/*Filtered.fastq

#generate QC reports for adapter trimmed(cutadapt) R1 and R2 files: 
fastqc --outdir /projects/bgmp/shared/2021_projects/Salish/fastqc --format fastq --threads 4 /projects/bgmp/shared/2021_projects/Salish/fastqc/output_cutadapt_R1.fastq
fastqc --outdir /projects/bgmp/shared/2021_projects/Salish/fastqc --format fastq --threads 4 /projects/bgmp/shared/2021_projects/Salish/fastqc/output_cutadapt_R2.fastq

#generate QC reports for adapter trimmed(bbduk) R1 and R2 files: 
bbduk.sh -Xmx1g in1=/projects/bgmp/shared/2021_projects/Salish/fastqc/Read1Filtered.fastq in2=/projects/bgmp/shared/2021_projects/Salish/fastqc/Read2Filtered.fastq out1=output_bbduk_R1.fq out2=output_bbduk_R2.fq ref=adapters.fa ktrim=r 