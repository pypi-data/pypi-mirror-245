#ifndef SEQGRAPH_HPP
#define SEQGRAPH_HPP

#include "seqvertex.hpp"
#include "seqedge.hpp"

#include "HapNet.h"

#include <vector>
#include <string>

enum PopartNetworkAlgo{
	MINIMUM_SPANNING_TREE = 0,
	MED_JOIN_NET = 1,
	TIGHT_SPAN_WALKER = 2,
	TCS_NETWORK = 3,
#ifndef DISABLE_INTNJ
	INTEGER_NJ_NET = 4,
#endif

	POPART_NETWORK_ALGO_COUNT
};

class SeqGraph{
public:
	SeqGraph(std::vector<Sequence*> const& s, PopartNetworkAlgo a, bool moID = false);

	void setColoringFromMoID();
	void calc();
	void print() const;

	HapNet* g;
	PopartNetworkAlgo algo;
	void* p0;
	void* p1;
	std::vector<Sequence*>           seqs;
	std::map<Sequence*, std::string> coloring;
	std::vector<SeqVertex>           vertices;
	std::vector<SeqEdge>             edges;
};

#endif
