from generator.book_chapters import import_book_chapters
from generator.books import import_books
from generator.chapter_characters import postprocess_chapter_characters
from generator.chapters_locations import postprocess_chapters_locations
from generator.characters import import_characters
from generator.dates import postprocess_dates
from generator.links import postprocess_links, import_links, postprocess_scut_links
from generator.locations import import_locations
from generator.stars import import_stars, import_starsmap
from generator.thresholds import import_thresholds
from generator.timeline import import_timeline_descriptions
from generator.travels import get_travels_dict, import_chapter_characters_travels


def import_combined(path):
    print('import books...')
    books = import_books(path)
    print('OK')

    print('import stars...')
    stars = import_stars()
    import_starsmap()
    print('OK')

    print('import locations...')
    locations = import_locations()
    print('OK')

    print('import characters...')
    characters = import_characters()
    print('OK')

    print('import book chapters...')
    book_chapters = import_book_chapters(books)
    print('OK')

    postprocess_chapter_characters()

    print('import links between characters...')
    links = import_links(book_chapters)
    print('OK')

    print('import chapter characters travels...')
    import_chapter_characters_travels(book_chapters)
    print('OK')

    print('import thresholds...')
    import_thresholds()
    print('OK')

    print('import timeline descriptions...')
    import_timeline_descriptions()
    print('OK')

    postprocess_dates()

    postprocess_links()
    postprocess_chapters_locations()
    postprocess_scut_links()
