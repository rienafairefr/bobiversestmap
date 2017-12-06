from genealogy import read_genealogy
from locations import read_locations
from read_dates import read_dates
from readcombined import read_combined
from relationships import read_relationships
from write_data_json import write_data_json

read_combined()
read_dates()
read_genealogy()
read_locations()
read_relationships()

write_data_json()
write_data_json(1)
write_data_json(2)
write_data_json(3)
