import csv
import glob
import os
import re

def Main():
    #path="S:/Course work/Spring 19/Garmin/openaddr-collected-north_america-sa/jm"
    dir="S:/Course work/Spring 19/Garmin/openaddr-collected-europe-sa "
    subdirs = [x[0] for x in os.walk(dir)]
    for subdir in subdirs:
        for path in glob.glob(os.path.join(subdir, '*.csv')):
            with open(path, 'rt') as csvfile:
                csvData = csv.reader(csvfile)
                next(csvData, None)  # Skips headers
                it = next(csvData,"")
                try:
                    if(re.search("^node", it[9])):
                        print(path)
                except IndexError:
                    pass
if __name__== "__main__":
  Main()
