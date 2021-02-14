"""
{ "nodes": [
            {"name":node_name, "group":node_group},
            {"name":another_node_name, "group":another_node_group}, ...
],
  "links":[
            {"source"link_source, "target":link_target, "value":link_value,
            {"source"another_link_source, "target":another_link_target, "value":another_link_value}, ...
]
}
"""
from sqlalchemy import not_

from app import db
from generator.models import Character, Link, ChapterCharacter, ChapterLink


def get_book_characters(nb=None):
    q = db.session.query(Character).join(ChapterCharacter)
    if nb is not None:
        q = q.filter(ChapterCharacter.chapter_nb == nb)

    return [
        {
            "id": char.id,
            "name": char.name,
            "group": "Bob" if char.is_bob else char.affiliation,
        }
        for char in q
    ]


def get_book_links(nb=None):
    q = db.session.query(ChapterLink)
    if nb is not None:
        q = q.filter(ChapterLink.chapter_nb == nb)

    return [
        {"source": cl.link.characterA_id, "target": cl.link.characterB_id, "value": 1}
        for cl in q
        if cl.link.characterA_id != cl.link.characterB_id
    ]


def get_cooccurences_json(nb=None):
    return {"nodes": get_book_characters(nb), "links": get_book_links(nb)}
