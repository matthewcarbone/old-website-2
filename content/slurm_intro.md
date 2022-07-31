Title: An introduction to SLURM
Date: 2022-07-25 23:20
Modified: 2022-07-25 23:20
Category: High-performance computing
Tags: hpc, slurm
Slug: an-introduction-to-slurm
Authors: Matthew R. Carbone
Summary: SLURM is complicated, so lets start from the beginning
Status: published

In computational science, we must often utilize high-performance computing (HPC) resources in order to do our work, as the necessary scope of the computations far exceeds what is available on a single workstation (e.g., your laptop). This can be due to at least one of the following reasons:

- Lack of computational power, i.e. we need more CPU's or GPU's.

- Lack of memory, i.e. we need more RAM.

- Runtime is long, i.e. we don't want to leave our workstations on overnight.
Many jobs need to be run, but you don't want to run hundreds of jobs in series on your workstation. Instead, you want to run them in parallel.

HPC resources rely on job schedulers, which provide a way of allowing users to submit jobs to specialized compute nodes, while also using sophisticated algorithms to control which users get which resources and when.  SLURM is one of these schedulers.

# Overview

I believe there is a dearth of content intended for extreme beginners using job controllers on HPC platforms, and for better or worse, the official documentation is quite dense. What I do know for sure is that some years ago when I was a new graduate student, I would have found a barebones-simple introduction to the topic useful. Students just entering the world of HPC will probably get the most out of this, but everyone can use a refresher!

If all goes well, this will be part of a series of posts. The general plan is:

1. A brief, simplest possible introduction, covering basic HPC jargon, output/error streams, partitions, time limits and basic job submission. **[You are here]**

2. A slightly more advanced introduction, covering CPUs, memory allocation, and some other SLURM flags.

3. Practical Message Passing Interface (MPI) usage and processes.

# Some HPC jargon

Before continuing, it is important to get some jargon out of the way. I will try to avoid using any jargon not common to your average Stack Overflow post. Anything not "common knowledge" will be described here!

## Nodes/machines and memory (and HPC platforms)
An HPC platform is not like your laptop, which is a single machine. An HPC platform consists of many machines. A "machine" in this context is a self-contained "computer" in which each central processing unit (CPU or core) shares the same memory (known often as RAM). For example, my current laptop has 6 physical cores and 32 GB of RAM. When running computations on my laptop, each core can access that RAM. However, unless I do something quite complicated, my laptop's cores cannot access, say, my Desktop's, as that computer is a separate machine.

Similarly, in the HPC world, a machine is known as a node. While it is the case that in the real world nodes are much more complicated than I will explain here, the two most important puzzle pieces for the average user are cores and memory. Each node has some number of CPU cores and some amount of memory (RAM). For example, on the [Cori Haswell supercomputer](https://docs.nersc.gov/systems/cori/), there are a total of 2,388 nodes. Each (standard) node has 32 cores, and each node has 128 GB of memory, shared between those 32 cores. Nodes can indeed be connected during computations to allow for even more computational power, but that is a discussion for another time!

To be absolutely clear, memory is not the same as what's on your hard drive. Memory is used temporarily and then discarded after your program finishes. On an HPC platform, your "hard drive" is usually a chunk of some login node.


## "The queue"

I will be referring to "the queue" a lot in the future, and it's something you will be checking quite often if you run jobs on an HPC platform. Without specifying to SLURM, the queue (job queue) is a list of currently running [on compute nodes] and pending jobs. Users can use the queue to check the status of their own and other peoples' jobs.


# What is SLURM?

The [Simple Linux Utility for Resource Management](https://slurm.schedmd.com/quickstart.html), or SLURM for short, is a common resource scheduling software that is used everywhere in the HPC world, from research group-owned clusters of a hand full of nodes, to massive supercomputers. Long story short, from cluster login nodes, it allows users to request certain resources for certain time periods, in order to run their code.

Contrary to it's name, SLURM is not necessarily... simple. Like Git, it takes quite a bit of time to get down the basics, and it is near impossible to master it to 100% of it's functionality. Nevertheless, for most, the basics are sufficient. In what follows, we will touch on a small percent of those basics.

# SLURM "hello world"
Let's go over a minimal example first. Here, your submit script might be entitled `hello_world.sbatch`,

```bash
#!bin/bash
#SBATCH -o path/to/my_output_stream.out
#SBATCH -e path/to/my_error_stream.err
#SBATCH -p my_partition_name
#SBATCH -t 00:30:00

python3 hello_world.py
```

where `hello_world.py` is

```python
#!/usr/bin/env python3

if __name__ == '__main__':
    print("hello world")
```

A quick note: the `.sbatch` "extension" is not necessary. You could just as well called the script `hello_world.sh`, since essentially it is just a shell script. I simply use the `.sbatch` suffix to indicate that the shell script is also a SLURM submission script.

Another quick note: if you're wondering what the following are:
* `#!bin/bash` & `#!/usr/bin/env python3` are "shebangs." See e.g. [here](https://stackoverflow.com/questions/6908143/should-i-put-shebang-in-python-scripts-and-what-form-should-it-take).
* `if __name__ == '__main__':` is good practice in Python coding when writing scripts (programs you execute from the command line or in this case, a SLURM job). See e.g. [here](https://medium.com/python-features/understanding-if-name-main-in-python-a37a3d4ab0c3).

Let's go over what each component of this job will do if you were to submit this to some HPC cluster. It is worth noting that you can run any SLURM script like a bash script, e.g., `bash hello_world.sbatch`, and it would ignore any lines starting with `#`. However, when submitting to the job controller using `sbatch`, e.g., `sbatch hello_world.sbatch`, it (SLURM) will look for any lines starting with `#SBATCH` and use those flags to specify a variety of parameters for the job.

## Output and error streams
When you run e.g. a Python script, there are streams of output that your computer will handle: the output and error streams.

The usual stuff, like calling `print` in Python, or `std::cout` in C++, will pipe to the output stream. Usually, this is your console, but in the HPC world, your job is being run on a compute node. Unless you were to try something fancy, which you probably shouldn't, there is no console output to view. Instead, the output stream is piped to an output file, which is specified by `#SBATCH -o`. In the example provided, your output stream will be piped instead to `path/to/my_output_stream.out`.

Anything representing a problem (or possible problem) with the execution of your code, e.g. warnings or errors, will be piped to the error stream. Usually, this is also your console, but for the same reasons as the output stream, we will not have a console. So, your warnings and errors (such as those thrown by the [Python warnings module](https://docs.python.org/3/library/warnings.html)) will be piped instead to `path/to/my_error_stream.err`. If it wasn't clear, this is specified by the `#SBATCH -e` flag.

Keep in mind, piping to output or error streams writes to storage (your user directory) in the same way saving a file does. This is usually a relatively slow operation, so as general good practice, you'll want to do this as little as possible. Logging some progress information is fine, but for example, saving massive files (e.g. full machine learning models at every epoch) could slow down your code significantly.

## Partitions
Often, the administrators of HPC platforms will "partition" (zing) available nodes into different groups which serve different purposes. These are called partitions and are best explained through example. Here are a few kinds of partitions I have run into in my time using many HPC platforms.

* `debug`: This is probably the most ubiquitous type of partition (i.e., basically every HPC platform has one). It is usually only a few nodes (on small platforms, it can be as few as 2), and is reserved for (you guessed it!) debugging your code. The most commonly shared property of nodes in a debugging partition is a short time limit. In other words, you can only use the resources continuously for a short amount of time, usually about 30 minutes. This ensures high-throughput, so lots of users can use the resources to quickly debug their code without having to wait in the queue very long.

* `standard` or `long`: This is the main subset of the platform, consisting of nodes used for "long" jobs, usually 24-48 hours. There are generally no special shared properties of these types of nodes, and users can usually request many at once, sometimes 20 (on e.g. medium-sized clusters), sometimes thousands (e.g. on the [Cori Knight's Landing supercomputer](https://docs.nersc.gov/systems/cori/knl_modes/))! Generally, the more resources you request, the longer it will take for your job to start running.

* "Big memory": Big memory nodes are just what you expect. Instead of the standard nodes that have 128–256 GB of memory, these nodes can have a few TB of memory. There are usually very few of these, if any, and they should only be used for jobs that require that much memory.

* Project-specific: Sometimes, researchers can "buy" entire chunks of a supercomputer for specific projects tied to specific grants. Likely, these are not anything you need to worry about, but if you see a partition like covid19_drug_design or something like that, it could be a part of the platform that has been allocated for a specific purpose for use by specific researchers.

Continuing with the intuitive labeling, partitions are specified by `#SBATCH -p`. Also, keep in mind the above names are just examples, and will be different depending on the cluster you're using.

## Time limits

Time limits are self-explanatory on face, but come with a subtlety. The more time you request, e.g. `#SBATCH -t 01:00:00` (one day) the longer it will take your job to start running, since SLURM and other job controllers prioritize filling "gaps" in the queue with shorter jobs. The less time you request, e.g. `#SBATCH -t 00:01:00` (one hour), the more likely it is your job will start quickly, but if your time limit runs out before your job is complete, your job will be terminated, forcing you to restore from checkpoint (if you have that functionality) or worse, restarting completely. Thus, balancing the time you request with the time you actually _need_ is quite important, especially on some of the larger clusters such as Cori, where a job can stay in the queue for weeks depending on the resources and time requested.


# Submitting jobs

So now that you have your `hello_world.py` file and SLURM submission script ready to go, you're able to submit to the SLURM job controller. This is done by running

> `sbatch submit.sbatch`

from your terminal on the HPC platform login node (where you connect to when you `ssh` into the platform). It's that simple! You will also likely see some feedback on your terminal, something akin to
> `Submitted batch job ######`

where the number is the _job ID_ of the job.

## Checking the status of submitted jobs

It may seem surprising the first time you submit a job, but other than the output described above, it will seem that nothing has happened! If everything was done properly, you are still on the login node, where you started, and your job is running on a compute node. There are a few things you can do to check that everything is running properly.

Check the status of your `.out` and `.err` files via, for example, `cat path/to/my_output_stream.out` or `cat path/to/my_error_stream.err`. Note: the frequency at which these files updates depends on how often your code flushes the output/error stream buffers (see e.g. [here](https://stackoverflow.com/questions/230751/how-can-i-flush-the-output-of-the-print-function)).

Check the queue. You can actually see all users running jobs, including you! For example, to check everyone's jobs, simply use squeue. To check only your jobs, you can use `squeue -u <you_username>`.

# Conclusion

SLURM has a steep learning curve. It can be difficult at first to figure out precisely what's going on under the hood, and how to setup jobs to run efficiently. In the first part of this guide, I hope you've come away with a better understanding of the basics of what SLURM is, how it works (to a limited extent) and how to setup your first `hello_world.sbatch` script. In the posts to come, I will present more complex topics that build on the concepts presented here, such as specifying CPU and GPU resources, and parallel computing, such as using MPI.

