import math
import os
import time

from Bitstream import Bitstream


class Golomb:
    def __init__(self, filename, m):
        self.bitstream = Bitstream(filename)
        self.m = m

    def encode(self, n, last=False):
        r = n % self.m
        q = n // self.m

        for i in range(q):  # unary side of the code
            self.bitstream.write_one_bit(1)

        self.bitstream.write_one_bit(0)

        self.bitstream.write_n_bits(r, self.m)  # binary side of the code

        if self.bitstream.bitstream and last:
            self.bitstream.padding_last_byte = 8 - len(self.bitstream.bitstream)
            self.bitstream.write_to_file()

        return self.bitstream.bitstream

    def decode(self):
        k = math.ceil(math.log2(self.m))
        t = math.pow(2, k) - self.m
        r = 0
        q = 0
        i = 0

        while True:
            #print("Hey: ", self.bitstream.bitstream)
            bit = self.bitstream.read_one_bit()
            if bit == '0':
                break
            q += 1
            i += 1

        #print("Q: ", q, self.bitstream.bitstream, k)
        temp = self.bitstream.read_n_bits(0, k - 1)
        r = int("".join(str(x) for x in temp), 2)
        #print("R: ", r, "T: ", t, self.bitstream.bitstream)

        if r < t:
            result = q * self.m + r
            #print("Resultado: ", result, self.bitstream.bitstream)
            return result

        else:
            r = r * 2 + int(self.bitstream.read_one_bit())
            result = q * self.m + r - t
            #print("Resultado: ", result, self.bitstream.bitstream)
            return result



def main():
    g = Golomb('outputfile.txt', 78)
    g.bitstream.open_file_write()
    g.encode(261)
    g.encode(250)
    g.encode(257)
    g.encode(253)
    g.encode(256)
    g.encode(1)
    g.encode(25)
    g.encode(258)
    if g.bitstream.bitstream:
        g.bitstream.padding_last_byte = 8 - len(g.bitstream.bitstream)
        g.bitstream.write_to_file()

    g.bitstream.close_file()

    g.bitstream.open_file_read()
    print(g.decode())
    print(g.decode())
    print(g.decode())
    print(g.decode())
    print(g.decode())
    print(g.decode())
    print(g.decode())
    print(g.decode())
    g.bitstream.close_file()


if __name__ == '__main__':
    main()
