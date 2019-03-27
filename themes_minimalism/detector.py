from rutermextract import TermExtractor


def get_topic_from_caption(caption: str):
    term_extractor = TermExtractor()

    themes = []
    for term in term_extractor(caption, limit=3):
        themes.append(term.normalized)

    return themes
