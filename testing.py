# Import modules
import DictBuilder
import Partitioning
import SizeSSD

# Choose sample file and set parameters
trace_file = 'traces\cheetah.cs.fiu.edu-110108-113008.1_sample.blkparse'
sectors_per_logical_block = 8

print("building dictionary")

# Create dictionary using DictBuilder
freq_dict = DictBuilder.build_dict(trace_file, sectors_per_logical_block)
# print(freq_dict.values())
# print(len(freq_dict))

# Or use sample dict
# freq_dict = {23:2, 24:2, 25:3, 26:5, 27:3, 28:6, 29:3, 30:9}
# print("frequency dictionary:", freq_dict)

print("\ngetting number of partitions")

# Get number of partitions from ratio
ratio = 3
num_partitions = Partitioning.num_partitions_from_ratio(freq_dict, ratio)
# print("Number of partitions:", partitions)
print("ratio:", ratio, "\nnumber of partitions:", num_partitions)

# Get ratio from number of partitions
# partitions = 3
# ratio = Partitioning.ratio_from_num_partitions(freq_dict, partitions)
# print("Update frequency ratio:", ratio)

print("\ngetting partition boundaries")

# define partition boundaries
partitions = Partitioning.define_partitions(freq_dict, ratio, num_partitions)
print("partition boundaries:", partitions)

print("\nassigning blocks to partitions")

# assign blocks to partitions
partition_dict = Partitioning.assign_to_partitions(freq_dict, ratio, partitions)
# print("assigned partitions:", partition_dict)
# print(partition_dict.values())

# get required number of logical blocks
num_logical_blocks = SizeSSD.count_logical_blocks(partition_dict, 28)
print("\nnumber of logical blocks required:", num_logical_blocks)

# get required number of erase blocks
num_erase_blocks = SizeSSD.count_erase_blocks(num_logical_blocks, 4096.0, 4.096)
print("\nnumber of erase blocks required:", num_erase_blocks)

print("done")