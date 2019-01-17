# 2019-snakemake-cli

[![travis](https://img.shields.io/travis/charlesreid1/2019-snakemake-cli.svg)](https://travis-ci.org/charlesreid1/2019-snakemake-cli.svg)
[![license](https://img.shields.io/github/license/charlesreid1/2019-snakemake-cli.svg)](https://github.com/charlesreid1/2019-snakemake-cli/blob/master/LICENSE)

An example of a Snakemake command line interface
bundled up as an installable Python package.

This example bundles the Snakefile with the
command line tool, but this tool can also look
in the user's working directory for Snakefiles.

Snakemake functionality is provided through
a command line tool called `bananas`.

# Quickstart

This runs through the installation and usage 
of 2019-snakemake-cli.

## Installing bananas

Start by setting up a virtual environment,
and install the required packages into the
virtual environment:

```
pip install -r requirements.txt
```

Now install the `bananas` command line tool:

```
python setup.py build install
```

Now you can run

```
which bananas
```

and you should see `bananas` in your virtual 
environment's `bin/` directory.

## Running bananas

Move to the `test/` directory and run the tests
with the provided config and params files.

Run the hello workflow with Amy params:

```
rm -f hello.txt
bananas workflow-hello params-amy
```

Run the hello workflow with Beth params:

```
rm -f hello.txt
bananas workflow-hello params-beth
```

Run the goodbye workflow with Beth params:

```
rm -f goodbye.txt
bananas workflow-goodbye params-beth
```

# Details

The entrypoint of the command line interface is
the `main()` function of `cli/command.py`.

The location of the Snakefile is `cli/Snakefile`.

An alternative arrangement would be for users
to provide a Snakefile via rules in the working
directory, or via a Github URL or a remote URL.

