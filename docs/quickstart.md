# Quickstart

This runs through the installation and usage 
of `2019-snakemake-byok8s`.

Step 1: Set up Kubernetes cluster with `minikube`.

Step 2: Install `byok8s`.

Step 3: Run the `byok8s` workflow using the Kubernetes cluster. 

Step 4: Tear down Kubernetes cluster with `minikube`.


## Step 1: Set Up Virtual Kubernetes Cluster 

For the purposes of the quickstart, we will walk
through how to set up a local, virtual Kubernetes
cluster using `minikube`.

Start by installing minikube:

```
scripts/install_minikube.sh
```

Once it is installed, you can start up a kubernetes cluster
with minikube using the following commands:

```
cd test
minikube start
```

NOTE: If you are running on AWS, run this command first

```
minikube config set vm-driver none
```

to set the the vm driver to none and use native Docker to run stuff.

If you are running on AWS, the DNS in the minikube
kubernetes cluster will not work, so run this command
to fix the DNS settings (should be run from the
`test/` directory):

```
kubectl apply -f fixcoredns.yml
kubectl delete --all pods --namespace kube-system
```


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

You should have your workflow in a `Snakefile` in the
current directory. Use the `--snakefile` flag if it is
named something other than `Snakefile`.

You will also need to specify your AWS credentials
via the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
environment variables. These are used to to access
S3 buckets for file I/O.

Finally, you will need to create an S3 bucket for
Snakemake to use for file I/O. Pass the name of the
bucket using the `--s3-bucket` flag.

Start by exporting these two vars (careful to
scrub them from bash history):

```
export AWS_ACCESS_KEY_ID=XXXXX
export AWS_SECRET_ACCESS_KEY=XXXXX
```

Run the alpha workflow with blue params:

```
byok8s --s3-bucket=mah-bukkit workflow-alpha params-blue
```

Run the alpha workflow with red params:

```
byok8s --s3-bucket=mah-bukkit workflow-alpha params-red
```

Run the gamma workflow with red params, &c:

```
byok8s --s3-bucket=mah-bukkit workflow-gamma params-red
```

(NOTE: May want to let the user specify 
input and output directories with flags.)

All input files are searched for relative to the working
directory.


## Step 4: Tear Down Kubernetes Cluster

The last step once the workflow has been finished,
is to tear down the kubernetes cluster. The virtual
kubernetes cluster created by minikube can be torn
down with the following command:

```
minikube stop
```


