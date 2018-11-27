#!/usr/bin/env python3

import sys
import lxml.etree as ET

tree = ET.parse(sys.argv[1])
newtree = ET.parse(sys.argv[1])

for e in tree.iter():
	idref = e.get('IDREF')
	if idref is None:
		continue
	newe = newtree.find(".//*[@IDREF='{}']".format(idref))
	orig = tree.find(".//*[@ID='{}']".format(idref))
	newe.clear()
	newe.tag = orig.tag
	newe[:] = list(orig)
	for attrib in orig.items():
		if attrib[0] == 'ID':
			continue
		newe.set(attrib[0], attrib[1])
	newe.text = orig.text


newroot = newtree.getroot()
pliste = ET.Element('plist', attrib={'version': '1.0'})
pliste.append(newroot)
newtree._setroot(pliste)
with open(sys.argv[2], 'wb') as outf:
	outf.write(ET.tostring(
		newtree,
		pretty_print=True,
		xml_declaration=True,
		encoding='UTF-8',
		doctype='<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">'
	))
