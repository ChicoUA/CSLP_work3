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

int Golomb::decode(){
	int k = ceil(log2(getM()));
	int t = pow(2, k) - getM();
	int r = 0;
	int q = 0;

	while(true){
		//cout << "here: " << bt.getBitstream() << endl;
		char bit = bt.readOneBit();
		if(bit == '0'){
			break;
		}
		q += 1;
	}
	/*
	cout << q << "\n";
	cout << k << "\n";
	*/

	std::string temp = bt.readNBits(0, k - 1);
	r = std::stoi(temp, nullptr, 2);

	/*
	cout << r << "\n";
	cout << t << "\n";
	*/

	if(r < t){
		return q * getM() + r;
	}
	else{
		r = r * 2 + (int)bt.readOneBit() - 48; // 48 vem de 0 no tabela ascii ser 48
		return q * getM() + r - t;
	}

}

Bitstream& Golomb::getBitstream(){
	return bt;
}

int Golomb::getM(){
	return m;
}


int main(){
	Golomb g(5);
	cout << g.encode(15).getBitstream() << "\n";
	cout << g.encode(4).getBitstream() << "\n";
	cout << g.encode(16).getBitstream() << "\n";
	cout << g.encode(12).getBitstream() << "\n";

	if(g.getBitstream().getBitstream().length() > 0){
		g.getBitstream().lastByteLength = g.getBitstream().getBitstream().length();
		g.getBitstream().writeToFile();
	}
	else
		g.getBitstream().lastByteLength = 8;

	g.getBitstream().readFile();
	cout << g.decode() << "\n";
	cout << "---------------------------------------" << endl;
	cout << g.decode() << "\n";
	cout << "---------------------------------------" << endl;
	cout << g.decode() << "\n";
	cout << "---------------------------------------" << endl;
	cout << g.decode() << "\n";
}




