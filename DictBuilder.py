def filter_event(event):
    '''(list of str) -> bool

    Returns True if trace event is a write event and a complete event

    e.g.
    >>>filter_event(['8,16', '2', '14722', '73.165905398', '0', 'C', 'WS', '12858376', '+', '32', '[0]'])
    True

    >>>filter_event(['8,16', '2', '10013', '16.774178596', '3929', 'C', 'R', '5149344', '+', '120', '[0]'])
    False

    >>>filter_event(['8,16', '1', '14483', '615.865377616', '3997', 'D', 'W', '7240192', '+', '1536', '[kworker/u8:0]'])
    False
    '''
    
    # If the event is not some type of write ('W', 'WS', or 'WM' in column 6), return False
    if event[6][0] != 'W':
        return False
    # If event is not the completed part of the transaction ('C' in column 5), return False
    elif event[5] != 'C':
        return False
    else:
        return True


def get_blocks(event, sectors_per_block):
    '''(list of str) -> list of int
    
    Makes a list of all blocks effected by an IO trace event.

    e.g.
    >>>get_blocks(['8,16', '2', '14722', '73.165905398', '0', 'C', 'WS', '12858376', '+', '32', '[0]'], 8)
    [12858376, 12858377, 12858378, 12858379]

    >>>get_blocks(['8,16', '1', '14739', '619.781547871', '0', 'C', 'W', '8697448', '+', '8', '[0]'], 8)
    [8697448]
    '''
    # Get start block and request size from columns 7 and 9 of event, convert them to integer
    start_block = int(event[7])
    req_size = int(event[9])
    # Determine end block, also convert to integer
    end_block = int(start_block + (req_size / sectors_per_block))
    # Make list of all effected blocks and return the list
    blocks = list(range(start_block, end_block))
    return(blocks)


def add_to_dict(blocks, freq_dict):
    '''(list of int) -> dict of int:int
    
    Adds to a dictionary tracking the number of times logical blocks have been updated.
    Takes a list of updated logical blocks and increments their values by +1 in the dictionary.

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


def update_dict(event, sectors_per_block, freq_dict):
    '''(list of str, int, dict of int:int) -> dict of int:int

    Combines functionality of get_blocks and add_to_dict.
    Takes an IO event and increments update frequencies for effected blocks by +1 in a dictionary.

    e.g.
    update_dict(['8,16', '2', '14722', '73.165905398', '0', 'C', 'WS', '12858376', '+', '32', '[0]'], 8, {})
    {12858376: 1, 12858377: 1, 12858378: 1, 12858379: 1}
    '''
    blocks = get_blocks(event, sectors_per_block)
    add_to_dict(blocks, freq_dict)
    return freq_dict


def build_dict(trace_file, sectors_per_block):
    '''(file) -> dict of int:int

    e.g.
    >>>build_dict('blkparseout_ext4.txt', 8)
    {}
    '''
    freq_dict = {}
    trace_data = open(trace_file, 'r')
    # Read events from the trace file and put in a list one-by-one
    for event in trace_data:
        event = event.split()
        # Stop when you get to the metadata at the end and return updated dict
        if event[0] == 'CPU0':
            trace_data.close()
            return freq_dict
        # For each event, check if it's a complete write and if so, update dict
        else:
            if filter_event(event) == False:
                continue
            elif filter_event(event) == True:
                freq_dict = update_dict(event, sectors_per_block, freq_dict)
                continue