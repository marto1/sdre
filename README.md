Supervised data refining engine. Really experimental.

# Accumulating
By a given subject(enumeration of tokens) specified in link_dump.py should
traverse various resources on the web and accumulate a list of usable links to be processed.

gather_info.py will gather all text considered useful from the files.

At this point all raw data has been accumulated.

# Refining

The gathered data is passed to structure.py which would try to formulate meaningful sentences
based on the raw data, from which the user refines the results interactively. 

