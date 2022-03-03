"""Main Function"""
from record import Record
import os
import glob

if __name__ == "__main__":
    record_nums = map(lambda x: x[-8:-4], os.listdir("./data/annotations/csv"))
    img_dirs = list(map(lambda x: x[-4:], glob.glob(f'./data/images/*', recursive=False)))

    for rec in record_nums:
        if rec in img_dirs:
            record = Record(rec)
            record.clearImages()
            record.saveImages()
            del record