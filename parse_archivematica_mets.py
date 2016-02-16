import os

from datetime import datetime
from lxml import etree
from os.path import join

namespaces = {
"mets": "http://www.loc.gov/METS/",
"premis": "info:lc/xmlns/premis-v2"
}

def parse_archivematica_mets(archivematica_mets):
	tree = etree.parse(archivematica_mets)

	amdSecs = tree.xpath('//mets:amdSec', namespaces=namespaces)

	amdSec_dict = {}
	for amdSec in amdSecs:
		amdSec_ID = amdSec.attrib['ID']
		techMD = amdSec.xpath('./mets:techMD', namespaces=namespaces)[0]
		filename = techMD.xpath('.//premis:originalName', namespaces=namespaces)[0].text.split('/')[-1]
		rightsMDs = amdSec.xpath('./mets:rightsMD',namespaces=namespaces)
		if rightsMDs:
			rightsMD = tree.getpath(rightsMDs[0])
		else:
			rightsMD = False

		amdSec_dict[amdSec_ID] = {
		"filename":filename,
		"rightsMD":rightsMD
		}
	parse_rights(tree, amdSec_dict)

def make_selection(amdSec_dict):
	print "\n"
	amdSec_ids = sorted(amdSec_dict)
	for amdSec_id in amdSec_ids:
		print "{0} - {1}".format(amdSec_ids.index(amdSec_id)+1, amdSec_dict[amdSec_id]['filename'])
	selection = raw_input("Select a file to view rights information: ")

	try:
		selection = int(selection)-1
	except:
		print "\n"
		print "*** Please enter a number ***"
		make_selection(amdSec_dict)

	if selection in range(len(amdSec_ids)):
		return amdSec_ids[selection]
	else:
		print "\n"
		print "*** Please choose one of the provided options ***"
		make_selection(amdSec_dict)

def print_rights_info(tree, selection):
	print "\n"
	if selection['rightsMD'] is not False:
		rightsMD = tree.xpath(selection['rightsMD'], namespaces=namespaces)[0]
		rightsBasis = rightsMD.xpath('.//premis:rightsBasis', namespaces=namespaces)[0].text
		
		rights_info = {}
		if rightsBasis.lower() == 'other':
			otherRightsBasis = rightsMD.xpath('.//premis:otherRightsBasis',namespaces=namespaces)[0].text
			otherRightsNotes = rightsMD.xpath('.//premis:otherRightsNote',namespaces=namespaces)
			if otherRightsNotes:
				otherRightsNote = otherRightsNotes[0].text
			else:
				otherRightsNote = False
			rights_info['basis'] = otherRightsBasis
			rights_info['note'] = otherRightsNote
		elif rightsBasis.lower() == 'copyright':
			rights_info['basis'] = 'Copyright'
			copyrightNotes = rightsMD.xpath('.//premis:copyrightNote',namespaces=namespaces)
			if copyrightNotes:
				copyrightNote = copyrightNotes[0].text
			else:
				copyrightNote = False
			rights_info['note'] = copyrightNote
		rightsGranteds = rightsMD.xpath('.//premis:rightsGranted', namespaces=namespaces)
		if rightsGranteds:
			rightsGranted = rightsGranteds[0]
			rights_info['act'] = rightsGranted.xpath('.//premis:act',namespaces=namespaces)[0].text
			rights_info['restriction'] = rightsGranted.xpath('.//premis:restriction',namespaces=namespaces)[0].text
			start_date = rightsGranted.xpath('.//premis:startDate',namespaces=namespaces)
			end_date = rightsGranted.xpath('.//premis:endDate',namespaces=namespaces)
			if start_date:
				rights_info['start_date'] = start_date[0].text
			if end_date:
				rights_info['end_date'] = end_date[0].text

		if 'end_date' in rights_info:
			now = datetime.now().strftime("%Y-%m-%d")
			if now < rights_info['end_date']:
				in_effect = "This restriction is still in effect"
			else:
				in_effect = "This restriction has expired"
		else:
			in_effect = 'This Rights statement has no time component'

		print "{0} has the following PREMIS Rights information:".format(selection['filename'])
		print "\n"
		print_order = ['basis','note','act','restriction','start_date','end_date']
		translations = {'basis':'Basis','note':'Note','act':'Act','restriction':'Restriction','start_date':'Start Date','end_date':'End Date','in_effect':''}
		for field in print_order:
			if field in rights_info:
				print "{0}: {1}".format(translations[field], rights_info[field])
		print in_effect

	else:
		print "{0} has no PREMIS Rights information".format(selection['filename'])

def parse_rights(tree, amdSec_dict):
	selection = make_selection(amdSec_dict)
	print_rights_info(tree, amdSec_dict[selection])

	while True:
		print "\n"
		another = raw_input("Select another file? (y/n):")
		if another.lower() == 'y':
			selection = make_selection(amdSec_dict)
			print_rights_info(tree, amdSec_dict[selection])
		else:
			print "Bye!"
			quit()

def main():
	example_files = 'example_files'
	archivematica_mets = join(example_files,'archivematica_mets.xml')
	parse_archivematica_mets(archivematica_mets)

if __name__ == "__main__":
	main()