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
	pstring = pstring + "global dt\n"
	for i in root:
		#* Delay tag parsing
		if i.tag == 'delay':
			delay += float(i.attrib['duration'])
		#* Section tag parsing
		if i.tag == 'section':
			count += 1
			pstring = pstring + f"global essg{count}\n"
			pstring = pstring + f"essg{count} = pygame.sprite.Group()\n"
		#* Bullet tag parsing, spawns a bullet
		if i.tag == 'bullet':
			pstring = pstring + f"essg{count}.add(" + addEnemy(float(i.attrib['px']), float(i.attrib['py']), i.attrib['imagepath'], float(i.attrib['velocity']), delay, float(i.attrib['angle']), float(i.attrib['waittime'])) + ")\n"
		#* Bullet wall tag parsing, spawns a bullet wall
		if i.tag == 'bwallx':
			spacing = float(i.attrib['spacing'])
			for spaces in range(0, int(windowY / spacing)):
				pstring = pstring + f"essg{count}.add(" + addEnemy(float(i.attrib['px']), (spaces * spacing + float(i.attrib['offset'])) % windowY, i.attrib['imagepath'], float(i.attrib['velocity']), delay, float(i.attrib['angle']), float(i.attrib['waittime'])) + ")\n"
		#* Bullet wall tag parsing, spawns a bullet wall
		if i.tag == 'bwally':
			spacing = float(i.attrib['spacing'])
			for spaces in range(0, int(windowX / spacing)):
				pstring = pstring + f"essg{count}.add(" + addEnemy((spaces * spacing + float(i.attrib['offset'])) % windowX, float(i.attrib['py']), i.attrib['imagepath'], float(i.attrib['velocity']), delay, float(i.attrib['angle']), float(i.attrib['waittime'])) + ")\n"
		#* Repeat tag parsing, repeats tags inside it
		if i.tag == 'repeat':
			for _ in range(int(i.attrib['amount'])):
				for j in i:
					#* Delay tag parsing
					if j.tag == 'delay':
						delay += float(j.attrib['duration'])
					#* Bullet wall parsing
					if j.tag == 'bwallx':
						for k, l in zip(i.attrib['prop'].split(','), i.attrib['increment'].split(',')):
							j.attrib[k] = str(float(j.attrib[k]) + float(l))
						#j.attrib[i.attrib['prop']] = str(float(j.attrib[i.attrib['prop']]) + float(i.attrib['increment']))
						spacing = float(j.attrib['spacing'])
						for spaces in range(0, int(windowY / spacing)):
							pstring = pstring + f"essg{count}.add(" + addEnemy(float(j.attrib['px']), (spaces * spacing + float(j.attrib['offset'])) % windowY, j.attrib['imagepath'], float(j.attrib['velocity']), delay, float(j.attrib['angle']), float(j.attrib['waittime'])) + ")\n"
					if j.tag == 'bwally':
						for k, l in zip(i.attrib['prop'].split(','), i.attrib['increment'].split(',')):
							j.attrib[k] = str(float(j.attrib[k]) + float(l))
						#j.attrib[i.attrib['prop']] = str(float(j.attrib[i.attrib['prop']]) + float(i.attrib['increment']))
						spacing = float(j.attrib['spacing'])
						for spaces in range(0, int(windowX / spacing)):
							pstring = pstring + f"essg{count}.add(" + addEnemy((spaces * spacing + float(j.attrib['offset'])) % windowX, float(j.attrib['py']), j.attrib['imagepath'], float(j.attrib['velocity']), delay, float(j.attrib['angle']), float(j.attrib['waittime'])) + ")\n"
	plstring = plstring + "global parsed\n"
	for i in range(0, count):
		plstring = plstring + f"global essg{i + 1}\n"
	plstring = plstring + "global has_died\n"
	plstring = plstring + "def parsed():\n"
	plstring = plstring + "\tglobal has_died\n"
	for i in range(0, count):
		plstring = plstring + f"\tglobal essg{i + 1}\n"
		plstring = plstring + f"\tessg{i + 1}.update(dt)\n"
		plstring = plstring + f"\tessg{i + 1}.draw(screen)\n"
		plstring = plstring + f"\thas_died = has_died | player.collides(essg{i + 1})\n"
	print(plstring)
	return pstring, plstring