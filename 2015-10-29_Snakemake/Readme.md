# Snakemake

**Köster, Johannes**, and Sven Rahmann. "Snakemake—a scalable bioinformatics workflow engine." *Bioinformatics* 28.19 (2012): 2520-2522.

- Similar to GNU Make, you specify targets in terms of a pseudo rule at the top.
- For each target and intermediate file, you create rules that define how they are created from from input files.
- Snakemake determines the rule dependencies by matching file names.
- Input and output files can contain multiple named wildcards.
- Rules can either use shell commands or plain Python code to create output files from input files. Further, Snakemake can interface with R to specify R code inside rules.
- Snakemake workflows can be executed on workstations and clusters without modification. The job scheduling can be constrained by arbitrary resources like e.g. available CPU cores, memory or GPUs.

## [Introduction/Tutorial](http://slides.com/johanneskoester/deck-1) from author himself ***<font color='orange'>worth seeing</font>***

## Installation

- From a working **Python 3** setup install it like any other Python package
```bash
pip3 install snakemake
```

<font color='green'>*Note: Demo in a virtual environment*</font>

### Recommendations

- Install [PyYAML](https://pypi.python.org/pypi/PyYAML/) for YAML config file support
```bash
pip3 install pyyaml
```

## Example workflow `foo` - save file as ***Snakefile***

> Change directory to `./foo` for premade **Snakefile**

```
rule foo:
    input: "input.txt"
    output: "output.txt"
    shell: "sort {input} > {output}"
```
### Execute from command line

```bash
❯ snakemake -p # -p for printing shell commands
```

```
Provided cores: 1
Rules claiming more threads will be scaled down.
Job counts:
  count jobs
  1 foo
  1
rule foo:
  input: input.txt
  output: output.txt
sort input.txt > output.txt
1 of 1 steps (100%) done
```

## Example Snakefile `simulate_reads`

> Change directory to `./bar` for premade **Snakefile**

```
samples = ['flee',
           'elba',
           'ljod',
           'exit',
           'joss',
           'raab',
           'tule',
           'irus',
           'deny',
           'gapy']

rule all:
  input: expand("{sample}_{pair}.fq", sample=samples, pair=['1','2'])

rule simulate_reads:
  output:
    "{sample}_1.fq",
    "{sample}_2.fq"
  params:
    executable = "$HOME/packages/art_bin_ChocolateCherryCake/art_illumina",
    name = "{sample}"
  shell:
    "{params.executable} -na -i genome.fa -p -l 125 -ss HS25 -f 20 -m 200 \
    -s 10 -sp -o {params.name}_"
```

### Execute from command line
```bash
❯ snakemake -n -p # -n corresponds to --dry-run, -p print shell commands
```
```
rule simulate_reads:
  output: gapy_1.fq, gapy_2.fq
$HOME/packages/art_bin_ChocolateCherryCake/art_illumina -na -i genome.fa -p -l 125 -ss HS25 -f 20 -m 200     -s 10 -sp -o gapy_
rule simulate_reads:
  output: flee_1.fq, flee_2.fq
$HOME/packages/art_bin_ChocolateCherryCake/art_illumina -na -i genome.fa -p -l 125 -ss HS25 -f 20 -m 200     -s 10 -sp -o flee_
rule simulate_reads:
  output: raab_1.fq, raab_2.fq
$HOME/packages/art_bin_ChocolateCherryCake/art_illumina -na -i genome.fa -p -l 125 -ss HS25 -f 20 -m 200     -s 10 -sp -o raab_
rule simulate_reads:
  output: exit_1.fq, exit_2.fq
$HOME/packages/art_bin_ChocolateCherryCake/art_illumina -na -i genome.fa -p -l 125 -ss HS25 -f 20 -m 200     -s 10 -sp -o exit_
rule simulate_reads:
  output: tule_1.fq, tule_2.fq
$HOME/packages/art_bin_ChocolateCherryCake/art_illumina -na -i genome.fa -p -l 125 -ss HS25 -f 20 -m 200     -s 10 -sp -o tule_
rule simulate_reads:
  output: joss_1.fq, joss_2.fq
$HOME/packages/art_bin_ChocolateCherryCake/art_illumina -na -i genome.fa -p -l 125 -ss HS25 -f 20 -m 200     -s 10 -sp -o joss_
rule simulate_reads:
  output: irus_1.fq, irus_2.fq
$HOME/packages/art_bin_ChocolateCherryCake/art_illumina -na -i genome.fa -p -l 125 -ss HS25 -f 20 -m 200     -s 10 -sp -o irus_
rule simulate_reads:
  output: deny_1.fq, deny_2.fq
$HOME/packages/art_bin_ChocolateCherryCake/art_illumina -na -i genome.fa -p -l 125 -ss HS25 -f 20 -m 200     -s 10 -sp -o deny_
rule simulate_reads:
  output: ljod_1.fq, ljod_2.fq
$HOME/packages/art_bin_ChocolateCherryCake/art_illumina -na -i genome.fa -p -l 125 -ss HS25 -f 20 -m 200     -s 10 -sp -o ljod_
rule simulate_reads:
  output: elba_1.fq, elba_2.fq
$HOME/packages/art_bin_ChocolateCherryCake/art_illumina -na -i genome.fa -p -l 125 -ss HS25 -f 20 -m 200     -s 10 -sp -o elba_
localrule all:
  input: flee_1.fq, elba_1.fq, ljod_1.fq, exit_1.fq, joss_1.fq, raab_1.fq, tule_1.fq, irus_1.fq, deny_1.fq, gapy_1.fq, flee_2.fq, elba_2.fq, ljod_2.fq, exit_2.fq, joss_2.fq, raab_2.fq, tule_2.fq, irus_2.fq, deny_2.fq, gapy_2.fq
Job counts:
  count jobs
  1 all
  10  simulate_reads
  11
```

> Change directory to `./fred` for premade **Snakefile**

## Build dags and make it easy to explain
```bash
❯ snakemake --configfile config.yaml build_genome generate_bams clean header merge --rulegraph | dot -Tpng > rules.png
```

```bash
❯ snakemake --configfile config.yaml build_genome generate_bams clean header merge --dag | dot -Tpng > dag.png
```

## Config files

- Support for `JSON` and `YAML` files
  - Should install [`pyyaml`](https://pypi.python.org/pypi/PyYAML) to make use of `YAML` files
- Make it more configurable, advanced and a bit user friendly
- Change parameters on the fly at execution time

### Provide config file as a parameter
```bash
❯ snakemake --configfile config.yaml
```

### Parse config file within the Snakefile before all the rules
```
configfile: "config.yaml"

```

### Example config file

```yaml
bowtie2_preset: "--very-sensitive"
bowtie2_index: "relative_large_genome"
merged_output: "combined.bam"
bamCoverage: "$HOME/.virtualenvs/py27/bin/bamCoverage"
samples:
- fedora
- debian
- arch
- opensuse
```

### Use of config variables in the rules
```
rule bam_coverage:
  input: "{sample}.bam"
  output: "{sample}.rpkm.bw"
  params: 
    executable = config["bamCoverage"]
  run:
    shell("{params.executable} --bam {input} --binSize 10 --normalizeUsingRPKM \
          -o {output}")
```

## Snakemake use on Grid Engines

- Haven't digged into this because using a server without a grid engine.

```bash
❯ snakemake --cluster qsub -j 32
```

- **Sorry, I haven't tested this and not going to cover this but it works as advertised (a lot of Snakefiles in conversations in the Snakemake google group use qsub very effectively)**
- **Works similarly as a regular snakemake but will submit every job using qsub**

### Cluster config files

- Useful for extra parameters and more detailed job control while submitting

```bash
❯ snakemake --cluster-config cluster_config.yaml
```

## Scripting in Snakefiles

- Your Snakefile is basically a python script, so you can run your python code natively

```
  run:
    # Write your python code
```

- Snakemake supports R scripting through [rpy2](https://pypi.python.org/pypi/rpy2)

```
from snakemake.utils import R

rule scripting:
  output: "{sample}.pdf"
  run:
    R("""
    # Write your R code
    suppressWarnings(library(ggplot2))

    xvar <- c(rnorm(1500, mean = -1), rnorm(1500, mean = 1.5))
    yvar <- c(rnorm(1500, mean = 1), rnorm(1500, mean = 1.5))
    zvar <- as.factor(c(rep(1, 1500), rep(2, 1500)))
    xy <- data.frame(xvar, yvar, zvar)

    plot = ggplot(xy, aes(x=xvar)) + geom_histogram(aes(y = ..density..),
      binwidth=0.1, color="black", fill=NA) + theme_bw()
    ggsave(plot, file="{output}", width=6, height=6)    
    """)

```

- Or, you can create your executable script and place it wherever you like and execute using `shell()`

```
  run:
    shell("Rscript /path/to/your/script.R")
```
