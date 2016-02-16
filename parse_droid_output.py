import csv
import os

from os.path import join

def parse_droid_output(droid_output):
	extensions = {}
	mimetypes = {}
	pronom_ids = {}
	with open(droid_output,'rb') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			extension = row['EXT']
			mimetype = row['MIME_TYPE']
			pronom_id = row['PUID']
			if extension:
				if extension not in extensions:
					extensions[extension] = 0
				extensions[extension] += 1
			if mimetype:
				if mimetype not in mimetypes:
					mimetypes[mimetype] = 0
				mimetypes[mimetype] += 1
			if pronom_id:
				if pronom_id not in pronom_ids:
					pronom_ids[pronom_id] = 0
				pronom_ids[pronom_id] += 1
	print "\n"
	print "*** TOP 5 EXTENSIONS ***"
	print_top_five(extensions)
	print "\n"
	print "*** TOP 5 MIMETYPES ***"
	print_top_five(mimetypes)
	print "\n"
	print "*** TOP 5 PUIDS ***"
	print_top_five(pronom_ids)

def print_top_five(dictionary):
	sorted_dictionary = sorted(dictionary, key=dictionary.get, reverse=True)
	for n in range(5):
		key = sorted_dictionary[n]
		value = dictionary[key]
		print "{0}. {1} - {2}".format(n+1, key, value)

def main():
	example_files = "example_files"
	droid_output = join(example_files,'DROID.csv')
	parse_droid_output(droid_output)

if __name__ == "__main__":
	main()