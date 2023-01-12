import os, json, subprocess, platform, tempfile, gc, sys

pydir = os.path.abspath(os.path.dirname(__file__))
otfccdump = os.path.join(pydir, 'otfcc/otfccdump')
otfccbuild = os.path.join(pydir, 'otfcc/otfccbuild')
otf2otc = os.path.join(pydir, 'otf2otc.py')
outd=str()
if platform.system() in ('Mac', 'Darwin'):
	otfccdump += '1'
	otfccbuild += '1'
if platform.system() == 'Linux':
	otfccdump += '2'
	otfccbuild += '2'
TG= ('msyh', 'msjh', 'mingliu', 'simsun', 'yugoth', 'msgothic', 'malgun', 'msmincho', 'meiryo', 'batang')
WT=('extralight', 'light', 'semilight', 'normal', 'regular', 'medium', 'semibold', 'bold', 'heavy')

def getwt(font):
	if 'macStyle' in font['head'] and 'bold' in font['head']['macStyle'] and font['head']['macStyle']['bold']:
		return 'Bold'
	wtn={250:'ExtraLight', 300:'Light', 350:'Normal', 400:'Regular', 500:'Medium', 600:'SemiBold', 900:'Heavy'}
	wtc=font['OS_2']['usWeightClass']
	if wtc<300:
		wtc=250
	if wtc in wtn:
		return wtn[wtc]
	else:
		return 'Regular'

def getver(nmo):
	for n1 in nmo:
		if n1['languageID']==1033 and n1['nameID']==5:
			return n1['nameString'].split(' ')[-1]
	return 0

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
	end={'ExtraLight':'xl', 'Light':'l', 'Semilight':'sl', 'Normal':'nm', 'Regular':'', 'Medium':'md', 'SemiBold':'sb', 'Bold':'bd', 'Heavy':'hv'}
	ncfg=json.load(open(os.path.join(pydir, f'names/{tgft}.json'), 'r', encoding = 'utf-8'))
	font['OS_2']['ulCodePageRange1']=ncfg['ulCodePageRange1']
	if wt not in ('Regular', 'Bold', 'Semilight', 'Light'):
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

def bldttcft(font, tgft, wt):
	end={'ExtraLight':'xl', 'Light':'l', 'Semilight':'sl', 'Normal':'nm', 'Regular':'', 'Medium':'md', 'SemiBold':'sb', 'Bold':'bd', 'Heavy':'hv'}
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
	elif tgft=='mingliu':
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

def parseArgs(args):
	global outd
	nwk=dict()
	nwk['inFilePath'], nwk['outDir'], nwk['tarGet'], nwk['weight']=(str() for i in range(4))
	argn = len(args)
	i = 0
	while i < argn:
		arg  = args[i]
		i += 1
		if arg == "-i":
			nwk['inFilePath'] = args[i]
			i += 1
		elif arg == "-d":
			nwk['outDir'] = args[i]
			i += 1
		elif arg == "-wt":
			nwk['weight'] = args[i]
			i += 1
		elif arg == "-tg":
			nwk['tarGet'] = args[i].lower()
			i += 1
		else:
			raise RuntimeError("Unknown option '%s'." % (arg))
	if not nwk['inFilePath']:
		raise RuntimeError("You must specify one input font.")
	if not nwk['tarGet']:
		raise RuntimeError(f"You must specify target.{TG}")
	elif nwk['tarGet'] not in TG:
		raise RuntimeError(f"Unknown target \"{nwk['tarGet']}\"，please use {TG}.\n")
	if nwk['weight']:
		if nwk['weight'].lower() not in WT:
			raise RuntimeError(f'Unknown weight "{nwk["weight"]}"，please use "ExtraLight", "Light", "Semilight", "Normal", "Regular", "Medium", "SemiBold", "Bold", "Heavy"。\n')
		nwk['weight']=nwk['weight'].lower()
		if nwk['weight']=='extralight':
			nwk['weight']='ExtraLight'
		elif nwk['weight']=='semibold':
			nwk['weight']='SemiBold'
		else:
			nwk['weight']=nwk['weight'].capitalize()
	if nwk['outDir']:
		if not os.path.isdir(nwk['outDir']):
			raise RuntimeError(f"Can not fint directory \"{nwk['outDir']}\".\n")
		else:
			outd=nwk['outDir']
	return nwk

def run(args):
	wkfl=parseArgs(args)
	print('正在载入字体...')
	font = json.loads(subprocess.check_output((otfccdump, '--no-bom', wkfl['inFilePath'])).decode("utf-8", "ignore"))
	if not wkfl['weight']:
		wkfl['weight']=getwt(font)
	if 'macStyle' in font['head']:
		font['head']['macStyle']['bold']=wkfl['weight']=='Bold'
	if 'fsSelection' in font['OS_2']:
		font['OS_2']['fsSelection']['bold']=wkfl['weight']=='Bold'
	tg=wkfl['tarGet']
	if tg=='malgun':
		bldttfft(font, tg, wkfl['weight'])
	else:
		bldttcft(font, tg, wkfl['weight'])
	print('完成!')

def main():
	run(sys.argv[1:])

if __name__ == "__main__":
	main()
