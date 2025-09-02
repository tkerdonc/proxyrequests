#!/usr/bin/python3

import sys
import os
import numpy as np
import random
from PIL import ExifTags
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import json

OUT_EXT = ".jpg"
OUT_BASENAME = "proxy_request_"
font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 32)
caption_font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf", 64)
HEADER_FONT = "/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf"
lspacing = 10

def hLayout(inputs, outpath, headers = [], font_size=32):

    font = ImageFont.truetype(HEADER_FONT, font_size)

    images = openImages(inputs)
    out_h = min([u.size[1] for u in images])

    # Resize the images to have all the same height
    for im in images:
        w, h = im.size
        ratio = float(out_h) / h
        im.thumbnail((int(im.size[0] * ratio), int(im.size[1] * ratio)), Image.ANTIALIAS)

    out_w = np.sum([u.size[0] for u in images])

    #Insert carriage returns in order for each sentence to fit onscreen
    newHeaders = {}
    for h in headers:
        headerText = h.upper() + ' : '
        text = headerText
        currentText = headerText
        words = headers[h].split(' ')
        for w in words:
            if font.getsize(currentText + ' ' + w)[0] > out_w * 0.9:
                text += '\n'
                currentText = ''
            else:
                text += ' '
                currentText += ' '
            text += w
            currentText += w
        newHeaders[h] = text[len(headerText):]

    headers = newHeaders

    for h in headers:
        lineCount = headers[h].count('\n') + 1
        out_h += font.getsize(h)[1] * lineCount
        out_h += lspacing

    out_h += lspacing

    output = Image.new("RGB", (out_w, out_h))
    draw = ImageDraw.Draw(output)

    curY = lspacing
    curX = 0
    for h in headers:
        text = h.upper() + ' : ' + headers[h]
        draw.text((0.05 * out_w, curY),text,(255,255,255),font=font)
        _, caph = font.getsize(text)
        lineCount = headers[h].count('\n') + 1
        curY += caph * lineCount
        curY += lspacing

    for imIdx, im in enumerate(images):
        w, h = im.size
        output.paste(im, (int(curX), curY))
        curX += w

    output.save(outpath)

def openImages(paths):
    retval = []
    for img in [Image.open(f) for f in paths]:
        if img._getexif() is not None:
            exif=dict(
                (ExifTags.TAGS[k], v)
                for k, v in img._getexif().items()
                if k in ExifTags.TAGS
            )
            flag = exif['Orientation']
            newImage = None
            if flag == 1:
                #newImage = img.rotate(-180, expand=True)
                newImage = img
            elif flag == 6:
                newImage = img.rotate(-90, expand=True)
            else:
                print ("Unsupported Orientation " + str(flag))
                sys.exit(1)

            retval.append(newImage)
        else:
            retval.append(img)

    return retval


root = sys.argv[1]
folders = [
            os.path.join(root, item)
            for item in os.listdir(root)
            if os.path.isdir(os.path.join(root, item))
]

for folder in sorted(folders):

    inF = open(os.path.join(folder, "data.json"), 'r')
    data = json.load(inF)
    extra_images = []
    if "extra_images" in data:
        extra_images = data["extra_images"]
    font_size = 35
    if "font_size" in data:
        font_size = data["font_size"]

    filepaths = [
        os.path.join(folder, img)
        for img in ["1.jpg", "2.jpg"] + extra_images
    ]

    text = ""
    headers = {}
    if 'model' in data:
        headers["Datasheet"] = data['model']
    if 'notes' in data and len(data['notes']) > 0:
        headers["notes"] = data['notes']

    out_name = OUT_BASENAME + "_" + data['model'] + OUT_EXT
    hLayout(filepaths, out_name, headers=headers, font_size=font_size)
