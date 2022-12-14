import models
import couchdb
from sys import exit

class CouchDB_CSV_Import():
    
    def __init__(self, host, dataBase, dataType, dataFile):
        self.host = host
        self.dataFile = dataFile
        
        if dataType.lower() == 'veteran':
            self.data_class = models.Veteran
        elif dataType.lower() == 'guardian':
            self.data_class = models.Guardian
        elif dataType.lower() == 'volunteer':
            self.data_class = models.Volunteer
        elif dataType.lower() == 'flight':
            self.data_class = models.Flight
        elif dataType.lower() == 'location':
            self.data_class = models.Location
        elif dataType.lower() == 'crew':
            self.data_class = models.Crew
        elif dataType.lower() == 'veteran2':
            self.data_class = models.Veteran2
        elif dataType.lower() == 'guardian2':
            self.data_class = models.Guardian2
        else:
            print("Data type not supported.")
            exit(1)

        couch = couchdb.Server(host)
        self.db = couch[dataBase]

    def upload_Data(self):
        from csv import DictReader
        rowCount = 0
        for row in DictReader(file(self.dataFile)):
            data_point = self.data_class()
            if hasattr(data_point, 'metadata'):
                data_point.metadata['created_by'] = 'couch_db_csv_import v01.00'
            data_point.adapt_csv(row)
            data_enc = data_point.__dict__
            print(data_enc)
            rowCount += 1
            self.db.save(data_enc)
        print(rowCount)

def main():
    from sys import argv, exit
    if len(argv) != 5:
        print("Usage: %s host database doctype dataFile" % argv[0])
        print("Example: %s http://localhost:5984 hf veteran VeteranWaitlist.csv" % argv[0])
        exit(1)
    importer = CouchDB_CSV_Import(argv[1], argv[2], argv[3], argv[4])
    importer.upload_Data()

if __name__ == "__main__": main()

