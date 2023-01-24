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

	for i in root:
		if i.tag == 'delay':
			delay += int(i.attrib['duration'])
		if i.tag == 'section':
			count += 1
			pstring = pstring + f"essg{count} = pygame.sprite.Group()\n"
		if i.tag == 'bullet':
			pstring = pstring + f"essg{count}.add(Enemy(screen, {int(i.attrib['px'])}, {int(i.attrib['py'])}, \"{i.attrib['imagepath']}\", velocity={int(i.attrib['velocity'])}, delay={delay}, angle={int(i.attrib['angle'])}, waittime={int(i.attrib['waittime'])}))\n"
	for i in range(0, count):
		plstring = plstring + f"essg{i + 1}.update(dt)\n"
		plstring = plstring + f"essg{i + 1}.draw(screen)\n"
		plstring = plstring + f"has_died = has_died | player.collides(essg{i + 1})"
	return pstring, plstring