import math

# Given update frequency ratio, compute number of partitions
def num_partitions_from_ratio(freq_dict, ratio):
    '''(dict of int:int, number) -> int

    Given update frequency ratio, calculates the minimum number of partitions required to ensure ratio is not exceeded
    (Update frequency ratio is the ratio between maximum and minimum update frequencies of pages in a partition)
    Returns the number of partitions, rounded up to the nearest integer.

    e.g.
    >>> num_partitions_from_ratio({123:2, 234:2, 345:3, 456:5, 567:3, 678:6, 789:3, 890:9}, 2)
    3
    '''
    # get max and min values from freq_dict
    max_freq = (max(freq_dict.values()))
    min_freq = (min(freq_dict.values()))
    # compute number of partitions and round up to a whole number
    num_partitions = (math.log(max_freq/min_freq))/(math.log(ratio))
    # round num_partitions up to nearest whole number
    num_partitions = int(-(-num_partitions // 1))
    # return number of partitions
    return num_partitions


# Given number of partitions, compute update frequency ratio
def ratio_from_num_partitions(freq_dict, num_partitions):
    '''(dict of int:int, int) -> int

    Given number of partitions, calculates the lowest update frequency ratio required to ensure number of partitions is not exceeded
    (Update frequency ratio is the ratio between maximum and minimum update frequencies of pages in a partition)

    e.g.
    >>>ratio_from_num_partitions({123:2, 234:2, 345:3, 456:5, 567:3, 678:6, 789:3, 890:9}, 2)
    2.12
    '''
    # get max and min values from freq_dict
    max_freq = (max(freq_dict.values()))
    min_freq = (min(freq_dict.values()))
    # compute update frequency ratio and round to two decimals
    ratio = (max_freq/min_freq)**(1/num_partitions)
    ratio = round(ratio, 2)
    # return update frequency ratio
    return ratio


def define_partitions(freq_dict, ratio, num_partitions):
    '''(dict of int:int, number, int) -> list of (int,int)

    From update frequency ratio and number of partitions, computes partition boundaries. Returns partitions in a list of
    min and max update frequencies for each partition.

    e.g.
    >>> define_partitions({23:2, 24:2, 25:3, 26:5, 27:3, 28:6, 29:3, 30:9}, 2, 3)
    [(2, 4), (4, 8), (8, 16)]
    '''
    partitions = []

    # Get min value from freq_dict
    min_freq = (min(freq_dict.values()))

    # Push min and max partition values as a tuple to the list
    i = 0
    while i < num_partitions:
        partitions.append((min_freq, min_freq * ratio))
        min_freq = min_freq * ratio
        i += 1

    return partitions
    
def assign_to_partitions(freq_dict, ratio, partitions):
    '''(dict of int:int, number, list of (int, int)) -> dict of int:int

    Replaces the value corresponding to each logical block in freq_dict with a partition number.

    e.g.
    >>> assign_to_partitions({77:1, 78:2, 79:3, 80:4, 81:8, 82:7}, 2, [(1, 2), (2, 4), (4, 8)])
    {77: 0, 78: 0, 79: 1, 80: 1, 81: 2, 82: 2}
    '''

    partition_dict = {}

    for key in freq_dict:
        freq = freq_dict[key]
        i = 0
        for bounds in partitions:
            if freq >= bounds[0] and freq <= bounds[1]:
                partition_dict[key] = i
                break
            i += 1

    return partition_dict