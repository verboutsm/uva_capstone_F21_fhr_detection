"""Accessing and interacting with Record files"""
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

        # Call to get annotations
        self.__getannotations__(self.record_name)

    def __getannotations__(self, record_name) -> None:
        """Gets the annotations from the annotation csv file
        and populates the appropriate annotation list"""

        with open(f'../data/annotations/csv/annotation_{record_name}.csv', newline='',
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
