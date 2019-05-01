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

    # Is there a way to group the parameters so we don't have so many?

# Outputs:
    # write_amplification


# Note: current module is only built for cases where logical block size 
# equals physical page size.

# If logical_block_size_in_KB > physical_page_size_in_KB, 
# the module will not deal with it correctly.

# If logical_block_size_in_KB < physical_page_size_in_KB, 
# the page size is irrelevant. SizeSSD assigns each logical block 1 full page.


import DictBuilder

class Error(Exception):
    '''Base class for exceptions in this module.'''
    pass

class GarbageCollectionRequired(Error):
    '''Exception raised when an operation attempts to write to a partition
    that has no free space.'''
    pass

class PartitionCompletelyFull(Error):
    '''Exception raised when an operation attempts to write to a partition
    that has no free space, and cannot make space with garbage collection.'''
    pass

def free_pages(block_num, partition):
    '''(int, list of lists of int) -> list of lists of int

    Checks all erase blocks in a partition for block number. If it is found, 
    changes block number to a negative number. Returns the partition.

    e.g.
    >>> free_pages(12, [[10, 11, 12], [13, 14, 15]])
    [[10, 11, -12], [13, 14, 15]]
    '''
    overwrite = 0
    for erase_block in partition:
        try:
            index = erase_block.index(block_num)
            erase_block[index]= -(block_num)
            overwrite += 1
            return (partition, overwrite)
        except ValueError:
            continue

    return (partition, overwrite)


def garbage_collect(partition, pages_per_erase_block):
    '''(list of lists of int, int) -> (list of lists of int, int)

    Takes a partition. Writes all valid data from erase blocks into a new
    partition, counting the number of writes the occurred to move data from
    erase blocks containing invalid pages. Splits new partition into correct
    number of erase blocks and returns a tuple of (new_partition, GC_writes)

    e.g.
    >>>garbage_collect([[-12, 15, -14], [-13, 12, 14], [22, 24, 25], [13]], 3)
    ([[22, 24, 25], [13, 15, 12], [14], []], 3)
    '''
    GC_writes = 0

    # Create temporary list
    temp = []

    for erase_block in partition:
        # Write full blocks with no invalid pages to temp
        # And Write partial blocks with no invalid pages to temp
        # Do not increment GC_writes
        if all(i > 0 for i in erase_block) and \
        len(erase_block) <= pages_per_erase_block:
            temp.extend(erase_block)

        # Write blocks with one or more invalid pages to temp
        # Increment GC_writes
        #if not all(i > 0 for i in erase_block):
        else:
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


def locate_space(partition, pages_per_erase_block):
    '''(list of lists of int, int) -> (int)

    Given a partition, searches for empty space. If it's found, returns the 
    index numbers of the erase block where data can be appended. If there is
    no space, raises GarbageCollectionRequired exception.

    e.g.
    >>> locate_space([[22, 24, 25], [13, 15, 12], [14], []], 3)
    2

    >>> locate_space([[22, 24, 25], [13, 15, 12], [14, 17, 18], [19, 20, 21]], 3)
    __main__.GarbageCollectionRequired
    '''
    # Check each erase block for empty pages and if found, return block index
    for erase_block_index in range(len(partition)):
        if len(partition[erase_block_index]) < pages_per_erase_block:
                return erase_block_index
    # Otherwise, if no empty space, require garbage collection
    raise GarbageCollectionRequired
    

def write_to_partition(blocks, partition_dict, SSD, pages_per_erase_block, 
main_blocks_per_partition, is_static):
    '''(list, dict of int:int, list of list of list, int, int, bool) -> 
    (int, int)

    Writes a list of block numbers to the simulated SSD. Returns number of user 
    writes and number of garbage collection writes that occurred.
    '''
    user_writes = 0
    GC_writes = 0
    overwrites = 0

    # For one block at a time, get assigned partition from partition_dict
    for block in blocks:
        partition_index = partition_dict[block]
        # print('\nblock =', block)
        # print('partition index =', partition_index)

    # Free up page(s) where that block is already written in that partition
        SSD[partition_index], pages_overwritten = free_pages(block, SSD[partition_index])
        overwrites += pages_overwritten
        # print('SSD with freed pages:', SSD)

    # Attempt to locate space in the partition. 
    # If there is no space, garbage collect, then locate space again
        try:
            erase_block_index = locate_space(SSD[partition_index], 
            pages_per_erase_block)
            # print('Space in this erase block:', erase_block_index)
        except GarbageCollectionRequired:
            # print('Garbage collection required')
            # If dynamic provisioning, assign partition an erase block from pool
            if not is_static:
                if SSD[len(SSD) - 1]: # check if pool still has spare blocks
                    SSD[len(SSD) - 1].remove([]) # take block from pool
                    SSD[partition_index].append([]) #add to partition
            SSD[partition_index], new_writes = garbage_collect(
                SSD[partition_index], pages_per_erase_block)
            # print('SSD after garbage collection:', SSD)
            # print('garbage collection performed')
            GC_writes += new_writes
            try:
                erase_block_index = locate_space(SSD[partition_index], 
                pages_per_erase_block)
            except GarbageCollectionRequired:
                raise PartitionCompletelyFull
            # print('Space now in this erase block:', erase_block_index)
    
    # Write block to empty space
        SSD[partition_index][erase_block_index].append(block)
        # print('SSD with block written:', SSD)
        # print('block written')
        user_writes += 1

    return (user_writes, GC_writes, overwrites)


def Run_IO(trace_file, logical_block_size_in_KB, logical_sector_size_in_KB, 
partition_dict, SSD, pages_per_erase_block, main_blocks_per_partition, 
is_static):
    '''(file, int, int, dict of int:int, list of lists, int, int, bool) -> 
    float

    Reads events from a file of trace data, runs them through simulated SSD, 
    and tracks writes. Then computes and returns write amplification.
    '''
    trace_data = open(trace_file, 'r')
    total_user_writes = 0
    total_GC_writes = 0
    total_overwrites = 0
    WA_history = []
    
    # Read events from the trace file and put in a list one-by-one
    for event in trace_data:
        event = event.split()
    
    # For each event, use filter_event to check if it's a valid write event 
        if DictBuilder.filter_event(event) == False:
            continue

    # If so, get blocks, then write blocks to partition
        else:
            blocks = DictBuilder.get_blocks(event, logical_block_size_in_KB, 
            logical_sector_size_in_KB)
            user_writes, GC_writes, pages_overwritten = write_to_partition(blocks, partition_dict, 
            SSD, pages_per_erase_block, main_blocks_per_partition, is_static)
            total_user_writes += user_writes
            total_GC_writes += GC_writes
            total_overwrites += pages_overwritten
            current_WA = (total_user_writes + total_GC_writes)/total_user_writes
            WA_history.append(current_WA)
            if (total_user_writes % 10000 == 0):
                print("Total user writes:", total_user_writes, "   Total updates:", total_overwrites, "   Total GC writes:", total_GC_writes, "   Current WA:", round(current_WA, 2))
            # if total_user_writes >= 550000:
                # return sum(WA_history)/len(WA_history)
            continue
    print("Total user writes:", total_user_writes, "   Total updates:", total_overwrites, "   Total GC writes:",
          total_GC_writes, "   Current WA:", round(current_WA, 2))
    # Close file, then compute and return write amplification
    trace_data.close()
    return sum(WA_history)/len(WA_history)



# TESTING
#____________________________________________________________________

# Sample values for write_to_partition

# blocks = [18, 19, 20, 21, 22]

# pages_per_erase_block = 3

# main_blocks_per_partition = 4

# partition_dict = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 
# 11:1, 12:1, 13:1, 14:1, 15:1, 16:1, 17:1, 18:1, 19:1, 20:1, 21:1, 22:1}

# is_static = True

# if is_static == True:
#     SSD = [
#     [[5, 6, -7], [7, 8, 9], [], []],
#     [[-12, 13, -14], [-15, 12, 14], [16, 17, 18], []]
#     ]

# if is_static == False:
#     SSD = [
#     [[5, 6, -7], [7, 8, 9], [], []],
#     [[-12, 13, -14], [-15, 12, 14], [16, 17, 18], []],
#     [[], []] 
#     ]

# print(write_to_partition(blocks, partition_dict, SSD, pages_per_erase_block, 
# main_blocks_per_partition, is_static))
