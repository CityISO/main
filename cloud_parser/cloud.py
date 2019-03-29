def cloud(file):
    import os
    from os import path
    from wordcloud import WordCloud
    # get data directory (using getcwd() is needed to support running example in generated IPython notebook)
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    # Read the whole text.
    text = open(path.join(d,  file)).read()
    # Generate a word cloud image
    wordcloud = WordCloud(background_color='white',width=1600, height=800).generate(text)
    # Display the generated image:
    # the matplotlib way:
    import matplotlib.pyplot as plt
    plt.imshow(wordcloud, interpolation='bilinear')
    #     plt.axis("off")
    # lower max_font_size
    # wordcloud = WordCloud(max_font_size=40).generate(text)
    # plt.figure()
    # plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    plt.savefig('plt.png')
    # The pil way (if you don't have matplotlib)
    # image = wordcloud.to_image()
    # image.show()
cloud('somewords.txt')
