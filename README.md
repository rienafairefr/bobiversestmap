
Some data visualisation based on the books of the Bobiverse by Dennis E. taylor

In order to run the scripts, you need a Combined.txt with the fulltext of
the books that is formatted like this:

    ##BookTitle
    1. Title Chapter
    Corresponding-Bob
    Time-Date
    Location
    This is the content of the chapter[...]
    2. other Chapter
    [...]
    ##OtherBook

You can get this from the epub of the books

Book 1 deviates a bit from that convention so you'll need to edit a bit manually

Install requirements with `pip3 install -r requirements.txt'

Then,


    python3 readcombined.py
    python3 read_dates.py
    python3 genealogy.py
    python3 relationships.py

Will generate the scenes.json, containing which characters are found in which chapters

    python3 write_data.json.py

Will combine all these in the data.json that is used in index.html (chart.js)




All characters and stories belong to Dennis E. Taylor and are &copy; Dennis E. Taylor

layout-narrative from https://github.com/abcnews/d3-layout-narrative/