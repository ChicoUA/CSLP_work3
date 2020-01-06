/*
 * Golomb.h
 *
 *  Created on: 21 Nov 2019
 *      Author: ghost
 */
#include "Bitstream.h";

#ifndef GOLOMB_H_
#define GOLOMB_H_

class Golomb {

public:
	Bitstream bt;
	int m;
	Golomb(int m1);
	Bitstream encode(int n);
	int decode();
	Bitstream& getBitstream();
	int getM();
};

#endif /* GOLOMB_H_ */
