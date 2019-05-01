# Inputs: 
    # num_partitions
    # main_blocks_per_partition
    # num_overprovisioned_erase_blocks
    # static vs. dynamic allocation

# Outputs:
    # SSD

def make_SSD(num_partitions, main_blocks_per_partition, num_overprovisioned_erase_blocks, is_static):
    '''(int, int, float, bool) -> list of lists of lists

    Creates nested lists to simulate the structure of an SSD. Takes the number of partitions, the number of main erase blocks per partition, 
    the total number of overprovisioned erase blocks, and a bool indicating whether overprovisioned erase blocks should be allocated statically.
    If static provisioning, divides overprovisioned blocks by partitions, rounds up to integer, and adds that number of lists to each partition. 
    If dynamic, rounds number of overprovisioned erase blocks up to nearest integer and stores all overprovisioned blocks in separate list.

    e.g.
    >>>make_SSD(3, 4, 3.0, True)
    [[[], [], [], [], []], [[], [], [], [], []], [[], [], [], [], []]]

    >>>make_SSD(3, 4, 3.0, False)
    [[[], [], [], []], [[], [], [], []], [[], [], [], []], [[], [], []]
    '''
    SSD = []

    # if it's static allocation, we add eraseblocks into the partitions
    blocks_per_partition = main_blocks_per_partition
    if is_static:
        blocks_per_partition += int(-(-num_overprovisioned_erase_blocks // num_partitions))

    i = 0
    while i < num_partitions:
        j = 0
        partition = []
        while j < blocks_per_partition:
            partition.append(set())
            j += 1
        SSD.append(partition)
        i += 1

    # if it's dynamic allocation, we put the overprovisioned blocks in an extra partition at the end
    if not is_static:
        num_overprovisioned_erase_blocks = int(-(-num_overprovisioned_erase_blocks // 1)) # rounds up to nearest int
        j = 0
        op_partition = []
        while j < num_overprovisioned_erase_blocks:
            op_partition.append(set())
            j += 1
        SSD.append(op_partition)

    return SSD