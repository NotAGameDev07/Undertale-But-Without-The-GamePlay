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
			pstring = pstring + f"essg{count}.add(" + addEnemy(int(i.attrib['px']), int(i.attrib['py']), i.attrib['imagepath'], int(i.attrib['velocity']), delay, int(i.attrib['angle']), float(i.attrib['waittime'])) + ")\n"
		#* Bullet wall tag parsing, spawns a bullet wall
		if i.tag == 'bwallx':
			spacing = int(i.attrib['spacing'])
			for spaces in range(0, int(windowY / spacing)):
				pstring = pstring + f"essg{count}.add(" + addEnemy(int(i.attrib['px']), (spaces * spacing + int(i.attrib['offset'])) % windowY, i.attrib['imagepath'], int(i.attrib['velocity']), delay, int(i.attrib['angle']), float(i.attrib['waittime'])) + ")\n"
		#* Bullet wall tag parsing, spawns a bullet wall
		if i.tag == 'bwally':
			spacing = int(i.attrib['spacing'])
			for spaces in range(0, int(windowX / spacing)):
				pstring = pstring + f"essg{count}.add(" + addEnemy((spaces * spacing + int(i.attrib['offset'])) % windowX, int(i.attrib['py']), i.attrib['imagepath'], int(i.attrib['velocity']), delay, int(i.attrib['angle']), float(i.attrib['waittime'])) + ")\n"
		#* Repeat tag parsing, repeats tags inside it
		if i.tag == 'repeat':
			for _ in range(int(i.attrib['amount'])):
				for j in i:
					#* Delay tag parsing
					if j.tag == 'delay':
						delay += float(j.attrib['duration'])
					#* Bullet wall parsing
					if j.tag == 'bwallx':
						j.attrib[i.attrib['prop']] = str(int(j.attrib[i.attrib['prop']]) + int(i.attrib['increment']))
						spacing = int(j.attrib['spacing'])
						for spaces in range(0, int(windowY / spacing)):
							pstring = pstring + f"essg{count}.add(" + addEnemy(int(j.attrib['px']), (spaces * spacing + int(j.attrib['offset'])) % windowY, j.attrib['imagepath'], int(j.attrib['velocity']), delay, int(j.attrib['angle']), float(j.attrib['waittime'])) + ")\n"
					if j.tag == 'bwally':
						j.attrib[i.attrib['prop']] = str(int(j.attrib[i.attrib['prop']]) + int(i.attrib['increment']))
						spacing = int(j.attrib['spacing'])
						for spaces in range(0, int(windowX / spacing)):
							pstring = pstring + f"essg{count}.add(" + addEnemy((spaces * spacing + int(j.attrib['offset'])) % windowX, int(j.attrib['py']), j.attrib['imagepath'], int(j.attrib['velocity']), delay, int(j.attrib['angle']), float(j.attrib['waittime'])) + ")\n"
	for i in range(0, count):
		plstring = plstring + f"essg{i + 1}.update(dt)\n"
		plstring = plstring + f"essg{i + 1}.draw(screen)\n"
		plstring = plstring + f"has_died = has_died | player.collides(essg{i + 1})\n"
	return pstring, plstring