#include <cstdio>
#include <cassert>

#include "convphase.h"

std::string readFile(char const* filename){
	FILE* file = fopen(filename, "r");
	assert(file);
	fseek(file, 0, SEEK_END);
	long len = ftell(file);
	rewind(file);

	char* str = new char[len+1];
	fread(str, 1, len, file);
	str[len] = 0;

	fclose(file);
	return str;
}

int main(int argc, char* argv[]){
	if(argc <= 1)
		fprintf(stderr, "Error: No input file given\n");
	char const* inputFile = argv[1];

	std::vector<char const*> options{};
	for(int i = 2; i < argc; ++i)
		options.push_back(argv[i]);

	//FastaConverter conv;
	//printf("%s", conv.parseMoIDFasta(readFile(inputFile)).getHapViewFasta().c_str());
	////FastaConverter conv2{readFile(inputFile)};
	////std::string fasta = conv2;
	////printf("%s", fasta.c_str());

	//return 0;



	//initHxcpp();
	//SeqPhaseStep1Result step1 = seqPhaseStep1(readFile(inputFile));
	//PhaseOutput phaseOut = phase(step1, options);
	////printf("%s\n\n\n", phaseOut.output.c_str());
	//std::string result = seqPhaseStep2(phaseOut.output, step1.constData);

	//FastaConverter result = convPhase(FastaConverter{readFile(inputFile)}, options);
	//printf("%s\n", result.toString().c_str());
	std::string result = convPhase(readFile(inputFile), options);
	printf("%s\n", result.c_str());

	return 0;
}
