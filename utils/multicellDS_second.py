import os
import glob
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from scipy.io import loadmat
import xml.etree.ElementTree as ET

class MultiCellDS_second:
    def __init__(self, output_folder="./", xml_fname="initial.xml", sep="_"):
        self._output_folder = output_folder
        self._separator = sep
        self._globing = os.path.join(output_folder, "output*.xml")

        xml_fname = os.path.join(output_folder, xml_fname)
        self._tree = ET.parse(xml_fname)

        self._cell_columns = self._get_cell_columns()
        self._microenvironment_columns = self._get_microenvironment_columns()

    def _get_cell_info_recursive(self, node):
        for child in node:
            if child.tag == "simplified_data" and child.attrib.get("source") == "PhysiCell":
                return child
        return None
    
    def _get_cell_columns(self):
        root = self._tree.getroot()
        node = root.find("cellular_information/cell_populations/cell_population/custom/simplified_data/labels")

        cell_columns = []
        for child in node:
            column = child.text.strip()
            size = int(child.attrib.get("size", 1))  # Se `size` non esiste, usa 1

            if size == 1:
                cell_columns.append(column)
            else:
                suffixes = ['x', 'y', 'z', 'w', 'v', 'u'][:size]
                cell_columns.extend(f"{s}{self._separator}{column}" for s in suffixes)

        return cell_columns


    def _get_microenvironment_columns(self):
        root = self._tree.getroot()
        node = root.find("microenvironment/domain/variables")
        return [(child.attrib['name'], child.attrib['units'], child.attrib['ID']) for child in node.findall("variable")]

    def get_cells_matrix(self, tree):
        matfile = os.path.join(self._output_folder, self.get_cells_fname(tree))
        data = self._read_matlab_mat(matfile, "cells")
        return data.T if data is not None else None

    def get_cells_fname(self, tree):
        root = tree.getroot()

        # Trova il nodo <cellular_information>
        node = root.find("cellular_information/cell_populations/cell_population/custom/simplified_data")

        filename_node = node.find("filename")

        filename = filename_node.text.strip()  # Rimuove eventuali spazi bianchi

        return filename


    def _read_matlab_mat(self, fname, column):
        try:
            stru = loadmat(fname)
            return stru.get(column)
        except:
            print(f"Cannot read MAT file {fname}")
            return None
    
    def cells_as_frames_iterator(self):
        xml_list = sorted(glob.glob(self._globing))
        for xml_fname in xml_list:
            tree = ET.parse(xml_fname)
            cell_matrix = self.get_cells_matrix(tree)
            if cell_matrix is None:
                continue
            df = pd.DataFrame(cell_matrix, columns=self._cell_columns)
            df = df.set_index("ID")
            yield (self.get_time(tree), df)
    
    def get_time(self, tree):
        root = tree.getroot()
        node = root.find("metadata/current_time")
        return int(float(node.text))