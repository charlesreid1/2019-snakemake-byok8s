# 2019-snakemake-byok8s tests

This guide assumes you have minikube installed. (See `../scripts/` directory...)

We will need to fix a problem with a DNS setting in Kubernetes if we are on
an AWS EC2 node, so we'll walk through how to do that first.

Then we'll cover how to start a Kubernetes cluster and run a simple test.


## Fix k8s DNS problem

If you are running on EC2, you will have
to fix the DNS settings inside the container
by patching the `kube-dns` container that
runs as part of Kubernetes.

Apply the DNS fix to the container,

```
kubernetes apply -f fixcoredns.yml
```

(If you are using an older version of minikube + kubernetes
that uses kube-dns, use `fixkubedns.yml` instead.)


## Start (restart) cluster

If you don't already have a Kubernetes cluster running,
start one with minikube:

```
minikube start

# or, if on ec2,

sudo minikube start
```

If you have a Kubernetes pod currently running,
you can delete all of the kube-system pods, and
they will automatically respawn, including the
(now-fixed) kube-dns container:

```
kubernetes delete --all pods --namespace kube-system
```


## Running tests

Now that DNS is fixed, the host and container can
properly communicate, which is required for Kubernetes
to return files it has created.





