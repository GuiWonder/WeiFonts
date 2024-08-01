import sys, os, tempfile, shutil
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

def buitotc(infile, outfile, mfile):
	fileList=list()
	fonts=getfonts(mfile)
	tmp=tempfile.mktemp()
	os.mkdir(tmp)
	for i in range(len(fonts)):
		tmpfile=os.path.join(tmp, fonts[i]+'.ttf')
		buitotf(infile, tmpfile, mfile, i)
		fileList.append(tmpfile)
	runottf2otf(fileList, outfile)
	shutil.rmtree(tmp)

def buitotf(infile, outfile, mfile, i=-1):
	fontm=ttLib.TTFont(mfile, fontNumber=i)
	ftnm=fontm["name"].getDebugName(6)
	inft=infile[ftnm.split('-')[-1]]
	newft=ttLib.TTFont(inft, recalcTimestamp=False, recalcBBoxes=False)
	newft['OS/2'].achVendID=fontm['OS/2'].achVendID
	newft['OS/2'].ulCodePageRange1=fontm['OS/2'].ulCodePageRange1
	newft['head'].fontRevision=fontm['head'].fontRevision
	newft['name']=fontm['name']
	newft["head"].macStyle=fontm["head"].macStyle
	newft["OS/2"].fsSelection=fontm["OS/2"].fsSelection
	newft['OS/2'].usWeightClass=fontm['OS/2'].usWeightClass
	newft.save(outfile)
	newft.close()
	fontm.close()

def parseArgs(args):
	outFilePath=str()
	infiles={'Regular':'', 'Medium':'', 'Semibold':'', 'Light':'', 'Thin':'', 'Ultralight':''}
	i, argn = 0, len(args)
	while i < argn:
		arg  = args[i]
		i += 1
		if arg == "-o":
			outFilePath = args[i]
			i += 1
		elif arg == "-f1":
			infiles['Regular'] = args[i]
			i += 1
		elif arg == "-f2":
			infiles['Medium'] = args[i]
			i += 1
		elif arg == "-f3":
			infiles['Semibold'] = args[i]
			i += 1
		elif arg == "-f4":
			infiles['Light'] = args[i]
			i += 1
		elif arg == "-f5":
			infiles['Thin'] = args[i]
			i += 1
		elif arg == "-f6":
			infiles['Ultralight'] = args[i]
			i += 1
		else:
			raise RuntimeError("Unknown option '%s'." % (arg))
	for k in infiles.keys():
		if not os.path.isfile(infiles[k]):
			raise FileNotFoundError(f"Can not find file \"{infiles[k]}\".\n")
	if not outFilePath:
		raise RuntimeError("You must specify one output font file.")
	return infiles, outFilePath

def main(args):
	ifiles, ofile=parseArgs(args)
	print('Process...')
	mfile=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'names/pingfang.ttc')
	assert os.path.isfile(mfile)
	buitotc(ifiles, ofile, mfile)
	print('End')

if __name__ == '__main__':
	main(sys.argv[1:])
