"""
Flattens the OpenTaxonomy for tagging purposes
Currently parses v2.0

Source for the taxonomy: 
http://openeligibility.org
"""

__author__ = 'Risto Stevcev'
  
import argparse      
import xml.etree.ElementTree as ET
import json


class Flattener(object):
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.services = set()
        self.situations = set()
        self.tags = {}
    
    def run(self):
        tree = ET.parse(self.input_file)
        root = tree.getroot()
        self.flatten(self.services, root.find('services'))
        self.flatten(self.situations, root.find('situations'))

        self.tags = {"services": sorted(list(self.services)), "situations": sorted(list(self.situations))}
        json.dump(self.tags, self.output_file)

    def flatten(self, tags, node):
        if not node:
            return
        for item in node:
            title = item.attrib.get('title')
            if title:
                tags.add(title.lower())
            self.flatten(tags, item)


def main():
    argparser = argparse.ArgumentParser(description='OpenTaxonomy Flattener - by %s.' % __author__)
    argparser.add_argument('-i', '-input-file', type=argparse.FileType('r'), required=True, 
            help='taxonomy file (xml)')
    argparser.add_argument('-o', '-output-file', type=argparse.FileType('w'), required=True, 
            help='output file (json)')
    args = argparser.parse_args()

    flattener = Flattener(args.i, args.o)
    flattener.run()

    print("Complete: the taxonomy file '%s' has been flattened into '%s'." % (args.i.name, args.o.name))
    args.i.close()
    args.o.close()


if __name__ == "__main__":
    main()
