import DictBuilder

# trace_file = 'traces\sample_trace.txt'
# trace_file = 'traces\blkparseout_ext4.txt'
# trace_file = 'traces\blkparseout_btrfs.txt'
# trace_file = 'traces\blkparseout_f2fs.txt'
trace_file = 'traces\cheetah.cs.fiu.edu-110108-113008.1_sample.blkparse'
sectors_per_block = 8

test_dict = DictBuilder.build_dict(trace_file, sectors_per_block)
print(test_dict)
# values = test_dict.values()
# print(values)