import xml.etree.ElementTree as ET


def parse(screen):
	windowX, windowY = screen.get_size()
	curr_delay = 0
	tree = ET.parse('level1.xml')
	pstring = ""
	plstring = ""
	tabs = 0
	count = 0
	delay = 0

	root = tree.getroot()

	def addEnemy(px, py, imagepath, velocity, delay, angle, waittime):
		return f"Enemy(screen, {px}, {py}, \"{imagepath}\", velocity={velocity}, delay={delay}, angle={angle}, waittime={waittime})"

	for i in root:
		if i.tag == 'delay':
			delay += int(i.attrib['duration'])
		if i.tag == 'section':
			count += 1
			pstring = pstring + f"essg{count} = pygame.sprite.Group()\n"
		if i.tag == 'bullet':
			pstring = pstring + f"essg{count}.add(" + addEnemy(int(i.attrib['px']), int(i.attrib['py']), i.attrib['imagepath'], int(i.attrib['velocity']), delay, int(i.attrib['angle']), int(i.attrib['waittime'])) + ")\n"
		if i.tag == 'bwallx':
			spacing = int(i.attrib['spacing'])
			for spaces in range(0, int(windowY / spacing)):
				pstring = pstring + f"essg{count}.add(" + addEnemy(int(i.attrib['px']), spaces * spacing, i.attrib['imagepath'], int(i.attrib['velocity']), delay, int(i.attrib['angle']), int(i.attrib['waittime'])) + ")\n"
	for i in range(0, count):
		plstring = plstring + f"essg{i + 1}.update(dt)\n"
		plstring = plstring + f"essg{i + 1}.draw(screen)\n"
		plstring = plstring + f"has_died = has_died | player.collides(essg{i + 1})"
	return pstring, plstring