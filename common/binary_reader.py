# -----------------------------------
# import
# -----------------------------------
import os
import struct

# -----------------------------------
# define
# -----------------------------------
BIG_LITTLE = {'little':'<', 'big':'>'}


# -----------------------------------
# function
# -----------------------------------


class BinaryReader:

    def __init__(self, file_path):
        self.file_path = file_path
        self.f = open(file_path, 'rb')
        self.file_size = os.path.getsize(file_path)

        self.start_fp = self.f.tell()

    def num_bytes_left(self):
        return self.file_size - (self.f.tell() - self.start_fp)

    def seek_to_end(self):
        self.f.seek(self.file_size, 0)

    def seek(self, offset, whence=0):
        self.f.seek(offset, whence)

    def tell(self):
        return self.f.tell()

    def read_raw(self, size):
        return self.f.read(size)

    def read_8bits(self, byteorder='big', signed=False, decode=False):
        if decode:
            return self.f.read(1).decode()
        else:
            if signed:
                format_char = 'b'
            else:
                format_char = 'B'
            return struct.unpack(BIG_LITTLE[byteorder] + format_char, self.f.read(1))[0]

    def read_16bits(self, byteorder='big', signed=False, decode=False):
        if decode:
            return self.f.read(2).decode()
        else:
            if signed:
                format_char = 'h'
            else:
                format_char = 'H'
            return struct.unpack(BIG_LITTLE[byteorder] + format_char, self.f.read(2))[0]

    def read_32bits(self, byteorder='big', signed=False, decode=False):
        if decode:
            return self.f.read(4).decode()
        else:
            if signed:
                format_char = 'l'
            else:
                format_char = 'L'
            return struct.unpack(BIG_LITTLE[byteorder] + format_char, self.f.read(4))[0]

    def read_64bits(self, byteorder='big', signed=False, decode=False):
        if decode:
            return self.f.read(8).decode()
        else:
            if signed:
                format_char = 'q'
            else:
                format_char = 'Q'
            return struct.unpack(BIG_LITTLE[byteorder] + format_char, self.f.read(8))[0]

    def read_nbits(self, size_bits, byteorder='big', signed=False, decode=False):
        if size_bits == 64:
            data = self.read_64bits(byteorder, decode)
        elif size_bits == 32:
            data = self.read_32bits(byteorder, decode)
        elif size_bits == 16:
            data = self.read_16bits(byteorder, decode)
        elif size_bits == 8:
            data = self.read_8bits(byteorder, decode)
        else:
            raise ValueError()

        return data

    def read_null_terminated(self):
        null = b'\x00'
        s = ''
        while True:
            c = self.read_8bits('big', decode=True)
            s += c
            if c.encode() == null:
                break
        return s

    def close(self):
        if self.f:
            self.f.close()
            self.f = None

# -----------------------------------
# main
# -----------------------------------
if __name__ == '__main__':
    pass
