d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

# Read the whole text.
text = open(path.join(d, 'somewords.txt')).read()

# read the mask image
# taken from
# http://www.stencilry.org/stencils/movies/alice%20in%20wonderland/255fk.jpg
alice_mask = np.array(Image.open(path.join(d, "logo.png")))

#stopwords = set(STOPWORDS)
#stopwords.add("said")

wc = WordCloud(background_color="white", max_words=2000, mask=alice_mask,
                contour_width=1, contour_color='white')

# generate word cloud
wc.generate(text)

# store to file
wc.to_file(path.join(d, "alice.png"))

default_colors = wc.to_array()
plt.title("Custom colors")
plt.imshow(wc.recolor(colormap='bone', random_state=3),
           interpolation="bilinear")
# show
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
#plt.figure()
#plt.imshow(alice_mask, cmap=plt.cm.gray, interpolation='bilinear')
# plt.axis("off")
plt.show()
