import sys
import getopt
import StringsTools
import os

__author__ = 'Ales Oskar Kocur'

path = '.'
output = 'Localizable.strings'
append = False
verbose = False

# Parse arguments
try:
    opts, args = getopt.getopt(sys.argv[1:], "i:o:auv", ["idir=", "ofile=", "verbose"])

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
    elif opt in ("-v", "--verbose"):
        verbose = True

# Check for existing keys

reader_writer = StringsTools.StringsReaderWriter(output)
parser = StringsTools.StringsParser(path)

existing_keys = []
localized_strings = ''

if append:
    existing_keys = reader_writer.read_existing_keys()

    if verbose:
        filename = os.path.basename(reader_writer.strings_file_path)
        print("Found existing keys in file", filename)
        print("\n".join(existing_keys))

# Search files for NSLocalizedString macro

if verbose:
    print("Scanning for localizations in *.swift and *.m files")

items = parser.get_keys_and_comments()

formatted_content = ''
new_key_and_comment = []

for (key, comment) in items:
    if key not in existing_keys:
        new_key_and_comment.append((key, comment))

if verbose:
    print("Found", len(items), "keys.", len(new_key_and_comment), "of them are new.")

# Write new file with changes
reader_writer.write(new_key_and_comment, append)

# Report what's happened

if len(new_key_and_comment) == 0:
    print("Done! There are no new keys.")
else:
    if verbose:
        print("Done! New keys:")
        print(', '.join([key for (key, note) in new_key_and_comment]))
    else:
        print("Done! Number of new keys:", len(new_key_and_comment))
