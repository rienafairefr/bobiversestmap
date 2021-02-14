
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

For dependencies, use poetry: `poetry install`, then `poetry shell`

Then,

    python3 manage.py importdata

This will import the Combined.txt into multiple datasets, all stored in a SQLite database

* Book data (lines, chapters)
* Characters for each Chapter
* Characters location
* Links (each sentence where two characters are is a link, some are SCUT --faster than light--)
* Lines talked by each character
* First/last appearances of a character
* Space location (distances between stars etc)

Then run

    python3 manager.py runserver
    
This will serve a Flask & D3.js web-app on localhost:5000 where you can see graphs about
that dataset 

    python3 manage.py freeze freeze
    
Will store in docs/ a frozen dataset. This permits that the web-app to be "run"
statically on github.io


All characters and stories belong to Dennis E. Taylor and are &copy; Dennis E. Taylor

layout-narrative from https://github.com/abcnews/d3-layout-narrative/