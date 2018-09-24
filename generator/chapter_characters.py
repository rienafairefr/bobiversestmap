from app import db
from generator.characters import get_characters
from generator.models.chapters import BookChapter
from generator.models.characters import Character
from generator.thresholds import get_thresholds_last, get_thresholds_first


def treat_one_chapters_characters(book_chapter, characters=None):
    if characters is None:
        characters = get_characters()

    current_bob_character = book_chapter.bob_character
    if current_bob_character not in book_chapter.characters:
        book_chapter.characters.append(current_bob_character)
    for character in characters:
        for name in character.all_names:
            for tokenized_sentence in book_chapter.tokenized_content:
                if name in tokenized_sentence:
                    if character not in book_chapter.characters:
                        book_chapter.characters.append(character)


def postprocess_chapter_characters():
    book_chapters = db.session.query(BookChapter).all()
    characters = get_characters()

    for book_chapter in book_chapters:
        treat_one_chapters_characters(book_chapter, characters)

    db.session.commit()


    # False positive/ negative matches:
    def remove(nb, nc, character_id):
        character = db.session.query(Character).get(character_id)
        try:
            if isinstance(nc, int):
                book_chapter = db.session.query(BookChapter).get((nb, nc))
                if book_chapter is None:
                    pass
                if character not in book_chapter.characters:
                    pass
                book_chapter.characters.remove(character)
            else:
                for nc_element in nc:
                    remove(nb, nc_element, character_id)
            db.session.commit()
        except ValueError:
            pass

    # Tom Hanks in chapter 13
    remove(1, 13, 'Tom')
    # Will
    remove(1, 3, 'Riker')
    remove(1, 37, 'Riker')

    thresholds_last = get_thresholds_last()
    thresholds_first = get_thresholds_first()

    for book_chapter in book_chapters:
        k = book_chapter.k
        for character in list(book_chapter.characters):
            for character_id, bc in thresholds_last.items():
                if book_chapter > bc and character.id == character_id:
                    remove(*k, character_id)
            for character_id, bc in thresholds_first.items():
                if book_chapter < bc and character.id == character_id:
                    remove(*k, character_id)

    # 1-39 Bob talking about others
    remove(1, 39, 'Milo')
    remove(1, 39, 'Bill')
    remove(1, 39, 'Mario')

    # mentions
    # remove(106, 'Linus')
    # remove(181, 'Linus')
    # remove(62, 'Bert')
    # remove(148, 'Claude')

    # mentions
    remove(2, 14, 'Ralph')  # talk about sending him a missive
    remove(2, 77, 'Oliver')  # talk about him building a fleet
    remove(3, 15, 'Oliver')  # same

    remove(3, 68, 'Neil')  # same

    remove(2, [16, 30, 38, 39, 52, 54, 55, 60, 64], 'Mario')
    remove(3, [17, 33, 38, 70, 71], 'Mario')

    remove(3, [25, 75], 'Mack')

    remove(3, 73, 'Luke')
    remove(2, [17, 22, 24], 'Luke')

    remove(2, [52, 56], 'Loki')

    remove(2, 7, 'Julia')  # in stasis

    remove(2, [50, 60, 72], "Jacques")

    remove(3, [71, 73], "Icarus")

    remove(2, [33, 52, 61], "Howard")
    remove(3, [16, 18, 39], "Howard")

    remove(2, [12, 18, 26], "Homer")

    remove(2, 42, "Henry")

    remove(2, 55, "Hal")

    remove(1, 22, "Goku")
    remove(3, 39, "Goku")

    remove(2, 53, "Garfield")
    remove(3, 39, "Garfield")

    remove(3, 45, "Ferb")

    remove(2, 15, "Dopey")

    remove(3, [18, 51], "Dexter")

    remove(3, [11, 71], "Daedalus")

    remove(3, 11, "Claude")

    remove(1, 47, "Charles")
    remove(2, 14, "Charles")  # talk about sending him a missive

    remove(1, [22, 40], "Calvin")

    remove(3, [73, 57, 60, 54, 55, 51, 47, 45, 44, 41, 39, 35, 33, 30, 21, 18, 15, 14, 13, 8, 4], "Bob")
    remove(2, [77, 72, 70, 67, 63, 59, 52, 51, 50, 48, 46, 42, 39, 34, 32, 31, 30, 28, 20, 18, 15, 13, 10, 7, 5], "Bob")
    remove(1, [60, 58, 57, 54, 49, 47, 45, 42, 40, 38, 34, 32, 29, 25, 24, 22, 21, 20, 18], "Bob")

    remove(1, [19, 21, 23, 24, 26, 27, 28, 40, 46, 47, 53, 57, 58], "Bill")
    remove(2, [1, 2, 4, 10, 13, 14, 17, 19, 20, 27, 38, 41, 48, 49, 50, 53, 58, 65, 68, 73], "Bill")
    remove(3, [16, 18, 22, 24, 26, 31, 38, 39, 41, 45, 48, 67, 74, 75], "Bill")

    remove(2, 2, 'Bert')
    remove(2, 15, 'Bashful')

    remove(1, range(1, 44), 'Archimedes')  # remove instances before first contact with Archimedes

    # Fred represents 3 different characters
    for book_chapter in book_chapters:
        nb, nc = book_chapter.k
        if any('Fred' in char.id for char in book_chapter.characters):
            # the Bob clone in book1
            if nb == 1:
                remove(nb, nc, 'Fred_Deltan')
            remove(nb, nc, 'Fred_Carleon')
            # the deltan hunter
            if nb == 2:
                remove(nb, nc, 'Fred')
            remove(nb, nc, 'Fred_Carleon')
            # the foe from Carleon
            if nb == 3:
                remove(nb, nc, 'Fred')
            remove(nb, nc, 'Fred_Deltan')

    remove(3, 40, "Fred_Carleon")

    remove(1, 54, 'Sam')
    remove(2, 2, 'Sam')
    remove(2, 7, 'Sam')
