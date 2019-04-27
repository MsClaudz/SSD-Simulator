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
