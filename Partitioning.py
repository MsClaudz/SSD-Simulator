import math

# Given update frequency ratio, compute number of partitions
def partitions_from_ratio(freq_dict, ratio):
    '''(dict of int:int, int) -> int

    Given update frequency ratio, calculates the minimum number of partitions required to ensure ratio is not exceeded
    (Update frequency ratio is the ratio between maximum and minimum update frequencies of pages in a partition)

    e.g.
    >>>partitions_from_ratio({123:2, 234:2, 345:3, 456:5, 567:3, 678:6, 789:3, 890:9}, 2)
    3
    '''
    # find max and min values
    max_freq = (max(freq_dict.values()))
    min_freq = (min(freq_dict.values()))
    # compute number of partitions and round up
    partitions = (math.log(max_freq/min_freq))/(math.log(ratio))
    partitions = round(partitions + 0.5)
    # return number of partitions
    return partitions


# Given number of partitions, compute update frequency ratio
def ratio_from_partitions(freq_dict, partitions):
    '''(dict of int:int, int) -> int

    Given number of partitions, calculates the lowest update frequency ratio required to ensure number of partitions is not exceeded
    (Update frequency ratio is the ratio between maximum and minimum update frequencies of pages in a partition)

    e.g.
    >>>ratio_from_partitions({123:2, 234:2, 345:3, 456:5, 567:3, 678:6, 789:3, 890:9}, 2)
    2.12
    '''
    # find max and min values
    max_freq = (max(freq_dict.values()))
    min_freq = (min(freq_dict.values()))
    # compute update frequency ratio and round to two decimals
    ratio = (max_freq/min_freq)**(1/partitions)
    ratio = round(ratio, 2)
    # return update frequency ratio
    return ratio


def define_partitions(freq_dict, ratio, partitions):
    '''(dict of int:int, int, int) -> dict of int:list of int

    From update frequency ratio and number of partitions, computes partition boundaries. Returns partitions in a dict
    with keys as numbers and values as min and max update frequencies for each partition.

    e.g.
    >>>define_partitions({23:2, 24:2, 25:3, 26:5, 27:3, 28:6, 29:3, 30:9}, 2, 3)
    {1:[ , ], 2:[ , ], 3:[ , ]}
    '''
    # Create a dictionary with keys equal to the number of partitions

    # Get max value from freq_dict
    max_freq = (max(freq_dict.values()))

    # Assign max and min partition values to each key
        # i.e. assign max to dict[partitions][1], then max/ratio to dict[partitions][0]
        # then set i = 1
        # while i < partitions, repeat assignments for dict[partitions - i], increment i by 1

    
def assign_to_partitions(freq_dict, ratio, partitions):
    '''
    Replaces the value corresponding to each logical block in freq_dict with a partition number.

    e.g.
    >>>assign_to_partitions({77:1, 78:2, 79:3, 80:4, 81:8, 82:7}, 2, 3)
    {77: , 78: , 79: , 80: , 81: , 82: }
    '''
    # For each key in freq_dict, check partitions from greatest to smallest
    # As you check each partition, if dict value <= partition[1] and dict value >= partition[0], replace value with partition number
    # If you get to the last partition, you can just assign it