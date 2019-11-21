import math

from Bitstream import Bitstream


class Golomb:
    def __init__(self, filename, m):
        self.bitstream = Bitstream(filename)
        self.m = m

    def encode(self, n):
        r = n % self.m
        q = n // self.m

        for i in range(q):  # unary side of the code
            self.bitstream.write_one_bit(1)

        self.bitstream.write_one_bit(0)

        self.bitstream.write_n_bits(r, self.m)  # binary side of the code

        return self.bitstream.bitstream

    def decode(self, bitstream):
        k = math.ceil(math.log2(self.m))
        t = math.pow(2, k) - self.m
        r = 0
        q = 0

        for i in range(len(bitstream.bitstream)):
            bit = bitstream.read_one_bit(i)
            if bit == '0':
                break
            q += 1

        temp = bitstream.read_n_bits(q + 1, k - 2)
        r = int("".join(str(x) for x in temp), 2)

        if r < t:
            return q * self.m + r

        else:
            r = r * 2 + int(bitstream.read_one_bit(k + 1))
            return q * self.m + r - t


def main():
    g = Golomb('test', 5)
    print(g.encode(15))
    print(g.decode(g.bitstream))


if __name__ == '__main__':
    main()
