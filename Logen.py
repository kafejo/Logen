import sys
import getopt
import StringsTools

__author__ = 'Ales Oskar Kocur'

path = '.'
output = 'Localizable.strings'
append = False

# Parse arguments
try:
    opts, args = getopt.getopt(sys.argv[1:], "i:o:au", ["idir=", "ofile="])

except getopt.GetoptError:
    print('Logen.py -i <inputdirectory> -o <outputfile>\n ' \
          '-a for appending only new keys at the end of the output file\n' \
          '-u for unsafe mode, no backup file is created')
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-i", "--idir"):
        path = arg
    elif opt in ("-o", "--ofile"):
        output = arg
    elif opt in ("-a", "--append"):
        append = True

# Check for existing keys

reader_writer = StringsTools.StringsReaderWriter(output)
parser = StringsTools.StringsParser(path)

existing_keys = []
localized_strings = ''

if append:
    existing_keys = reader_writer.read_existing_keys()

# Search files for NSLocalizedString macro

items = parser.get_keys_values()
formatted_content = ''
new_key_comment = []

for (key, note) in items:
    if key not in existing_keys:
        new_key_comment.append((key, note))

# Write new file with changes
reader_writer.write(new_key_comment, append)

# Report what's happened

if len(new_key_comment) == 0:
    print("Done! There are no new keys.")
else:
    print("Done! New keys: ", new_key_comment)
