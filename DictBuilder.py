# Inputs:
# trace_file
# logical_block_size_in_KB
# logical_sector_size_in_KB

# Outputs:
# freq_dict

def get_blocks(event, logical_block_size_in_KB, logical_sector_size_in_KB):
    '''(list of str, int) -> list of int
    
    Makes a list of all logical blocks affected by an IO trace event.

    e.g. (note that examples are based on our trace data, not FIU trace data)
    >>>get_blocks(['8,16', '2', '14722', '73.165905398', '0', 'C', 'WS', '12858376', '+', '32', '[0]'], 4.096, 0.512)
    [12858376, 12858377, 12858378, 12858379]

    >>>get_blocks(['8,16', '1', '14739', '619.781547871', '0', 'C', 'W', '8697448', '+', '8', '[0]'], 4.096, 0.512)
    [8697448]
    '''
    # Get start block and request size from event, convert them to integer
    
    ## Our traces:
    # start_block = int(event[7])
    # req_size = int(event[9])

    ## FIU traces (different output format):
    start_block = int(event[3])
    req_size = int(event[4])

    # Determine end block, also convert to integer
    logical_sectors_per_logical_block = logical_block_size_in_KB/logical_sector_size_in_KB
    end_block = int(start_block + (req_size / logical_sectors_per_logical_block))
    
    # Make list of all affected blocks and return the list
    blocks = list(range(start_block, end_block))
    return(blocks)


def filter_event(event):
    '''(list of str) -> bool
    
    Returns True if trace event is a valid, complete write event.
    
    e.g. (note that examples are based on our trace data, not FIU trace data)
    >>>filter_event(['8,16', '2', '14722', '73.165905398', '0', 'C', 'WS', '12858376', '+', '32', '[0]'])
    True

    >>>filter_event(['8,16', '2', '10013', '16.774178596', '3929', 'C', 'R', '5149344', '+', '120', '[0]'])
    False
    '''
    try:
        # Our traces
        # If the event is not some type of write ('W', 'WS', or 'WM'), or not the completed part of the transaction ('C') return False
        # if (event[6][0] != 'W') or (event[5] != 'C'):
            # return False
        # else:
            # return True

        # FIU traces
        # If event is not some type of write ('W', 'WS', or 'WM'), return false
        if event[5][0] != 'W':
            return False
        else:
            return True   
    
    # Exclude lines from beginning and end of the file that are not trace events
    except IndexError:
        return False

        
def add_to_dict(blocks, freq_dict):
    '''(list of int, dict of int:int) -> dict of int:int
    
    Takes a list of logical blocks affected by a trace event and increments their values by +1 in a dictionary.

    e.g.
    >>>add_to_dict([8697448], {})
    {8697448: 1}
    
    >>>add_to_dict([76, 77, 78, 79], {})
    {76: 1, 77: 1, 78: 1, 79: 1}

    >>>add_to_dict([48], {48:2})
    {48: 3}

    >>>add_to_dict([76, 77, 78, 79], {78:1, 79:2, 80:4, 90:5})
    {80: 4, 90: 5, 76: 1, 77: 1, 78: 2, 79: 3}
    '''
    for block in blocks:
    
    # If the block does not yet exist in the dictionary, add it and set its value to 1
        if block not in freq_dict:
            freq_dict[block] = 1
    
    # If block already exists in dictionary, increment its value by 1
        elif block in freq_dict:
            freq_dict[block] += 1
    
    # return updated dictionary
    return freq_dict


def build_dict(trace_file, logical_block_size_in_KB, logical_sector_size_in_KB):
    '''(txt file, int) -> dict of int:int

    Reads data from a trace file line-by-line and calls filter_event to skip lines that are non-write events or incomplete events.
    For valid, complete write events, calls get_blocks then add_to_dict to populate a dictionary with logical block update frequencies.
    Takes a file of trace data and logical block and sector sizes for the file system from which the traced requests were issued.

    e.g.
    >>>build_dict('blkparseout.txt', 4.096, 0.512)
    {6810720: 1, 6810721: 3, 6810722: 2, 6810723: 5, 6810724: 8}
    '''
    freq_dict = {}
    trace_data = open(trace_file, 'r')
    num_writes = 0
    # Read events from the trace file and put in a list one-by-one
    for event in trace_data:
        event = event.split()

    # For each event, use filter_event to check if it's a valid, complete write event and if so, update dict
        if filter_event(event) == False:
            continue
        else:
            add_to_dict((get_blocks(event, logical_block_size_in_KB, logical_sector_size_in_KB)), freq_dict)
            num_writes += 1
            continue

    # Close file and return updated dict
    print("Total write events:", num_writes)
    trace_data.close()
    return freq_dict