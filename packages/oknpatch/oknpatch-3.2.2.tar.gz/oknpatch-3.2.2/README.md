# OKNPATCH PYTHON PACKAGE LIBRARY MANUAL
## Description
This program will fix or rerun the web experiment related functions.

There are 3 types of oknpatch which are:
1.  **trial_data_lost** which is to fix the data lost of trial csv by referencing the gaze.csv.  
2.  **update** which is to rerun the given trial csv by the updater function of the oknserver.  
3.  **change_direction_and_rerun** which is to change direction of the trial csv and rerun the updater and okn detection.

## Installation requirements and guide
### Anaconda
To install this program, `Anaconda python distributing program` and `Anaconda Powershell Prompt` are needed.  
If you do not have `Anaconda`, please use the following links to download and install:  
Download link: https://www.anaconda.com/products/distribution  
Installation guide link: https://docs.anaconda.com/anaconda/install/  
### PIP install
To install `oknpatch`, you have to use `Anaconda Powershell Prompt`.  
After that, you can use the `oknpatch` from any command prompt.  
In `Anaconda Powershell Prompt`:
```
pip install oknpatch
```  
## Usage guide
### The usage will be depend on the type of oknpatch. 
There is a example folder under `development` folder.  
If you want to test this program, you can clone this repository, install `oknpatch` and run the following command:  
For **trial_data_lost** oknpatch type  
```
oknpatch -t trial_data_lost -i development/example/trial-2_disk-condition-1-1.csv -gi development/example/gaze.csv
```
For **update** oknpatch type  
```
oknpatch -t update -i development/example/trial-2_disk-condition-1-1.csv
```  
That will rerun the updater function of oknserver and produce `updated_trial-2_disk-condition-1-1.csv`.  
Since there is only input (-i) in the command line, it will use default `extra_string` which is "updated_" to give the output csv name and built-in config to update the given csv.  
If you want to give your custom `extra_string`, use (-es):  
If you want to use your own config to update, use (-uc):
```
oknpatch -t update -i development/example/trial-2_disk-condition-1-1.csv -es "(custom extra string)" -uc "(directory to your custom config)"
```
For **change_direction_and_rerun** oknpatch type  
```
oknpatch -t change_direction_and_rerun -i development/example/trial-2_disk-condition-1-1.csv -di 1 -okndl (okn_detector_location)
```
That will change the direction column value of the given csv and rerun the updater function of oknserver and produce `updated_trial-2_disk-condition-1-1.csv` and `result` folder which contains `signal.csv`.  
Since there is no input for custom extra string, config to update and config for okn detection in the command line, it will use default `extra_string` which is "updated_" to give the output csv name, built-in updater config and built-in okn detector config.  
If you want to give your custom `extra_string`, use (-es):  
If you want to use your own config to update, use (-uc):
If you want to use your own config for okn detection, use (-okndc):
```
oknpatch -t change_direction_and_rerun -i development/example/trial-2_disk-condition-1-1.csv -es "(custom extra string)" -uc "(directory to your custom config)" -okndc "(directory to your custom okn detector config)" -di 1 -okndl (okn_detector_location)
```
### To upgrade version  
In `Anaconda Powershell Prompt`,
```
pip install -U oknpatch
```
or
```
pip install --upgrade oknpatch
```
