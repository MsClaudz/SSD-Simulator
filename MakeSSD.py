# We have: Number of partitions, number of erase blocks per partition, and a dict of block numbers assigned to partitions
# We can figure out the number of logical blocks that can fit into an erase block
    # e.g. For a standard 4 MB erase block and 4 KB-sized logical blocks, each erase block holds 1000 logical blocks
    # So, 1000 elements are allowed in each sub-list before erase block is "full" and data must be entered in the next sub-list
    
# What we need to do: 
    # Create lists of lists to simulate an SSD structure
        # e.g. If 6 partitions and 40 erase blocks per partition, create 6 lists of 40 lists each
        # Determine the amount of overprovisioned blocks that should be kept empty in each partition (about 11 blocks for above example)

