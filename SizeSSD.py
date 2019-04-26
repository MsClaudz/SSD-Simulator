# Inputs: 
# partition assignments dict
# percent overprovisioning
# erase block size (i.e. pages per erase block)
# pages per logical block
# num_partitions

# Outputs: 
# main_blocks_per_partition
# num_overprovisioned_erase_blocks

def count_logical_blocks(trace_dict):
    '''(dict of int:int, int) -> int

    Returns number of unique logical blocks from freq_dict or partition_dict.

    >>>count_logical_blocks({34:1, 35:2, 36:3})
    3
    '''
    return len(trace_dict)

   
def calculate_num_erase_blocks(num_logical_blocks, pages_per_logical_block, pages_per_erase_block, pct_overprov):
    '''(int, int, int, int) -> int

    Takes a number of logical blocks, the number of flash pages per logical block, the number of flash pages per erase block, 
    and a desired percentage of overprovisioning, and returns the number of main and overprovisioned erase blocks required 
    to accommodate the data stored in the number of logical blocks. Returns a tuple with both values rounded to whole numbers.
    
    >>>calculate_num_erase_blocks(16, 8, 128, 28)
    (1, 1)

    >>>calculate_num_erase_blocks(300000, 8, 128, 28)
    (18750, 5250)
    '''
    num_main_erase_blocks = round((num_logical_blocks * pages_per_logical_block)/pages_per_erase_block)
    num_overprovisioned_erase_blocks = round(num_main_erase_blocks * (pct_overprov/100))
    return (num_main_erase_blocks, num_overprovisioned_erase_blocks)


def main_blocks_per_partition(num_main_erase_blocks, num_partitions):
    '''(int, int) -> int

    Returns the number of erase blocks to allocate to each SSD partition.

    e.g.
    >>>blocks_per_partition(300, 3)
    100
    '''
    return int(num_main_erase_blocks/num_partitions)