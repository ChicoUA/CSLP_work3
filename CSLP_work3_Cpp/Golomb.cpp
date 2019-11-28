/*
 * Golomb.cpp
 *
 *  Created on: 21 Nov 2019
 *      Author: ghost
 */

#include "Golomb.h"
#include <functional>
#include <iostream>
#include <cmath>
#include <bitset>
#include <string>

using namespace std;

Golomb::Golomb(int m1) {
	Bitstream bt;
	m = m1;
}

Bitstream Golomb::encode(int n){
	int r = n % getM();
	int q = n / getM();

	for(int i = 0; i < q; i++){
		bt.writeOneBit(1);
	}


	bt.writeOneBit(0);
	bt.writeNBits(r, getM());


	return bt;
}

int Golomb::decode(Bitstream bt){
	int k = ceil(log2(getM()));
	int t = pow(2, k) - getM();
	int r = 0;
	int q = 0;

	for(int i = 0; i < bt.getBitstream().length(); i++){
		char bit = bt.readOneBit(i);
		if(bit == '0'){
			break;
		}
		q += 1;
	}

	std::string temp = bt.readNBits(q + 1, k - 1);
	r = std::stoi(temp, nullptr, 2);
	/*
	cout << r << "\n";
	cout << q << "\n";
	cout << k << "\n";
	cout << t << "\n";
	*/

	if(r < t){
		return q * getM() + r;
	}
	else{
		r = r * 2 + (int)bt.readOneBit(bt.getBitstream().length() - 1) - 48; // 48 vem de 0 no tabela ascii ser 48
		return q * getM() + r - t;
	}

}

Bitstream Golomb::getBitstream(){
	return bt;
}

int Golomb::getM(){
	return m;
}


int main(){
	Golomb g(128);
	cout << g.encode(255).getBitstream() << "\n";
	cout << g.decode(g.getBitstream()) << "\n";
}


