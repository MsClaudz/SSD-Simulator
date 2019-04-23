# SSD-Simulator

## Modules:

#### 1. DictBuilder
**Inputs:** trace file, sectors per block
**Outputs:** frequency dict

#### 2. Partitioning
**Inputs:** frequency dict, update frequency ratio
**Outputs:** number of partitions, partition assignments dict

#### 3. SizeSSD
**Inputs:** partition assignments dict, percent overprovisioning, erase block size, logical block size
**Outputs:** number of erase blocks per partition, max number of logical blocks per erase block, number of overprovisioned erase blocks per partition

#### 4. MakeSSD
**Inputs:** number of partitions, number of erase blocks per partition, partition assignments dict
**Outputs:** SSD

#### 5. SimulateIO
**Inputs:** trace file, partition assignments dict, max number of logical blocks per erase block, number of overprovisioned erase blocks per partition, SSD
**Outputs:** total writes by user, total garbage collection writes



#### Retrieving FIU trace files:

* Go to http://iotta.snia.org/traces/390
* Select "Download all subtraces via Unix shell script"
* You will receive a file called "download_all_subtraces_of_391.sh"
* Save the file to your computer
* Open a terminal window, navigate to the location of the file, then enter:
* sh download_all_subtraces_of_391.sh
