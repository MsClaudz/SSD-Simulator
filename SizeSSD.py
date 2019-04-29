# Inputs: 
# partition_dict
# logical_block_size_in_KB
# physical_page_size_in_KB
# pages_per_erase_block
# percent_of_overprovisioning
# num_partitions

# Outputs: 
# main_blocks_per_partition
# num_main_erase_blocks
# num_overprovisioned_erase_blocks

def count_logical_blocks(trace_dict):
    '''(dict of int:int, int) -> int

    Returns number of unique logical blocks from freq_dict or partition_dict.

    >>>count_logical_blocks({34:1, 35:2, 36:3})
    3
    '''
    return len(trace_dict)

   
def calculate_num_erase_blocks(num_logical_blocks, logical_block_size_in_KB, physical_page_size_in_KB, pages_per_erase_block, percent_of_overprovisioning):
    '''(int, int, int, int) -> (float, float)

    Takes a number of logical blocks, the number of flash pages per logical block, the number of flash pages per erase block, 
    and a desired percentage of overprovisioning, and returns the number of main and overprovisioned erase blocks required 
    to accommodate the data stored in the number of logical blocks. Returns a tuple with both values.
    
    >>>calculate_num_erase_blocks(32, 4.096, 0.512, 128, 28)
    (2.0, 0.56)

    >>>calculate_num_erase_blocks(300000, 4.096, 4.096, 128, 28)
    (2343.75, 656.2500000000001)
    '''
    physical_pages_per_logical_block = logical_block_size_in_KB/physical_page_size_in_KB
    num_main_erase_blocks = (num_logical_blocks * physical_pages_per_logical_block)/pages_per_erase_block
    num_overprovisioned_erase_blocks = num_main_erase_blocks * (percent_of_overprovisioning/100)
    return (num_main_erase_blocks, num_overprovisioned_erase_blocks)


def main_blocks_per_partition(num_main_erase_blocks, num_partitions):
    '''(float, int) -> int

    Returns the number of erase blocks to allocate to each SSD partition. Rounds up to nearest whole number.

    e.g.
    >>>blocks_per_partition(300.0, 3)
    100
    '''
    return int(-(-num_main_erase_blocks // num_partitions))