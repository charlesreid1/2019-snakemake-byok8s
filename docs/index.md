# 2019-snakemake-byok8s

[![travis](https://img.shields.io/travis/charlesreid1/2019-snakemake-byok8s.svg)](https://travis-ci.org/charlesreid1/2019-snakemake-byok8s)
[![license](https://img.shields.io/github/license/charlesreid1/2019-snakemake-byok8s.svg)](https://github.com/charlesreid1/2019-snakemake-byok8s/blob/master/LICENSE)

# Overview

This is an example of a Snakemake workflow that:

- is a **command line utility** called `byok8s`
- is bundled as an installable **Python package**
- is designed to run on a **Kubernetes (k8s) cluster**
- can be **tested with Travis CI** (and/or locally) using [minikube](https://github.com/kubernetes/minikube)

## How is byok8s invoked?

Snakemake functionality is provided through
a command line tool called `byok8s`, so that
it allows you to do this (also see the 
[Quickstart Guide](quickstart.md)).

```
# Install byok8s
python setup.py build install

# Create virtual k8s cluster
minikube start

# Run the workflow on the k8s cluster
cd /path/to/workflow/
byok8s my-workflowfile my-paramsfile --s3-bucket=my-bucket

# Clean up the virtual k8s cluster
minikube stop
```

## Getting Up and Running

See the [Quickstart Guide](quickstart.md) to get up and running with 
byok8s on an AWS node.

## How does byok8s work?

The command line utility requires the user to provide three inputs:

* A snakemake workflow, via a `Snakefile`
* A workflow configuration file (JSON)
* A workflow parameters file (JSON)

Additionally, the user must have a Kubernetes cluster running.
(The approach is for the user to bring their own Kubernetes cluster
to the table - hence byok8s = Bring Your Own Kubernetes).

The workflow config file specifies which workflow targets
and input files to use.

The workflow parameters file specifies which parameters to
use for the workflow steps.

## Why S3 Buckets?

AWS credentials and an S3 bucket is required to run workflows because 
of restrictions on file I/O on nodes in a kubernes cluster. The Snakemake
workflows use AWS S3 buckets as remote providers for the Kubernetes nodes,
but this can be modified to any others that Snakemake supports.

AWS credentials are set with the two environment variables:

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

These are passed into the Kubernetes cluster by byok8s and Snakemake.

## Kubernetes and Minikube

[Kubernetes](https://kubernetes.io/) is a technology that utilizes Docker
container to orchestrate a cluster of compute nodes. These compute nodes are
usually real compute nodes requested and managed via a cloud provider, like AWS
or Google Cloud.

But the compute nodes can also be virtual, which is where
[minikube](https://github.com/kubernetes/minikube) comes in.  It creates a
kubernetes cluster that is entirely local and virtual, which makes testing
easy. See the [byok8s Minikube Guide](kubernetes_minikube.md) for details
about how to use minikube with byok8s.

The Travis CI tests also utilize minikube to run test workflows. See [byok8s
Travis Tests](travis_tests.md) for more information.

## Cloud Providers

For real workflows, your options for
kubernetes clusters are cloud providers.
We have guides for the following:

- AWS EKS (Elastic Container Service)
- GCP GKE (Google Kuberntes Engine)
- Digital Ocean Kubernetes service

# Kubernetes + byok8s: In Practice

|  Cloud Provider             | Kubernetes Service              | Guide                                           |
|-----------------------------|---------------------------------|-------------------------------------------------|
| Minikube (on AWS EC2)       | Minikube                        | [byok8s Minikube Guide](kubernetes_minikube.md) |
| Google Cloud Platform (GCP) | Google Container Engine (GKE)   | [byok8s GCP GKE Guide](kubernetes_gcp.md)       | 
| Amazon Web Services (AWS)   | Elastic Container Service (EKS) | [byok8s AWS EKS Guide](kubernetes_aws.md)       | 
| Digital Ocean (DO)          | DO Kubernetes (DOK)             | [byok8s DO DOK Guide](kubernetes_dok.md)        | 

