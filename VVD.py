import sys
from pprint import pprint
try:
    from .ByteIO import ByteIO
    from .VVD_DATA import SourceVvdFileData
except:
    from ByteIO import ByteIO
    from VVD_DATA import SourceVvdFileData


class SourceVvdFile49:
    def __init__(self, path = None,file = None):
        if path:
            self.reader = ByteIO(path = path + ".vvd")
        elif file:
            self.reader = file
        self.vvd = SourceVvdFileData()
        self.vvd.read(self.reader)
    def test(self):
        print(len(self.vvd.theVertexes))

if __name__ == '__main__':
    with open('log.log', "w") as f:  # replace filepath & filename
        with f as sys.stdout:
            model = r'.\test_data\xenomorph'
            # MDL_edit('E:\\MDL_reader\\sexy_bonniev2')
            SourceVvdFile49(model).test()