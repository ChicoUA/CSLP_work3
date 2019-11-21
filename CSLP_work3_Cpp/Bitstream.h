/*
 * Bitstream.h
 *
 *  Created on: 21 Nov 2019
 *      Author: ghost
 */
#include <string>

#ifndef BITSTREAM_H_
#define BITSTREAM_H_

class Bitstream {

private:
	std::string bitstream;


public:
	Bitstream();

	void writeOneBit(int bit);
	char readOneBit(int bit);

	void writeNBits(int r, int m);
	std::string readNBits(int start, int k);

	std::string getBitstream();

};

#endif /* BITSTREAM_H_ */
