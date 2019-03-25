from nltk.sentiment.vader import SentimentIntensityAnalyzer
from googletrans import Translator
import emoji
import string
translator = Translator()
table=str.maketrans({key: None for key in string.punctuation})
sid = SentimentIntensityAnalyzer()
def give_emoji_free_text(text):
    allchars = [str for str in text.decode('utf-8')]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.decode('utf-8').split() if not any(i in str for i in emoji_list)])
    return clean_text
def sentiment(captions):
    charact=[]
    for i in captions:
        wt=0
        t=give_emoji_free_text(i.encode('utf8'))
        tt=t.translate(table)
        for ww in tt.split():
            if ww.isalpha()==False and ww!='\n':
                wt=1
        if wt!=1:
            st=translator.translate(tt).text
            ss=sid.polarity_scores(st)
            sss=sorted(ss)
            charact.append(float('{1}'.format(sss[0], ss[sss[0]])))
    return( sum(charact) / len(charact))
#print(sentiment(cap))
