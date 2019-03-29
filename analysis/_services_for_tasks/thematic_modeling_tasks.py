from datetime import datetime
import itertools
import binascii

from celery import shared_task
from rutermextract import TermExtractor

from instagram_parser.models import InstagramPost

from analysis.models import InstagramPostsThemesByDate

MAX_SYMBOLS_FOR_TOPIC = 15

@shared_task
def generate_save_themes_by_city_from_date_to_date(city_id: int, from_date_str: str, to_date_str: str) -> None:
    from_date = datetime.fromisoformat(from_date_str)
    to_date = datetime.fromisoformat(to_date_str)

    posts = InstagramPost.objects.filter(processed=True, is_ad=False, city_id=city_id,
                                         timestamp__gt=from_date, timestamp__lt=to_date)

    themes = [_detect_topic_from_caption(post.text) for post in posts]

    filtered = _finish_check(list(itertools.chain(*themes)))

    InstagramPostsThemesByDate.objects.create(date_start=from_date, date_end=to_date,
                                              city_id=city_id, themes=",".join(filtered))


def _detect_topic_from_caption(caption: str) -> list:
    term_extractor = TermExtractor()

    themes = []
    for term in term_extractor(caption, limit=3):
        if len(term.normalized) <= MAX_SYMBOLS_FOR_TOPIC:
            themes.append(term.normalized)

    return themes


def _canonize(source):
        stop_symbols = '.,!?:;-\n\r()'
        stop_words = (u'это', u'как', u'так',u'и', u'в', u'над',u'к', u'до', u'не',u'на', u'но', u'за',u'то', u'с', u'ли',u'а', u'во', u'от',u'со', u'для', u'о',u'же', u'ну', u'вы',u'бы', u'что', u'кто',u'он', u'она')
        return [x for x in [y.strip(stop_symbols) for y in source.lower().split()] if x and (x not in stop_words)]


def _genshingle(source):
    shingle_len = 1
    out = []
    for i in range(len(source)-(shingle_len-1)):
        out.append(binascii.crc32(' '.join( [x for x in source[i:i+shingle_len]] ).encode('utf-8')))
    return out


def _compare(source1, source2):
    same = 0
    for i in range(len(source1)):
        if source1[i] in source2:
            same = same + 1
    return same*2/float(len(source1) + len(source2))*100


def _finish_check(themes: list):

    for text1 in themes:
        for text2 in themes:
            if text1 != text2:
                cmp1 = _genshingle(_canonize(text1))
                cmp2 = _genshingle(_canonize(text2))

                if _compare(cmp1, cmp2) > 66:
                    try:
                        themes.remove(text1)
                    except ValueError:
                        pass

    return themes


__all__ = (
    'generate_save_themes_by_city_from_date_to_date',
)
