# YOKO ONtO: You only KNIT one ontology

[![Python](https://img.shields.io/badge/python-3.9-blue.svg?style=flat-square)](https://python.org)
[![License](https://img.shields.io/github/license/KhaosResearch/TITAN-API.svg?style=flat-square)](https://github.com/ProyectoAether/KNIT/blob/main/LICENSE)

The YOKO ONtO tool provides a visualization layer on top of [KNIT](https://github.com/ProyectoAether/KNIT), presenting a draft knowledge graph with data retrieved from existing ontologies.

## Getting started

```
$ cd YOKO
$ docker build -t yoko_onto:1.0.0 . 

```
And finally, run docker container:

```
$ docker run -d -p 0.0.0.0:8501:8501 yoko_onto:1.0.0
```
