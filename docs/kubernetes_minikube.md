# Running byok8s with minikube

## Installing

See the [Installing](installing.md) page for details
about installing byok8s and its prerequisites
(including minikube).

We cover two scenarios:

- bare metal machine, i.e., a laptop or desktop machine
  that can run a hypervisor like VirtualBox

- cloud machine, i.e., AWS EC2 node, which is itself a
  virtual machine and cannot run a hypervisor

These quickstarts assume you have Python and minikube
installed, and that you have cloned and installed byok8s
at `~/2019-snakemake-byok8s/`.

## Quickstart on Bare Metal Machine

On a bare metal machine, the procedure is 
relatively uncomplicated: we create a cluster,
we export some variables, we run the workflow,
we tear down the cluster:

```plain
# Start a minikube cluster
minikube start

# Verify k8s is running
minikube status

# Export AWS credentials
export AWS_ACCESS_KEY_ID="XXXXX"
export AWS_SECRET_ACCESS_KEY="XXXXX"

# Run the workflow
byok8s workflow-alpha params-blue --s3-bucket=mah-bukkit 

# Stop the minikube cluster
minikube stop
```

## Quickstart on Cloud Machine

As mentioned above, cloud compute nodes are virtual machines
themselves and cannot run a hypervisor, so things are a bit
more complicated.

To tell minikube not to use a virtual machine driver,
run the following command in a terminal to create
a minikube config file:

```
cat <<'EOF' > ~/.minikube/config/config.json
{
    "vm-driver": "none"
}
EOF
```

Now you can start up a minikube cluster. 

There is an additional DNS problem that needs to be fixed
in the containers before you proceed. You will know there
is a problem if you run the `get pods` command with
`kubectl` and see your CoreDNS containers in a 
`CrashLoopBackOff` state:

```text
$ kubectl get pods --namespace=kube-system
NAME                               READY   STATUS             RESTARTS   AGE
coredns-86c58d9df4-lvq8b           0/1     CrashLoopBackOff   5          5m17s
coredns-86c58d9df4-pr52t           0/1     CrashLoopBackOff   5          5m17s
...                                ...     ...                ...        ...
```

To fix the problem with the DNS settings, we have to patch
the CoreDNS image being used by `kube-system`.
To do that, use the file
[`test/fixcoredns.yml`](https://github.com/charlesreid1/2019-snakemake-byok8s/blob/master/test/fixcoredns.yml)
in this repository with `kubectl apply`:

```plain
# Fix the DNS container
kubectl apply -f fixcoredns.yml

# Delete all kube-system containers
kubectl delete --all pods --namespace kube-system
```

The kube-system containers will be re-spawned by the cluster control system.
It should happen in a few seconds, and then you'll be ready to run byok8s:

```
# Return to our virtual environment
cd ~/2019-snakemake-byok8s/test/
source vp/bin/activate

# Verify k8s is running
minikube status

# Export AWS keys for Snakemake
export AWS_ACCESS_KEY_ID="XXXXX"
export AWS_SECRET_ACCESS_KEY="XXXXX"

# Run byok8s
byok8s workflow-alpha params-blue --s3-bucket=mah-bukkit 
```

Congratulations! You've just run an executable Snakemake workflow
on a minikube kubernetes cluster.

