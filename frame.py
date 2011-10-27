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

RefLabelsAcross = 3
RefLabelsUp = 6
RefPointX = RefLabelsAcross * HorizPitch
RefPointY = (RefLabelsUp * VertSize)

### CALIBRATION

# Transform
TranslateForPrinter = True

# Last time (copy in from line at bottom of paper):
LastXTrans = -2.130 # Positive moves labels to right
LastYTrans = 0.020 # Positive moves labels up

LastXScale = 1.00199
LastYScale = 1.00051

# This time (measure these)
# X distance between left side of page and left side of grid
MeasuredXLS = 4.0565
## MeasuredXLS = LeftMargin
# Y distance between bottom of page and bottom of grid
MeasuredYLS = 9.4
##MeasuredYLS = TopMargin
# X distance between left side of grid and reference mark
##MeasuredXLStoRP = RefLabelsAcross * HorizPitch
MeasuredXLStoRP = 121.99
# Y distance between bottom of grid and reference mark
# MeasuredYLStoRP = RefLabelsUp * VertSize
MeasuredYBGtoRP = 126.84

# Calculate translate
print "%# LastXTrans=", LastXTrans, "LastYTrans=", LastYTrans
print "%# LeftMargin=", LeftMargin, "TopMargin=", TopMargin
print "%# MeasuredXLS=", MeasuredXLS, "MeasuredYLS=", MeasuredYLS
ThisXTrans = LeftMargin - MeasuredXLS
ThisYTrans = TopMargin - MeasuredYLS
print "%# ThisXTrans=", ThisXTrans, "ThisYTrans=", ThisYTrans

TranslateX = LastXTrans + ThisXTrans # Positive moves labels to right
TranslateY = LastYTrans + ThisYTrans   # Positive moves labels up
print "%# TranslateX=", TranslateX, "TranslateY=", TranslateY
print "%#"

# Calculate transform
DescaledX = MeasuredXLStoRP / LastXScale
DescaledY = MeasuredYBGtoRP / LastYScale

ScaleX = RefPointX / DescaledX
ScaleY = RefPointY / DescaledY

# ThisXScale = RefPointX / MeasuredXLStoRP
# ThisYScale = RefPointY / MeasuredYLStoRP

# ScaleX = LastXScale / ThisXScale
# ScaleY = LastYScale / ThisYScale
print "%# LastXScale=", LastXScale, "LastYScale=", LastYScale
print "%# RefPointX=", RefPointX, "RefPointY=", RefPointY
print "%# MeasuredXLStoRP=", MeasuredXLStoRP, "MeasuredYBGtoRP=", MeasuredYBGtoRP
print "%# DescaledX=", DescaledX, "DescaledY=", DescaledY
# print "%# ThisXScale=", ThisXScale, "ThisYScale=", ThisYScale
print "%# ScaleX=", ScaleX, "ScaleY=", ScaleY

if TranslateForPrinter:
	transform = "%s mm %s mm translate %s %s scale %s neg %s add mm %s neg %s add mm translate" % (LeftMargin, TopMargin, ScaleX, ScaleY, LeftMargin, TranslateX, TopMargin, TranslateY)
	comment = "% "
	# comment = ""
else:
	transform = ("% no translation")
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

%%%%Page: 1 1

0.5 setlinewidth [1 3] 0 setdash

%s mm %s mm moveto -4 mm -4 mm rlineto stroke\n""" % (LeftMargin, TopMargin)

localtime = time.asctime( time.localtime(time.time()) )
print """/Times-Roman findfont
10 scalefont
setfont
newpath
100 mm %s 2 mul moveto
(Date: %s t(%2.3f, %2.3f) s(%2.5f, %2.5f)) show
closepath
stroke

""" % (TopMargin, localtime, TranslateX, TranslateY, ScaleX, ScaleY)

print "\n%s\n" % transform

print """

[40000] 0 setdash

%% INSERT-POINT

[1 3] 0 setdash

%s50 mm 50 mm moveto 50 mm 100 mm lineto 100 mm 100 mm lineto 100 mm 50 mm lineto 50 mm 50 mm lineto stroke

%s0 0 moveto %s mm %s mm rlineto stroke""" % (comment, comment, HorizPageWidth, VertPageLength)

print "\n0.3 setgray\n"

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

# Draw the reference point
print "newpath %s mm %s mm moveto %s mm %s mm rlineto stroke" % (LeftMargin + RefPointX, TopMargin + RefPointY, -HorizGap, HorizGap)
print "newpath %s mm %s mm moveto %s mm %s mm rlineto stroke" % (LeftMargin + RefPointX, TopMargin + RefPointY, -HorizGap, -HorizGap)

print """
showpage

%%Trailer
"""

