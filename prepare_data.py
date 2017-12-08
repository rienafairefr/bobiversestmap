import os


import time
from write_data_json import write_data_json

os.makedirs('generated', exist_ok=True)


start = time.time()
write_data_json()
end = time.time()
print(end - start)
#write_data_json(1)
#write_data_json(2)
#write_data_json(3)
