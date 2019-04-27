# SSD-Simulator

## Modules:

#### 1. DictBuilder
**Inputs:** trace file, logical block size in KB, logical sector size in KB
**Outputs:** frequency dict

#### 2. Partitioning
**Inputs:** frequency dict, update frequency ratio
**Outputs:** number of partitions, partition assignments dict

#### 3. SizeSSD
**Inputs:** partition assignments dict, percent overprovisioning, logical block size in KB, physical page size in KB, pages per erase block, number of partitions
**Outputs:** number of main erase blocks, number of overprovisioned erase blocks, number of main erase blocks per partition

#### 4. MakeSSD
**Inputs:** number of partitions, number of main erase blocks per partitions, number of overprovisioned erase blocks, static vs. dynamic allocation
**Outputs:** SSD 

#### 5. SimulateIO
**Inputs:** trace file, partition assignmnets dict, SSD, number of main erase blocks per partition, pages per erase block
**Outputs:** write amplification



#### Retrieving FIU trace files:

* Go to http://iotta.snia.org/traces/390
* Select "Download all subtraces via Unix shell script"
* You will receive a file called "download_all_subtraces_of_391.sh"
* Save the file to your computer
* Open a terminal window, navigate to the location of the file, then enter: sh download_all_subtraces_of_391.sh
