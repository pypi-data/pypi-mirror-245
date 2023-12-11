#include "fastaconverter.h"

#include <regex>

#define VALID_CHARS "ACGTUIRYKMSWBDHVN-"
#define contains(str, chars) (str.find(chars) != std::string::npos)

#ifdef REGEX_FASTA_CHECK
#define fastaCheck(...) fastaCheck1(__VA_ARGS__)
#else
#define fastaCheck(...) fastaCheck2(__VA_ARGS__)
#endif

FastaConverter::FastaConverter(std::string in, FastaConverterFormat f){
	if(in.find("\r\n") != std::string::npos){
		fprintf(stderr, "Warning: data is in CRLF format\n");
		std::regex re{"\r\n"};
		in = std::regex_replace(in, re, "\n");
	} else if(in.find("\r") != std::string::npos){
		fprintf(stderr, "Warning: data is in CR format\n");
		std::regex re{"\r"};
		in = std::regex_replace(in, re, "\n");
	}

	switch(f){
		case FCF_NONE:
			parse(in);
			break;
		case FCF_FASTA:
			parseFasta(in);
			break;
		case FCF_MOID_FASTA:
			parseMoIDFasta(in);
			break;
		case FCF_HAPVIEW_FASTA:
			parseHapViewFasta(in);
			break;
		case FCF_RAWFASTA:
			parseRawFasta(in);
			break;
		case FCF_TSV:
			parseTsv(in);
			break;
		case FCF_NEXUS:
			parseNexus(in);
			break;
		default:
			fprintf(stderr, "Error: Format not supported for parsing\n");
	}
}
FastaConverter::FastaConverter(std::vector<Sequence> v){
	add(v);
}

FastaConverter::operator std::string(){
	return toString();
}
FastaConverter::operator std::vector<Sequence>(){
	return getSequences();
}

inline bool fastaCheck1(std::string in, std::string sep = ""){
	std::string seqNameRe = ".*";
	if(sep.size())
		seqNameRe += sep + seqNameRe;

	std::string newLine = "\r\n";
	std::string seqIdRe{">" + seqNameRe};
	std::string oneLineSeqDataRe{"[" VALID_CHARS "]+"};
	std::string seqDataRe = oneLineSeqDataRe + "(\n" + oneLineSeqDataRe + ")*";
	std::string seqRe = seqIdRe + "\n" + seqDataRe + "\n*";
	std::string re = seqRe + "(\n" + seqRe + ")*";

	std::regex validRe{re};

	return std::regex_match(in, validRe);
}
inline bool fastaCheck2(std::string in, std::string sep = ""){
	char sepChar = 0;
	if(sep.size()){
		if(sep[0] == '\\' && sep.size() == 2)
			sepChar = sep[1];
		else
			sepChar = sep[0];
	}
	std::string ws{" \t\r\n"};
	std::string validChars{VALID_CHARS};
	for(size_t i = 0; i < in.size(); ++i){
		if(contains(ws, in[i]))
			continue;
		if(in[i] != '>')
			return false;
		++i;
		bool sepExist = false;
		if(!sepChar)
			sepExist = true;
		for(; i < in.size() && in[i] != '\n'; ++i)
			if(in[i] == sepChar)
				sepExist = true;
		if(!sepExist)
			return false;
		++i;
		for(; i < in.size() && in[i] != '>'; ++i){
			if(in[i] == '\n')
				continue;
			if(!contains(validChars, in[i]))
				return false;
		}
		--i;
	}
	return true;
}
inline bool tsvCheck(std::string in){
	std::string reValidStr{".*\t.*\t.*\t.*"};
	reValidStr += "(\n+" + reValidStr + ")*\n*";
	return std::regex_match(in, std::regex{reValidStr});
}
FastaConverter& FastaConverter::parse(std::string in){
	if(fastaCheck(in)){
		if(fastaCheck(in, "\\|")){
			return parseMoIDFasta(in);
		}
		if(fastaCheck(in, "\\.")){
			return parseHapViewFasta(in);
		}
		return parseFasta(in);
	}
	if(tsvCheck(in))
		return parseTsv(in);

	fprintf(stderr, "Error: Format not recognized for parsing\n");
	return *this;
}
inline std::string parseFastaSequence(std::string in){
	std::string seq;
	std::regex dataRe{"\n([>" VALID_CHARS "]+)*"};
	std::smatch dataMatch;
	while(std::regex_search(in, dataMatch, dataRe)){
		if(dataMatch[0].str()[1] == '>')
			break;
		seq += dataMatch[1];
		in = dataMatch.suffix();
	}
	return seq;
}
FastaConverter& FastaConverter::parseFasta(std::string in, std::string sep){
	std::string seqNameRe = "(.*)";
	if(sep.size())
		seqNameRe += sep + seqNameRe;
	else
		format = FCF_FASTA;

	if(!fastaCheck(in, sep))
		fprintf(stderr, "Warning: Data not in specified fasta format!\n");

	std::regex idRe{">" + seqNameRe};
	std::smatch idMatch;
	while(std::regex_search(in, idMatch, idRe)){
		Sequence seq;
		seq.seqid = idMatch[1].str();
		if(sep.size())
			seq.taxon = idMatch[2].str();
		in = idMatch.suffix();

		seq.data = parseFastaSequence(in);

		sequences.push_back(seq);
	}
	return *this;
}
FastaConverter& FastaConverter::parseMoIDFasta(std::string in){
	if(!format)
		format = FCF_MOID_FASTA;
	return parseFasta(in, "\\|");
}
FastaConverter& FastaConverter::parseHapViewFasta(std::string in){
	if(!format)
		format = FCF_HAPVIEW_FASTA;
	return parseFasta(in, "\\.");
}
FastaConverter& FastaConverter::parseRawFasta(std::string in){
	format = FCF_RAWFASTA;

    std::regex fastaRegex(">([^\n]+)\n([^>]+)");

    std::smatch matches;
    std::string::const_iterator searchStart(in.cbegin());

    while (std::regex_search(searchStart, in.cend(), matches, fastaRegex)) {
        std::string identifier = matches[1];
        std::string sequence = matches[2];
        sequence.erase(std::remove(sequence.begin(), sequence.end(), '\n'), sequence.end());

		Sequence seq;
		seq.seqid = identifier;
		seq.data = sequence;
		sequences.push_back(seq);

        searchStart = matches.suffix().first;
    }

	return *this;
}
FastaConverter& FastaConverter::parseTsv(std::string in){
	if(!tsvCheck(in)){
		fprintf(stderr, "Error: data not in tsv format with 4 values per line\n");
		return *this;
	}

	std::regex re{"(.*)\t(.*)\t(.*)\t(.*)"};
	std::smatch match;
	while(std::regex_search(in, match, re)){
		Sequence s;
		s.seqid    = match[1];
		s.taxon    = match[2];
		s.locality = match[3];
		s.data     = match[4];
		sequences.push_back(s);
		in = match.suffix();
	}

	return *this;
}
FastaConverter& FastaConverter::parseNexus(std::string in){
	if(!format)
		format = FCF_NEXUS;
	return *this;
	//TODO
}

FastaConverter& FastaConverter::add(std::vector<Sequence> v){
	for(Sequence const& e: v)
		sequences.push_back(e);
	return *this;
}

std::string FastaConverter::toString(){
	switch(format){
		case FCF_NONE:
		case FCF_FASTA:
			return getFasta();
		case FCF_MOID_FASTA:
			return getMoIDFasta();
		case FCF_HAPVIEW_FASTA:
			return getHapViewFasta();
		case FCF_NEXUS:
			return getNexus();
		default:
			fprintf(stderr, "Error: fasta format not supported for toString\n");
			return "";
	}
}
std::string FastaConverter::getFasta(std::string sep){
	std::string out;

	for(Sequence const& seq: sequences){
		out += ">";
		out += seq.seqid;
		if(sep.size()){
			out += seq.allele;
			out += sep;
			out += seq.taxon;
		} else{
			out += seq.taxon;
			out += seq.allele;
		}
		out += "\n";
		out += seq.data;
		out += "\n";
	}

	return out;
}
std::string FastaConverter::getMoIDFasta(){
	return getFasta("|");
}
std::string FastaConverter::getHapViewFasta(){
	return getFasta(".");
}
std::string FastaConverter::getTsv(){
	std::string out;
	for(Sequence const& s: sequences){
		out += s.seqid;
		out += "\t";
		out += s.allele;
		out += "\t";
		out += s.taxon;
		out += "\t";
		out += s.locality;
		out += "\t";
		out += s.data;
		out += "\n";
	}
	return out;
}
std::string FastaConverter::getNexus(){
	std::string out;
	return out;
	//TODO
}
std::vector<Sequence> FastaConverter::getSequences(){
	return sequences;
}

void FastaConverter::clear(){
	sequences.clear();
	format = FCF_NONE;
}
bool FastaConverter::allHaveTaxon(){
	for(Sequence const& s: sequences)
		if(!s.taxon.size())
			return false;
	return true;
}
