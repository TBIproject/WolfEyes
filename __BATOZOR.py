from glob import glob

for file in glob('*.py'):
	with open(file + '.bat', 'w') as f:
		f.write('%s\npause' % file)