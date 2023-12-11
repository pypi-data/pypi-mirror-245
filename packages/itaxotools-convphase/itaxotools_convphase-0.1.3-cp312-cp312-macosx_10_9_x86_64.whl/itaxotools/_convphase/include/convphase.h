#ifndef CONVPHASE_H
#define CONVPHASE_H

#ifdef _MSC_VER
#define CONVPHASE_API __declspec(dllexport)
#else
#define CONVPHASE_API
#endif

#include "phase.h"
#include "fastaconverter.h"

#include <vector>
#include <string>

void initHxcpp(); //Must be called once before calling seqPhaseStep1 or seqPhaseStep2

CONVPHASE_API SeqPhaseStep1Result seqPhaseStep1(std::string str1, std::string str2 = "", std::string str3 = "");
CONVPHASE_API PhaseOutput phase(PhaseInput input, std::vector<char const*> options = std::vector<char const*>{});
CONVPHASE_API std::string seqPhaseStep2(
	std::string phaseOut, std::string constFile = "",
	bool reduce = false, bool sort = false
);
CONVPHASE_API FastaConverter convPhase(
	FastaConverter input, std::vector<char const*> options = std::vector<char const*>{},
	bool reduce = false, bool sort = false
);

char** createArgArray(std::vector<char const*> args); //Allocations have to be freed with deleteArgArray
void deleteArgArray(char** argArr, int count);
#endif
