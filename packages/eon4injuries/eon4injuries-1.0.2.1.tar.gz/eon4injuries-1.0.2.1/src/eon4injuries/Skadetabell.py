# author: Oliver Glant
# email: oliver.glant@gmail.com
# Eon IV injury tables

import os
import importlib.resources as pkg_resources


class Skadetabell:
    table = {}
    content_list = []

    def __init__(self):
        filename = 'skadetabell.txt'

        # Check current directory first
        if os.path.isfile(filename):
            file_path = filename
        else:
            # If not found, check the eon4injuries package
            if pkg_resources.is_resource('eon4injuries', filename):
                with pkg_resources.path('eon4injuries', filename) as package_path:
                    file_path = str(package_path)
            else:
                raise FileNotFoundError(f"{filename} not found in the current directory or the eon4injuries package.")

        with open(file_path, 'r', encoding="utf-8") as file:
            current_table = []
            nameflag = True
            for line in file.readlines():
                if line.strip() == 'XXX':
                    nameflag = True  # True om nästa rad är namnet på tabellen
                    table_name = current_table[0].strip()
                    self.content_list.append(table_name)
                    table_contents = current_table[0:]
                    self.table[table_name] = table_contents
                    current_table = []
                elif line[0].isdigit() or nameflag:
                    current_table.append(line)
                    nameflag = False
                else:
                    current_table[-1] = current_table[-1] + ' ' + line
