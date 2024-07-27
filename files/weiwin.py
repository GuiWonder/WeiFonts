import os, json, tempfile, gc, sys, shutil
from fontTools import ttLib

'''otc'''
import struct
class FontEntry:
	def __init__(self, sfntType, searchRange, entrySelector, rangeShift):
		self.sfntType = sfntType
		self.searchRange = searchRange
		self.entrySelector = entrySelector
		self.rangeShift = rangeShift
		self.tableList = []
	def append(self, tableEntry):
		self.tableList.append(tableEntry)
	def getTable(self, tableTag):
		for tableEntry in self.tableList:
			if tableTag == tableEntry.tag:
				return tableEntry
		raise KeyError("Failed to find tag: " + tableTag)
	def __str__(self):
		dl = [ "fontEntry sfntType: %s, numTables: %s." % (self.sfntType, len(self.tableList) )]
		for table in self.tableList:
			dl.append(str(table))
		dl.append("")
		return os.linesep.join(dl)
	def __repr__(self):
		return str(self)
class TableEntry:
	def __init__(self, tag, checkSum, length):
		self.tag = tag
		self.checksum = checkSum
		self.length = length
		self.data = None
		self.offset = None
		self.isPreferred = False
	def __str__(self):
		return "Table tag: %s, checksum: %s, length %s." % (self.tag, self.checksum, self.length )
	def __repr__(self):
		return str(self)
ttcHeaderFormat = ">4sLL"
ttcHeaderSize = struct.calcsize(ttcHeaderFormat)
offsetFormat = ">L"
offsetSize = struct.calcsize(">L")
sfntDirectoryFormat = ">4sHHHH"
sfntDirectorySize = struct.calcsize(sfntDirectoryFormat)
sfntDirectoryEntryFormat = ">4sLLL"
sfntDirectoryEntrySize = struct.calcsize(sfntDirectoryEntryFormat)
def readFontFile(fontPath):
	fontEntryList = []
	with open(fontPath, "rb") as fp:
		data = fp.read()
	# See if this is a OTC file first.
	TTCTag, version, numFonts = struct.unpack(ttcHeaderFormat, data[:ttcHeaderSize])
	if TTCTag != b'ttcf':
		# it is a regular font.
		fontEntry = parseFontFile(0, data)
		fontEntryList.append(fontEntry)
	else:
		offsetdata = data[ttcHeaderSize:]
		i = 0
		while i < numFonts:
			offset = struct.unpack(offsetFormat, offsetdata[:offsetSize])[0]
			fontEntry = parseFontFile(offset, data)
			fontEntryList.append(fontEntry)
			offsetdata = offsetdata[offsetSize:]
			i += 1
	return fontEntryList
def parseFontFile(offset, data):
	sfntType, numTables, searchRange, entrySelector, rangeShift = struct.unpack(sfntDirectoryFormat, data[offset:offset+sfntDirectorySize])
	fontEntry = FontEntry(sfntType, searchRange, entrySelector, rangeShift)
	curData = data[offset+sfntDirectorySize:]
	i = 0
	while i < numTables:
		tag, checkSum, offset, length = struct.unpack(sfntDirectoryEntryFormat, curData[:sfntDirectoryEntrySize])
		tableEntry = TableEntry(tag, checkSum, length)
		tableEntry.data = data[offset:offset+length]
		fontEntry.append(tableEntry)
		curData =  curData[sfntDirectoryEntrySize:]
		i += 1
	return fontEntry
def writeTTC(fontList, tableList, ttcFilePath):
	numFonts = len(fontList)
	header = struct.pack(ttcHeaderFormat, b'ttcf', 0x00010000,  numFonts)
	dataList = [header]
	fontOffset = ttcHeaderSize + numFonts*struct.calcsize(">L")
	for fontEntry in fontList:
		dataList.append(struct.pack(">L",fontOffset))
		fontOffset += sfntDirectorySize + len(fontEntry.tableList)*sfntDirectoryEntrySize
	# Set the offsets in the tables.
	for tableEntryList in tableList:
		for tableEntry in tableEntryList:
			tableEntry.offset = fontOffset
			paddedLength = (tableEntry.length + 3) & ~3
			fontOffset += paddedLength
	# save the font sfnt directories
	for fontEntry in fontList:
		data = struct.pack(sfntDirectoryFormat, fontEntry.sfntType, len(fontEntry.tableList), fontEntry.searchRange, fontEntry.entrySelector, fontEntry.rangeShift)
		dataList.append(data)
		for tableEntry in fontEntry.tableList:
			data = struct.pack(sfntDirectoryEntryFormat, tableEntry.tag, tableEntry.checksum, tableEntry.offset, tableEntry.length)
			dataList.append(data)
	# save the tables.
	for tableEntryList in tableList:
		for tableEntry in tableEntryList:
			paddedLength = (tableEntry.length + 3) & ~3
			paddedData = tableEntry.data + b"\0" * (paddedLength - tableEntry.length)
			dataList.append(paddedData)
	
	fontData = b"".join(dataList)
	
	with open(ttcFilePath, "wb") as fp:
		fp.write(fontData)
	return
def runottf2otf(fileList, ttcFilePath):
	tagOverrideMap={}
	print("TTC fonts:", str(len(fileList))+' fonts.')
	fontList = []
	tableMap = {}
	tableList = []
	# Read each font file into a list of tables in a fontEntry
	for fontPath in fileList:
		fontEntryList = readFontFile(fontPath)
		fontList += fontEntryList
	# Add the fontEntry tableEntries to tableList.
	for fontEntry in fontList:
		tableIndex = 0
		numTables = len(fontEntry.tableList)
		while tableIndex < numTables:
			tableEntry = fontEntry.tableList[tableIndex]
			try:
				fontIndex = tagOverrideMap[tableEntry.tag]
				tableEntry = fontList[fontIndex].getTable(tableEntry.tag)
				fontEntry.tableList[tableIndex] = tableEntry
			except KeyError:
				pass
			try:
				tableEntryList = tableMap[tableEntry.tag]
				matched = 0
				for tEntry in tableEntryList:
					if (tEntry.checksum == tableEntry.checksum) and (tEntry.length == tableEntry.length) and (tEntry.data == tableEntry.data):
						matched = 1
						fontEntry.tableList[tableIndex] = tEntry
						break
				if not matched:
					tableEntryList.append(tableEntry)
			except KeyError:
				tableEntryList = [tableEntry]
				tableMap[tableEntry.tag] = tableEntryList
				tableList.insert(tableIndex, tableEntryList)
			tableIndex += 1
	writeTTC(fontList, tableList, ttcFilePath)
	print("Output font:", ttcFilePath)
	# report which tabetablesls are shared.
	sharedTables = []
	unSharedTables = []
	for tableEntryList in tableList:
		if len(tableEntryList) > 1:
			unSharedTables.append(tableEntryList[0].tag.decode('ascii'))
		else:
			sharedTables.append(tableEntryList[0].tag.decode('ascii'))
	if len(sharedTables) == 0:
		print("No tables are shared")
	else:
		print("Shared tables: %s" % repr(sharedTables))
	if len(unSharedTables) == 0:
		print("All tables are shared")
	else:
		print("Un-shared tables: %s" % repr(unSharedTables))
	print("Done")
'''otc'''

pydir = os.path.abspath(os.path.dirname(__file__))

outd=str()
it='a'
rmttf=False

TG= ('msyh', 'msjh', 'mingliu', 'simsun', 'simhei', 'msgothic', 'msmincho', 'meiryo', 'malgun', 'yugoth', 'yumin', 'batang', 'gulim', 'allsans', 'allserif', 'all', 'mingliub', 'simsunb')
WT=('thin', 'extralight', 'light', 'semilight', 'demilight', 'normal', 'regular', 'medium', 'demibold', 'semibold', 'bold', 'black', 'heavy')
end={'Thin':'th', 'ExtraLight':'xl', 'Light':'l', 'Semilight':'sl', 'DemiLight':'dm', 'Normal':'nm', 'Regular':'', 'Medium':'md', 'Demibold':'db', 'SemiBold':'sb', 'Bold':'bd', 'Black':'bl', 'Heavy':'hv'}

def getwt(font):
	if font["head"].macStyle & (1 << 0) > 0:
		return 'Bold'
	wtn={250:'ExtraLight', 300:'Light', 350:'Normal', 400:'Regular', 500:'Medium', 600:'SemiBold', 900:'Heavy'}
	wtc=font['OS/2'].usWeightClass
	if wtc<300:
		return wtn[250]
	if wtc in wtn:
		return wtn[wtc]
	return 'Regular'

def setuswt(font, wt):
	uswt={'thin':100, 'extralight':250, 'light':300, 'semilight':350, 'demilight':350, 'normal':350, 'regular':400, 'medium':500, 'demibold':600, 'semibold':600, 'bold':700, 'black':900, 'heavy':900}
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
		

def getver(nmo):
	for n1 in nmo:
		if n1['languageID']==1033 and n1['nameID']==5:
			return n1['nameString'].split(' ')[-1]
	return 1

def otpth(ftf):
	if outd:
		return os.path.join(outd, ftf)
	return ftf

def wtbuil(nml, wt):
	nwtnm=list()
	for n1 in nml:
		n2=dict(n1)
		if n2['nameID'] in (1, 3, 4, 6, 17):
			n2['nameString']=n2['nameString'].replace('Light', wt)
		nwtnm.append(n2)
	return nwtnm

def itbuil(nms):
	nwtnm=list()
	isbold=False
	for n1 in nms:
		if n1['nameID']==2 and 'Bold' in n1['nameString']:
			isbold=True
			break
	for n1 in nms:
		n2=dict(n1)
		if n2['nameID']==2:
			if 'Italic' in n2['nameString']:
				return nms
			if isbold:
				n2['nameString']='Bold Italic'
			else:
				n2['nameString']='Italic'
		elif n2['nameID'] in (3, 4, 17):
			n2['nameString']+=' Italic'
		elif n2['nameID']==6:
			if '-' in n2['nameString']:
				n2['nameString']+='Italic'
			else:
				n2['nameString']+='-Italic'
		nwtnm.append(n2)
	return nwtnm

def toname(nmls):
	newnane=ttLib.newTable('name')
	for nm in nmls:
		newnane.setName(nm['nameString'], nm['nameID'], nm['platformID'], nm['encodingID'], nm['languageID'])
	return newnane

def bldttfft(font, tgft, wt):
	ncfg=json.load(open(os.path.join(pydir, f'names/{tgft}.json'), 'r', encoding = 'utf-8'))
	font['OS/2'].ulCodePageRange1=ncfg['ulCodePageRange1']
	if tgft=='malgun':wts=('Regular', 'Bold', 'Semilight', 'Light')
	elif tgft=='yumin':wts=('Regular', 'Bold', 'Demibold', 'Light')
	else:wts=('Regular', 'Bold', 'Light')
	if wt not in wts: nmslist=wtbuil(ncfg[tgft+'l'], wt)
	else: nmslist=ncfg[tgft+end[wt]]
	ttflist=otpth(tgft+end[wt]+'.ttf')
	if it=='y':
		nmslist=itbuil(nmslist)
		ttflist=otpth(tgft+end[wt]+'It.ttf')
	font['head'].fontRevision=float(getver(nmslist))
	font['name']=toname(nmslist)
	print('Building font(s)...')
	print('Saving TTF...')
	font.save(ttflist)
	print('Done!')

def bldttcft(font, tgft, wt):
	ncfg=json.load(open(os.path.join(pydir, f'names/{tgft}.json'), 'r', encoding = 'utf-8'))
	font['OS/2'].ulCodePageRange1=ncfg['ulCodePageRange1']
	spwt=dict()
	isit=it=='y'
	if tgft in ('msyh', 'msjh', 'meiryo'):
		if wt not in ('Regular', 'Bold', 'Light'):
			nmslist=[wtbuil(ncfg[tgft+'l'], wt), wtbuil(ncfg[tgft+'ui'+'l'], wt)]
		else:
			nmslist=[ncfg[tgft+end[wt]], ncfg[tgft+'ui'+end[wt]]]
		edl=end[wt]
		if tgft=='meiryo': edl=end[wt].replace('bd', 'b')
		ttflist=[otpth(tgft+edl+'.ttf'), otpth(tgft+'ui'+edl+'.ttf')]
		ttcfil=otpth(tgft+edl+'.ttc')
	elif tgft=='simsun':
		if wt not in ('Regular', 'Bold', 'Light'):
			nmslist=[wtbuil(ncfg[tgft+'l'], wt), wtbuil(ncfg['n'+tgft+'l'], wt)]
		else:
			nmslist=[ncfg[tgft+end[wt]], ncfg['n'+tgft+end[wt]]]
		ttflist=[otpth(tgft+end[wt]+'.ttf'), otpth('p'+tgft+end[wt]+'.ttf')]
		ttcfil=otpth(tgft+end[wt]+'.ttc')
	elif tgft in ('mingliu', 'mingliub'):
		if wt not in ('Regular', 'Bold', 'Light'):
			nmslist=[wtbuil(ncfg[tgft+'l'], wt), wtbuil(ncfg['p'+tgft+'l'], wt), wtbuil(ncfg[tgft+'_hkscsl'], wt)]
		else:
			nmslist=[ncfg[tgft+end[wt]], ncfg['p'+tgft+end[wt]], ncfg[tgft+'_hkscs'+end[wt]]]
		ttflist=[otpth(tgft+end[wt]+'.ttf'), otpth('p'+tgft+end[wt]+'.ttf'), otpth(tgft+'_hkscs'+end[wt]+'.ttf')]
		ttcfil=otpth(tgft+end[wt]+'.ttc')
	elif tgft=='msgothic':
		if wt not in ('Regular', 'Bold', 'Light'):
			nmslist=[wtbuil(ncfg[tgft+'l'], wt), wtbuil(ncfg['msuigothicl'], wt), wtbuil(ncfg['mspgothicl'], wt)]
		else:
			nmslist=[ncfg[tgft+end[wt]], ncfg['msuigothic'+end[wt]], ncfg['mspgothic'+end[wt]]]
		ttflist=[otpth(tgft+end[wt]+'.ttf'), otpth('msuigothic'+end[wt]+'.ttf'), otpth('mspgothic'+end[wt]+'.ttf')]
		ttcfil=otpth(tgft+end[wt]+'.ttc')
	elif tgft=='msmincho':
		if wt not in ('Regular', 'Bold', 'Light'):
			nmslist=[wtbuil(ncfg[tgft+'l'], wt), wtbuil(ncfg['mspminchol'], wt)]
		else:
			nmslist=[ncfg[tgft+end[wt]], ncfg['mspmincho'+end[wt]]]
		ttflist=[otpth(tgft+end[wt]+'.ttf'), otpth('mspmincho'+end[wt]+'.ttf')]
		ttcfil=otpth(tgft+end[wt]+'.ttc')
	elif tgft=='batang':
		if wt not in ('Regular', 'Bold', 'Light'):
			nmslist=[wtbuil(ncfg[tgft+'l'], wt), wtbuil(ncfg['batangchel'], wt), wtbuil(ncfg['gungsuhl'], wt), wtbuil(ncfg['gungsuhchel'], wt)]
		else:
			nmslist=[ncfg[tgft+end[wt]], ncfg['batangche'+end[wt]], ncfg['gungsuh'+end[wt]], ncfg['gungsuhche'+end[wt]]]
		ttflist=[otpth(tgft+end[wt]+'.ttf'), otpth('batangche'+end[wt]+'.ttf'), otpth('gungsuh'+end[wt]+'.ttf'), otpth('gungsuhche'+end[wt]+'.ttf')]
		ttcfil=otpth(tgft+end[wt]+'.ttc')
	elif tgft=='gulim':
		if wt not in ('Regular', 'Bold', 'Light'):
			nmslist=[wtbuil(ncfg[tgft+'l'], wt), wtbuil(ncfg['gulimchel'], wt), wtbuil(ncfg['dotuml'], wt), wtbuil(ncfg['dotumchel'], wt)]
		else:
			nmslist=[ncfg[tgft+end[wt]], ncfg['gulimche'+end[wt]], ncfg['dotum'+end[wt]], ncfg['dotumche'+end[wt]]]
		ttflist=[otpth(tgft+end[wt]+'.ttf'), otpth('gulimche'+end[wt]+'.ttf'), otpth('dotum'+end[wt]+'.ttf'), otpth('dotumche'+end[wt]+'.ttf')]
		ttcfil=otpth(tgft+end[wt]+'.ttc')
	elif tgft=='yugoth':
		if wt =='Regular':
			nmslist=[ncfg['yugoth'], ncfg['yugothuisl']]
			ttflist=[otpth('YuGothR.ttf'), otpth('YuGothuiSL.ttf')]
			spwt[1]='semilight'
			ttcfil=otpth('YuGothR.ttc')
		elif wt =='Bold':
			nmslist=[ncfg['yugothbd'], ncfg['yugothuibd'], ncfg['yugothuisb']]
			ttflist=[otpth('YuGothB.ttf'), otpth('YuGothuiB.ttf'), otpth('YuGothuiSB.ttf')]
			spwt[2]='semibold'
			ttcfil=otpth('YuGothB.ttc')
		elif wt =='Medium':
			nmslist=[ncfg['yugothmd'], ncfg['yugothui']]
			ttflist=[otpth('YuGothM.ttf'), otpth('YuGothuiR.ttf')]
			ttcfil=otpth('YuGothM.ttc')
			spwt[1]='regular'
		elif wt =='Light':
			nmslist=[ncfg['yugothl'], ncfg['yugothuil']]
			ttflist=[otpth('YuGothL.ttf'), otpth('YuGothuiL.ttf')]
			ttcfil=otpth('YuGothL.ttc')
		else:
			nmslist=[wtbuil(ncfg['yugothl'], wt), wtbuil(ncfg['yugothuil'], wt)]
			ttflist=[otpth('YuGoth'+end[wt].upper()+'.ttf'), otpth('YuGothui'+end[wt].upper()+'.ttf')]
			ttcfil=otpth('YuGoth'+end[wt].upper()+'.ttc')
	if isit:
		nmslist=[itbuil(nm) for nm in nmslist]
		ttflist=[ttfl.replace('.ttf', 'It.ttf') for ttfl in ttflist]
		ttcfil=ttcfil.replace('.ttc', 'It.ttc')
	print('Building font(s)...')

	tmpf=list()
	wtcls=font['OS/2'].usWeightClass
	fssl=font["OS/2"].fsSelection
	macsl=font["head"].macStyle
	for i in range(len(nmslist)):
		font['head'].fontRevision=float(getver(nmslist[i]))
		font['name']=toname(nmslist[i])
		if i in spwt:
			setuswt(font, spwt[i])
		print('Saving TTFs...')
		font.save(ttflist[i])
		font['OS/2'].usWeightClass=wtcls
		font["OS/2"].fsSelection=fssl
		font["head"].macStyle=macsl
	print('Saving TTC...')
	runottf2otf(ttflist, ttcfil)
	if rmttf:
		for tpttf in ttflist: os.remove(tpttf)
	print('Done!')

def parseArgs(args):
	global outd, rmttf, it
	inFilePath, outDir, tarGet, weight=(str() for i in range(4))
	i, argn = 0, len(args)
	while i < argn:
		arg  = args[i]
		i += 1
		if arg == "-i":
			inFilePath = args[i]
			i += 1
		elif arg == "-d":
			outDir = args[i]
			i += 1
		elif arg == "-wt":
			weight = args[i]
			i += 1
		elif arg == "-it":
			it = args[i]
			i += 1
		elif arg == "-tg":
			tarGet = args[i].lower()
			i += 1
		elif arg == "-r":
			rmttf = True
		else:
			raise RuntimeError("Unknown option '%s'." % (arg))
	if not inFilePath:
		raise RuntimeError("You must specify one input font.")
	if not os.path.isfile(inFilePath):
		raise FileNotFoundError(f"Can not find file \"{inFilePath}\".\n")
	if not tarGet:
		raise RuntimeError(f"You must specify target.{TG}")
	elif tarGet not in TG:
		raise RuntimeError(f"Unknown target \"{tarGet}\"，please use {TG}.\n")

	if it.lower() not in ('a', 'y', 'n'):
		raise RuntimeError(f'Unknown italic setting "{it}"，please use "y" or "n".\n')
	if weight:
		if weight.lower() not in WT:
			raise RuntimeError(f'Unknown weight "{weight}"，please use {tuple(end.keys())}.\n')
		weight=weight.lower()
		if weight=='extralight': weight='ExtraLight'
		elif weight=='semibold': weight='SemiBold'
		elif weight=='demilight': weight='DemiLight'
		else: weight=weight.capitalize()
	if outDir:
		if not os.path.isdir(outDir):
			raise RuntimeError(f"Can not find directory \"{outDir}\".\n")
		else:
			outd=outDir
	return inFilePath, tarGet, weight

def run(args):
	global it
	ftin, tg, setwt=parseArgs(args)
	print('Loading...')
	font = ttLib.TTFont(ftin)
	if it=='a':
		it=getit(font)
	else:
		setit(font, it=='y')
	if not setwt:
		setwt=getwt(font)
	else:
		setuswt(font, setwt.lower())
	if tg in ('malgun', 'all', 'allsans'):
		bldttfft(font, 'malgun', setwt)
	if tg in ('simhei', 'all', 'allsans'):
		bldttfft(font, 'simhei', setwt)
	if tg in ('yumin', 'all', 'allserif'):
		bldttfft(font, 'yumin', setwt)
	if tg=='all':
		for stg in ('msyh', 'msjh', 'mingliu', 'simsun', 'yugoth', 'msgothic', 'msmincho', 'meiryo', 'batang', 'gulim'):
			bldttcft(font, stg, setwt)
	elif tg=='allsans':
		for stg in ('msyh', 'msjh', 'yugoth', 'msgothic', 'meiryo', 'gulim'):
			bldttcft(font, stg, setwt)
	elif tg=='allserif':
		for stg in ('mingliu', 'simsun', 'msmincho', 'batang'):
			bldttcft(font, stg, setwt)
	elif tg=='simsunb':
		bldttfft(font, tg, setwt)
	elif tg not in ('malgun', 'simhei', 'yumin'):
		bldttcft(font, tg, setwt)
	print('End!')

def main():
	run(sys.argv[1:])

if __name__ == "__main__":
	main()
