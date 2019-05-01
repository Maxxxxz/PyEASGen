from PIL import ImageFilter, Image, ImageDraw, ImageFont
import subprocess
import random

W = 1280
H = 720

#thanks github https://gist.github.com/glenrobertson/2288152
def get_white_noise_image(width=1280, height=720):
    pil_map = Image.new("RGBA", (width, height), 255)
    random_grid = map(lambda x: (
            int(random.random()*20),
            int(random.random()*30),
            int(random.random()*40)
        ), [0] * width * height)
    pil_map.putdata(list(random_grid), 2, 0)
    return pil_map

def createNoiseImage():
    img = get_white_noise_image(W, H)
#    img.save("image.png", "PNG")
    msg = "NATIONAL ALERT"
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("‪C:\\Windows\\Fonts\\VCR_OSD_MONO_1.001.ttf", 45)
    w, h = draw.textsize(msg, font)
    wOff = random.randrange(-5, 5)
    hOff = random.randrange(-5, 5)
    draw.text((((W - w) / 2) + wOff, 30 + hOff), msg, fill=(117, 117, 117), font=font)
    return img

def createImages(msgList):
    i = 0

    img = createNoiseImage()
    font = ImageFont.truetype("‪C:\\Windows\\Fonts\\VCR_OSD_MONO_1.001.ttf", 25)
    img.save("test.png", "PNG")
    for msg in msgList:
        for line in msg:
            img = createNoiseImage()
            draw = ImageDraw.Draw(img)
            w, h = draw.textsize(line, font)
            wOff = random.randrange(-5, 5)
            hOff = random.randrange(-5, 5)
            draw.text((((W-w)/2) + wOff, ((H-h)/2) + hOff), line, fill=(117, 117, 117), font=font)
            img.save("image{}.png".format(i), "PNG")
            i += 1

def createVideo(length):
                            ##MANUALLY CHANGE -r # to 6*length. subprocess.call does not like formatting for some reason
    subprocess.call("ffmpeg -framerate 1/6 -i image%01d.png -r 30 aOut.mp4")
    subprocess.call("ffmpeg -i aOut.mp4 -i EASfakeheader.mp3 -af apad -shortest bOut.mp4", shell=True)
    subprocess.call("ffmpeg -i bOut.mp4 -vf \"movie=aOut.mp4,scale=1280:720[m];"
                    " [in][m]overlay=y='3*sin(200.65*n)':x='2*cos(100.34*n)' \""
                    " cOut.mp4", shell=True)
    subprocess.call("ffmpeg -i cOut.mp4 -codec:v huffyuv -bsf:v noise=3500000 -s 960x540 dOut.mkv", shell=True)
    subprocess.call("ffmpeg -i dOut.mkv -codec:v libx264 -crf 38 FINALOut.mp4", shell=True)

def main():
    msgList =   [[
        "Emergency Alert System\n"
        "   Emergenecy Action\n"
        "     Notification",
        "USSF has been compromised",
        "More information will become available soon.",
        "Stay indoors.",
                ]]

    length = msgList.__len__()
    createImages(msgList)
    createVideo(length*6)

if __name__ == "__main__":
    main()

