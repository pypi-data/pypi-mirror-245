import os as _os
from importlib import resources as _resources

import fileunity as _fu
import wonderparse as _wp


def main(args=None):
    result = _wp.easymode.simple_run(
        prog='ankiapp_easy_deck',
        program_object=run,
        endgame='return',
        args=args,
    )

def run(
    infile,
    *,
    first_language=None,
    second_language=None,
    deck_name=None,
    outfile=None,
):
    first_language = _first_language(first_language)
    second_language = _second_language(second_language)
    deck_name = _deck_name(
        deck_name,
        infile=infile,
    )
    outfile = _outfile(
        outfile,
        infile=infile,
    )

    card_draft_text = _get_card_draft_text()
    deck_draft_text = _get_deck_draft_text()

    inhandler = _fu.TextUnit.handlerclass()(infile)
    cards = ""
    for rawline in inhandler.read():
        line = rawline.strip()
        if line == "":
            continue
        try:
            second_language_text, first_language_text = line.split('=')
        except:
            raise ValueError(f"Faulty line: {line}")
        first_language_text = _language_text(first_language_text)
        second_language_text = _language_text(second_language_text)
        card = card_draft_text.format(
            first_language=first_language,
            first_language_text=first_language_text,
            second_language=second_language,
            second_language_text=second_language_text,
        )
        cards += card + '\n'
    deck = deck_draft_text.format(
        deck_name=deck_name,
        cards=cards,
        first_language=first_language,
        second_language=second_language,
    )
    outunit = _fu.TextUnit.by_str(deck)
    outunit.save(outfile)

def _language_text(value, /):
    value = value.strip()
    if value == "":
        raise ValueError
    parts = value.split()
    parts = [x for x in parts if (x != "")]
    value = ' '.join(parts)
    for x in "{}\"\n\t=":
        if x in value:
            raise ValueError
    return value

def _deck_name(value, /, *, infile):
    if value is not None:
        return value
    root, filename = _os.path.split(infile)
    filelabel, ext = _os.path.splitext(filename)
    ans = filelabel.strip()
    return ans

def _first_language(value, /):
    if value is not None:
        return value
    return _get_config()['languages', 'first']

def _second_language(value, /):
    if value is not None:
        return value
    return _get_config()['languages', 'second']

def _outfile(value, /, *, infile):
    if value is not None:
        return value
    value = str(value)
    trunk, ext = _os.path.splitext(infile)
    value = trunk + ".xml"
    if value == infile:
        raise IOError
    return value

def _get_deck_draft_text():
    return _resources.read_text("ankiapp_easy_deck.drafts", "deck.txt")

def _get_card_draft_text():
    return _resources.read_text("ankiapp_easy_deck.drafts", "card.txt")

def _get_config():
    try:
        text = _resources.read_text("ankiapp_easy_deck", "config.toml")
    except FileNotFoundError:
        text = ""
    return _fu.TOMLUnit.by_str(text)

