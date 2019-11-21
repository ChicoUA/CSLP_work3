import math


class Bitstream:
    def __init__(self, filename):
        self.bitstream = []
        self.filename = filename

    def read_one_bit(self, position):  # or is it to get a bit from the bitstream????
        '''
                assert 0 <= bit < 8
                file = open(self.filename, "rb")
                file.seek(byte, 1)
                b = bin(ord(file.read(1)))
                b = list(b[2:])

                while len(b) < 8:
                    b = ['0'] + b

                file.close()
                return b[bit]
        '''
        assert position < len(self.bitstream)
        return self.bitstream[position]

    def write_one_bit(self, bit):
        assert bit == 1 or bit == 0
        self.bitstream.append(str(bit))
        return bit

    def read_n_bits(self, start, k):
        return self.bitstream[start:start+k+1]

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
                    bits = [0] + bits

            else:
                r = r + level
                bits = bin(r)
                bits = list(bits[2:])

                while len(bits) < b:
                    bits = [0] + bits

        else:
            bits = bin(r)
            bits = list(bits[2:])

        self.bitstream += bits
        return bits


def main():
    bs = Bitstream("test")

    print(bs.write_n_bits(15, 18))
    print(bs.read_one_bit(0))
    print(bs.read_n_bits(1, 2))


if __name__ == "__main__":
    main()
