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


class Error(Exception):
    '''Base class for exceptions in this module.'''
    pass


class GarbageCollectionRequired(Error):
    '''Exception raised when an operation attempts to write to a partition
    that has no free space.'''
    pass


def free_pages(block_num, partition):
    '''(int, list of lists of int) -> list of lists of int

    Checks all erase blocks in a partition for block number. If it is found, 
    changes block number to a negative number. Returns the partition.

    e.g.
    >>> free_pages(12, [[10, 11, 12], [13, 14, 15]])
    [[10, 11, -12], [13, 14, 15]]
    '''
    for erase_block in partition:
        i = 0
        while i < len(erase_block):
            if erase_block[i] == block_num:
                erase_block[i] = -(block_num)
                return partition
            i += 1
    return partition


def garbage_collect(partition, pages_per_erase_block):
    '''(list of lists of int, int) -> (list of lists of int, int)

    Takes a partition. Writes all valid data from erase blocks into a new
    partition, counting the number of writes the occurred to move data from
    erase blocks containing invalid pages. Splits the new partition into correct
    number of erase blocks and returns a tuple of (new_partition, GC_writes)

    e.g.
    >>>garbage_collect([[-12, 15, -14], [-13, 12, 14], [22, 24, 25], [13]], 3)
    ([[22, 24, 25], [13, 15, 12], [14], []], 3)
    '''
    GC_writes = 0

    # Create temporary list
    temp = []

    # Write full blocks with no invalid pages to temp, do not increment GC_writes
    for erase_block in partition:
        if all(i > 0 for i in erase_block) and len(erase_block) == pages_per_erase_block:
            for page in erase_block:
                temp.append(page)
    
    # Write partial blocks with no invalid pages to temp, do not increment GC_writes
        if all(i > 0 for i in erase_block) and len(erase_block) < pages_per_erase_block:
            for page in erase_block:
                temp.append(page)

    # Write blocks with one or more invalid pages to temp, increment GC_writes
    for erase_block in partition:
        if not all(i > 0 for i in erase_block):
            for page in erase_block:
                if page > 0:
                    temp.append(page)
                    GC_writes += 1

    # Create a new_partition variable
    new_partition = []

    # Split temp into erase block-sized chunks and store them in new_partition
    for i in range(0, len(temp), pages_per_erase_block):
        new_partition.append(temp[i:i+pages_per_erase_block])

    # Add empty erase blocks to new partition to bring it up to original size
    i = len(partition)
    while len(new_partition) < i:
        new_partition.append([])

    # return (new_partition, GC_writes)
    return (new_partition, GC_writes)


def locate_space(partition, pages_per_erase_block, main_blocks_per_partition, is_static):
    '''(list of lists of int, int, int, bool) -> (int, int)

    Given a partition, searches for empty space. If it's found, returns the 
    index numbers of the erase block and the page where data can be written. 
    Returns a tuple of (erase_block_index, page_index). If there is no space, 
    raises GarbageCollectionRequired exception.

    e.g.
    >>> locate_space([[22, 24, 25], [13, 15, 12], [14], []], 3, 3, True)
    (2, 1)

    >>> locate_space([[22, 24, 25], [13, 15, 12], [14, 17, 18], []], 3, 3, True)
    __main__.GarbageCollectionRequired

    >>> locate_space([[22, 24, 25], [13, 15, 12], []], 3, 3, False)
    (2, 0)

    >>> locate_space([[22, 24, 25], [13, 15, 12], [14, 17, 18]], 3, 3, False)
    __main__.GarbageCollectionRequired
    '''
    if is_static:
        print('is static')
    # Check each erase block to see that it's not an overprovisioned block
        for erase_block_index in range(len(partition)):
            if erase_block_index >= main_blocks_per_partition:
                print('is overprovisioned')
    # If you've reached an overprovisioned block, require garbage collection
                raise GarbageCollectionRequired
    # If not overprovisioned, check if block has an empty page
            elif len(partition[erase_block_index]) < pages_per_erase_block:
                print('is main')
    # If it does, return indexes of block and empty page
                return (erase_block_index, len(partition[erase_block_index]))

    if not is_static:
        print('is not static')
    # Check each erase block for empty pages and if found, return indexes
        for erase_block_index in range(len(partition)):
            if len(partition[erase_block_index]) < pages_per_erase_block:
                return (erase_block_index, len(partition[erase_block_index]))
    # Otherwise, if no empty space, require garbage collection
        raise GarbageCollectionRequired


def write_to_partition(blocks, partition_dict, SSD, pages_per_erase_block, main_blocks_per_partition, is_static):
    '''(list, dict of int:int, list of list of list, int, int, bool) -> (int, int)

    Writes a list of block numbers to the simulated SSD. 
    Returns number of user writes and number of garbage collection writes that occurred.

    '''
    user_writes = 0
    GC_writes = 0

    # For one logical block at a time, get number of assigned partitions from partition_dict
    for block_num in blocks:
        partition_num = partition_dict[block]

    # Free up page(s) where that block is already written in that partition
        free_pages(block_num, SSD[partition_num])

    # Attempt to locate space in the partition. If there is no space, garbage collect and increment writes, then locate space again
        try:
            erase_block_index, page_index = locate_space(SSD[partition_num], pages_per_erase_block, main_blocks_per_partition, is_static)
        except GarbageCollectionRequired:
            SSD[partition_num], new_writes = collect_garbage(SSD[partition_num], pages_per_erase_block)
            GC_writes += new_writes
            erase_block_index, page_index = locate_space(SSD[partition_num], pages_per_erase_block, main_blocks_per_partition, is_static)
    
    # Write block to empty space
        SSD[partition_num][erase_block_index][page_index] = block_num
        user_writes += 1

    return (user_writes, GC_writes)


def Run_IO(trace_file, logical_block_size_in_KB, logical_sector_size_in_KB, partition_dict, SSD, pages_per_erase_block, main_blocks_per_partition, is_static):
    '''(file, int, int, dict of int:int, list of lists, int, int, bool) -> float

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