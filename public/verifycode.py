from django.http import HttpResponse


def verify_code(request):
    from PIL import Image, ImageDraw, ImageFont
    import random
    bgcolor = (random.randrange(40, 200), random.randrange(40, 200), 255)
    width = 200
    height = 40
    im = Image.new('RGB', (width, height), bgcolor)
    draw = ImageDraw.Draw(im)
    for i in range(100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill)

    str1 = 'ABCDEFG123HIGKLMN456OPQRST789UVWXYZ'
    code = ''
    for i in range(4):
        code += str1[random.randrange(0, len(str1))]
    # font = ImageFont.load_default().font
    font = ImageFont.truetype(r'C:\Windows\Fonts\Arial.ttf', size=23)
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    draw.text((20, 10), code[0], font=font, fill=fontcolor)
    draw.text((70, 10), code[1], font=font, fill=fontcolor)
    draw.text((120, 10), code[2], font=font, fill=fontcolor)
    draw.text((170, 10), code[3], font=font, fill=fontcolor)
    del draw
    request.session['verify_code'] = code

    import io
    buf = io.BytesIO()
    im.save(buf, 'png')
    return HttpResponse(buf.getvalue(), 'image/png')
