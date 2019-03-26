import re
import pymorphy2
def AdFilterPost(caption):
    f = open('AdFilter.txt', 'r')
    StopWords = [line.strip() for line in f]
    f.close()
    k = 0
    morph = pymorphy2.MorphAnalyzer()
    caption = morph.parse(caption)[0].normal_form
    for i in StopWords:
        result = re.findall(morph.parse(StopWords[k])[0].normal_form, str(caption))
        k += 1
        if result != []:
            AdState = "Рекламный пост"
            break
        else:
            AdState = "Не рекламный пост"
    return AdState
def AdFilterHashtag(hashtag):
    f = open('AdFilter.txt', 'r')
    StopWords = [line.strip() for line in f]
    f.close()
    AdState = None
    k = 0
    g = 0
    morph = pymorphy2.MorphAnalyzer()
    result = []
    while result == [] and k != len(StopWords):
        for i in StopWords:
            for j in range(len(hashtag)):
                hashtag[g] = morph.parse(hashtag[g])[0].normal_form
                result = re.findall(StopWords[k], str(hashtag[g]))
                g += 1
                if result != []:
                    AdState = "Рекламный пост"
                    break
                else:
                    AdState = "Не рекламный пост"
            if result != []:
                AdState = 'Рекламный пост'
                break
            g = 0
            k += 1
    return AdState
