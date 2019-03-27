from nltk.sentiment.vader import SentimentIntensityAnalyzer
from googletrans import Translator
import emoji
import string
from rutermextract import TermExtractor
term_extractor = TermExtractor()
translator = Translator()
table=str.maketrans({key: None for key in string.punctuation})
sid = SentimentIntensityAnalyzer()
import re
def AdFilterPost(caption):
    f = open('AdFilter.txt', 'r')
    StopWords = [line.strip() for line in f]
    f.close()
    k = 0
    for i in StopWords:
        result = re.findall(StopWords[k], str(caption))
        if result != []:
            AdState = 0
            return AdState
        else:
            AdState = 1
            return AdState
        k += 1
def give_emoji_free_text(text):
    allchars = [str for str in text.decode('utf-8')]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.decode('utf-8').split() if not any(i in str for i in emoji_list)])
    return clean_text
def TopicDetectorCaption(caption):
    text =give_emoji_free_text(caption.encode('utf8'))
    topics=[]
    for term in term_extractor(text, limit = 3):
        print(term.normalized)
        print(term.count)
        f_tc = open('TopicWordsCaption.txt', 'a')
        f_tc.write(str(term.normalized) + " " + str(term.count)  + '\n')
        f_tc.close()
        topics.append(term.normalized)
    return topics
def give_emoji_free_text(text):
    allchars = [str for str in text.decode('utf-8')]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.decode('utf-8').split() if not any(i in str for i in emoji_list)])
    return clean_text
def sentiment(caption):
    charact=[]
    i=caption
    wt=0
    t=give_emoji_free_text(i.encode('utf8'))
    tt=t.translate(table)
    mark=0
    for ww in tt.split():
        if ww.isalpha()==False and ww!='\n':
            wt=1
    if wt!=1:
        st=translator.translate(tt).text
        ss=sid.polarity_scores(st)
        sss=sorted(ss)
        mark=float('{1}'.format(sss[0], ss[sss[0]]))
    return(mark)
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
import instaloader
advert=["надевать","дизайн","вопрос","студия","покупка","предложение","скидка","новый","этаж","ссылка","каблук","заказ","продавцы","цена","размер","приобрести","информация","заказ","наращивание","запись","заказать","купить","стоимость","наличие","примерка","доставка","адрес","продажа","инструкция"]
L = instaloader.Instaloader(download_pictures=True, download_geotags=False, download_comments=False, download_videos=False, download_video_thumbnails=False, compress_json=False)
likes = instaloader.Post.get_likes(L)
EKB_id = '221661431'
max_count = 50
ca=[]
i = 0
import codecs
with codecs.open('HashtagName.txt', encoding='utf-8') as fin:
    firstline=fin.readlines()[0].strip()
hash_to_find=firstline
for post_EKB in L.get_hashtag_posts(hash_to_find):
    if post_EKB.likes > 15 and post_EKB.is_video == False and post_EKB.caption != "" and AdFilterPost(post_EKB.caption)==1:
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
pol=[]
otr=[]
neu=[]
for i in cap:
            mark=sentiment(i)
            try:
                topic_l=TopicDetectorCaption(i)
                if mark==0:
                    neu.append(i)
                else:
                    for top in topic_l:
                        f_tc = open('TopicWordsCaptionSents.txt', 'a')
                        f_tc.write(top + " " + str(mark)+ '\n')
                        f_tc.close()
                    if mark<0:
                        otr.append(i)
                    else:
                        pol.append(i)
            except:
                pass
print(pol)
print(otr)
print(neu)
