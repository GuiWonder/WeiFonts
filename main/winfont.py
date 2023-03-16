import os, json, subprocess, platform, tempfile, gc, sys

pydir = os.path.abspath(os.path.dirname(__file__))
otfccdump = os.path.join(pydir, 'otfcc/otfccdump')
otfccbuild = os.path.join(pydir, 'otfcc/otfccbuild')
otf2otc = os.path.join(pydir, 'otf2otc.py')
outd=str()
rmttf=False
if platform.system() in ('Mac', 'Darwin'):
	otfccdump += '1'
	otfccbuild += '1'
if platform.system() == 'Linux':
	otfccdump += '2'
	otfccbuild += '2'
TG= ('msyh', 'msjh', 'mingliu', 'mingliub', 'simsun', 'simsunb', 'yugoth', 'msgothic', 'malgun', 'msmincho', 'meiryo', 'batang', 'gulim', 'all', 'allsans', 'allserif')
WT=('thin', 'extralight', 'light', 'semilight', 'demilight', 'normal', 'regular', 'medium', 'semibold', 'bold', 'black', 'heavy')

def getwt(font):
	if 'macStyle' in font['head'] and 'bold' in font['head']['macStyle'] and font['head']['macStyle']['bold']:
		return 'Bold'
	wtn={250:'ExtraLight', 300:'Light', 350:'Normal', 400:'Regular', 500:'Medium', 600:'SemiBold', 900:'Heavy'}
	wtc=font['OS_2']['usWeightClass']
	if wtc<300:
		return wtn[250]
	if wtc in wtn:
		return wtn[wtc]
	return 'Regular'

def getver(nmo):
	for n1 in nmo:
		if n1['languageID']==1033 and n1['nameID']==5:
			return n1['nameString'].split(' ')[-1]
	return 1

def mktmp(font):
	tmp = tempfile.mktemp('.json')
	with open(tmp, 'w', encoding='utf-8') as f:
		f.write(json.dumps(font))
	return tmp

def otpth(ftf):
	if outd:
		return os.path.join(outd, ftf)
	return ftf

def svtottf(jsf, ttff):
	subprocess.run((otfccbuild, '--keep-modified-time', '--keep-average-char-width', '-O2', '-q', '-o', ttff, jsf))
	os.remove(jsf)

def wtbuil(nml, wt):
	nwtnm=list()
	for n1 in nml:
		n2=dict(n1)
		if n2['nameID'] in (1, 3, 4, 6, 17):
			n2['nameString']=n2['nameString'].replace('Light', wt)
		nwtnm.append(n2)
	return nwtnm

def bldttfft(font, tgft, wt):
	end={'Thin':'th', 'ExtraLight':'xl', 'Light':'l', 'Semilight':'sl', 'DemiLight':'dm', 'Normal':'nm', 'Regular':'', 'Medium':'md', 'SemiBold':'sb', 'Bold':'bd', 'Black':'bl', 'Heavy':'hv'}
	ncfg=json.load(open(os.path.join(pydir, f'names/{tgft}.json'), 'r', encoding = 'utf-8'))
	font['OS_2']['ulCodePageRange1']=ncfg['ulCodePageRange1']
	if tgft=='malgun':wts=('Regular', 'Bold', 'Semilight', 'Light')
	else:wts=('Regular', 'Bold', 'Light')
	if wt not in wts:
		nmslist=wtbuil(ncfg[tgft+'l'], wt)
	else:
		nmslist=ncfg[tgft+end[wt]]
	ttflist=otpth(tgft+end[wt]+'.ttf')
	font['head']['fontRevision']=float(getver(nmslist))
	font['name']=nmslist
	print('正在生成字体...')
	tmpf=mktmp(font)
	del font
	gc.collect()
	print('正在保存TTF...')
	svtottf(tmpf, ttflist)
	print('完成!')

def bldttcft(font, tgft, wt):
	end={'Thin':'th', 'ExtraLight':'xl', 'Light':'l', 'Semilight':'sl', 'DemiLight':'dm', 'Normal':'nm', 'Regular':'', 'Medium':'md', 'SemiBold':'sb', 'Bold':'bd', 'Black':'bl', 'Heavy':'hv'}
	ncfg=json.load(open(os.path.join(pydir, f'names/{tgft}.json'), 'r', encoding = 'utf-8'))
	font['OS_2']['ulCodePageRange1']=ncfg['ulCodePageRange1']
	if tgft in ('msyh', 'msjh', 'meiryo'):
		if wt not in ('Regular', 'Bold', 'Light'):
			nmslist=[wtbuil(ncfg[tgft+'l'], wt), wtbuil(ncfg[tgft+'ui'+'l'], wt)]
		else:
			nmslist=[ncfg[tgft+end[wt]], ncfg[tgft+'ui'+end[wt]]]
		if tgft=='meiryo': end[wt]=end[wt].replace('bd', 'b')
		ttflist=[otpth(tgft+end[wt]+'.ttf'), otpth(tgft+'ui'+end[wt]+'.ttf')]
		ttcfil=otpth(tgft+end[wt]+'.ttc')
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
			ttcfil=otpth('YuGothR.ttc')
		elif wt =='Bold':
			nmslist=[ncfg['yugothbd'], ncfg['yugothuibd'], ncfg['yugothuisb']]
			ttflist=[otpth('YuGothB.ttf'), otpth('YuGothuiB.ttf'), otpth('YuGothuiSB.ttf')]
			ttcfil=otpth('YuGothB.ttc')
		elif wt =='Medium':
			nmslist=[ncfg['yugothmd'], ncfg['yugothui']]
			ttflist=[otpth('YuGothM.ttf'), otpth('YuGothuiR.ttf')]
			ttcfil=otpth('YuGothM.ttc')
		elif wt =='Light':
			nmslist=[ncfg['yugothl'], ncfg['yugothuil']]
			ttflist=[otpth('YuGothL.ttf'), otpth('YuGothuiL.ttf')]
			ttcfil=otpth('YuGothL.ttc')
		else:
			nmslist=[wtbuil(ncfg['yugothl'], wt), wtbuil(ncfg['yugothuil'], wt)]
			ttflist=[otpth('YuGoth'+end[wt].upper()+'.ttf'), otpth('YuGothui'+end[wt].upper()+'.ttf')]
			ttcfil=otpth('YuGoth'+end[wt].upper()+'.ttc')
	print('正在生成字体...')
	tmpf=list()
	for i in range(len(nmslist)):
		font['head']['fontRevision']=float(getver(nmslist[i]))
		font['name']=nmslist[i]
		tmpf.append(mktmp(font))
	del font
	gc.collect()
	print('正在保存TTFs...')
	for i in range(len(nmslist)):
		svtottf(tmpf[i], ttflist[i])
	print('正在生成TTC...')
	ttcarg=['python', otf2otc, '-o', ttcfil]
	ttcarg+=ttflist
	subprocess.run(tuple(ttcarg))
	if rmttf:
		for tpttf in ttflist: os.remove(tpttf)
	print('完成!')

def parseArgs(args):
	global outd, rmttf
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
	if weight:
		if weight.lower() not in WT:
			raise RuntimeError(f'Unknown weight "{weight}"，please use {tuple(end.keys())}。\n')
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
	ftin, tg, setwt=parseArgs(args)
	print('正在载入字体...')
	font = json.loads(subprocess.check_output((otfccdump, '--no-bom', ftin)).decode("utf-8", "ignore"))
	if not setwt:
		setwt=getwt(font)
	if 'macStyle' in font['head']:
		font['head']['macStyle']['bold']=setwt=='Bold'
	if 'fsSelection' in font['OS_2']:
		font['OS_2']['fsSelection']['bold']=setwt=='Bold'
	if tg in ('malgun', 'all', 'allsans'):
		bldttfft(font, 'malgun', setwt)
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
	elif tg!='malgun':
		bldttcft(font, tg, setwt)
	print('结束!')

def main():
	run(sys.argv[1:])

if __name__ == "__main__":
	main()
