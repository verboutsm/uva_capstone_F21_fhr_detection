"""Accessing and interacting with Record files"""
# imports
import matplotlib.pyplot as plt
import numpy.ma as ma
import pandas as pd
import glob
import os
import csv

class Record():
    """Class for interacting with record files"""

    def __init__(self, record_name: str) -> None:
        """Initialzes the record class"""
        self.record_name = record_name
        self.uc_list = []
        self.dec_list = []
        self.acc_list = []
        self.tachy_list = []
        self.brady_list = []
        self._signalDf = pd.read_csv(f'./data/database/signals/{record_name}.csv')

        # Call to get annotations
        self.__getannotations(self.record_name)

        # call to static method to create uc_dict
        self.uc_pairs = self.uc_list_to_dict(self.uc_list)        

    def __getannotations(self, record_name) -> None:
        """Gets the annotations from the annotation csv file
        and populates the appropriate annotation list"""

        with open(f'./data/annotations/csv/annotation_{record_name}.csv', newline='',
        encoding='UTF-8') as csvfile:
            annreader = csv.reader(csvfile, delimiter=',')
            for i, row in enumerate(annreader):
                joined_row = ''.join(row)
                if 'UC' in joined_row:
                    self.uc_list.append((i, joined_row))
                if 'DEC' in joined_row:
                    self.dec_list.append((i, joined_row))
                if 'ACC' in joined_row:
                    self.acc_list.append((i, joined_row))
                if 'TC' in joined_row:
                    self.tachy_list.append((i, joined_row))
                if 'BC' in joined_row:
                    self.brady_list.append((i, joined_row))

    def plotUC(self, ucNum: int):
        """Plots the UC contraction and FHR specified by ucNum"""
        plotNum = 'UC'+str(ucNum)
        if plotNum in self.uc_pairs.keys():
            start, end = self.uc_pairs[plotNum]
            x = self._signalDf['seconds'][start:end].to_numpy()
            y_uc = self._signalDf['UC'][start:end].to_numpy()
            y_fhr = self._signalDf['FHR'][start:end].to_numpy()

            fig, ax = plt.subplots(nrows=1, ncols=1)
            ax.set_title(f'Record {self.record_name} {plotNum}')
            ax.plot(x, y_uc, '#1f77b4', x, y_fhr, '#ff7f0e')
            ax.set_xlim(start+2, end+2)
            ax.set_ylim(0, 200)
            fig.set_size_inches(18, 8)

            plt.show()


    def _savePlot(self, ucStr):
        """Plots the UC contraction and FHR specified by ucNum"""
        plotNum = ucStr
        if plotNum in self.uc_pairs.keys():
            start, end = self.uc_pairs[plotNum]
            x = self._signalDf['seconds'][start:end].to_numpy()
            y_uc = self._signalDf['UC'][start:end].to_numpy()
            y_fhr = self._signalDf['FHR'][start:end].to_numpy()
            
            fig, ax = plt.subplots(nrows=1, ncols=1)
            ax.set_title(f'Record {self.record_name} {plotNum}')
            ax.plot(x, y_uc, '#1f77b4', x, y_fhr, '#ff7f0e')
            ax.set_xlim(start+2, end+2)
            ax.set_ylim(0, 200)
            fig.set_size_inches(18, 8)

            fig = plt.gcf()
            fig.set_size_inches(18, 8)
            fig.savefig(f"./data/images/record_{self.record_name}/{plotNum}.png", bbox_inches='tight')
            plt.close(fig)

    def saveImages(self):
        """Saves the images in ./data/images/{record_name}"""
        for key, val in self.uc_pairs.items():
            self._savePlot(key)
        print(f"Images for Record {self.record_name} have been saved.")
                
    def clearImages(self):
        """Deletes the images in ./data/images/{record_name}"""
        imgs = glob.glob(f'./data/images/record_{self.record_name}/*.png', recursive=True)

        for img in imgs:
            try:
                os.remove(img)
            except OSError as e:
                print("Error: %s : %s" % (img, e.strerror))
            
    @staticmethod
    def uc_list_to_dict(uc_list: list) -> dict:
        """Converts list to dict and removes all unmatched UCs (due to signal loss)"""
        uc_dict = {}
        size = len(uc_list) - 1
        for i, _ in enumerate(uc_list):
            if i + 1 > size:
                break
            if uc_list[i][1][1:] == uc_list[i+1][1][1:]:
                uc_dict[uc_list[i][1][1:]] = (uc_list[i][0], uc_list[i+1][0])
                i += 1
        return uc_dict

    @staticmethod
    def interpolate_zeros(arr):
        mask = ma.masked_where(arr == 0)
        

        