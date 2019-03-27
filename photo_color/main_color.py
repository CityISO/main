def main_color(files):
    from PIL import Image
    rl=[]
    gl=[]
    bl=[]
    for file in files:
        image = Image.open(file)
        w, h = image.size
        pixel = []
        for x in range(w):
            for y in range(h):
                r, g, b = image.getpixel((x, y))
                pixel.append([r, g, b])
        print(pixel)
        avr = [sum(x)//len(x) for x in zip(*pixel)]
        rl.append(avr[0])
        gl.append(avr[1])
        bl.append(avr[2])
    return [sum(rl)//len(rl),sum(gl)//len(gl),sum(bl)//len(bl)]
#print(main_color(['137aa5dc30d7e4c9ede9fd64edd7300a.jpeg']))
