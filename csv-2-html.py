import os
import csv
import pandas


pandas.set_option('display.max_rows', None)
parent_directory = os.path.expanduser('~')
file = os.path.join(parent_directory, 'ORACC-Files',     # location of files (from unzip)
                    'oracc.csv')                    # target catalogue

df = pandas.read_csv(file)
print(df)
