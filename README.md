# CurateGPT

[![DOI](https://zenodo.org/badge/645996391.svg)](https://zenodo.org/doi/10.5281/zenodo.8293691)


CurateGPT is a prototype web application and framework for performing general purpose AI-guided curation
and curation-related operations over *collections* of objects.


See also the app on [curategpt.io](https://curategpt.io) (note: this is sometimes down, and may only have a
subset of the functionality of the local app)


## Installation

You will first need to [install Poetry](https://python-poetry.org/docs/#installation).

Then clone this repo 

```
git clone https://github.com/monarch-initiative/curate-gpt.git
cd curate-gpt
```

and install the dependencies:


```
poetry install
```

In order to get the best performance from CurateGPT, we recommend getting an OpenAI API key, and setting it:

```
export OPENAI_API_KEY=<your key>
```

(for members of Monarch: ask on Slack if you would like to use the group key)

## Loading example data and running the app

You initially start with an empty database. You can load whatever you like into this
database! Any JSON, YAML, or CSV is accepted.
CurateGPT comes with *wrappers* for some existing local and remote sources, including
ontologies. The [Makefile](Makefile) contains some examples of how to load these. You can
load any ontology using the `ont-<name>` target, e.g.:

```
make ont-cl
```

This loads CL (via OAK) into a collection called `ont_cl`

Note that by default this loads into a collection set stored at `stagedb`, whereas the app works off
of `db`. You can copy the collection set to the db with:

```
cp -r stagedb/* db/
```


You can then run the streamlit app with:

```
make app
```

## Building Indexes

CurateGPT depends on vector database indexes of the databases/ontologies you want to curate.

The flagship application is ontology curation, so to build an index for an OBO ontology like CL:

```
make ont-cl
```

This requires an OpenAI key.

(You can build indexes using an open embedding model, modify the command to leave off
the `-m` option, but this is not recommended as currently oai embeddings seem to work best).


To load the default ontologies:

```
make all
```

(this may take some time)

To load different databases:

```
make load-db-hpoa
make load-db-reactome
```



You can load an arbitrary json, yaml, or csv file:

```
curategpt view index -c my_foo foo.json
```

(you will need to do this in the poetry shell)

To load a GitHub repo of issues:

```
curategpt -v view index -c gh_uberon -m openai:  --view github --init-with "{repo: obophenotype/uberon}"
```

The following are also supported:

- Google Drives
- Google Sheets
- Markdown files
- LinkML Schemas
- HPOA files
- GOCAMs
- MAXOA files
- Many more

## Notebooks

- See [notebooks](notebooks) for examples.

## Selecting models

Currently this tool works best with the OpenAI gpt-4 model (for instruction tasks) and OpenAI `ada-text-embedding-002` for embedding.

Curate-GPT is layered on top of [simonw/llm](https://github.com/simonw/llm) which has a plugin
architecture for using alternative models. In theory you can use any of these plugins.

Additionally, you can set up an openai-emulating proxy using [litellm](https://github.com/BerriAI/litellm/).

The `litellm` proxy may be installed with `pip` as `pip install litellm[proxy]`.

Let's say you want to run mixtral locally using ollama. You start up ollama (you may have to run `ollama serve` first):

```
ollama run mixtral
```

Then start up litellm:

```
litellm -m ollama/mixtral
```

Next edit your `extra-openai-models.yaml` as detailed in [the llm docs](https://llm.datasette.io/en/stable/other-models.html):

```
- model_name: ollama/mixtral
  model_id: litellm-mixtral
  api_base: "http://0.0.0.0:8000"
```

You can now use this:

```yaml
curategpt ask -m litellm-mixtral -c ont_cl "What neurotransmitter is released by the hippocampus?"
```

But be warned that many of the prompts in curategpt were engineered
against openai models, and they may give suboptimal results or fail
entirely on other models. As an example, `ask` seems to work quite
well with mixtral, but `complete` works horribly. We haven't yet
investigated if the issue is the model or our prompts or the overall
approach.

Welcome to the world of AI engineering!

## Using the command line

```bash
curategpt --help
```

You will see various commands for working with indexes, searching, extracting, generating, etc.

These functions are generally available through the UI, and the current priority is documenting these.

### Chatting with a knowledge base

```
curategpt ask -c ont_cl "What neurotransmitter is released by the hippocampus?"
```

may yield something like:

```
The hippocampus releases gamma-aminobutyric acid (GABA) as a neurotransmitter [1](#ref-1).

...

## 1

id: GammaAminobutyricAcidSecretion_neurotransmission
label: gamma-aminobutyric acid secretion, neurotransmission
definition: The regulated release of gamma-aminobutyric acid by a cell, in which the
  gamma-aminobutyric acid acts as a neurotransmitter.
...
```

### Chatting with pubmed

```
curategpt view ask -V pubmed "what neurons express VIP?"
```

### Chatting with a GitHub issue tracker

```
curategpt ask -c gh_obi "what are some new term requests for electrophysiology terms?"
```

### Term Autocompletion (DRAGON-AI)

```
curategpt complete -c ont_cl  "mesenchymal stem cell of the apical papilla"
```

yields

```yaml
id: MesenchymalStemCellOfTheApicalPapilla
definition: A mesenchymal cell that is part of the apical papilla of a tooth and has
  the ability to self-renew and differentiate into various cell types such as odontoblasts,
  fibroblasts, and osteoblasts.
relationships:
- predicate: PartOf
  target: ApicalPapilla
- predicate: subClassOf
  target: MesenchymalCell
- predicate: subClassOf
  target: StemCell
original_id: CL:0007045
label: mesenchymal stem cell of the apical papilla
```

### All-by-all comparisons

You can compare all objects in one collection 

`curategpt all-by-all --threshold 0.80 -c ont_hp -X ont_mp --ids-only -t csv > ~/tmp/allxall.mp.hp.csv`

This takes 1-2s, as it involves comparison over pre-computed vectors. It reports top hits above a threshold.

Results may vary. You may want to try different texts for embeddings
(the default is the entire json object; for ontologies it is
concatenation of labels, definition, aliases).

sample:

```
HP:5200068,Socially innappropriate questioning,MP:0001361,social withdrawal,0.844015132437909
HP:5200069,Spinning,MP:0001411,spinning,0.9077306606290237
HP:5200071,Delayed Echolalia,MP:0013140,excessive vocalization,0.8153252835818089
HP:5200072,Immediate Echolalia,MP:0001410,head bobbing,0.8348177036912526
HP:5200073,Excessive cleaning,MP:0001412,excessive scratching,0.8699103725005582
HP:5200104,Abnormal play,MP:0020437,abnormal social play behavior,0.8984862078522344
HP:5200105,Reduced imaginative play skills,MP:0001402,decreased locomotor activity,0.85571629684631
HP:5200108,Nonfunctional or atypical use of objects in play,MP:0003908,decreased stereotypic behavior,0.8586700411012859
HP:5200129,Abnormal rituals,MP:0010698,abnormal impulsive behavior control,0.8727804272023427
HP:5200134,Jumping,MP:0001401,jumpy,0.9011393233129765
```

Note that CurateGPT has a separate component for using an LLM to evaluate candidate matches (see also https://arxiv.org/abs/2310.03666); this is
not enabled by default, this would be expensive to run for a whole ontology.

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
