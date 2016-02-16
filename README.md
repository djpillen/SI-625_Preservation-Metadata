#SI 625 - Preservation Metadata
Example files and instructions for SI 625 Preservation Metadata lecture and exercises

##Requirements/Setup

* Install [Python 2.7](https://www.python.org/)
** Install [pip](https://pip.pypa.io/en/stable/installing/) if necessary (new installations of Python should come with pip)
* Install [lxml](http://lxml.de/)
** Try `pip install lxml`
** Windows: Download and install lxml-3.4.4.win32-py2.7.exe from the lxml [Python Package Index](https://pypi.python.org/pypi/lxml/3.4.4)
** Mac: You may need to install Xcode if you have not already done so
* Clone or download a ZIP of this repo

##Introduction

Preservation metadata is defined in the [PREMIS Data Dictionary](http://www.loc.gov/standards/premis/v3/premis-3-0-final.pdf) as "[T]he information a repository uses to support the digital preservation process." This can include administrative, technical, and structural metadata.

Preservation metadata allows repositories and archivists to manage Archival Information Packages (AIPs). It can provide an understanding of past preservation actions (such as file format identification, virus scans, and file format conversions) and current technical and administrative characteristics (such as fixity and rights information), as well as facilitate future preservation actions (such as file format migrations, fixity checks, and use).

The PREMIS Data Dictionary defines "semantic units" rather than "metadata elements" due to the "need to know rather than the need to record or represent in any particular way." The included example files and scripts demonstrate how to record and parse preservation metadata that has been represented in some particular ways, including in the form of CSV outputs from the Bentley Historical Library's AutoPro and the [DROID](http://www.nationalarchives.gov.uk/information-management/manage-information/preserving-digital-records/droid/) file format identification tool and METS XML from [Deep Blue](http://deepblue.lib.umich.edu/handle/2027.42/65133) and [Archivematica](https://www.archivematica.org/en/).

##Example files

The `example_files` directory includes the following:
* archivematica_mets.xml - Sample METS XML output from Archivematica
* convertedFiles.csv - CSV output showing files converted during digital processing, including the starting filename, its derivative, and the software used
* DROID.csv - CSV output from a DROID file format identification scan
* dspace_mets.xml - METS XML from Deep Blue, UM's DSpace repository
* PREMIS.csv - CSV detailing preservation events during digital processing, including details of each event, the agent responsible, and the software used

##Parsing DROID output

Use `parse_droid_output.py` to output the top 5 file extensions, mimetypes, and PRONOM IDs from a sample DROID CSV output.

Technical metadata, such as file format information, aids future preservation activities such as format migrations.

##Parsing DSpace METS

Use `parse_dspace_mets.py` to parse a sample METS file from Deep Blue and output the identifier, checksum, file size, and mimetype for each file in the METS fileSec.

Technical metadata, such as file format and checksum information, is necessary for future preservation activities such as format migration and fixity checks.

##Parsing Archivematica METS

Use `parse_archivematica_mets.py` to parse a sample METS file from Archivematica and output PREMIS Rights information for each METS amdSec.

Rights metadata aids in preservation by detailing what actions a repository is permitted to take on a digital object, and can also be used to enforce access and/or use restrictions based on copyright, donor agreement, or other policies.