# IMPORT MODULES
import DictBuilder
import Partitioning

# CHOOSE SAMPLE FILE AND SET PARAMETERS
trace_file = 'traces\cheetah.cs.fiu.edu-110108-113008.1_sample.blkparse'
sectors_per_block = 8

# TEST DICTBUILDER
freq_dict = DictBuilder.build_dict(trace_file, sectors_per_block)
# print(freq_dict)
# print(freq_dict.values())

# TEST PARTITIONING FROM RATIO
ratio = 3
partitions = Partitioning.partitions_from_ratio(freq_dict, ratio)
# print("Number of partitions:", partitions)

# TEST PARTITIONING FROM NUMBER OF PARTITIONS
# partitions = 3
# ratio = Partitioning.ratio_from_partitions(freq_dict, partitions)
# print("Update frequency ratio:", ratio)
