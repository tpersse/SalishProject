# Cancer detection by genomic analysis of cell-free DNA 

## Project Members: Sneha Challa<sup>1</sup>, Nora Kearns<sup>1</sup>, Thomas Persse<sup>1</sup>, Dr. Chris Raymond, PhD<sup>2</sup>


### Project Goal:
We sought to create a portable bioinformatic pipeline for performing variant calling on cell free DNA (cfDNA) collected from liquid biopsies, with an end goal of detecting recurrent cancer. Pipeline is designed to detect circulating tumor DNA (ctDNA) at frequencies of roughly 1 fragment per 1000 cfDNA fragments.

### Workflow: 
---
| ![workflow](images/SalishWkflw.jpg) |
|:--:|
| <b>Overall project workflow, from molecular biology to bioinformatic approach used. </b>|

cfDNA is extracted via liquid biopsy, then prepped via the addition of UMI (clone id + LINDA (sample id)), and targeted via 40nt probe sequences. Samples were then sequenced via Illumina paired-end short read sequencing (151x151nt). 

Our first bioinformatic step is quality assessment, during which reads with imperfect LINDA and/or probe sequences were eliminated (filter_2_csv.py), then adapters were trimmed. Remaining reads were then aligned to the ensembl reference human genome via **bwa mem**, then deduplicated and error corrected using an in house python script (Deduplicate/Dedup_ErrorCorrect.py). Coverage was determined by generating consensus cfDNA fragments from the reads, then determining the number of fragments per position within EGFR and TP53. Finally, variant calling was performed using **lofreq**.

### Required Inputs:
---
This pipeline requires the following inputs to run to completion:

1. All LINDA (effectively sample-id) and Probe sequences used in sample prep

2. Input fastq files (paired end, Illumina 151x151nt)

3. Reference Human Genome fasta file (via ensembl, used in alignments/coverage/etc.)
- link: http://ftp.ensembl.org/pub/release-105/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz


### Acknowledgements
 ---
A special thank you to everyone at Salish Bioscience and the University of Oregon Bioinformatics and Genomics Track for the opportunities, assistance, and guidance throughout this project.

This work benefited from access to the University of Oregon high performance computing cluster, Talapas.
