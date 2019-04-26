# Inputs: 
    # num_partitions
    # erase_blocks_per_partition

# Outputs:
    # SSD

# What we need to do: 
    # Create lists of lists to simulate an SSD structure
        # e.g. If 6 partitions and 40 erase blocks per partition, create 6 lists of 40 lists each

    # Figure out a way to do this that might help later with static vs. dynamic allocation of overprovisioned erase blocks

