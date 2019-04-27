# Import modules
import DictBuilder
import Partitioning
import SizeSSD

# Choose sample file and set parameters
trace_file = 'traces\cheetah.cs.fiu.edu-110108-113008.1_sample.blkparse'
logical_block_size_in_KB = 4.096
page_size_in_KB = 0.512
pages_per_erase_block = 128 # i.e. physical block size
update_frequency_ratio = 2
percent_of_overprovisioning = 28

# Calculate pages_per_logical_block
print("\ncalculating pages per logical block...")
pages_per_logical_block = int(logical_block_size_in_KB/page_size_in_KB)
print("pages per logical block:", pages_per_logical_block)

# Create dictionary using DictBuilder
print("\nbuilding dictionary...")
freq_dict = DictBuilder.build_dict(trace_file, pages_per_logical_block)
print("dictionary built")

# Get number of partitions from update frequency ratio
print("\ngetting number of partitions...")
num_partitions = Partitioning.num_partitions_from_ratio(freq_dict, update_frequency_ratio)
# print("Number of partitions:", partitions)
print("required number of partitions:", num_partitions)

# Get ratio from number of partitions
# partitions = 3
# ratio = Partitioning.ratio_from_num_partitions(freq_dict, partitions)
# print("Update frequency ratio:", ratio)

# define partition boundaries
print("\ngetting partition boundaries...")
partitions = Partitioning.define_partitions(freq_dict, update_frequency_ratio, num_partitions)
print("partition boundaries:", partitions)

# assign blocks to partitions
print("\nassigning blocks to partitions...")
partition_dict = Partitioning.assign_to_partitions(freq_dict, update_frequency_ratio, partitions)
print("partitions assigned to logical block numbers")

# get required number of erase blocks
print("\ncalculating required number of main and overprovisioned erase blocks...")
num_logical_blocks = SizeSSD.count_logical_blocks(partition_dict)
num_main_erase_blocks, num_overprovisioned_erase_blocks = SizeSSD.calculate_num_erase_blocks(num_logical_blocks, pages_per_logical_block, pages_per_erase_block, percent_of_overprovisioning)
main_blocks_per_partition = SizeSSD.main_blocks_per_partition(num_main_erase_blocks, num_partitions)
print("total number of main erase blocks required:", num_main_erase_blocks)
print("number of main erase blocks required per partition:", main_blocks_per_partition)
print("total number of overprovisioned erase blocks required:", num_overprovisioned_erase_blocks)

print("\ndone")