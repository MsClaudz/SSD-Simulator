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


def Run_IO(trace_file, logical_block_size_in_KB, logical_sector_size_in_KB,   ): # ADD OTHER PARAMETERS
    '''(file, int, int,   ) -> float

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
            user_writes, GC_writes = write_to_partition(blocks,   ) # ADD OTHER PARAMETERS
            total_user_writes += user_writes
            total_GC_writes += GC_writes
            continue
        
    # Close file, compute write amplification, and return write amplification
    trace_data.close()
    write_amplification = (total_user_writes + total_GC_writes)/total_user_writes
    return write_amplification


def write_to_partition(blocks, partition_dict, SSD,   ): # ADD OTHER PARAMETERS
    '''(list, dict of int:int, list of list of list,    ) -> (int, int)


    Returns number of user writes and number of garbage collection writes that occurred.

    '''
    # For each logical block in list:
        # Check assigned partition in partition_dict
        # Go to assigned partition in SSD and check all sublists of partition for block number
        # If it's there, change it to a negative number. If not, just continue on
        # Then check same partition, from beginning, sublist-by-sublist until one sublist is not full 
            # (A sublist is full if length of sublist >= pages_per_erase_block)
        # If index of empty sublist <= main_blocks_per_partition, write the block number to the sublist 
            # (do we have to write 8 times if 1 erase block = 8 pages? I think so)
        # If index of empty sublist > main_blocks_per_partition, garbage collect -- you have reached the overprovisioned blocks
            # Once garbage collection is complete, have it return GC_writes and add that to total_GC_writes
            # then check sublists again to find the first empty one, and write block number there
        # increment total_user_writes += 1


def garbage_collect(   ):
    # garbage collection
    # define as a separate function - takes a partition, returns a new partition and returns GC_writes
        # For each sublist (i.e. erase block) in the partition:
            # rewrite all positive block numbers to new erase blocks, counting every write, then empty the old blocks
            # At some point, have to sort so empty lists are at the end of the partition


# How do we statically vs. dynamically allocate erase blocks?