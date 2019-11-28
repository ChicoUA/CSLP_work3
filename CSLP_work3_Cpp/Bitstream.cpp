/*
 * Bitstream.cpp
 *
 *  Created on: 21 Nov 2019
 *      Author: ghost
 */

#include "Bitstream.h"
#include <functional>
#include <iostream>
#include <cmath>
#include <bitset>
#include <string>

using namespace std;

Bitstream::Bitstream() {
	bitstream = "";
}

void Bitstream::writeOneBit(int bit){

	bitstream += std::to_string(bit);

}

std::string Bitstream::getBitstream(){
	return bitstream;
}

void Bitstream::writeNBits(int r, int m){
	double b = log2(m);
	std::string binr = "";
	if(ceil(b) != floor(b)){
		int b2 = int(ceil(b));
			int level = int(pow(2, b2) - m);

			if(r < level){
				binr = std::bitset<8>(r).to_string();

				while(binr.length() > b2 - 1){
					binr.erase(binr.begin());
				}
			}

			else{
				r += level;
				binr = std::bitset<8>(r).to_string();

				while(binr.length() > b2){
					binr.erase(binr.begin());
				}
			}
	}
	else{
		cout << "hey" << "\n";
		binr = std::bitset<8>(r).to_string();
		while(true){
			if(binr.length() == 1){
				break;
			}
			if(binr.at(0) == '1'){
				break;
			}
			binr.erase(binr.begin());
		}
	}

	bitstream += binr;

}

char Bitstream::readOneBit(int bit){
	try{
		return bitstream.at(bit);
	}
	catch(const std::exception& e){
		cout << "Read one bit failed" << "\n";
		exit(1);
	}
}

std::string Bitstream::readNBits(int start, int k){
	try{
		return bitstream.substr(start, k);
	}
	catch(const std::exception& e){
		cout << "Read N bits failed" << "\n";
		exit(1);
	}
}
/*
int main(){
	Bitstream bt;
	bt.writeOneBit(1);
	cout << bt.getBitstream() << "\n";
	cout << "hey" << "\n";
	bt.writeNBits(2, 4);
	cout << bt.getBitstream() << "\n";
	cout << bt.readOneBit(0) << "\n";
	cout << bt.readNBits(0, 2) << "\n";

}
*/


