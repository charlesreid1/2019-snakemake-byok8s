# 2019-snakemake-byok8s tests

Assuming you have minikube installed (see `scripts/` directory if you don't)...

Start a cluster:

```
minikube start

# or, if on ec2,

sudo minikube start
```

Now, if you are running on EC2, you will have
to fix the DNS settings inside the container
by patching the `kube-dns` container that
runs as part of Kubernetes.

Apply the DNS fix to the container,

```
kubernetes apply -f fixdns.yml
```

If you have a Kubernetes pod currently running,
you can delete all of the kube-system pods, and
they will automatically respawn, including the
(now-fixed) kube-dns container:

```
kubernetes delete --all pods --namespace kube-system
```

