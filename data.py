# a parser to scrape bgb.xml and return it in JSON format
# input: bgb.xml
# output: bgb.json
# usage: python data.py

import xml.etree.ElementTree as ET
import json
import re

def clean_string(string):
    if string is not None:
        # remove xml and html tags
        string = re.sub('<[^<]+?>', '', string)
        # remove newlines and whitespaces
        string = re.sub('\n', '', string)
        string = re.sub(' +', ' ', string)
    return string

def parse_xml(path_in, path_out):
    tree = ET.parse(path_in)
    root = tree.getroot()

    array = []

    for norm in root.findall('.//norm'):
        jurabk = norm.find('.//jurabk').text
        enbez = norm.find('.//enbez')
        title = norm.find('.//titel')
        content = ' '.join(norm.find('.//textdaten').itertext())
        if jurabk:
            if enbez is not None:
                enbez = enbez.text
            if title is not None:
                title = title.text
            if content is not None:
                content = content
            if title is None or content is None:
                    continue
            if "weggefallen" in content or "weggefallen" in title:
                    continue

            jurabk = clean_string(jurabk)
            enbez = clean_string(enbez)
            title = clean_string(title)
            content = clean_string(content)
            object = {'jurabk': jurabk, 'enbez': enbez, 'title': title, 'content': content}
            array.append(object)

    with open(path_out, 'w') as outfile:
        json.dump(array, outfile, indent=4, sort_keys=True, ensure_ascii=False)


if __name__ == "__main__":
    parse_xml('data/input/bgb.xml', 'data/output/bgb.json')
