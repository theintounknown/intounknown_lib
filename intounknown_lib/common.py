import csv

def readFile(filename, binary=False):
    ''' read a file from disk '''
    content = ''
    if not binary:
        with open(filename, 'r') as f:
            content = f.read()
    else:
        with open(filename, 'r+b') as f:
            content = f.read()

    return content


def writeFile(filename, content, binary=False):
    ''' write file to disk '''
    if not binary:
        with open(filename, 'w') as f:
            f.write(content)
    else:
        with open(filename, 'w+b') as f:
            f.write(content)


def readCsv(path, newline='', delimiter=',', quotechar='"', as_dict=False):
    headers = None
    ''' read a CSV file '''
    with open(path, newline=newline) as csvfile:
        result = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
        for row in result:
            if as_dict and headers == None:
                headers = row
                continue

            if as_dict:
                obj = dict(zip(headers, row))
                yield obj
            else:
                yield row


class WriteCustomCsv:
    ''' Customer CSV writer '''
    def __init__(self, path):
        self.path = path
        self.newline = ''
        self.delimiter = ','
        self.quotechar = '"'

        self.writer = None
        self.file_handle = None

        self.headers = []

    def write(self, obj=None):
        ''' row is is dict '''
        if not self.writer:
            self.file_handle = open(self.path, 'w', newline=self.newline)
            self.writer = csv.writer(self.file_handle, delimiter=self.delimiter,
                quotechar=self.quotechar, quoting=csv.QUOTE_ALL)

            self.headers = list(obj.keys())         # get headers
            self.writer.writerow(self.headers)      # write header to first line

        row = [obj[a] for a in self.headers]        # order rows by header order
        self.writer.writerow(row)       # write record to file

    def close(self):
        if self.file_handle:
            self.file_handle.close()



if __name__ == '__main__':
    dir_path = '\\temp\\'

    if False:
        #filename = 'test.txt'
        filename = 'screenshot.png'
        file_path = dir_path + filename

        #writeFile(file_path, 'hello world!\nsomething else, that is here')
        output = readFile(file_path, binary=True)

        new_file_path = dir_path + 'output.png'
        writeFile(new_file_path, output, binary=True)
        print(output)


    records = [
        {'id': 1, 'name': 'Orange', 'category': 'A'},
        {'id': 2, 'name': 'Blue', 'category': 'A'},
        {'id': 3, 'name': 'Red', 'category': 'B'},
        {'id': 4, 'name': 'Purple', 'category': 'C'},
    ]

    file_path = dir_path + 'test.csv'
    if False:
        writer = WriteCustomCsv(file_path)
        for row in records:
            writer.write(row)
        writer.close()

    #for row in readCsv(file_path):
    for row in readCsv(file_path, as_dict=True):
        print(row)

