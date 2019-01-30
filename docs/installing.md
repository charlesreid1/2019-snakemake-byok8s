# Installing byok8s

byok8s requires two pieces of prerequisite software:

- python (conda)
- virtualenv (optional)

It also requires an AWS S3 bucket to be specified 
(the bucket must exist and credentials to access it
must be provided via environment variables, see the
[Quickstart](quickstart.md)).

Additionally, if you are planning to run byok8s on
a local virtual kubernetes cluster, you must install:

- minikube

Otherwise, if you are planning on running byok8s on 
remote kubernetes clusters provided by cloud providers, 
you must install:

- kubernetes, ***OR***
- a cloud provider command line tool (`gcloud`, `aws`)

## Installing Python

We recommend installing pyenv and using pyenv
to install miniconda:

```plain
curl https://pyenv.run | bash
```

Restart your shell and install miniconda:

```plain
pyenv update
pyenv install miniconda3-4.3.30
pyenv global miniconda3-4.3.30
```

## Installing virtualenv

You will need the virtualenv package to
set up a virtual environment:

```plain
pip install virtualenv
```

## Installing minikube

This step is only required if you plan to run byok8s
kubernetes workflows locally on a virtual kubernetes
cluster (i.e., testing mode).

Install the 64-bit Linux version of minikube, or visit the
[installing minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/)
to find the right version:

```plain
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 \
  && sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

(On a Mac you can do `brew install minikube`.)

If you are planning on running on a bare metal
machine, you will also need to install a hypervisor
like VirtualBox or KVM, see [installing minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/).

If you are planning on running minikube on a compute
node in the cloud, you cannot run a hypervisor, so you
will need to run using the native driver; see 
[installing minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/).

Once you have installed minikube, you do not need to
install kubernetes.

## Installing byok8s

Start by cloning the repo and installing byok8s:

```plain
cd 
git clone https://github.com/charlesreid1/2019-snakemake-byok8s.git
cd ~/2019-snakemake-byok8s
```

Next, you'll create a virtual environment:

```plain
virtualenv vp
source vp/bin/activate

pip install -r requirements.txt
python setup.py build install
```

Now you should be ready to rock:

```
which byok8s
```

This will only be present when you have activated
your virtual environment. To activate/re-activate your 
virtual environment:

```
cd ~/2019-snakemake-byok8s
source vp/bin/activate
```

