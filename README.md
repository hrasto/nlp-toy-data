# NLP toy data generator

This repository contains a utility for generating toy data suitable for development of NLP models.
The idea is to create sequences that satisfy the following properties: 
- vocabulary size is very small and limited (no unknown words to be encountered at test time)
- there is an infinite supply of possible sensible combinations (even with a small vocabulary)
- sequences posses some trivial syntactic rules that the model can learn
- sequences of one language can be translated to other language via a set of not too ambiguous rules
