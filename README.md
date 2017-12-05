
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

Then,

    python readcombined.py

Will generate a Combined.json

    python genealogy.py

Will generate a bob_characters.json

    python relationships.py

Will generate the scenes.json, containing which characters are found in which chapters
You then combine all these in the data.json

    python write_data.json.py

All characters and stories belong to Dennis E. Taylor and are &copy; Dennis E. Taylor

layout-narrative from https://github.com/abcnews/d3-layout-narrative/