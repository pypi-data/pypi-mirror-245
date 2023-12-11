#ifndef FASTACONVERTER_H
#define FASTACONVERTER_H

#include <string>
#include <vector>

struct Sequence{
	std::string seqid;
	std::string taxon;
	std::string allele;
	std::string locality;
	std::string data;
};

enum FastaConverterFormat{
	FCF_NONE = 0,
	FCF_FASTA,
	FCF_MOID_FASTA,
	FCF_HAPVIEW_FASTA,
	FCF_RAWFASTA,
	FCF_TSV,
	FCF_NEXUS,
	FCF_NUM
};

class FastaConverter{
public:
	FastaConverter() = default;
	FastaConverter(std::string in, FastaConverterFormat f = FCF_NONE);
	FastaConverter(std::vector<Sequence> v);

	operator std::string();
	operator std::vector<Sequence>();

	FastaConverter& parse(std::string in); // tries to guess format
	FastaConverter& parseFasta(std::string in, std::string sep = ""); // separator has to be escaped if needed
	                                                                  // for regular expression
	FastaConverter& parseMoIDFasta(std::string in);
	FastaConverter& parseHapViewFasta(std::string in);
	FastaConverter& parseRawFasta(std::string in);
	FastaConverter& parseTsv(std::string in);
	FastaConverter& parseNexus(std::string in);

	FastaConverter& add(std::vector<Sequence> v);

	std::string toString();
	std::string getFasta(std::string sep = "");
	std::string getMoIDFasta();
	std::string getHapViewFasta();
	std::string getTsv();
	std::string getNexus();

	std::vector<Sequence> getSequences();

	void clear();
	bool allHaveTaxon();

	std::vector<Sequence> sequences;
	FastaConverterFormat format = FCF_NONE;
};

#endif
