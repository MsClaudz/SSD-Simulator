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