# What we need to do: Read through trace again. For each logical block:
    # Check assigned partition
    # Go to assigned partition and check all sublists for block number.
        # If it's there, change it to a negative number.
    # Then check sublist-by-sublist to find one that is not full (can just check length of sublists to make sure it's under the max)
    # If all up sublists to overprovisioned lists are full, garbage collect
        # This involves rewriting positive block numbers from each erase block to a new erase block, and deleting the rest
        # Need to think here about whether to sort lists so the empty ones are at the end again, or how to experiment with dynamic allocation
        # Count all garbage collection writes
    # Write block number to a list with space
    # Count write

# What to return: total writes by user and total writes driving garbage collection
