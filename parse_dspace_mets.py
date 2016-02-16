import os

from lxml import etree
from os.path import join

def parse_dspace_mets(dspace_mets):
	tree = etree.parse(dspace_mets)
	ns = {'mets':'http://www.loc.gov/METS/','dim': 'http://www.dspace.org/xmlns/dspace/dim','xlink':'http://www.w3.org/TR/xlink/'}
	XLINK = 'http://www.w3.org/TR/xlink/'
	abstract = tree.xpath("//dim:field[@element='description'][@qualifier='abstract']", namespaces=ns)[0].text
	item_title = tree.xpath("//dim:field[@element='title']", namespaces=ns)[0].text
	handle = tree.xpath("//dim:field[@element='identifier'][@qualifier='uri']", namespaces=ns)[0].text
	rights = tree.xpath("//dim:field[@element='rights'][@qualifier='access']", namespaces=ns)[0].text
	titles = []
	files_info = {}
	fileGrp = tree.xpath("//mets:fileGrp[@USE='CONTENT']", namespaces=ns)[0]
	mets_files = fileGrp.xpath('./mets:file',namespaces=ns)
	for mets_file in mets_files:
		FLocat = mets_file.xpath('./mets:FLocat',namespaces=ns)[0]
		mimetype = mets_file.attrib['MIMETYPE']
		checksum = mets_file.attrib['CHECKSUM']
		size = mets_file.attrib['SIZE']
		file_id = mets_file.attrib['ID']
		title = FLocat.attrib['{%s}title' % (XLINK)].strip()
		titles.append(title)

		files_info[title] = {
		"title":title,
		"mimetype":mimetype,
		"checksum":checksum,
		"size":size,
		"ID":file_id
		}

	print "Title: {0}".format(item_title)
	print "Handle: {0}".format(handle)
	print "Description: {0}".format(abstract)
	print "Rights: {0}".format(rights)
	
	title = choose_dspace_mets_file(titles, files_info)
	file_info = files_info[title]
	print_file_info(file_info)
			
	while True:
		print "\n"
		another = raw_input("Choose another file? (y/n): ")
		if another.lower() == 'y':
			title = choose_dspace_mets_file(titles, files_info)
			file_info = files_info[title]
			print_file_info(file_info)
		else:
			print "Bye!"
			quit()

def choose_dspace_mets_file(titles, files_info):
	print "\n"
	for title in titles:
		option = titles.index(title)
		print "{0} - {1}".format(option+1, title)
	action = raw_input("Choose a number or enter q to quit: ")
	if action.lower() == 'q':
		print "Bye!"
		quit()
		
	try:
		action = int(action) - 1
	except:
		print "\n"
		print "*** Please enter a number ***"
		choose_dspace_mets_file(titles, files_info)

	if action in range(len(titles)):
		title = titles[action]
	else:
		print "\n"
		print "*** Please choose one of the given options ***"
		choose_dspace_mets_file(titles, files_info)
	return title

def print_file_info(file_info):
	print "\n"
	print "Title: {0}".format(file_info['title'])
	print "ID: {0}".format(file_info['ID'])
	print "Mimetype: {0}".format(file_info['mimetype'])
	print "Size: {0} bytes".format(file_info['size'])
	print "Checksum: {0}".format(file_info['checksum'])

def main():
	example_files = "example_files"
	dspace_mets = join(example_files,'dspace_mets.xml')
	parse_dspace_mets(dspace_mets)

if __name__ == "__main__":
	main()