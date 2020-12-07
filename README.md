# Contact tracing simulation of different proximity detection ranges and usage stops for COVID-19
 
This repository contains the Python code for the spatial simulation of a research manuscript. The experiments were conducted within a Python 3.8.3 environment on a high performance computing cluster, running on a Unix operating systems and running with the Slurm Workload Manager. The execution of the code requires the following python libraries, which we installed via pip: numpy (version 1.18.5), scipy (version 1.5.0), intervaltree (version 3.0.2), matplotlib (version 3.2.2)

## Running the simulation on a high performance computing cluster

To run the simulation on a high performance computing cluster with the Slurm Workload Manager, you can specify the settings (i.e., cores per node, maximum run time of a job) in the files "run_1.py", "run_2.py", and "run_3.py". Afterward, create another folder in this directory entitled "baseInitial". Copy (do not cut) all of the files here into this folder.
You can then submit the initial simulation jobs with "run_1.py" from the parent folder. After these run, you can consolidate the simulation states and continue simulating non-finished simulations using the "run_2.py" - repeat this, until the simulations are all completed and stored in the "finishedSimulationStates" folder. Then, you can consolidate the final simulation states using the "run_3.py" file. The simulation part of the software may run several days.

## Running the simulation on a local computer

You can also run the simulations on your local computer instead of a high performance computing cluster. For performance reasons, however, you may have to adapt the settings. Specifically, you may want to increase the "simulationTimeStepInMillisecond" parameter in the "ConstantsAndRandom.py" file (e.g., to 1000 milliseconds). Furthermore, you may want to decrease the population size with the "Main_populationSize" parameter (e.g., to 2500), and accordingly, the number of supermarkets with the "Main_numberOfSupermarkets" parameter (e.g., to 1).

You can then adapt the number of cores in the "main_par_experiment.py" file, and then run this file to start the simulations. After all simulations are finished, you can run the run_3.py file to consolidate the simulation results.

## Plotting the results

After you run the simulations and consolidated the results, you can run the "print_figure2.py", "print_figure3.py", and "print_figure4.py" files to plot the results. "print_figure2.py" also generates a table of the results, stored in a .csv file.