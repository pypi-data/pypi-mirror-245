This is a partial implementation of the SPARQL grammar in Python using Pydantic models to represent the grammar.

It should be split

Suggested testing strategy:
1. Generate simple SPARQL queries using the grammar
2. Parse the output queries using RDFLib's SPARQL query parser
3. Ensure the output queries from RDFLib are equivalent to the input queries
This would unfortunately need to consider query formatting.

Alternatively SPARQL grammar 