#!/usr/bin/env python

# Author: Luca Ferroni <luca@befair.it>
# License: GNU Affero General Public License

import csv, os, time

# TODO: 
# 1) Get delimiter from locale settings
# 2) Optional filename. Ask for overwriting existing file if necessary

class CSVManager:
    def __init__(self, fieldnames, delimiter=";", encoding='utf-8'):
        
        self.filename = "/tmp/csv_" + str(time.time())
        self.fieldnames = fieldnames
        self.delimiter = delimiter
        self.encoding = encoding

    def read(self, csvdata):
        #Write CSV file with data
        s = csv.Sniffer()
        if s.has_header(csvdata):
            csvdata = csvdata[csvdata.find("\n")+1:]
        csvfile = file(self.filename, "w")
        csvfile.write(csvdata)
        csvfile.close()

        #Read data into dictionary
        csvfile = file(self.filename, "r")
        csvr = csv.DictReader(csvfile, fieldnames=self.fieldnames, delimiter=self.delimiter)
        rows = []
        for r in csvr:
            #print("DEBUG", r)
            for k,v in r.items():
                r[k] = v.decode(self.encoding)
            rows.append(r)
        csvfile.close()
        os.remove(self.filename)
        return rows

    def write(self, rows, header=True):

        #Write CSV file with rows data ignoring fields not included in fieldnames list
        csvfile = file(self.filename, "w")
        csvwriter = csv.DictWriter(csvfile, fieldnames=self.fieldnames, delimiter=self.delimiter, extrasaction='ignore')

        if header:
            header_d = {}
            for field in self.fieldnames:
                header_d[field] = field.upper()
            csvwriter.writerow(header_d)

        for r in rows:
            csvwriter.writerow(r)
        csvfile.close()

        #Return csv data
        csvfile = file(self.filename, "r")
        csvdata = csvfile.read().decode('latin-1')
        csvfile.close()
        os.remove(self.filename)
        return csvdata

#----------------------------------------------------------

if __name__ == "__main__":
    import sys
    try:
        filename = sys.argv[1]
        fieldnames = sys.argv[2].split(",")
    except IndexError:
        print "Usage: %s <filename> <fieldname1>[,[fieldname2],...]" % sys.argv[0]
        sys.exit(0)

    f = file(filename, "r")
    csvdata = f.read()
    f.close()
    m = CSVManager(fieldnames=fieldnames)
    print m.read(csvdata)
    
