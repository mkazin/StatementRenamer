from .reader import Reader


class FilenameReader(Reader):

    def parse(self, fname):
        return fname

# This is the contents of my old AmEx statement renamer, which
# used the filename as the data source.

# import os
# import re

# month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
#          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
# path = './'
# listing = os.listdir(path)
# for infile in listing:
# # print "current file is: " + infile

#   result = re.match("Statement_(\w+) (\d+).pdf", infile);

#   if (result):
#       month_number = month_names.index(result.group(1)) + 1
#       new_name = 'AmExBlue_' + result.group(2) + '_' + str(month_number).zfill(2) + '.pdf'

#       if os.path.isfile(new_name):
#           print 'File [' + new_name + '] already exists.  Ignoring [ ' + infile + ']'
#           continue

#       os.rename(infile, new_name)
#       print 'Renamed [' + infile + '] to : [' + new_name + ']'
# # else:
# #     print '   (skipped ' + infile + ')'
