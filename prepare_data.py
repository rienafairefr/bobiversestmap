import os
from genealogy import read_genealogy
from locations import read_locations
from read_dates import read_dates
from read_travels import read_travels
from readcombined import read_combined
from scenes_locations import read_scenes_locations
from scenes import read_scenes
from write_data_json import write_data_json

os.makedirs('generated', exist_ok=True)

read_combined()
read_dates()
read_genealogy()
read_locations()
read_scenes_locations()
read_scenes()
read_travels()

write_data_json()
write_data_json(1)
write_data_json(2)
write_data_json(3)
