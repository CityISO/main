# *** TODO ***

import pymorphy2
import instaloader
advert = ["надевать","дизайн","вопрос","студия","покупка","предложение","скидка","новый","этаж","ссылка","каблук","заказ","продавцы","цена","размер","приобрести","информация","заказ","наращивание","запись","заказать","купить","стоимость","наличие","примерка","доставка","адрес","продажа","инструкция"]
L = instaloader.Instaloader(download_pictures=False, download_geotags=False, download_comments=False, download_videos=False, download_video_thumbnails=False, compress_json=False)
likes = instaloader.Post.get_likes(L)
city_id = input('Enter location id: ')
max_count = int(input('Max count: '))
ca = []

def parser():
    i = 0
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    from googletrans import Translator
    import emoji
    import string
    from rutermextract import TermExtractor
    term_extractor = TermExtractor()
    translator = Translator()
    table=str.maketrans({key: None for key in string.punctuation})
    sid = SentimentIntensityAnalyzer()
    def give_emoji_free_text(text):
        allchars = [str for str in text.decode('utf-8')]
        emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
        clean_text = ' '.join([str for str in text.decode('utf-8').split() if not any(i in str for i in emoji_list)])
        return clean_text
    def TopicDetectorCaption(caption):
        text = caption
        for term in term_extractor(text, limit = 3):
            f_tc = open(f'{city_id}_topic_words.txt', 'a')
            f_tc.write((str(term.normalized) + '\n') * term.count)
            f_tc.close()
    morph = pymorphy2.MorphAnalyzer()
    
    for post_EKB in L.get_location_posts(location=city_id):
        if post_EKB.likes > 15 and not post_EKB.is_video and post_EKB.caption != "":
            L.download_post(post_EKB, target=city_id)
            i += 1
            pc = round(int(i) / max_count * 100)
            print(f'Downloading {pc}% ({i}/{max_count}', end='\r')
            dec = 0
            unha = 0
            try:
                for p in post_EKB.caption.split():
                    if morph.parse(p.lower())[0].normal_form in advert:
                        dec = 1
                    if ord(p[0]) != 35:
                        unha += 1
            except(AttributeError):
                dec = 1
            if not dec and unha:
                ca.append(post_EKB.caption)
            if i == max_count:
                break
    cap = ca
    w = []
    charact = []
    i = 0
    for i in cap:
            wt = 0
            pc = round(i / max_count * 100)
            print(f'Parsing topic {pc}% ({i}/{max_count}', end='\r')
            t = give_emoji_free_text(i.encode('utf8'))
            TopicDetectorCaption(t)
            tt = t.translate(table)
            for ww in tt.split():
                if not ww.isalpha() and ww != '\n':
                    wt = 1
            if wt != 1:
                st = translator.translate(tt).text
                ss = sid.polarity_scores(st)
                sss = sorted(ss)
                charact.append(float('{1}'.format(sss[0], ss[sss[0]])))
    print('... done')
if __name__ == '__main__':
    parser()
