import xml.etree.ElementTree as ET


def parse(screen, root=None):
	windowX, windowY = screen.get_size()
	curr_delay = 0
	pstring = ""
	plstring = ""
	tabs = 0
	count = 0
	delay = 0

	if root == None:
		tree = ET.parse('level1.xml')
		root = tree.getroot()

	def addEnemy(px, py, imagepath, velocity, delay, angle, waittime):
		return f"Enemy(screen, {px}, {py}, \"{imagepath}\", velocity={velocity}, delay={delay}, angle={angle}, waittime={waittime})"
	for i in root:
		#* Delay tag parsing
		if i.tag == 'delay':
			delay += float(i.attrib['duration'])
		#* Section tag parsing
		if i.tag == 'section':
			count += 1
			pstring = pstring + f"essg{count} = pygame.sprite.Group()\n"
		#* Bullet tag parsing, spawns a bullet
		if i.tag == 'bullet':
			pstring = pstring + f"essg{count}.add(" + addEnemy(float(i.attrib['px']), float(i.attrib['py']), i.attrib['imagepath'], float(i.attrib['velocity']), delay, float(i.attrib['angle']), float(i.attrib['waittime'])) + ")\n"
		#* Bullet wall tag parsing, spawns a bullet wall
		if i.tag == 'bwallx':
			if str(i.attrib['min'])[0] == "%":
				i.attrib['min'] = str(float(i.attrib['min'][1::]) / 100 * windowY)
			if str(i.attrib['max'])[0] == "%":
				i.attrib['max'] = str(float(i.attrib['max'][1::]) / 100 * windowY)
			spacing = float(i.attrib['spacing'])
			for spaces in range(0, int(windowY / spacing)):
				calc = ((((spaces * spacing + float(i.attrib['offset'])) % windowY)) % (float(i.attrib['max']) - float(i.attrib['min'])) + float(i.attrib['min'])) % windowY
				pstring = pstring + f"essg{count}.add(" + addEnemy(float(i.attrib['px']), calc, i.attrib['imagepath'], float(i.attrib['velocity']), delay, float(i.attrib['angle']), float(i.attrib['waittime'])) + ")\n"
		#* Bullet wall tag parsing, spawns a bullet wall
		if i.tag == 'bwally':
			if str(i.attrib['min'])[0] == "%":
				i.attrib['min'] = str(float(i.attrib['min'][1::]) / 100 * windowX)
			if str(i.attrib['max'])[0] == "%":
				i.attrib['max'] = str(float(i.attrib['max'][1::]) / 100 * windowX)
			spacing = float(i.attrib['spacing'])
			for spaces in range(0, int(windowX / spacing)):
				calc = ((((spaces * spacing + float(i.attrib['offset'])) % windowX)) % (float(i.attrib['max']) - float(i.attrib['min'])) + float(i.attrib['min'])) % windowX
				pstring = pstring + f"essg{count}.add(" + addEnemy(calc, float(i.attrib['py']), i.attrib['imagepath'], float(i.attrib['velocity']), delay, float(i.attrib['angle']) + 90, float(i.attrib['waittime'])) + ")\n"
		#* Repeat tag parsing, repeats tags inside it
		if i.tag == 'repeat':
			for _ in range(int(i.attrib['amount'])):
				for j in i:
					#* Delay tag parsing
					if j.tag == 'delay':
						delay += float(j.attrib['duration'])
					#* Bullet wall parsing
					if j.tag == 'bwallx':
						if str(j.attrib['min'])[0] == "%":
							j.attrib['min'] = str(float(j.attrib['min'][1::]) / 100 * windowY)
							print("Ymin", j.attrib['min'])
						if str(j.attrib['max'])[0] == "%":
							j.attrib['max'] = str(float(j.attrib['max'][1::]) / 100 * windowY)
							print("Ymax", j.attrib['max'])
						for k, l in zip(i.attrib['prop'].split(','), i.attrib['increment'].split(',')):
							j.attrib[k] = str(float(j.attrib[k]) + float(l))
						#j.attrib[i.attrib['prop']] = str(float(j.attrib[i.attrib['prop']]) + float(i.attrib['increment']))
						spacing = float(j.attrib['spacing'])
						for spaces in range(0, int(windowY / spacing)):
							calc = ((((spaces * spacing + float(j.attrib['offset'])) % windowY)) % (float(j.attrib['max']) - float(j.attrib['min'])) + float(j.attrib['min'])) % windowY
							pstring = pstring + f"essg{count}.add(" + addEnemy(float(j.attrib['px']), calc, j.attrib['imagepath'], float(j.attrib['velocity']), delay, float(j.attrib['angle']), float(j.attrib['waittime'])) + ")\n"
					#* Tag parsing
					if j.tag == 'bwally':
						if str(j.attrib['min'])[0] == "%":
							j.attrib['min'] = str(float(j.attrib['min'][1::]) / 100 * windowX)
							print("Xmin", j.attrib['min'])
						if str(j.attrib['max'])[0] == "%":
							j.attrib['max'] = str(float(j.attrib['max'][1::]) / 100 * windowX)
							print("Xmax", j.attrib['max'])
						for k, l in zip(i.attrib['prop'].split(','), i.attrib['increment'].split(',')):
							j.attrib[k] = str(float(j.attrib[k]) + float(l))
						#j.attrib[i.attrib['prop']] = str(float(j.attrib[i.attrib['prop']]) + float(i.attrib['increment']))
						spacing = float(j.attrib['spacing'])
						for spaces in range(0, int(windowX / spacing)):
							calc = ((((spaces * spacing + float(j.attrib['offset'])) % windowX)) % (float(j.attrib['max']) - float(j.attrib['min'])) + float(j.attrib['min'])) % windowX
							pstring = pstring + f"essg{count}.add(" + addEnemy(calc, float(j.attrib['py']), j.attrib['imagepath'], float(j.attrib['velocity']), delay, float(j.attrib['angle']) + 90, float(j.attrib['waittime'])) + ")\n"
	for i in range(0, count):
		plstring = plstring + f"essg{i + 1}.update(dt)\n"
		plstring = plstring + f"essg{i + 1}.draw(screen)\n"
		plstring = plstring + f"has_died = has_died | player.collides(essg{i + 1})\n"
	print(plstring)
	return pstring, plstring