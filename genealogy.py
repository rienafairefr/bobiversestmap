import json
import os

with open(os.path.join('public_data','genealogy.txt')) as genealogy:
    lines = genealogy.readlines()

bobs = []
for line in lines:
    bobs.append(line.strip().split(':'))

json.dump(bobs, open(os.path.join('generate','genealogy.json'),'w'))

bob_characters = []
for bob in bobs:
    char = {'id':bob[-1],'name':bob[-1]}
    if len(bob)!=1:
        char['affiliation'] = bob[-2]
    else:
        char['affiliation']= bob[-1]
    bob_characters.append(char)

json.dump(bob_characters, open(os.path.join('generated','bob_characters.json'),'w'))
