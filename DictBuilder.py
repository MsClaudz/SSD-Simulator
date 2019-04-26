def get_blocks(event, sectors_per_logical_block):
    '''(list of str, int) -> list of int
    
    Makes a list of all logical blocks affected by an IO trace event.

    e.g.
    >>>get_blocks(['8,16', '2', '14722', '73.165905398', '0', 'C', 'WS', '12858376', '+', '32', '[0]'], 8)
    [12858376, 12858377, 12858378, 12858379]

    >>>get_blocks(['8,16', '1', '14739', '619.781547871', '0', 'C', 'W', '8697448', '+', '8', '[0]'], 8)
    [8697448]
    '''
    # Get start block and request size from columns 7 and 9 of event, convert them to integer
    
    ## Our traces:
    # start_block = int(event[7])
    # req_size = int(event[9])

    ## FIU traces (different output format):
    start_block = int(event[3])
    req_size = int(event[4])

    # Determine end block, also convert to integer
    end_block = int(start_block + (req_size / sectors_per_logical_block))
    # Make list of all affected blocks and return the list
    blocks = list(range(start_block, end_block))
    return(blocks)


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


def build_dict(trace_file, sectors_per_logical_block):
    '''(txt file, int) -> dict of int:int

    Reads data from a trace file, then calls add_to_dict and get_blocks to populate a dictionary 
    with logical block update frequencies.

    e.g.
    >>>build_dict('blkparseout.txt', 8)
    {6810720: 1, 6810721: 3, 6810722: 2, 6810723: 5, 6810724: 8}
    '''
    freq_dict = {}
    trace_data = open(trace_file, 'r')
    # Read events from the trace file and put in a list one-by-one
    for event in trace_data:
        event = event.split()
        # For each event, check if it's a complete write and if so, update dict
        try:
            ## Our traces:
            # if (event[6][0] != 'W') or (event[5] != 'C'):
            ## FIU traces:
            if event[5][0] != 'W':
                continue
            else:
                add_to_dict((get_blocks(event, sectors_per_logical_block)), freq_dict)
                continue
        # But, exclude lines from the file that are not trace events
        except IndexError:
            continue
    # Return updated dict
    return freq_dict