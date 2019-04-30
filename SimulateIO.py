# Inputs:
    # trace_file
    # partition_dict 
    # SSD
    # main_blocks_per_partition
    # pages_per_erase_block
    # logical_block_size_in_KB
    # logical_sector_size_in_KB
    # physical_page_size_in_KB
    # is_static

# Outputs:
    # write_amplification

import DictBuilder

# Note
# Current module is only built for cases where logical_block_size_in_KB == physical_page_size_in_KB
    # If logical_block_size_in_KB > physical_page_size_in_KB, the module will not deal with it correctly.
    # If logical_block_size_in_KB < physical_page_size_in_KB, the page size is irrelevant. SizeSSD assigns each logical block a full page.


# Have not yet built in any functionality for static vs. dynamic allocation of erase blocks. Leave that until the end?


def free_pages(block_num, partition):
    '''(int, list of lists of int) -> list of lists of int

    Checks all erase blocks in a partition for block number. If it is found, changes block number to a negative number.
    Returns the partition.

    e.g.
    >>> free_pages(12, [[10, 11, 12], [13, 14, 15]])
    [[10, 11, -12], [13, 14, 15]]
    '''
    # finish this

    return partition


def garbage_collect(partition, pages_per_erase_block):
    '''(list of lists of int, int) -> (list of lists of int, int)

    Takes a partition. Performs garbage collection on partition and returns the new partition, along with the number of writes 
    that occurred to complete the garbage collection. Returns a tuple of (partition, GC_writes)

    e.g.
    >>>garbage_collect([[-12, 13, -14], [15, 12, 14], [13]], 3)
    [[15, 12, 14], [13], []]
    '''
    # finish this
    # should we have the lists filled with zeroes instead of empty space?

    GC_writes = 0
    # For each sublist (i.e. erase block) in the partition:
        # Rewrite all positive block numbers to new erase blocks, counting every write, then empty the old blocks
        # Sort so empty lists are at the end of the partition
    return (partition, GC_writes)


def locate_space(partition, pages_per_erase_block, main_blocks_per_partition):
    '''(list of lists of int, int, int) -> (int, int)

    Given a partition, searches for empty space. If it's found, returns the index numbers of the erase block and the page where data 
    can be written. Returns a tuple of (erase_block_index, page_index). If there is no space, raises GarbageCollectionRequired exception.

    '''
    # finish this

    # if there is space:
        # return the space in a tuple, like this: (erase_block_index, page_index)
    else:
        raise Exception('Garbage collection required')

    # Notes
    # Check partition from beginning, sublist-by-sublist, until one sublist is not full. A sublist is full if length of sublist >= pages_per_erase_block
        # When you find a sublist that is not full:
            # If index of empty sublist > main_blocks_per_partition, garbage collect -- you have reached the overprovisioned blocks
            # Otherwise, return indexes of block and empty page


def write_to_partition(blocks, partition_dict, SSD, pages_per_erase_block, main_blocks_per_partition):
    '''(list, dict of int:int, list of list of list, int, int) -> (int, int)

    Writes a list of block numbers to the simulated SSD. 
    Returns number of user writes and number of garbage collection writes that occurred.

    '''
    user_writes = 0
    GC_writes = 0

    # For one logical block at a time, get number of assigned partition from partition_dict
    for block_num in blocks:
        partition_num = partition_dict[block]

    # Free up page(s) where that block is already written in that partition
        free_pages(block_num, SSD[partition_num])

    # Attempt to locate space in the partition. If there is no space, garbage collect and increment writes, then locate space again
        try:
            erase_block_index, page_index = locate_space(SSD[partition_num], pages_per_erase_block, main_blocks_per_partition)
        except: # try to make this specific to the 'Garbage collection required' exception, or do this part without try and except
            SSD[partition_num], new_writes = collect_garbage(SSD[partition_num], pages_per_erase_block)
            GC_writes += new_writes
            erase_block_index, page_index = locate_space(SSD[partition_num], pages_per_erase_block, main_blocks_per_partition)
    
    # Write block to empty space
        SSD[partition_num][erase_block_index][page_index] = block_num
        user_writes += 1

    return (user_writes, GC_writes)


def Run_IO(trace_file, logical_block_size_in_KB, logical_sector_size_in_KB, partition_dict, SSD, pages_per_erase_block, main_blocks_per_partition):
    '''(file, int, int, dict of int:int, list of lists, int, int) -> float

    Reads events from a file of trace data, runs them through the simulated SSD, and tracks writes to compute write amplification.


    '''
    trace_data = open(trace_file, 'r')
    total_user_writes = 0
    total_GC_writes = 0
    
    # Read events from the trace file and put in a list one-by-one
    for event in trace_data:
        event = event.split()
    
    # For each event, use filter_event to check if it's a valid, complete write event and if so, get blocks
    # Then write blocks to partition and increment user_writes and GC_writes variables with return values
        if DictBuilder.filter_event(event) == False:
            continue
        else:
            blocks = DictBuilder.get_blocks(event, logical_block_size_in_KB, logical_sector_size_in_KB)
            user_writes, GC_writes = write_to_partition(blocks, partition_dict, SSD, pages_per_erase_block, main_blocks_per_partition) # ADD OTHER PARAMETERS
            total_user_writes += user_writes
            total_GC_writes += GC_writes
            continue
        
    # Close file, compute write amplification, and return write amplification
    trace_data.close()
    write_amplification = (total_user_writes + total_GC_writes)/total_user_writes
    return write_amplification