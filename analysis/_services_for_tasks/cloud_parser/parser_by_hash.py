def give_emoji_free_text(text):
    import emoji
    allchars = [str for str in text.decode('utf-8')]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.decode('utf-8').split() if not any(i in str for i in emoji_list)])
    return clean_text
def TopicDetectorCaption(caption):
    text = caption
    topics=[]
    from rutermextract import TermExtractor
    term_extractor = TermExtractor()
    for term in term_extractor(text, limit = 3):
        print(term.normalized)
        print(term.count)
        f_tc = open('TopicWordsCaption.txt', 'a')
        f_tc.write(str(term.normalized) + " " + str(term.count) + + '\n')
        f_tc.close()
        topics.append(term.normalized)
    return topics
def commerc(haash):
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    from googletrans import Translator
    import string

    translator = Translator()
    table=str.maketrans({key: None for key in string.punctuation})
    sid = SentimentIntensityAnalyzer()

    import pymorphy2
    morph = pymorphy2.MorphAnalyzer()
    import instaloader
    advert=["надевать","дизайн","вопрос","студия","покупка","предложение","скидка","новый","этаж","ссылка","каблук","заказ","продавцы","цена","размер","приобрести","информация","заказ","наращивание","запись","заказать","купить","стоимость","наличие","примерка","доставка","адрес","продажа","инструкция"]
    L = instaloader.Instaloader(download_pictures=True, download_geotags=False, download_comments=False, download_videos=False, download_video_thumbnails=False, compress_json=False)
    likes = instaloader.Post.get_likes(L)
    EKB_id = 'old'
    max_count = 5
    ca=[]
    i = 0
    hash_to_find=haash
    for post_EKB in L.get_hashtag_posts(hash_to_find):
        if post_EKB.likes > 15 and post_EKB.is_video == False and post_EKB.caption != "":
            L.download_post(post_EKB, target=EKB_id)
            User_Inf_List = [post_EKB.likes, post_EKB.comments, post_EKB.shortcode, post_EKB.owner_username] #Лайки, комменты, шорткод, никнейм
            f_Us_Inf = open('UserInf_' + str(i) +'.txt', 'w')
            for Us_inf in User_Inf_List:
                f_Us_Inf.write(str(Us_inf) + '\n')
            f_Us_Inf.close()
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
    pol=[]
    otr=[]
    neu=[]
    for i in cap:
        wt=0
        t = give_emoji_free_text(i.encode('utf8'))
        T=TopicDetectorCaption(t)
        tt=t.translate(table)
        for ww in tt.split():
            if ww.isalpha()==False and ww!='\n':
                wt=1
        if wt!=1:
            st=translator.translate(tt).text
            ss=sid.polarity_scores(st)
            sss=sorted(ss)
            mark=float('{1}'.format(sss[0], ss[sss[0]]))
            charact.append(mark)
            print(t,T)
            if mark>0:
                for tT in T:
                    pol.append(tT)
            elif mark<0:
                for tT in T:
                    otr.append(tT)
            else:
                for tT in T:
                    neu.append(tT)
    print('compound: ', charact)
    print('compound: ', sum(charact) / len(charact))
    print(pol)
    print(otr)
    print(neu)
commerc(input())
