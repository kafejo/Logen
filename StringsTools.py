import os
import re
import codecs


class StringsFile:
    def __init__(self, strings_file_path, language):
        self.strings_file_path = strings_file_path
        self.language = language
        # Load current content from file
        f = codecs.open(strings_file_path, encoding='utf-8')
        self.current_content = f.read()
        f.close()

    def read_existing_keys(self):
        strings_pattern = re.compile(r'"(.*)"\s*=\s*".*";')
        existing_keys = []

        for (key) in re.findall(strings_pattern, self.current_content):
            existing_keys.append(key)

        return existing_keys

    def write(self, key_comments, append=True):
        formatted_content = ''

        for (key, comment) in key_comments:
            n = 'No comment provided' if comment == 'nil' or comment == '' else comment
            formatted_content += '\n/* ' + n + ' */\n"' + key + '" = "";\n'

        if append:
            f = codecs.open(self.strings_file_path, mode='a', encoding='utf-8')
            f.write(formatted_content)
        else:
            f = codecs.open(self.strings_file_path, mode='w+')
            f.write(formatted_content)

        f.close()


class StringsParser:
    def __init__(self, dir_path):
        self.dir_path = dir_path

    def get_keys_and_comments(self):
        found_items = []

        objc_pattern = re.compile(r'NSLocalizedString\(\s*@"([^"]*?)",\s*?@"((?:[^"]*?)\s*?)"\)')
        # This regex matches the NSLocalizedString function and its key and comment parameters
        swift_pattern = re.compile(r'NSLocalizedString\(\s*"([^"]*?)",(?:(?!tableName).)*?comment:\s*?"((?:[^"]*?)*?)"\)')

        for path, dir_names, file_names in os.walk(self.dir_path):

            for filename in [f for f in file_names if f.endswith(".m") or f.endswith(".swift")]:
                file = open(os.path.join(path, filename), 'r')

                f_read = file.read()
                found_items.extend(re.findall(objc_pattern, f_read))
                found_items.extend(re.findall(swift_pattern, f_read))

        return found_items
