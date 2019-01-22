# 2019-snakemake-byok8s

[![travis](https://img.shields.io/travis/charlesreid1/2019-snakemake-byok8s.svg)](https://travis-ci.org/charlesreid1/2019-snakemake-byok8s.svg)
[![license](https://img.shields.io/github/license/charlesreid1/2019-snakemake-byok8s.svg)](https://github.com/charlesreid1/2019-snakemake-byok8s/blob/master/LICENSE)

This is an example of a Snakemake workflow that:

- is a command line utility
- is bundled as a Python package
- is designed to run on a Kubernetes cluster

Snakemake functionality is provided through
a command line tool called `byok8s`, so that
it allows you to do this:

```
# install minikube so you can 
# create a (virtual) k8s cluster
scripts/install_minikube.sh

# move to working directory
cd test

# deploy (virtual) k8s cluster
minikube start

# run the workflow
byok8s -w my-workflowfile -p my-paramsfile

# clean up (virtual) k8s cluster
minikube stop
```

Snakemake workflows are run on a Kubernetes (k8s)
cluster. The approach is for the user to provide
their own Kubernetes cluster (byok8s = Bring Your
Own Kubernetes).

The example above uses [`minikube`](https://github.com/kubernetes/minikube)
to make a virtual k8s cluster, useful for testing.

For real workflow,s your options for
kubernetes clusters are cloud providers:

- AWS EKS (Elastic Container Service)
- GCP GKE (Google Kuberntes Engine)
- Digital Ocean Kubernetes service
- etc...

Travis CI tests utilize minikube.


# Quickstart

This runs through the installation and usage 
of `2019-snakemake-byok8s`.

Step 1: Set up Kubernetes cluster with `minikube`.

Step 2: Install `byok8s`.

Step 3: Run the `byok8s` workflow using the Kubernetes cluster. 

Step 4: Tear down Kubernetes cluster with `minikube`.


## Step 1: Set Up VirtualKubernetes Cluster 

### Installing Minikube

For the purposes of the quickstart, we will walk
through how to set up a local, virtual Kubernetes
cluster using `minikube`.

Start by installing minikube:

```
scripts/install_minicube.sh
```

Once it is installed, you can start up a kubernetes cluster
with minikube using the following command:

```
minikube start
```

NOTE: If you are running on AWS, 

```
minikube config set vm-driver none
```

to set the the vm driver to none and use native Docker to run stuff.

## Step 2: Install byok8s

Start by setting up a python virtual environment,
and install the required packages into the
virtual environment:

```
pip install -r requirements.txt
```

This installs snakemake and kubernetes Python
modules. Now install the `byok8s` command line
tool:

```
python setup.py build install
```

Now you can run:

```
which byok8s
```

and you should see `byok8s` in your virtual 
environment's `bin/` directory.

This command line utility will expect a kubernetes
cluster to be set up before it is run. 

Setting up a kubernetes cluster will create...
(fill in more info here)...

Snakemake will automatically create the pods
in the cluster, so you just need to allocate
a kubernetes cluster.


## Step 3: Run byok8s

Now you can run the workflow with the `byok8s` command.
This submits the Snakemake workflow jobs to the Kubernetes
cluster that minikube created.

(NOTE: the command line utility must be run
from the same directory as the kubernetes 
cluster was created from, otherwise Snakemake
won't be able to find the kubernetes cluster.)

(Would be a good idea to instead specify paths
for workflow config and param files,
or have a built-in set of params and configs.)

Run the blue workflow with alpha params:

```
byok8s -w workflow-blue -p params-alpha
```

Run the blue workflow with gamma params, and 
kubernetes configuration details in kube-deets
(all json files):

```
byok8s -w workflow-blue -p params-gamma
```

Run the red workflow with gamma params, &c:

```
byok8s -w workflow-red -p params-gamma
```

(NOTE: May want to let the user specify 
input and output directories with flags.)

Make reasonable assumptions:

- if no input dir specified, use cwd
- if no output dir specified, make one w timestamp and workflow params
- don't rely on positional args, makes it harder to translate python code/command line calls


## Step 4: Tear Down Kubernetes Cluster

The last step once the workflow has been finished,
is to tear down the kubernetes cluster. The virtual
kubernetes cluster created by minikube can be torn
down with the following command:

```
minikube stop
```

