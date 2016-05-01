import sys
import getopt
import StringsTools
import os
import re

__author__ = 'Ales Oskar Kocur'

path = '.'
output = ''
rewrite = False
verbose = False

# Parse arguments
try:
    opts, args = getopt.getopt(sys.argv[1:], "i:o:ruv", ["idir=", "ofile=", "rewrite", "verbose"])

except getopt.GetoptError:
    print('Logen.py -i <inputdirectory>\n' \
          '-o <outputfile>\n' \
          '-r rewrites the output file (not append)\n' \
          '-v verbose mode')
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-i", "--idir"):
        path = arg
    elif opt in ("-o", "--ofile"):
        output = arg
    elif opt in ("-r", "--rewrites"):
        rewrite = True
    elif opt in ("-v", "--verbose"):
        verbose = True

# Check for existing keys

strings_files = []

if output == "":
    for p, dir_names, file_names in os.walk(path):
        for file_name in [f for f in file_names if f.endswith("Localizable.strings")]:
            m = re.search('.*/(.+?)\.lproj', p)
            if m:
                language = m.group(1)
                strings_file = StringsTools.StringsFile(os.path.join(p, file_name), language)
                strings_files.append(strings_file)
    if verbose:
        print("Found languages:", ",".join([l.language for l in strings_files]))
else:
    strings_file = StringsTools.StringsFile(output, "")
    strings_files.append(strings_file)
    
if verbose:
    print("Scanning for localizations in *.swift and *.m files")

parser = StringsTools.StringsParser(path)
items = parser.get_keys_and_comments()

for strings_file in strings_files:

    localized_strings = ''
    existing_keys = []

    if verbose:
        print("== Language:", strings_file.language)

    if not rewrite:
        existing_keys = strings_file.read_existing_keys()

        if verbose:
            filename = os.path.basename(strings_file.strings_file_path)
            print("Found existing keys in file", filename)
            print("\n".join(existing_keys))

    # Search files for NSLocalizedString macro

    formatted_content = ''
    new_key_and_comment = []

    for (key, comment) in items:
        if key not in existing_keys:
            new_key_and_comment.append((key, comment))

    if verbose:
        print("Found", len(items), "keys.", len(new_key_and_comment), "of them are new.")

    # Write new file with changes
    strings_file.write(new_key_and_comment, not rewrite)

    # Report what's happened

    if len(new_key_and_comment) == 0:
        print("Done! There are no new keys.")
    else:
        if verbose:
            print("Done! New keys:")
            print(', '.join([key for (key, note) in new_key_and_comment]))
        else:
            print("Done! Number of new keys:", len(new_key_and_comment))
