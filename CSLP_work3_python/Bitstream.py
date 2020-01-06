import math
import os


class Bitstream:
    def __init__(self, filename):
        self.bitstream = []
        self.filename = filename
        self.file = None
        self.padding_last_byte = 0
        self.file_size = 0
        self.bytes_read = 0

    def read_one_bit(self):  # or is it to get a bit from the bitstream????
        if not self.bitstream:
            self.read_from_file(True)
        return self.bitstream.pop(0)

    def write_one_bit(self, bit):
        assert bit == 1 or bit == 0
        if len(self.bitstream) == 8:
            self.write_to_file()
        self.bitstream.append(str(bit))

        return bit

    def read_n_bits(self, start, k):
        # print("hiiiiiiii: ", self.bitstream)
        while True:
            if len(self.bitstream) - 1 >= k:
                temp = self.bitstream[start:start + k]
                del self.bitstream[start:start + k]
                return temp
            else:
                self.read_from_file(True)

    def write_n_bits(self, r, m):
        assert r < m
        bits = []
        b = math.log2(m)
        if not b.is_integer():
            b = int(math.ceil(math.log2(m)))
            level = int(math.pow(2, b) - m)

            if r < level:
                bits = bin(r)
                bits = list(bits[2:])

                while len(bits) < b - 1:
                    bits = ['0'] + bits

            else:
                r = r + level
                bits = bin(r)
                bits = list(bits[2:])

                while len(bits) < b:
                    bits = ['0'] + bits

        else:
            b = int(math.ceil(math.log2(m)))
            level = int(math.pow(2, b) - m)

            if r < level:
                bits = bin(r)
                bits = list(bits[2:])

                while len(bits) < b - 1:
                    bits = ['0'] + bits

            else:
                r = r + level
                bits = bin(r)
                bits = list(bits[2:])

                while len(bits) < b:
                    bits = ['0'] + bits

        for x in bits:
            if len(self.bitstream) == 8:
                self.write_to_file()
            self.bitstream.append(x)

        return bits

    def write_to_file(self):
        #print("Writing to file... ", self.bitstream)
        self.file_size += 1
        value = int("".join(str(x) for x in self.bitstream), 2)
        self.bitstream.clear()
        self.file.write(bytes([value]))
        # print("Done")

    def read_from_file(self, special):
        self.bytes_read += 1
        by = self.file.read(1)
        value = int.from_bytes(by, byteorder="little")
        bits = [int(digit) for digit in bin(value)[2:]]
        result = [str(b) for b in bits]
        # print("Reading from file... ", result, self.bytes_read, self.file_size, self.bitstream)

        while len(result) < 8:
            result = ['0'] + result

        if self.bytes_read == self.file_size:
            for i in range(self.padding_last_byte):
                result.pop(0)

        self.bitstream += result
        # print("State of bitstream: ", self.bitstream)

    def open_file_write(self):
        self.file = open(self.filename, "wb")

    def open_file_read(self):
        self.file = open(self.filename, "rb")

    def close_file(self):
        self.file.close()


def main():
    bs = Bitstream("outputfile.txt")

    print(bs.write_n_bits(15, 18))
    print(bs.read_one_bit())
    print(bs.read_n_bits(1, 2))
    bs.open_file_write()
    bs.write_to_file()
    bs.close_file()
    bs.open_file_read()
    bs.read_from_file(True)
    bs.close_file()
    print(bs.bitstream)


if __name__ == "__main__":
    main()
