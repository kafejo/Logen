__author__ = 'oskar'

import os, re, sys, getopt, codecs

path = '.'
output = 'default.strings'
append = False
unsafe_mode = False

# Parse arguments
try:
    opts, args = getopt.getopt(sys.argv[1:], "i:o:au", ["idir=", "ofile="])

except getopt.GetoptError:
    print('localization_generator.py -i <inputdirectory> -o <outputfile>\n ' \
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
    elif opt in ("-u", "--unsafe"):
        unsafe_mode = True

existing_keys = []
current_content = ''

# Check for existing keys

if append:
    ofile = codecs.open(output)
    opattern = re.compile(r'"(.*)"\s*=\s*".*";')
    current_content = ofile.read()

    if not unsafe_mode:
        # create backup
        backup_file = codecs.open(output + '.backup', 'w+', encoding='utf-8')
        backup_file.write(current_content)

    for (key) in re.findall(opattern, current_content):
        existing_keys.append(key)

    ofile.close()

# Search files for NSLocalizedString macro

localized_strings = ''
objc_pattern = re.compile(r'NSLocalizedString\(\s*@"([^"]*)",\s*@"((?:[^"]*)\s*)"\)')
swift_pattern = re.compile(r'NSLocalizedString\(\s*"([^"]*)",\scomment:\s*"((?:[^"]*)\s*)"\)')
new_keys = []

for dirpath, dirnames, filenames in os.walk(path):
    for filename in [f for f in filenames if f.endswith(".m") or f.endswith(".swift")]:
        file = open(os.path.join(dirpath, filename), 'r')

        fread = file.read()

        for (key, note) in re.findall(objc_pattern, fread):

            if key not in existing_keys:
                n = 'No comment provided' if note == 'nil' else note
                current_content += '\n/* ' + n + ' */\n"' + key + '" = "";\n'
                new_keys.append(key)
                existing_keys.append(key)

        for (key, note) in re.findall(swift_pattern, fread):

            if key not in existing_keys:
                n = 'No comment provided' if note == 'nil' else note
                current_content += '\n/* ' + n + ' */\n"' + key + '" = "";\n'
                new_keys.append(key)
                existing_keys.append(key)

# Write new file with changes

ofile = codecs.open(output, mode='w+')
ofile.write(current_content)

# Report what's happened

if len(new_keys) == 0:
    print("Done. New keys weren't find")
else:
    print("Success! New keys: ", ', '.join(new_keys))
