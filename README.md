# CurateGPT

:iphone: For more usage details and additional information about the original work, please refer to: https://github.com/monarch-initiative/curategpt

CurateGPT is a prototype web application and framework for performing general purpose AI-guided curation
and curation-related operations over *collections* of objects.

## Building indexes

This action requires an OpenAI API key to build an index for the vector database.

To build an index for the BAO ontology or the ELSST thesaurus, you can run the following command:


```
curategpt index -c [collection_name] [location_of_file]
```

For example, for the BAO ontology the command will be:

```
curategpt index -c bao .\data\structured\BAO_train_set.json
```

And to build the index for the 'Background Knowledge' you can use the content inside the RAG folder that contains the additional documents.
For example, for the ontology's additional data you can use the command below:

```
curategpt index -c bao_background .\data\ForRAG\BAO\* 
```

## Generate relationships

To generate relationships for either the ontology or the thesaurus, you have to specify and primary collection that is going to be used as well as the model.

The command follow this format:

```
curategpt complete -c [collection_name] -m [model_name]
```

where models can be either: 'gpt-3.5-turbo' or 'gpt-3.5-turbo-instruct'. 


For example, for using the ontology's created index and the gpt-3.5-turbo model, you can use the command below:

```
curategpt complete -c bao -m gpt-3.5-turbo
```

To utilize the additional 'Background Knowledge' collections, either with or without the 'Custom Approach', you can use the following command format:

```
curategpt complete -c [collection_name] --secondary [seconday_collection_name] -m [model_name] --custom_approach [True/False]
```

For example, for using the ontology's created index and the additional 'Background Knowledge' with the 'Custom Approach', along with and the gpt-3.5-turbo model, you can use the command below:

```
curategpt complete -c bao --secondary bao_background -m gpt-3.5-turbo --custom_approach True
```


## Additional resources used as 'Background Knowledge'

### Books/Academic Papers for the ELSST background knowledge

1. Morgan, Rod, Mike Maguire, and Robert Reiner, eds. The Oxford handbook of criminology.
Oxford University Press (UK), 2012.
2. Berger, Ronald J., Marvin D. Free, and Patricia Searles. Crime, justice, and society: An introduction
to criminology. New York: Lynne Rienner Publishers, 2005.
3. Burke, Roger Hopkins. An introduction to criminological theory. Routledge, 2018.
4. Siegel, Jacob S., and David A. Swanson. ”The methods and materials of demography.” (No Title).
5. Amaral, Ernesto FL. ”An introduction to demography.” Population (2019).
6. Poston Jr, Dudley L., and Leon F. Bouvier. Population and society: An introduction to demography.
Cambridge University Press, 2010.
7. Neyer, Gerda, Gunnar Andersson, and Hill Kulu. The Demography of Europe: Introduction.
Springer Netherlands, 2013.
8. Van Sickle, John Valentine, and Benjamin A. Rogge. ”Introduction to economics.” (No Title) (1954).
9. Flynn, Sean Masaki. Economics for dummies. John Wiley & Sons, 2018.
10. Sloman, John, and Alison Wride. Economics. Pearson Education, 2009.
11. Bourchtein, Vitali. The Principles of Economics Textbook: An Analysis of Its Past, Present &
Future. Diss. Stern School of Business New York, 2011.
12. Arslan, Hasan, ed. An introduction to education. Cambridge Scholars Publishing, 2018.
13. Organisation for Economic Co-operation and Development (OECD). ”The future of education
and skills: Education 2030.” OECD education working papers (2018).
14. Amatullah, Tasneem, et al. ”Foundations of Education (Fall 2021).” (2021).
15. Langenbach, Michael, Courtney Vaughn, and Lola Aagaard. ”An introduction to educational
research.” (No Title) (1994).
16. Ward, Stephen, ed. A Student’s Guide to Education Studies: A Student’s Guide. Routledge, 2013.
17. Schumpeter, Joseph A. ”The General Theory of Employment, Interest and Money.” (1936): 791-795.
18. Robinson, Joan. ”Introduction to the Theory of Employment.” (No Title) (1969).
19. Lee, Kelley, and Kelley Lee. ”An Introduction to Global Health.” Globalization and Health: An
Introduction (2003): 1-29.
20. Falcone, Kelly. ”Introduction to HEALTH.” (2020).
21. Yazachew, Meseret, and Yihenew Alem. ”Introduction to health education.” (2004).
22. Sarkar, Sukanta. ”The role of information and communication technology (ICT) in higher educa-
tion for the 21st century.” Science 1.1 (2012): 30-41.
23. Schauer, Frederick F. Thinking like a lawyer: a new introduction to legal reasoning. Harvard
University Press, 2009.
24. Harris, Phil. An introduction to law. Cambridge University Press, 2015.
25. Berger, Suzanne. ”Globalization and politics.” Annual Review of Political Science 3.1 (2000): 43-62.
26. Weber, Max. From Max Weber: essays in sociology. Routledge, 2013.
27. Lukes, Steven. Power: A radical view. Bloomsbury Publishing, 2021.
28. Tansey, Stephen D., and Nigel Jackson. Politics: the basics. Routledge, 2014.
29. Munroe, Trevor. An introduction to politics. Canoe Press, 2002.
30. Doda, Zerihun. ”ntroduction to Sociology.” (2005).
31. Merton, Robert K. ”Social structure and anomie.” Gangs. Routledge, 2017. 3-13.
32. Stolley, Kathy S. The basics of sociology. Greenwood Press„ 2005.
33. Conerly, Tonja R. Introduction to sociology 3e. OpenStax, 2021.

### Ontologies/Vocabularies for the ELSST background knowledge

1. Humanities and Social Science Electronic Thesaurus (HASSET) thesaurus, https://vocabularies.uk-
dataservice.ac.uk/hasset/en/
2. Hoekstra, Rinke, et al. ”The LKIF Core Ontology of Basic Legal Concepts.” LOAIT 321 (2007):
43-63.
3. UNESCO Thesaurus, https://vocabularies.unesco.org/browser/thesaurus/en/
4. UNBIS Thesaurus, https://metadata.un.org/thesaurus/?lang=en

### Books/Academic Papers for the BAO background knowledge

1. Florence, Alexander T., and David Attwood. Physicochemical principles of pharmacy: In manu-
facture, formulation and clinical use. Pharmaceutical press, 2015.
2. Allison, Lizabeth A. Fundamental molecular biology. John Wiley & Sons, 2021.
3. Bolsover, Stephen R., et al. Cell biology: a short course. Vol. 1. John Wiley & Sons, 2011.
4. Phillips, Rob, et al. Physical biology of the cell. Garland Science, 2012.
5. May, Paul W., and Simon A. Cotton. Molecules that amaze us. Vol. 193. Boca Raton. FL: CRC
Press, 2015.
6. Weaver, Robert. EBOOK: Molecular Biology. McGraw Hill, 2011.
7. Shah, Biren N. Textbook of pharmacognosy and phytochemistry. Elsevier India, 2009.
8. Nelson, David L., Albert L. Lehninger, and Michael M. Cox. Lehninger principles of biochemistry.
Macmillan, 2008.
9. Doran, Pauline M. Bioprocess engineering principles. Elsevier, 1995.
10. Michael, L. Shuler, and Fikret Kargi. ”Bioprocess engineering: basic concepts.” (2002).
11. Bittker, Joshua A., and Nathan T. Ross, eds. High throughput screening methods: Evolution and
refinement. Royal Society of Chemistry, 2016.
12. Böhmer, Daniel, Vanda Repiská, and L. Danišovic. ”Introduction to medical and molecular biology.”
Asklepios: Bratislava (2010).
13. Wilson, Keith, et al., eds. Wilson and Walker’s principles and techniques of biochemistry and
molecular biology. Cambridge university press, 2018.
14. Lodish, Harvey F. Molecular cell biology. Macmillan, 2008.
15. Berg, Jeremy M., and L. John. ”Biochemistry 9th edition pdf.” (2002).

### Ontologies/Vocabularies for the BAO background knowledge

1. Buttigieg, Pier Luigi, et al. ”The environment ontology in 2016: bridging domains with increased
scope, semantic density, and interoperation.” Journal of biomedical semantics 7 (2016): 1-12.,
https://bioportal.bioontology.org/ontologies/ENVO
2. Diehl, Alexander D., et al. ”The Cell Ontology 2016: enhanced content, modularization, and
ontology interoperability.” Journal of biomedical semantics 7 (2016): 1-10., https://bioportal.bioon-
tology.org/ontologies/CL
3. Huang, Jingshan, et al. ”OmniSearch: a semantic search system based on the Ontology for
MIcroRNA Target (OMIT) for microRNA-target gene interaction data.” Journal of biomedical
semantics 7 (2016): 1-17.,
https://bioportal.bioontology.org/ontologies/OMIT
4. He, Yongqun, Yue Liu, and Bin Zhao. ”OGG: a Biological Ontology for Representing Genes and
Genomes in Specific Organisms.” ICBO. 2014., https://bioportal.bioontology.org/ontologies/OGG
