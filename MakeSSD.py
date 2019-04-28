# Inputs: 
    # num_partitions
    # main_blocks_per_partition
    # num_overprovisioned_erase_blocks
    # static vs. dynamic allocation

# Outputs:
    # SSD

# What we need to do: 
    # Create lists of lists to simulate an SSD structure
        # create SSD using num_partitions and main_blocks_per_partition
            # e.g. If 6 partitions and 40 erase blocks per partition, create 6 lists of 40 lists each
        # then add overprovisioned erase blocks
            # if static allocation, calculate num_overprovisioned_erase_blocks per partition and add to each partition of SSD
                # e.g. If 6 partitions and 12 overprovisioned erase blocks, add 2 overprovisioned erase blocks to each partition
            # if dynamic allocation... I guess create an extra partition with all the overprovisioned erase blocks in it?

def make_SSD(num_partitions, main_blocks_per_partition, num_overprovisioned_erase_blocks, is_static):
    SSD = []

    # if it's static allocation, we add eraseblocks into the partitions
    blocks_per_partition = main_blocks_per_partition
    if is_static:
        blocks_per_partition += num_overprovisioned_erase_blocks / num_partitions

    i = 0
    while i < num_partitions:
        j = 0
        partition = []
        while j < blocks_per_partition:
            partition.append([])
            j += 1
        SSD.append(partition)
        i += 1

    # if it's dynamic allocation, we put the overprovisioned blocks in an extra partition at the end
    if not is_static:
        j = 0
        op_partition = []
        while j < num_overprovisioned_erase_blocks:
            op_partition.append([])
            j += 1
        SSD.append(op_partition)

    return SSD