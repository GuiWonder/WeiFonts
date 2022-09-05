import os, json, subprocess, platform, tempfile, gc, sys

pydir = os.path.abspath(os.path.dirname(__file__))
otfccdump = os.path.join(pydir, 'otfcc/otfccdump')
otfccbuild = os.path.join(pydir, 'otfcc/otfccbuild')
otf2otc = os.path.join(pydir, 'otf2otc.py')
if platform.system() in ('Mac', 'Darwin'):
	otfccdump += '1'
	otfccbuild += '1'
if platform.system() == 'Linux':
	otfccdump += '2'
	otfccbuild += '2'

def ckfile(f):
	f=f.strip()
	if not os.path.isfile(f):
		if os.path.isfile(f.strip('"')):
			return f.strip('"')
		elif os.path.isfile(f.strip("'")):
			return f.strip("'")
	return f

def creattmp():
	print('正在检查字体...')
	fpn=str()
	global font
	for n1 in font['name']:
		if n1['nameID']==6 and '-' in n1['nameString']:
			fpn=n1['nameString']
			break
	print('字体为', fpn)
	print('正在设置字体信息...')
	if stl=='sans' or (stl!='serif' and 'Sans' in fpn):
		end={'Regular':'', 'Bold':'bd', 'Light':'l', 'Extralight':'xl', 'Heavy':'hv'}
		fml='none'
		if fv.capitalize() in end:
			fml=fv.capitalize()
		elif '-' in fpn:
			fml=fpn.split('-')[-1].capitalize()
		if fml not in end:
			print('文件不匹配，退出！')
			sys.exit()

		yh_ulCodePageRange1= {
			'latin1': True,
			'latin2': True,
			'cyrillic': True,
			'greek': True,
			'turkish': True,
			'gbk': True
		}
		jh_ulCodePageRange1= {
			'latin1': True,
			'greek': True,
			'big5': True
		}
		
		yh='msyh'+end[fml]
		jh='msjh'+end[fml]
		nyh=json.load(open(os.path.join(pydir, 'names/msyh.json'), 'r', encoding = 'utf-8'))
		njh=json.load(open(os.path.join(pydir, 'names/msjh.json'), 'r', encoding = 'utf-8'))
		yhver=str()
		jhver=str()
		yhverui=str()
		jhverui=str()
		for n1 in nyh[yh]:
			if n1['languageID']==1033:
				if n1['nameID']==5:
					yhver=n1['nameString'].split(' ')[-1]
		for n1 in njh[jh]:
			if n1['languageID']==1033:
				if n1['nameID']==5:
					jhver=n1['nameString'].split(' ')[-1]
		for n1 in nyh[yh+'ui']:
			if n1['languageID']==1033:
				if n1['nameID']==5:
					yhverui=n1['nameString'].split(' ')[-1]
		for n1 in njh[jh+'ui']:
			if n1['languageID']==1033:
				if n1['nameID']==5:
					jhverui=n1['nameString'].split(' ')[-1]
		
		font['OS_2']['ulCodePageRange1']=yh_ulCodePageRange1
		
		font['head']['fontRevision']=float(yhver)
		font['name']=nyh[yh]
		print('正在生成雅黑字体...')
		tmp['yh'] = tempfile.mktemp('.json')
		with open(tmp['yh'], 'w', encoding='utf-8') as f:
			f.write(json.dumps(font))
		
		font['head']['fontRevision']=float(yhverui)
		font['name']=nyh[yh+'ui']
		print('正在生成雅黑ui字体...')
		tmp['yhui'] = tempfile.mktemp('.json')
		with open(tmp['yhui'], 'w', encoding='utf-8') as f:
			f.write(json.dumps(font))
		
		font['OS_2']['ulCodePageRange1']=jh_ulCodePageRange1
		
		font['head']['fontRevision']=float(jhver)
		font['name']=njh[jh]
		print('正在生成正黑字体...')
		tmp['jh'] = tempfile.mktemp('.json')
		with open(tmp['jh'], 'w', encoding='utf-8') as f:
			f.write(json.dumps(font))

		font['head']['fontRevision']=float(jhverui)
		font['name']=njh[jh+'ui']
		print('正在生成正黑ui字体...')
		tmp['jhui'] = tempfile.mktemp('.json')
		with open(tmp['jhui'], 'w', encoding='utf-8') as f:
			f.write(json.dumps(font))
		
		del font
		gc.collect()
		
		print('正在生成雅黑字体OTF/TTF...')
		subprocess.run((otfccbuild, '--keep-modified-time', '--keep-average-char-width', '-O3', '-q', '-o', yh+'.otf', tmp['yh']))
		os.remove(tmp['yh'])
		print('正在生成雅黑ui字体OTF/TTF...')
		subprocess.run((otfccbuild, '--keep-modified-time', '--keep-average-char-width', '-O3', '-q', '-o', yh+'ui.otf', tmp['yhui']))
		os.remove(tmp['yhui'])
		print('正在生成正黑字体OTF/TTF...')
		subprocess.run((otfccbuild, '--keep-modified-time', '--keep-average-char-width', '-O3', '-q', '-o', jh+'.otf', tmp['jh']))
		os.remove(tmp['jh'])
		print('正在生成正黑ui字体OTF/TTF...')
		subprocess.run((otfccbuild, '--keep-modified-time', '--keep-average-char-width', '-O3', '-q', '-o', jh+'ui.otf', tmp['jhui']))
		os.remove(tmp['jhui'])
		
		print('正在生成雅黑字体OTC/TTC...')
		subprocess.run(('python', otf2otc, '-t', '"CFF "=0', '-o', yh+'.ttc', yh+'.otf', yh+'ui.otf'))
		print('正在生成正黑字体OTC/TTC...')
		subprocess.run(('python', otf2otc, '-t', '"CFF "=0', '-o', jh+'.ttc', jh+'.otf', jh+'ui.otf'))
	
	elif stl=='serif' or 'Serif' in fpn:
		s_ulCodePageRange1= {
			'latin1': True,
			'gbk': True
		}
		nssn=json.load(open(os.path.join(pydir, 'names/simsun.json'), 'r', encoding = 'utf-8'))
		snver=str()
		nsnver=str()
		for n1 in nssn['simsun']:
			if n1['languageID']==1033:
				if n1['nameID']==5:
					snver=n1['nameString'].split(' ')[-1]
		for n1 in nssn['nsimsun']:
			if n1['languageID']==1033:
				if n1['nameID']==5:
					nsnver=n1['nameString'].split(' ')[-1]
		
		font['OS_2']['ulCodePageRange1']=s_ulCodePageRange1
		
		font['head']['fontRevision']=float(snver)
		font['name']=nssn['simsun']
		print('正在生成宋体字体...')
		tmp['sn'] = tempfile.mktemp('.json')
		with open(tmp['sn'], 'w', encoding='utf-8') as f:
			f.write(json.dumps(font))
		
		font['head']['fontRevision']=float(nsnver)
		font['name']=nssn['nsimsun']
		print('正在生成新宋体字体...')
		tmp['nsn'] = tempfile.mktemp('.json')
		with open(tmp['nsn'], 'w', encoding='utf-8') as f:
			f.write(json.dumps(font))
		
		del font
		gc.collect()
		
		print('正在生成宋体字体OTF/TTF...')
		subprocess.run((otfccbuild, '--keep-modified-time', '--keep-average-char-width', '-O3', '-q', '-o', 'simsun.otf', tmp['sn']))
		os.remove(tmp['sn'])
		print('正在生成新宋体字体OTF/TTF...')
		subprocess.run((otfccbuild, '--keep-modified-time', '--keep-average-char-width', '-O3', '-q', '-o', 'nsimsun.otf', tmp['nsn']))
		os.remove(tmp['nsn'])
		
		print('正在生成宋体字体OTC/TTC...')
		subprocess.run(('python', otf2otc, '-t', '"CFF "=0', '-o', 'simsun.ttc', 'simsun.otf', 'nsimsun.otf'))
		
	else:
		print('文件不匹配，退出！')
		sys.exit()

print('====创建Windows取代字体====\n')
inf=str()
outf=str()
outfui=str()
if len(sys.argv)<2:
	while not os.path.isfile(inf):
		inf=input('请输入字体文件路径（或拖入文件）：\n')
		inf=ckfile(inf)
		if not os.path.isfile(inf):
			print('文件不存在，请重新选择！\n')
else:
	inf=sys.argv[1]
stl=str()
fv=str()
if len(sys.argv)>2:
	stl=sys.argv[2].lower()
	if stl not in ('sans', 'serif'):
		print(f'无效参数"{sys.argv[2]}"，请使用"Sans"或"Serif"。\n')
		sys.exit()
if len(sys.argv)>3:
	fv=sys.argv[3].lower()
	if stl=='sans' and fv not in ('regular', 'bold', 'light', 'extralight', 'heavy'):
		print(f'无效参数"{sys.argv[3]}"，请使用"Regular", "Bold", "Light", "ExtraLight","Heavy"。\n')
		sys.exit()

print('正在载入字体...')
font = json.loads(subprocess.check_output((otfccdump, '--no-bom', inf)).decode("utf-8", "ignore"))
tmp=dict()
creattmp()

print('完成!')
