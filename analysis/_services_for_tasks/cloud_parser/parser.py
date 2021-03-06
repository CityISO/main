def parser():
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
            print(term.normalized)
            print(term.count)
            f_tc = open('TopicWordsCaption.txt', 'a')
            f_tc.write((str(term.normalized) + '\n') * term.count)
            f_tc.close()
            #topics.append(term.normalized)
    #def TopicDetectorHashtag(hashtag):
    #    from rutermextract import TermExtractor
    #    term_extractor = TermExtractor()
    #    text = hashtag
    #    for term in term_extractor(text, limit=3):
    #        print(term.normalized)
    #        print(term.count)
    #        f_th = open('TopicWordsHashTag.txt', 'a')
    #        f_th.write(str(term.normalized) + " " + str(term.count) + '\n')
    #        f_th.close()
    import pymorphy2
    morph = pymorphy2.MorphAnalyzer()
    import instaloader
    advert=["надевать","дизайн","вопрос","студия","покупка","предложение","скидка","новый","этаж","ссылка","каблук","заказ","продавцы","цена","размер","приобрести","информация","заказ","наращивание","запись","заказать","купить","стоимость","наличие","примерка","доставка","адрес","продажа","инструкция"]
    L = instaloader.Instaloader(download_pictures=False, download_geotags=False, download_comments=False, download_videos=False, download_video_thumbnails=False, compress_json=False)
    likes = instaloader.Post.get_likes(L)
    EKB_id = '221661431'
    max_count = 10
    ca=[]
    i = 0
    for post_EKB in L.get_location_posts(location=EKB_id):
        if post_EKB.likes > 15 and post_EKB.is_video == False and post_EKB.caption != "":
            L.download_post(post_EKB, target=EKB_id)
            User_Inf_List = [post_EKB.likes, post_EKB.comments, post_EKB.shortcode, post_EKB.owner_username] #Лайки, комменты, шорткод, никнейм
            # f_Us_Inf = open('UserInf_' + str(i) +'.txt', 'w')
            # for Us_inf in User_Inf_List:
            #     f_Us_Inf.write(str(Us_inf) + '\n')
            # f_Us_Inf.close()
            i += 1
            dec=0
            unha=0
            try:
                for p in post_EKB.caption.split():
                    if morph.parse(p.lower())[0].normal_form in advert:
                        dec=1
                    if ord(p[0])!=35:
                        unha+=1
            except(AttributeError):
                dec=1
            if dec==0 and unha!=0:
                ca.append(post_EKB.caption)
            if i == max_count:
                break
    cap=ca
    w=[]
    charact=[]
    for i in cap:
            wt=0
            t = give_emoji_free_text(i.encode('utf8'))
            TopicDetectorCaption(t)
            tt=t.translate(table)
            for ww in tt.split():
                if ww.isalpha()==False and ww!='\n':
                    wt=1
            if wt!=1:
                st=translator.translate(tt).text
                ss=sid.polarity_scores(st)
                sss=sorted(ss)
                charact.append(float('{1}'.format(sss[0], ss[sss[0]])))
    #zeros=charact.count(0.0)
    #dell=len(charact)
    print('compound: ', charact)
    print('compound: ', sum(charact) / len(charact))
    #except(ZeroDivisionError):
     #   print('compound: 0.0')
if __name__ == '__main__':
    parser()
