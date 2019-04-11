import DictBuilder

trace_file = 'sample_trace.txt'
sectors_per_block = 8

test_dict = DictBuilder.build_dict(trace_file, sectors_per_block)
print(test_dict)