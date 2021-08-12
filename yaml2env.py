#!/usr/bin/env python3

##
## Given a list of YAML file(s) merge them together 
## and output the key and values as environment variables
##

#Based on the code from Veritone DevOps Team - devops@veritone.com

# Imports
import argparse
import os
import re
import sys
import hiyapyco
from visitor import Visitor


def parseArgs():
    parser = argparse.ArgumentParser(description='YAML to OS environment variable parser')
    parser.add_argument('-f', '--file', action='append', nargs='+', help='The filename of the manifest to be read.')
    parser.add_argument('-y', '--dump', action='store_true', help='Dump parsed and merged YAML file(s)')
    return parser.parse_args()

##
## Create a list from a dictionary
## that can be parsed and used
## to create environment variables
def read_dict(dictionary):
    write_list = []

    if(isinstance(dictionary, dict)):
        for key in dictionary:
            write_list.append(key)
            if(not isinstance(dictionary[key], str)):
                write_list += read_dict(dictionary[key])
    else:
        # recursive function
        write_list.append(str(dictionary))
    return write_list
##
## Create an OS variable from
## string and list of items
def create_os_var(prefix, string, listItems):
    listItems.insert(0,prefix)
    listItems.insert(1,string)
    value = listItems.pop()
    varName = "_".join(listItems)
    varName = re.sub(r'\.|-', '_', varName)
    return("%s=\"%s\"" % (varName.upper(),value))


class EnvEncoder(Visitor):
    def __init__(self):
        self.parentKey = ""

    def visit_NoneType(self, node):
        print(self.parentKey + "=")

    def visit_str(self, node):
        print(self.parentKey + "=" + node)

    def visit_int(self, node):
        return self.visit(str(node))

    def visit_bool(self, node):
        return self.visit(str(node).lower())

    def visit_list(self, node):
        # If list is empty, print empty value
        if len(node) == 0:
          print(self.parentKey + "=")
        elif len(node) > 0:
              values = []
              for item in node:
                  if isinstance(item, list) or isinstance(item, dict):
                      self.visit(item)
                  else:
                      values.append(item)
              if values:
                print(self.parentKey + "=" + ",".join(values))

    def visit_dict(self, node):
        prevParent = self.parentKey
        for key, value in sorted(node.items()):
            self.parentKey = prevParent + ("" if prevParent == "" else "_") + key.upper()
            if type(value) == str:
                print(self.parentKey + "=" + value)
            else:
                self.visit(value)
        # Pop the last known key
        self.parentKey = prevParent


def main():
    # Parse the arguments
    arguments = parseArgs()

    if arguments.file is None:
        raise ValueError("YamlFile(s) not defined. ")
    yamlFiles = arguments.file

    try:
        data = hiyapyco.load(yamlFiles, method=hiyapyco.METHOD_MERGE)

        if arguments.dump:
          # Print YAML output
          print(hiyapyco.dump(data, default_flow_style=False))
        else:
          # Print Env Var output
          EnvEncoder().visit(data)

    except Exception as e:
        print("Error: %s" % e)
        sys.exit(1)

if __name__ == '__main__':
    main()
