def image(hash_to_find):
    import instaloader
    import glob
    import shutil
    import os
    import json
    shutil.rmtree('test_hash')
    #shutil.rmtree('#'+hash_to_find)

    def main_color(file):
            from PIL import Image
            import colorsys
            image = Image.open(file)
            w, hh = image.size
            ha = 0
            for x in range(w):
                for y in range(hh):
                    r, g, b = image.getpixel((x, y))
                    h,s,v=colorsys.hsv_to_rgb(r/256,g/256,b/256)
                    ha += h
            ha /= w * hh
            gg = str(round(ha, 1))[2]
            print(gg)
            if int(gg)>7:
                gg='7'
            elif gg=='0':
                gg='1'
            shutil.copy(file, "test_hash\\" + gg)
    newpath = 'test_hash'
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    for i in range(1,8):
        newpath = 'test_hash\\'+str(i)
        if not os.path.exists(newpath):
            os.makedirs(newpath)
    L = instaloader.Instaloader(post_metadata_txt_pattern='', download_pictures=False, download_geotags=False, download_comments=False, download_videos=False, download_video_thumbnails=False, compress_json=False)
    max_count = 300
    i = 0
    for post_EKB in L.get_hashtag_posts(hash_to_find):
        if post_EKB.likes > 15 and post_EKB.is_video == False and post_EKB.caption != "":
            L.download_post(post_EKB, target='#'+hash_to_find)
            User_Inf_List = [post_EKB.likes, post_EKB.comments, post_EKB.shortcode, post_EKB.owner_username] #Лайки, комменты, шорткод, никнейм
            f_Us_Inf = open('UserInf_' + str(i) +'.txt', 'w')
            for Us_inf in User_Inf_List:
                f_Us_Inf.write(str(Us_inf) + '\n')
            f_Us_Inf.close()
            pic = glob.glob('#'+hash_to_find+"\\*.json")[0]
            with open(pic, 'r') as f:
                data = json.loads(f.read())
                textt=(data['node']['thumbnail_resources'][0]['src'])
            import urllib.request
            url = textt
            er = 'pict\\'+str(i)+'.jpeg'
            urllib.request.urlretrieve(url, er)
            try:
                main_color(er)
            except:
                pass
            shutil.rmtree('#'+hash_to_find)
            i += 1
            if i == max_count:
                break
    from PIL import Image
    import glob
    img = Image.new('RGB', (1650, 1650))
    ars=[]
    for i in range(8):
        ars.append(glob.glob(f'test_hash\\{i+1}\\*.jpeg'))
        print(ars)
    for i in range(11):
        for j in range(11):
            print(ars[(i+j)//3])
            im=Image.open(ars[(i+j)//3][0])
            img.paste(im, (i*150,j*150))
            if len(ars[(i+j)//3])>1:
                ars[(i+j)//3].pop(0)
    img.show()
    img.save("out.jpg")
image('staroměstskénáměstí')
