import os, sys, math
from fontTools import ttLib
from afdko import otf2otc

pydir = os.path.abspath(os.path.dirname(__file__))

TG=('msyh', 'msjh', 'mingliu', 'simsun', 'simhei', 'msgothic', 'msmincho', 'meiryo', 'malgun', 'yugoth', 'yumin', 'batang', 'gulim', 'allsans', 'allserif', 'all', 'mingliub', 'simsunb', 'deng', 'kaiu', 'simkai', 'simsunextg', 'simfang')
WT=('thin', 'extralight', 'light', 'semilight', 'demilight', 'normal', 'regular', 'medium', 'demibold', 'semibold', 'bold', 'extrabold', 'heavy', 'black', 'extrablack')
end={'Thin':'th', 'ExtraLight':'xl', 'Light':'l', 'Semilight':'sl', 'DemiLight':'dm', 'Normal':'nm', 'Regular':'', 'Medium':'md', 'Demibold':'db', 'SemiBold':'sb', 'Bold':'bd', 'ExtraBold':'xb', 'Heavy':'hv', 'Black':'bl', 'ExtraBlack':'xbl'}

def getwt(font):
	if font["head"].macStyle & (1 << 0) > 0:
		return 'Bold'
	v=font['OS/2'].usWeightClass
	if v<155: return 'Thin'
	if v<255: return 'ExtraLight'
	if v<355: return 'Light'
	if v<455: return 'Regular'
	if v<555: return 'Medium'
	if v<700: return 'SemiBold'
	if v<855: return 'ExtraBold'
	if v<950: return 'Heavy'
	return 'ExtraBlack'

def setuswt(font, wt):
	uswt={'thin':100, 'extralight':250, 'light':300, 'semilight':350, 'demilight':350, 'normal':350, 'regular':400, 'medium':500, 'demibold':600, 'semibold':600, 'bold':700, 'extrabold':800, 'heavy':900, 'black':900, 'extrablack':950}
	font['OS/2'].usWeightClass=uswt[wt]
	if wt=='bold':
		font["OS/2"].fsSelection |= 1 << 5
		font["head"].macStyle |= 1 << 0
	else:
		font["OS/2"].fsSelection &= ~(1 << 5)
		font["head"].macStyle &= ~(1 << 0)
	if wt=='regular':
		font["OS/2"].fsSelection |= 1 << 6
	else:
		font["OS/2"].fsSelection &= ~(1 << 6)

def getit(font):
	if font["head"].macStyle & (1 << 1) > 0:
		return 'y'
	return 'n'

def setit(font, isit):
	if isit:
		font["OS/2"].fsSelection |= 1 << 0
		font["head"].macStyle |= 1 << 1
	else:
		font["OS/2"].fsSelection &= ~(1 << 0)
		font["head"].macStyle &= ~(1 << 1)

def otpth(outdir, ftf):
	if outdir:
		return os.path.join(outdir, ftf)
	return ftf

def factor(n, f):
	if f==1: return n
	return int(math.floor(n*f+0.5))

def cpif(nft, mft, fac, option):
	for t in ('name', 'STAT', 'fvar'):
		if t in mft:
			nft[t]=mft[t]

	cpls=((("head"), ("fontRevision", "macStyle")), (("OS/2"), ("achVendID", "ulCodePageRange1", "fsSelection", "usWeightClass")))
	for t, v in cpls:
		if t in nft and t in mft:
			for v1 in v:
				if hasattr(nft[t], v1) and hasattr(mft[t], v1):
					setattr(nft[t], v1, getattr(mft[t], v1))

	if option.itarg=='y': setit(nft, True)
	if option.mkwt: setuswt(nft, option.tgwt.lower())

	if option.metrics:
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

def is_ttc(ftpath):
	with open(ftpath, 'rb') as f:
		fullhead=f.read(31)
		head=fullhead[0: 4]
		if head==b'ttcf':
			header=ttLib.sfnt.readTTCHeader(f)
			ftnum=header.numFonts
			return ftnum
	return -1

def covrb(mname):
	newnane=ttLib.newTable('name')
	for n1 in mname.names:
		nstr=str(n1)
		if n1.nameID==4 and 'Regular' not in nstr:
			nstr+=' Bold'
		elif n1.nameID==6 and 'Regular' not in nstr:
			nstr+='-Bold'
		elif n1.nameID in (2, 3, 4, 6, 17):
			nstr=nstr.replace('Regular', 'Bold')
		newnane.setName(nstr, n1.nameID, n1.platformID, n1.platEncID, n1.langID)
	return newnane

def covlo(mname, wt):
	newnane=ttLib.newTable('name')
	for n1 in mname.names:
		nstr=str(n1)
		if n1.nameID in (1, 3, 4, 6, 17):
			nstr=nstr.replace('Light', wt)
		newnane.setName(nstr, n1.nameID, n1.platformID, n1.platEncID, n1.langID)
	return newnane

def covro(mname, wt):
	newnane=ttLib.newTable('name')
	for n1 in mname.names:
		nstr=str(n1)
		if n1.nameID==1:
			fml=nstr.replace('Regular', '').strip()
			newnane.setName(fml, 16, n1.platformID, n1.platEncID, n1.langID)
			newnane.setName(wt, 17, n1.platformID, n1.platEncID, n1.langID)
		if n1.nameID in (1, 4) and 'Regular' not in nstr:
			nstr+=' '+wt
		elif n1.nameID==6 and 'Regular' not in nstr:
			nstr+='-'+wt
		elif n1.nameID in (1, 3, 4, 6, 17):
			nstr=nstr.replace('Regular', wt)
		newnane.setName(nstr, n1.nameID, n1.platformID, n1.platEncID, n1.langID)
	return newnane

def covit(mname):
	isbold='Bold' in mname.getDebugName(2)
	newnane=ttLib.newTable('name')
	for n1 in mname.names:
		nstr=str(n1)
		if n1.nameID==2:
			if 'Italic' in nstr: return mname
			if isbold: nstr='Bold Italic'
			else: nstr='Italic'
		elif n1.nameID in (3, 4, 17):
			nstr+=' Italic'
		elif n1.nameID==6:
			if '-' in nstr:
				nstr+='Italic'
			else:
				nstr+='-Italic'
		newnane.setName(nstr, n1.nameID, n1.platformID, n1.platEncID, n1.langID)
	return newnane

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

def build(option, outfile, mfile, cov=''):
	ftnum=is_ttc(mfile)
	isttc=ftnum!=-1

	if isttc: mfont0=ttLib.TTFont(mfile, fontNumber=0)
	else: mfont0=ttLib.TTFont(mfile)
	ifont=ttLib.TTFont(option.infile)
	upm, upi=mfont0["head"].unitsPerEm, ifont["head"].unitsPerEm
	fac=upi/upm

	if isttc:
		fileList=list()
		for i in range(ftnum):
			mfonti=ttLib.TTFont(mfile, fontNumber=i)
			if 'italic' in mfonti['name'].getDebugName(6).lower(): continue
			if cov=='rb': mfonti['name']=covrb(mfonti['name'])
			elif cov=='lo': mfonti['name']=covlo(mfonti['name'], option.tgwt)
			elif cov=='ro': mfonti['name']=covro(mfonti['name'], option.tgwt)
			if option.itarg=='y': mfonti['name']=covit(mfonti['name'])
			ftnm='unknow'
			if mfonti['name'].getDebugName(6):
				ftnm=mfonti['name'].getDebugName(6)
			tmpfile=os.path.join(option.outdir, ftnm+'.ttf')
			i=1
			while tmpfile in fileList:
				tmpfile=os.path.join(option.outdir, ftnm+str(j)+'.ttf')
				j+=1
			fileList.append(tmpfile)
			newft=ttLib.TTFont(option.infile, recalcTimestamp=False, recalcBBoxes=False)
			checkftname(mfonti, newft)
			cpif(newft, mfonti, fac, option)
			newft.save(tmpfile)
		ttcarg=['-o', outfile]+fileList
		otf2otc.run(ttcarg)
		if option.rmttf:
			for ff in fileList:
				os.remove(ff)
	else:
		mfont=ttLib.TTFont(mfile)
		newft=ttLib.TTFont(option.infile, recalcTimestamp=False, recalcBBoxes=False)
		if cov=='rb': mfont['name']=covrb(mfont['name'])
		elif cov=='lo': mfont['name']=covlo(mfont['name'], option.tgwt)
		elif cov=='ro': mfont['name']=covro(mfont['name'], option.tgwt)
		if option.itarg=='y': mfont['name']=covit(mfont['name'])
		checkftname(mfont, newft)
		cpif(newft, mfont, fac, option)
		newft.save(outfile)

def bldttcft(option, tgft):
	wt=option.tgwt
	if tgft in ['malgun', 'simhei', 'yumin', 'simsunb', 'deng', 'kaiu', 'simkai', 'simsunextg', 'simfang']:
		exname='.ttf'
	else:
		exname='.ttc'
	if tgft=='yugoth': tgft='YuGoth'
	if tgft=='deng': tgft='Deng'
	if tgft=='simsunextg': tgft='SimsunExtG'
	fed=dict()
	for w in end:
		if tgft=='YuGoth':
			if w=='Regular': fed[w]='R'
			elif w=='Bold': fed[w]='B'
			elif w=='Light': fed[w]='L'
			elif w=='Medium': fed[w]='M'
			else: fed[w]=end[w]
		elif tgft=='meiryo' and w=='Bold': fed[w]='b'
		elif tgft=='Deng' and w=='Bold': fed[w]='b'
		else: fed[w]=end[w]
	mfiler=os.path.join(pydir, f"datas/{tgft+fed['Regular']}{exname}")
	mfileb=os.path.join(pydir, f"datas/{tgft+fed['Bold']}{exname}")
	mfilel=os.path.join(pydir, f"datas/{tgft+fed['Light']}{exname}")
	mfile=os.path.join(pydir, f'datas/{tgft+fed[wt]}{exname}')
	if option.itarg=='y': itend='it'
	else: itend=''
	outfile=otpth(option.outdir, tgft+fed[wt]+itend+exname)
	option.mkwt=True
	if os.path.isfile(mfile):
		option.mkwt=False
		build(option, outfile, mfile)
	elif wt=='Bold':
		build(option, outfile, mfiler, cov='rb')
	elif os.path.isfile(mfilel):
		build(option, outfile, mfilel, cov='lo')
	else:
		build(option, outfile, mfiler, cov='ro')

class Option:
	def __init__(self):
		self.infile, self.outdir, self.tgwt, self.target=(str() for i in range(4))
		self.mkwt=True
		self.rmttf=False
		self.metrics=False
		self.itarg='a'

def parseArgs(option, args):
	extg={'yahei': 'msyh', 'jhenghei': 'msjh', 'songti': 'simsun', 'heiti': 'simhei', 'yugothic': 'yugoth', 'dengxian': 'deng', 'yumincho': 'yumin', 'gungsuh': 'batang', 'dotum': 'gulim', 'dfkai': 'kaiu', 'kaiti': 'simkai', 'mingliuextb': 'mingliub', 'simsunextb': 'simsunb', 'simsung': 'simsunextg'}
	i, argn = 0, len(args)
	while i < argn:
		arg  = args[i]
		i += 1
		if arg == "-i":
			option.infile = args[i]
			i += 1
		elif arg == "-d":
			option.outdir = args[i]
			i += 1
		elif arg == "-wt":
			option.tgwt = args[i]
			i += 1
		elif arg == "-it":
			option.itarg = args[i].lower()
			i += 1
		elif arg == "-tg":
			option.target = args[i].lower()
			if option.target in extg: option.target=extg[target]
			i += 1
		elif arg == "-r":
			option.rmttf = True
		elif arg == "-mt":
			option.metrics = True
		else:
			raise RuntimeError("Unknown option '%s'." % (arg))
	if not option.infile:
		raise RuntimeError("You must specify one input font.")
	if not os.path.isfile(option.infile):
		raise FileNotFoundError(f"Can not find file \"{option.infile}\".\n")
	if not option.target:
		raise RuntimeError(f"You must specify target.{TG}")
	elif option.target not in TG:
		raise RuntimeError(f"Unknown target \"{option.target}\"，please use {TG}.\n")
	if option.itarg not in ('a', 'y', 'n'):
		raise RuntimeError(f'Unknown italic setting "{option.itarg}"，please use "y" or "n".\n')
	if option.tgwt:
		if option.tgwt.lower() not in WT:
			raise RuntimeError(f'Unknown weight "{option.tgwt}"，please use {tuple(end.keys())}.\n')
		option.tgwt=option.tgwt.lower()
		if option.tgwt=='extralight': option.tgwt='ExtraLight'
		elif option.tgwt=='semibold': option.tgwt='SemiBold'
		elif option.tgwt=='demilight': option.tgwt='DemiLight'
		elif option.tgwt=='extrabold': option.tgwt='ExtraBold'
		elif option.tgwt=='extrablack': option.tgwt='ExtraBlack'
		else: option.tgwt=option.tgwt.capitalize()
	if option.outdir and not os.path.isdir(option.outdir):
		raise RuntimeError(f"Can not find directory \"{option.outdir}\".\n")

def run():
	option=Option()
	parseArgs(option, sys.argv[1:])
	print('Loading...')
	font=ttLib.TTFont(option.infile)
	if option.itarg=='a':
		option.itarg=getit(font)
	if not option.tgwt:
		option.tgwt=getwt(font)

	allsans=['msyh', 'msjh', 'yugoth', 'msgothic', 'meiryo', 'gulim', 'simhei', 'malgun', 'deng']
	allserif=['mingliu', 'simsun', 'msmincho', 'batang', 'yumin']
	if option.target=='all':
		tgs=allsans+allserif
	elif option.target=='allsans':
		tgs=allsans
	elif option.target=='allserif':
		tgs=allserif
	else:
		tgs=[option.target, ]
	for tgname in tgs:
		bldttcft(option, tgname)
	print('End.')

if __name__ == "__main__":
	run()
