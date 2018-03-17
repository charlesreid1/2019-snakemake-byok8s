# 2018-snakemake-cli

An example of parameterizing snakemake workflows with a simple CLI.

Usage:
```
./run <workflow_file> <parameters_file>
```

e.g.

```
rm -f hello.txt
./run workflow-hello params-amy
```
creates `hello.txt` with "hello amy" in it, while

```
rm -f hello.txt
./run workflow-hello params-beth
```
creates `hello.txt` with "hello beth" in it.

Here, the workflow file `workflow-hello.json` specifes the target
`hello.txt`, while the parameters file `params-amy` parameterizes
the workflow with the name "amy".

Likewise,

```
rm -f goodbye.txt
./run workflow-goodbye params-beth
```

will put `goodbye beth` in `goodbye.txt`.

All workflows use the same set of Snakemake rules in `Snakefile`.
