/*
 * Bitstream.cpp
 *
 *  Created on: 21 Nov 2019
 *      Author: ghost
 */

#include "Bitstream.h"
#include <functional>
#include <cmath>
#include <bitset>
#include <string>
#include <fstream>
#include <iostream>

using namespace std;

ifstream file;

Bitstream::Bitstream() {
	bitstream = "";
	filename = "output.bin";
	bytes = new char[1];
	readerCounter = 0;
}

void Bitstream::writeOneBit(int bit){
	if(bitstream.length() == 8){
		writeToFile();
	}

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
		//cout << "hey" << "\n";
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
	for(int i = 0; i < binr.length(); i++){
		if(bitstream.length() == 8){
			writeToFile();
		}
		char c = binr.at(i);
		bitstream += c;
	}

}

char Bitstream::readOneBit(){
	if(bitstream.length() == 0){
		readFromFile();
	}
	char bit = bitstream.at(0);
	bitstream.erase(bitstream.begin());
	return bit;

}

std::string Bitstream::readNBits(int start, int k){
	if(bitstream.length() - 1 < k){
		readFromFile();
	}
	//cout << "error: " << bitstream << endl;
	std::string result = bitstream.substr(start, k);
	bitstream.erase(start, k);
	//cout << "new: " << bitstream << endl;
	return result;
}

void Bitstream::readFromFile(){
	//cout << "Getting byte" << endl;
	int value = (int)bytes[readerCounter];
	if(value < 0)
		value = value + 256;
	std::string binr = std::bitset<8>(value).to_string();
	readerCounter++;
	if(readerCounter == filesize){
		int diff = 8 - lastByteLength;
		cout << "diff: " << diff << endl;
		binr = binr.substr(diff, (int)binr.length());
	}
	bitstream += binr;
	cout << "state of bitstream: " << binr << endl;

}

void Bitstream::writeToFile(){
	fstream file (filename, ios::out | ios::binary | ios::app);
	std::bitset<8> b(bitstream);
	int c = (int)b.to_ulong();
	cout << "Hey!!!" << b.to_string() << "hey: " << c << endl;
	int x[1] = {c};
	cout << x[0] << endl;
	file.write((char *)&x, 1);
	bitstream = "";
	file.close();
}

void Bitstream::readFile(){
	fstream file (filename, ios::in | ios::binary | ios::ate);
	filesize = file.tellg();
	cout << "Size: " << filesize << endl;
	bytes = new char[filesize];
	file.seekg(0, ios::beg);
	file.read(bytes, filesize);
	file.close();
	remove("output.bin");
}
/*
int main(){
	Bitstream bt;
	bt.writeOneBit(1);
	cout << "1: " << bt.getBitstream() << "\n";
	bt.writeNBits(2, 4);
	cout << "2: " << bt.getBitstream() << "\n";
	bt.writeToFile();
	bt.readFile();
	cout << "3: " << bt.readOneBit() << "\n";
	cout << "4: " << bt.readNBits(0, 2) << "\n";

}
*/



