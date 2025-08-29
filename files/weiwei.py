import sys, os, tempfile, shutil, math
from fontTools import ttLib
from fontTools.ttLib.scaleUpem import scale_upem
from afdko import otf2otc
import argparse

def factor(n, f):
	if f==1: return n
	return int(math.floor(n*f+0.5))

def cpif(nft, mft, fac, mt=False):
	for t in ('name', 'STAT', 'fvar'):
		if t in mft and t in nft:
			nft[t]=mft[t]

	cpls=((("head"), ("fontRevision", "macStyle")), (("OS/2"), ("achVendID", "ulCodePageRange1", "fsSelection", "usWeightClass")))
	for t, v in cpls:
		if t in nft and t in mft:
			for v1 in v:
				if hasattr(nft[t], v1) and hasattr(mft[t], v1):
					setattr(nft[t], v1, getattr(mft[t], v1))
	if mt:
		skls=((("head"), ("xMin", "yMin", "xMax", "yMax")), 
		(("post"), ("underlinePosition", "underlineThickness")), 
		(("VORG"), ("defaultVertOriginY", )), 
		(("hhea"), ("ascent", "descent", "lineGap", "advanceWidthMax", "minLeftSideBearing", "minRightSideBearing", "xMaxExtent", "caretOffset")), 
		(("vhea"), ("ascent", "descent", "lineGap", "advanceHeightMax", "minTopSideBearing", "minBottomSideBearing", "yMaxExtent", "caretOffset")), 
		(("OS/2"), ("xAvgCharWidth", "ySubscriptXSize", "ySubscriptYSize", "ySubscriptXOffset", "ySubscriptYOffset", "ySuperscriptXSize", "ySuperscriptYSize", "ySuperscriptXOffset", "ySuperscriptYOffset", "yStrikeoutSize", "yStrikeoutPosition", "sTypoAscender", "sTypoDescender", "sTypoLineGap", "usWinAscent", "usWinDescent", "sxHeight", "sCapHeight")))
		for t, v in skls:
			if t in nft and t in mft:
				for v1 in v:
					if hasattr(nft[t], v1) and hasattr(mft[t], v1):
						setattr(nft[t], v1, factor(getattr(mft[t], v1), fac))

def checkftname(mfont, newft):
	if 'GSUB' in newft:
		ids=set()
		for fr in newft["GSUB"].table.FeatureList.FeatureRecord:
			if hasattr(fr.Feature, 'FeatureParams') and hasattr(fr.Feature.FeatureParams, 'FeatUILabelNameID'):
				ids.add(fr.Feature.FeatureParams.FeatUILabelNameID)
		for n1 in mfont['name'].names:
			if n1.nameID in ids: return
		for n1 in newft['name'].names:
			if n1.nameID in ids:
				mfont['name'].setName(str(n1), n1.nameID, n1.platformID, n1.platEncID, n1.langID)

def built(options):
	ifile, ofile, mfile, mt, deep=options.i, options.o, options.m, options.mt, options.deep
	ftnum=is_ttc(mfile)
	isttc=ftnum!=-1

	if isttc: mfont0=ttLib.TTFont(mfile, fontNumber=0)
	else: mfont0=ttLib.TTFont(mfile)
	ifont=ttLib.TTFont(ifile)
	upm, upi=mfont0["head"].unitsPerEm, ifont["head"].unitsPerEm
	fac=upi/upm
	if deep and upm!=upi:
		assert 'glyf' in ifont, f'File "{ifile}" does not support yet, please convert it to TTF first.'
		removehint(ifont)
		scale_upem(font=ifont, new_upem=upm)

	if isttc:
		tmp=tempfile.mktemp()
		os.mkdir(tmp)
		fileList=list()
		for i in range(ftnum):
			mfonti=ttLib.TTFont(mfile, fontNumber=i)
			ftnm='unknow'
			if mfonti['name'].getDebugName(6):
				ftnm=mfonti['name'].getDebugName(6)
			tmpfile=os.path.join(tmp, ftnm+'.ttf')
			i=1
			while tmpfile in fileList:
				tmpfile=os.path.join(tmp, ftnm+str(j)+'.ttf')
				j+=1
			fileList.append(tmpfile)
			checkftname(mfonti, ifont)
			if deep:
				dcpif(ifont, mfonti, fac)
				ifont.save(tmpfile)
			else:
				newft=ttLib.TTFont(ifile, recalcTimestamp=False, recalcBBoxes=False)
				cpif(newft, mfonti, fac, mt)
				newft.save(tmpfile)
		ttcarg=['-o', ofile]+fileList
		otf2otc.run(ttcarg)
		shutil.rmtree(tmp)
	else:
		checkftname(mfont0, ifont)
		if deep:
			dcpif(ifont, mfont0, fac)
			ifont.save(ofile)
		else:
			newft=ttLib.TTFont(ifile, recalcTimestamp=False, recalcBBoxes=False)
			cpif(newft, mfont0, fac, mt)
			newft.save(ofile)

def is_ttc(ftpath):
	with open(ftpath, 'rb') as f:
		fullhead=f.read(31)
		head=fullhead[0: 4]
		if head==b'ttcf':
			header=ttLib.sfnt.readTTCHeader(f)
			ftnum=header.numFonts
			return ftnum
	return -1

def removehint(font):
	if 'glyf' in font:
		for glyph in font['glyf'].glyphs.values():
			glyph.removeHinting()

def dcpif(ifont, mfont, fac):
	ts=('head', 'hhea', 'vhea', 'OS/2', 'name', 'STAT', 'fvar')
	for attos2 in ('sxHeight', 'sCapHeight'):
		if hasattr(ifont['OS/2'], attos2) and not hasattr(mfont['OS/2'], attos2):
			setattr(mfont['OS/2'], attos2, factor(getattr(ifont['OS/2'], attos2), 1/fac))
	for attos2 in ('usFirstCharIndex', 'usLastCharIndex', 'version', 'usDefaultChar', 'usBreakChar', 'usMaxContext'):
		if hasattr(ifont['OS/2'], attos2):
			setattr(mfont['OS/2'], attos2, getattr(ifont['OS/2'], attos2))
	mfont['hhea'].numberOfHMetrics=ifont['hhea'].numberOfHMetrics
	if 'vhea' in mfont and 'vhea' in ifont:
		mfont['vhea'].numberOfVMetrics=ifont['vhea'].numberOfVMetrics
	for t in ts:
		if t in mfont and t in ifont:
			ifont[t]=mfont[t]

def main(args=None):
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", required=True, metavar="INPUT", help="Input font")
	parser.add_argument("-o", required=True, metavar="OUTPUT", help="Output font")
	parser.add_argument("-m", required=True, metavar="MODEL", help="Model font")
	parser.add_argument("-mt", action="store_true", help="Metrics")
	parser.add_argument("-deep", action="store_true", help="Use deep")
	options = parser.parse_args(args)

	for f in (options.i, options.m):
		if not os.path.isfile(f):
			parser.error(f'Can not find file "{f}".')
	print('Process...')
	built(options)
	print('End')

if __name__ == '__main__':
	sys.exit(main())
