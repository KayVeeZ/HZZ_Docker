# import samples
# for s in samples.samples:
#     print(s)

import get_data
import time
# running functions
start = time.time() # time at start of whole processing
data = get_data.get_data_from_files() # process all files
elapsed = time.time() - start # time after whole processing
print("Time taken: "+str(round(elapsed,1))+"s") # print total time taken to process every file