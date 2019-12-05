from PIL import Image
from sys import argv
import subprocess
def getMaxPixelVal(im):
    maxVal = 0
    for i in range(im.size[1]):
        for j in range(im.size[0]):
            r,g,b = im.getpixel((j,i))
            val = (r+g+b)/3
            if val > maxVal:
                maxVal = val
    return float(maxVal)
filename = argv[1]
isColor = argv[2] in ["True", "true"]
im = Image.open(filename)
im = im.convert('RGB')
ps = open(filename.split(".")[0] + ".ps", "w")
MAX_WIDTH = 370
width, height = im.size
if width > MAX_WIDTH:
    ratio = height / width
    newHeight = int(ratio * MAX_WIDTH)
    im = im.resize((MAX_WIDTH, newHeight), Image.ANTIALIAS)
maxVal = getMaxPixelVal(im)
greyScale = " .'`^-\",:;!i<~+?[{1|/roxnz&Q0OM$8B@"
increment = (len(greyScale)-1) / maxVal
ps.write("%!PS\n")
ps.write("90 rotate")
ps.write("/Courier findfont\n")
ps.write("4 scalefont\n")
ps.write("setfont\n")
ps.write("newpath\n")
xVal = 10
yVal = -10
DELTA = 2
numPrinted = 0
negative = False
for i in range(im.size[0]):
    for j in range(im.size[1]):
        ps.write(str(xVal) + " " + str(yVal) + " " + "moveto\n")
        numPrinted += 1
        yVal -= DELTA
        if numPrinted >= im.size[1]:
            numPrinted = 0
            xVal += DELTA
            yVal = -10
        r,g,b = im.getpixel((i,j))
        val = (r+g+b)/3
        if negative:
            r = 255 - r
            g = 255 - g
            b = 255 - b
        else:
            val = maxVal - val
        index = int(val * increment)
        char = greyScale[index]
        if not isColor:
            r,g,b = 255,255,255
        else:
            r = float(r) / 255
            g = float(g) / 255
            b = float(b) / 255
        ps.write(f"{r} {g} {b} setrgbcolor\n")
        ps.write("("+char+")" + " show\n")
        ps.write("stroke\n")
ps.write("showpage")
