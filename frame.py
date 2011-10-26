#! /usr/bin/python

import time;
# import sys;

HorizPageWidth = 210
HorizCount = 5
LeftMargin = 4.3
RightMargin = 4.8
# HorizSize = 38.1
HorizSize = 38.0335
HorizPitch = 40.71666
HorizGap = HorizPitch - HorizSize

VertPageLength = 297
VertCount = 13
TopMargin = 10.5
BottomMargin = 11.8
# VertSize = 21.06154
VertSize = 21.13
VertPitch = VertSize

# Transform
TranslateForPrinter = True

RefLabelsAcross = 3
RefLabelsUp = 6
RefPointX = LeftMargin + RefLabelsAcross * HorizPitch
RefPointY = TopMargin + RefLabelsUp * VertSize
# print "RefPointX=", RefPointX, "RefPointY=", RefPointY
# sys.exit(0)

# TranslateX = 3.97
# TranslateY = 10.8
TranslateX = 0 # Positive moves labels to right
TranslateY = 0   # Positive moves labels up
ScaleX = 1
ScaleY = 1

if TranslateForPrinter:
	# Reduce first number to move left
	# Reduce second number to make lower on page.
	translate = "%s mm %s mm" % (TranslateX, TranslateY)
	# Shrink (100,100) to (x, y)
	scale = "%s %s" % (ScaleX, ScaleY) 
	comment = "% "
else:
	translate = ("0 0")
	scale = ("1 1")
	comment = ""

# print LeftMargin + HorizCount * HorizPitch - HorizGap + RightMargin, HorizPageWidth
assert abs(LeftMargin + HorizCount * HorizSize + (HorizCount - 1) * HorizGap + RightMargin - HorizPageWidth) < 0.01

# print TopMargin + VertCount * VertSize + BottomMargin, VertPageLength
assert abs(TopMargin + VertCount * VertSize + BottomMargin - VertPageLength) < 0.01

def mm(x):
	return x * 360 / 127;

print """%%!PS-Adobe-2.0
%%%%Creator: "barcode", libbarcode sample frontend
%%%%DocumentPaperSizes: A4
%%%%EndComments
%%%%EndProlog

/mm { 360 mul 127 div } def

%s translate %s scale """ % (translate, scale)

print """
%%%%Page: 1 1


%% INSERT-POINT

%s50 mm 50 mm moveto 50 mm 100 mm lineto 100 mm 100 mm lineto 100 mm 50 mm lineto 50 mm 50 mm lineto stroke

%s0 0 moveto %s mm %s mm rlineto stroke""" % (comment, comment, HorizPageWidth, VertPageLength)

localtime = time.asctime( time.localtime(time.time()) )
print """/Times-Roman findfont
10 scalefont
setfont
newpath
100 mm %s 1.5 mul moveto %% as the name says, move the cursor to x y
(Date: %s t(%s, %s) s(%s, %s)) show %% ta daa A Square
closepath
stroke

0.85 setgray

""" % (TopMargin, localtime, TranslateX, TranslateY, ScaleX, ScaleY)

# Draw vertical lines
yd = VertPageLength - BottomMargin - TopMargin
for c in range(0, HorizCount):
	# Left label line
	xl = LeftMargin + c * HorizPitch
	xr = xl + HorizSize
	# print "A:", c, xl, "(%s, %s) - (%s, %s)" % (x1, y1, x2, y2)
	print "%s mm %s mm moveto 0 %s mm rlineto stroke" % (xl, TopMargin, yd)
	# Right label line
	# print "B:", c, xr, "(%s, %s) - (%s, %s)" % (x1, y1, x2, y2)
	print "%s mm %s mm moveto 0 %s mm rlineto stroke" % (xr, TopMargin, yd)

# Draw main horizontal lines
xd = HorizPageWidth - LeftMargin - RightMargin
for c in range(0, VertCount + 1):
	x1, y1 = LeftMargin, TopMargin + c * VertPitch
	# print "A:", c, xl, "(%s, %s) - (%s, %s)" % (x1, y1, x2, y2)
	print "%s mm %s mm moveto %s mm 0 rlineto stroke" % (x1, y1, xd)
	# for d in range(0, HorizCount):
		
# Draw the cut marks for the label halves
xd = -HorizGap
for c in range(0, VertCount):
	y1 = TopMargin + (c + 0.5) * VertPitch
	# print "A: c=", c, "xd=", xd, "y1=", y1
	for d in range(0, HorizCount + 1):
		x1 = LeftMargin + d * HorizPitch
		# print "B: d=", d, "x1=", x1
		xd1 = xd
		if d == 0:
			xd1 = -xd
		elif d == HorizCount:
			xd1 = xd * 3
		else:
			xd1 = xd
		print "%s mm %s mm moveto %s mm 0 rlineto stroke" % (x1, y1, xd1)

print """
showpage

%%Trailer
"""

