#include "convphase.h"

#include "SeqPhase1.h"
#include "SeqPhase1Result.h"
#include "SeqPhase2.h"
#include "Individuals.h"

#include <iostream>
#include <sstream>
#include <cassert>

void initHxcpp(){
	HX_TOP_OF_STACK
	hx::Boot();
	__boot_all();

	//hxcpp_set_top_of_stack();
	//hxRunLibrary();
}

SeqPhaseStep1Result seqPhaseStep1(std::string str1, std::string str2, std::string str3){
	SeqPhase1Result result = SeqPhase1_obj::doIt(
		String::create(str1.c_str(), str1.size()),
		str2.size() ? String::create(str2.c_str(), str2.size()) : null(),
		str3.size() ? String::create(str3.c_str(), str3.size()) : null()
	);
	assert(!result->hasErrors());

	SeqPhaseStep1Result data;
	if(result->hasErrors()){
		throw std::runtime_error("Error: SeqPhaseStep1 failed!");
	}
	if(result->hasInpFile())
		data.inpData = result->getInpFile().c_str();
	if(result->hasKnownFile())
		data.knownData = result->getKnownFile().c_str();
	if(result->hasConstFile())
		data.constData = result->getConstFile().c_str();
	//printf("inp:\n%s\n", data.inpData.c_str());
	//printf("known:\n%s\n", data.knownData.c_str());
	//printf("const:\n%s\n", data.constData.c_str());
	return data;
}
PhaseOutput phase(PhaseInput input, std::vector<char const*> options){
	options.insert(options.begin(), "");
	int argc = options.size();
	char** argv = createArgArray(options);

	PhaseData data{input};
	int ret = phase(data, argc, argv);
	assert(!ret);

	deleteArgArray(argv, options.size());
	return data.getOutput();
}
std::string seqPhaseStep2(std::string phaseOut, std::string constFile, bool reduce, bool sort){
	Individuals result = SeqPhase2_obj::parse(
		String::create(phaseOut.c_str(), phaseOut.size()),
		String::create(constFile.c_str(), constFile.size())
	);
	String fileContent = result->getFasta(reduce, sort);
	return std::string(fileContent.c_str());
}
FastaConverter convPhase(FastaConverter input, std::vector<char const*> options, bool reduce, bool sort){
	initHxcpp();

	SeqPhaseStep1Result step1 = seqPhaseStep1(
			(input.allHaveTaxon()) ? input.getMoIDFasta() : input.getFasta()
	);
	//printf("%s\n", step1.inpData.c_str());

	PhaseOutput phaseResult = phase(PhaseInput{step1.inpData}, options);
	//printf("%s\n", phaseResult.output.c_str());
	//printf("%s\n", phaseResult.pairs.c_str());
	//printf("freqs: \n%s\n\n\n", phaseResult.freqs.c_str());
	//printf("monitor: \n%s\n\n\n", phaseResult.monitor.c_str());
	//printf("hbg: \n%s\n\n\n", phaseResult.hbg.c_str());
	//printf("probs: \n%s\n\n\n", phaseResult.probs.c_str());

	//printf("recom: \n%s\n\n\n", phaseResult.recom.c_str());
	//printf("sample: \n%s\n\n\n", phaseResult.sample.c_str());
	//printf("pairs: \n%s\n\n\n", phaseResult.pairs.c_str());
	//printf("signif: \n%s\n\n\n", phaseResult.signif.c_str());
	//printf("hot: \n%s\n\n\n", phaseResult.hot.c_str());

	//printf("cout: \n%s\n\n\n", phaseResult.cout.c_str());
	//printf("cerr: \n%s\n\n\n", phaseResult.cerr.c_str());

	std::string phasedFasta = seqPhaseStep2(phaseResult.output, step1.constData, reduce, sort);
	FastaConverter step2(phasedFasta, FCF_RAWFASTA);
	for(Sequence& s: step2.sequences){
		if(s.taxon.size()){
			s.allele = s.taxon.back();
			s.taxon.pop_back();
		} else{
			s.allele = s.seqid.back();
			s.seqid.pop_back();
		}
	}
	//printf("%s\n", step2.c_str());

	return step2;
}

char** createArgArray(std::vector<char const*> args){
	char** argArr = new char*[args.size()];
	for(int i = 0; i < args.size(); ++i){
		argArr[i] = new char[strlen(args[i])+1];
		strcpy(argArr[i], args[i]);
	}
	return argArr;
}
void deleteArgArray(char** argArr, int count){
	for(int i = 0; i < count; ++i)
		delete[] argArr[i];
	delete[] argArr;
}
