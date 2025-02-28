# Start and Stop Test
Here you can find a guide to reproduce the results shown in the paper *"Start&Stop - a PhysiCell and PhysiBoSS 2.0 add-on for interactive simulation control"*.
All code was developed and executed on a Linux Ubuntu 22.04.4 LTS (GNU/Linux 5.15.0-131-generic x86_64) operating system and using Python3.10.
In case of any issues reproducing the results or installing the dependencies, we provide a Singularity container and a tutorial on how to execute it.


## Installation Guide

### Clone the Repository
First, clone the `start-and-stop-test` repository in your home folder:

```bash
git clone https://github.com/smilies-polito/start-and-stop-test
cd start-and-stop-test
```

### Install Dependencies
Install all required dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```
#### Utility Test on the first use case

This utility test demonstrates a practical use of the Start & Stop add-on by allowing the interruption and resumption of a simulation of the TNF tumor with updated parameters to convert an unsuccessful treatment into a successful one in real-time.

To run the utility test, navigate to the test folder and execute the utility_test.py script, specifying the folder where you want the test output to be saved and an image, as shown in Figure 4 of the paper.
```bash
cd test
python utility_test.py /path/to/your/output/folder/
```

#### Quantitative Test on the first use case

This quantitative test is performed to ensure that the Start & Stop add-on does not introduce biases into the simulator. To run the quantitative test, follow the same steps as for the utility test, but execute the quantitative_test.py script instead.
```bash
cd test
python quantitative_test.py /path/to/your/output/folder/
```

#### Utility Test on the second use case

This utility test demonstrates a practical use of the Start & Stop add-on by allowing the interruption and resumption of a simulation of the cancer invasion use case with updated parameters to add a knockout factor inhibiting the epithelial to mesenchymal transition.

To run the utility test, navigate to the test folder and execute the utility_test_second.py script, specifying the folder where you want the test output to be saved and an image, as shown in the paper.
```bash
cd ../test
python utility_test_second.py /path/to/your/output/folder/
```

#### Quantitative Test on the second use case

This quantitative test is performed to ensure that the Start & Stop add-on does not introduce biases into the simulator. To run the quantitative test, follow the same steps as for the utility test, but execute the quantitative_test_second.py script instead.
```bash
cd ../test
python quantitative_test_second.py /path/to/your/output/folder/
```

### Computational Times comparison
To save an image comparing the different execution times of continuous simulations and simulations with multiple stops and restarts, navigate to the helpers/plots folder and execute the time_plot.py script. Provide both JSON files containing the outputs of the quantitative tests and specify the output folder as follows.
```bash
cd ../helpers/plots
python time_plot.py /path/to/your/quantitative_test.json /path/to/your/quantitative_test_second.json /path/to/your/output/folder/
```

## Container
As mentioned, in case of problems reproducing the results, here we provide a guide on how to run the experiments on a Singularity container, both interactively and by executing a runscript.

## Experimental setup

Follow these steps to setup for reproducing the experiments provided in the paper
1) Install `Singularity` from https://docs.sylabs.io/guides/3.0/user-guide/installation.html:
	* Install `Singularity` release 3.10.2, with `Go` version 1.18.4
	* Suggestion: follow instructions provided in _Download and install singularity from a release_ section after installing `Go`
	* Install dependencies from: https://docs.sylabs.io/guides/main/admin-guide/installation.html

2) Clone the start-and-stop-test repository in your home folder
```
git clone https://github.com/smilies-polito/start-and-stop-test
```

3) Move to the source subfolder, and build the start-and-stop-test Singularity container with 
```bash
cd start-and-stop-test/source
sudo singularity build start-and-stop-test.sif start-and-stop-test.def
```
or using fake root privileges
```bash
cd start-and-stop-test/source
singularity build --fakeroot start-and-stop-test.sif start-and-stop-test.def
```

## Reproducing the analysis interactively within the start-and-stop-test Singularity container

To run testing, manually launch the start-and-stop-test Singularity container. Move to the `source` folder, and launch the scripts as follows.

First of all, launch the start-and-stop-test Singularity container
```bash
cd start-and-stop-test/source
singularity shell start-and-stop-test.sif
```
This will run a shell within the container, and the following prompt should appear:
```bash
Singularity>
```

Now follow the steps below. 

#### Utility Test on the first use case

To run the utility test, navigate to the test folder and execute the utility_test.py script, specifying the folder where you want the test output to be saved and an image, as shown in Figure 4 of the paper.
```bash
Singularity> cd ../test
Singularity> python utility_test.py /path/to/your/output/folder/
```

#### Quantitative Test on the first use case

To run the quantitative test, follow the same steps as for the utility test, but execute the quantitative_test.py script instead.
```bash
Singularity> cd ../test
Singularity>python quantitative_test.py /path/to/your/output/folder/
```

#### Utility Test on the second use case

To run the utility test, navigate to the test folder and execute the utility_test_second.py script, specifying the folder where you want the test output to be saved and an image, as shown in the paper.
```bash
Singularity> cd ../test
Singularity> python utility_test_second.py /path/to/your/output/folder/
```

#### Quantitative Test on the second use case

To run the quantitative test, follow the same steps as for the utility test, but execute the quantitative_test_second.py script instead.
```bash
Singularity> cd ../test
Singularity>python quantitative_test_second.py /path/to/your/output/folder/
```

### Computational Times comparison
To save an image comparing the different execution times of continuous simulations and simulations with multiple stops and restarts, navigate to the helpers/plots folder and execute the time_plot.py script.
```bash
Singularity> cd ../helpers/plots
Singularity>python time_plot.py /path/to/your/quantitative_test.json /path/to/your/quantitative_test_second.json /path/to/your/output/folder/
```

## Reproducing the analysis running the start-and-stop-test Singularity container

To reproduce the analysis from this paper, run the Singularity container start-and-stop-test.sif, specifying the output folder where you want the images to be saved.

Move to the `source` folder and run the `start-and-stop-test.sif` file
```bash
cd start-and-stop-test/source
singularity run start-and-stop-test.sif /path/to/your/output/folder/
```
## Disclaimer

Although the images used in the paper were generated in this same way, they may slightly differ from those produced by running these commands due to the high degree of randomness inherent in the simulator.

