from nltk.sentiment.vader import SentimentIntensityAnalyzer
from googletrans import Translator
import emoji
translator = Translator()
table=str.maketrans({key: None for key in string.punctuation})
sid = SentimentIntensityAnalyzer()
def give_emoji_free_text(text):                                             #избавление от смайликов, т.к. иначе translator выдаёт ошибки время от времени
    allchars = [str for str in text.decode('utf-8')]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.decode('utf-8').split() if not any(i in str for i in emoji_list)])
    return clean_text
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
import instaloader
advert=["надевать","дизайн","вопрос","студия","покупка","предложение","скидка","новый","этаж","ссылка","каблук","заказ","продавцы","цена","размер","приобрести","информация","заказ","наращивание","запись","заказать","купить","стоимость","наличие","примерка","доставка","адрес","продажа","инструкция"]
L = instaloader.Instaloader(download_pictures=True, download_geotags=False, download_comments=False, download_videos=False, download_video_thumbnails=False, compress_json=False)
likes = instaloader.Post.get_likes(L)
EKB_id = '221661431'
max_count = 20
ca=[]
i = 0
for post_EKB in L.get_location_posts(location=EKB_id):
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
                if morph.parse(p.lower())[0].normal_form in advert:         #что-то вроде проверки на рекламу
                    dec=1
                if ord(p[0])!=35:                                           #проверка на то, есть ли хотя бы какой-то текста без знака '#'
                    unha+=1
        except(AttributeError):                                             #если вся подпись состоит только из смайликов, прграмма не добавляет её в список для анализа текста
            dec=1
        if dec==0 and unha!=0:
            ca.append(post_EKB.caption)                                     #при выполнении всех условий подпись добавляется в список для анализа
        if i == max_count:
            break
cap=ca
w=[]
charact=[]
for i in cap:                                                               #тут уже начинаем анализировать каждую подпись
        wt=0
        t = give_emoji_free_text(i.encode('utf8'))                          #убирает смайлики
        tt=t.translate(table)                                               #переводит текст на английский
        for ww in tt.split():
            if ww.isalpha()==False and ww!='\n':                             
                wt=1
        if wt!=1:
            st=translator.translate(tt).text
            ss=sid.polarity_scores(st)                                      #определение тоналности и её добавление к общему списку
            sss=sorted(ss)
            charact.append(float('{1}'.format(sss[0], ss[sss[0]])))
print('compound: ', charact)
print('compound: ', sum(charact) / len(charact))                            #считает среднее арифметическое тональностей