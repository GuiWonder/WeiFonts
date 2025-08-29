import sys, os, tempfile, shutil, math
from fontTools import ttLib
from afdko import otf2otc
import argparse

def getfonts(infl):
	fts=list()
	fileob=open(infl, "rb")
	header=ttLib.sfnt.readTTCHeader(fileob)
	ftnum=header.numFonts
	fileob.close()
	for i in range(ftnum):
		fonti=ttLib.TTFont(infl, fontNumber=i)
		ps=fonti["name"].getDebugName(6)
		fts.append(ps)
		fonti.close()
	return fts

def buitotc(infile, outfile, mfile, mt):
	fileList=list()
	fonts=getfonts(mfile)
	tmp=tempfile.mktemp()
	os.mkdir(tmp)
	for i in range(len(fonts)):
		tmpfile=os.path.join(tmp, fonts[i]+'.ttf')
		buitotf(infile, tmpfile, mfile, mt, i)
		fileList.append(tmpfile)
	ttcarg=['-o', outfile]+fileList
	otf2otc.run(ttcarg)
	shutil.rmtree(tmp)

def factor(n, f):
	if f==1: return n
	return int(math.floor(n*f+0.5))

def buitotf(infile, outfile, mfile, mt, i=-1):
	fontm=ttLib.TTFont(mfile, fontNumber=i)
	ftnm=fontm["name"].getDebugName(6)
	inft=infile[ftnm.split('-')[-1]]
	newft=ttLib.TTFont(inft, recalcTimestamp=False, recalcBBoxes=False)

	for t in ('name', 'STAT', 'fvar'):
		if t in fontm:
			newft[t]=fontm[t]

	cpls=((("head"), ("fontRevision", "macStyle")), (("OS/2"), ("achVendID", "ulCodePageRange1", "fsSelection", "usWeightClass")))
	for t, v in cpls:
		if t in newft and t in fontm:
			for v1 in v:
				if hasattr(newft[t], v1) and hasattr(fontm[t], v1):
					setattr(newft[t], v1, getattr(fontm[t], v1))

	if mt:
		upm, upi=fontm["head"].unitsPerEm, newft["head"].unitsPerEm
		fac=upi/upm
		skls=((("head"), ("xMin", "yMin", "xMax", "yMax")), 
		(("post"), ("underlinePosition", "underlineThickness")), 
		(("VORG"), ("defaultVertOriginY", )), 
		(("hhea"), ("ascent", "descent", "lineGap", "advanceWidthMax", "minLeftSideBearing", "minRightSideBearing", "xMaxExtent", "caretOffset")), 
		(("vhea"), ("ascent", "descent", "lineGap", "advanceHeightMax", "minTopSideBearing", "minBottomSideBearing", "yMaxExtent", "caretOffset")), 
		(("OS/2"), ("xAvgCharWidth", "ySubscriptXSize", "ySubscriptYSize", "ySubscriptXOffset", "ySubscriptYOffset", "ySuperscriptXSize", "ySuperscriptYSize", "ySuperscriptXOffset", "ySuperscriptYOffset", "yStrikeoutSize", "yStrikeoutPosition", "sTypoAscender", "sTypoDescender", "sTypoLineGap", "usWinAscent", "usWinDescent", "sxHeight", "sCapHeight")))
		for t, v in skls:
			if t in newft and t in fontm:
				for v1 in v:
					if hasattr(newft[t], v1) and hasattr(fontm[t], v1):
						setattr(newft[t], v1, factor(getattr(fontm[t], v1), fac))

	newft.save(outfile)
	newft.close()
	fontm.close()

def main(args=None):
	parser = argparse.ArgumentParser()
	parser.add_argument("-o", required=True, metavar="OUTPUT", help="Output font")
	parser.add_argument("-f1", required=True, metavar="Regular")
	parser.add_argument("-f2", required=True, metavar="Medium")
	parser.add_argument("-f3", required=True, metavar="Semibold")
	parser.add_argument("-f4", required=True, metavar="Light")
	parser.add_argument("-f5", required=True, metavar="Thin")
	parser.add_argument("-f6", required=True, metavar="Ultralight")
	parser.add_argument("-mt", action="store_true", help="Metrics")
	options = parser.parse_args(args)
	infiles={'Regular': options.f1, 'Medium': options.f2, 'Semibold': options.f3, 'Light': options.f4, 'Thin': options.f5, 'Ultralight': options.f6}
	for f in infiles.values():
		if not os.path.isfile(f):
			parser.error(f'Can not find file "{f}".')
	mfile=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'names/pingfang.ttc')
	assert os.path.isfile(mfile)
	print('Process...')
	buitotc(infiles, options.o, mfile, options.mt)
	print('End')

if __name__ == '__main__':
	sys.exit(main())
