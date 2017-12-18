# More Snakemake

This session started with an intro to Snakemake, but this is better documented
elsewhere so I'll skip to the tips and suggestions, assuming you already know the
basics.

## 1) Order of rules

When starting to use Snakemake, one of the things that confuses newcomers is
that you are always working backwards. You start with the thing you want
to make and work back to discover the steps to make it.
For this reason, I always put the 'output' clause of my rules before the
'input' clause, just to remind myself that the output will be evaluated first
as Snakemake searches for rules to provide the requested output.

## 2) Merging patterns

Also when my workflow involves a merging step, I tend to use Python's standard
glob() and re.search() functions to discover what things I want to collect up and
merge. I do this in a clause outside any rules. For example, if my input files
are named like:

```
seqs1.fasta seqs2.fasta seqs3.fasta seqs4.fasta
```

I add these lines near the top of the Snakefile:

```
import re ; from glob import glob
all_sequences = [ re.search('\d+', f).group(0) for f in sorted(glob("seqs?.fasta")) ]
assert all_sequences, "Cannot work with no input sequences"

print("Input sequences: {:r}".format(all_sequences))
```

Snakemake provides a glob_wildcards() function but I find this troublesome. The above is long-winded
but precise. The sorted() bit is there for consistency (otherwise my merged FASTA files will be
in arbitrary order from run to run) and it's definitely worth adding the 'assert' because Snakemake
will happily try to merge zero files together but that is probably not what you want.

The print() statement reassures you that the inputs are as expected: ```['1', '2', '3', '4']```.

Now provide the input to your merging rule using the form ```expand("...", s=all_sequences)```.

## 3) Syntax hilighting

For Vim users, there is a Snakemake syntax hilighting package, but I find that Python syntax works
very well. Just add:

```# vim: ft=python```

Near the top of the file.

## 4) Always use -Trp

These flags add useful info to the Snakemake output (timestamp, reason, print commands) so use them.

## 5) Three-phase execution

This isn't really a tip, but it helps to understand that Snakemake executes your workflow in three phases.
In fact, if you don't appreciate this you'll struggle to go beyond the simplest workflows.

1. In the first phase, all the rules are collected and all the code outside of the rules (like the glob()
stuff above) is run.
1. In the second phase, Snakemake builds the DAG and any 'input' or 'params' which are functions or lambda
expressions are evaluated (with the appropriate wildcards each time).
1. In the third phase, the DAG is executed by choosing rules from the 'bag' for which all inputs are satisfied
and then running them. The execution engine can run up to J jobs at once, and these may be run locally or
as cluster jobs.

You should also know that when Snakemake runs a cluster job, the script it sends to the cluster
actually runs Snakemake on the cluster node. Therefore you need to have Snakemake installed in
a location where all nodes can run it. You also need to appreciate that any code you put outside
of your rules will be re-run, so if the code is slow, or if it takes up resouces, or if it produces
different results from one node to another, then you will be in trouble.

## 6) Running Snakemake on Eddie3.

### 6a) Installing it in your home.

```
$ module load python/3.4.3
$ pyvenv ./my_venv
$ source ./my_venv/bin/activate
$ pip3 install snakemake==3.13.3 drmaa
$ snakemake --version
```

Note that we're not using the latest version of Snakemake since this requires Python 3.5, but 3.13.3 is
perfectly good for most things.

### 6b) Using DRMAA.

The most reliable way to control cluster jobs is via the DRMAA mechanism. To make this work properly on
Eddie3, you need a custom job script and a wrapper script. The custom job script simpy uses 'bash -l'
instead of 'bash' as the executor. This subtle change loads your environment settings so jobs that
run on the worker nodes will see the same environment as things you test on the login node. I also
added a "sleep 2" which compensates for a maximum 2s clock skew between nodes (I'm not sure what
the max clock skew on Eddie is but this is generous and for most jobs the slowdown will be insignificant.)

You can add other initialisation here but be careful as it's easy to break things by messing with
this script.

```
$ cat >~/my_venv/snakemake/jobscript.sh <<'END'
#!/bin/bash -l

# properties = {properties}
sleep 2
{exec_job}
END
```

The wrapper script locates the DRMAA library and the job script. It also adds a more generous timeout to
deal with possible NFS latency on Eddie.

```
$ cat >~/bin/snakemake <<'END'
#!/bin/bash

export DRMAA_LIBRARY_PATH=/opt/sge/lib/linux-x64/libdrmaa.so

exec ~/my_venv/bin/snakemake \
    --jobscript ~/my_venv/snakemake/jobscript.sh \
    --latency-wait 200 "$@"
END
$ chmod +x ~/bin/snakemake
```

Note you still need to add the --drmaa flag when you run Snakemake, but with these settings that
is all you will need to do. You can of course add extra options if you wish.

### 6c) Avoid process timouts.

On the Eddie3 login nodes, long-running processes are killed. This is a problem for Snakemake
because you need the master process running to control the jobs. Some options are:

1. Run Snakemake as a job in itself. This works but is a little annoying.
1. Use the --immediate-submit mode to Snakemake. Unfortunately this seems to be broken
   in current versions of Snakemake, in general is not recommended.
1. Cheat, and disable to process limits...

```
prlimit --cpu=unlimited --pid $$
prlimit --cpu=unlimited --pid $PPID
```

This currently works, and your Snakemake process will run indefinitely on the login node (yay!),
but if people abuse this and leave sessions running on there the admins will notice and change
these into hard limits which cannot be bypassed (boo!). So only do this with caution. Option 1
is preferred.
