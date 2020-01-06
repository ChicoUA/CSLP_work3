/*
 * Bitstream.h
 *
 *  Created on: 21 Nov 2019
 *      Author: ghost
 */
#include <string>
#include <fstream>
#include <fstream>
#include <iostream>

#ifndef BITSTREAM_H_
#define BITSTREAM_H_

class Bitstream {

public:
	std::string bitstream;
	std::string filename;
	char * bytes;
	int readerCounter;
	int lastByteLength = 0;
	int filesize = 0;
	int bytesRead = 0;
	Bitstream();

	void writeOneBit(int bit);
	char readOneBit();

	void writeNBits(int r, int m);
	std::string readNBits(int start, int k);

	std::string getBitstream();

	void writeToFile();
	void readFromFile();
	void readFile();

};

#endif /* BITSTREAM_H_ */
