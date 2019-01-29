# Kubernetes on Google Cloud Platform

This document will walk you through how to start a
kubernetes cluster using Google Cloud Platform (GCP),
run the byok8s workflow on the kubernetes cluster,
and tear down the cluster.

## Setup

Before you can create a kubernetes cluster on Google Cloud,
you need a Google Cloud account and a Google Cloud project.
You can create a new project from the [Google Cloud Console](https://console.cloud.google.com/).

Once you have your account and your project, you can install
the `gcloud` Google Cloud SDK command line utility 
(see [Google Cloud SDK Quickstart Guide](https://cloud.google.com/sdk/docs/quickstarts)).

Once you have installed the `gcloud` utility, you will need 
to log in with your Google acount using the `init` command:

```
gcloud init
```

This will give you a link to enter into your browser, where 
you will log in with your Google account and recieve a code to
copy and paste into the terminal.

The **Compute API** and **Kubernetes API** will both need to be
enabled as well. These can be enabled via the 
[Google Cloud Console](https://console.cloud.google.com/),
or read on.

If you aren't sure what to do, start running the commands 
below to create a kubernetes cluster, and the gcloud utility
will let you know if it needs APIs enabled for actions.
If it can't enable the API for you, it will give you a 
direct link to the relevant Google Cloud Console page.

## Google Kubernetes Engine

GKE uses Google Cloud compute nodes to run a kubernetes cluster
on Google Cloud infrastructure. It automatically sets up the
cluster for you, and allows you to use `kubectl` and `gcloud` to
manage and interact with the remote cluster.

Official Google link: <https://cloud.google.com/kubernetes-engine/>

## Quickstart

As mentioned, make sure your account credentials are initialized:

```
gcloud init
```

Create a new GKE cluster:

```
gcloud container clusters create $CLUSTER_NAME --num-nodes=$NODES --region=us-west1
```

The `--scopes storage-rw` flag is required if you plan to use Google
Cloud buckets instead of S3 buckets (not currently enabled in byok8s).

Next get configuration details about the cluster so your local 
kubernetes controller can control the cluster:

```
gcloud container clusters get-credentials $CLUSTER_NAME
```

**This will take several minutes.**

The cluster should now be up and running and ready to rock:

```
$ kubectl get pods --namespace=kube-system
NAME                                                  READY   STATUS    RESTARTS   AGE
event-exporter-v0.2.3-54f94754f4-5jczv                2/2     Running   0          4m
fluentd-gcp-scaler-6d7bbc67c5-hkllz                   1/1     Running   0          4m
fluentd-gcp-v3.1.0-48pb2                              2/2     Running   0          2m
fluentd-gcp-v3.1.0-58dpx                              2/2     Running   0          2m
fluentd-gcp-v3.1.0-c4b49                              2/2     Running   0          2m
fluentd-gcp-v3.1.0-h24m5                              2/2     Running   0          2m
fluentd-gcp-v3.1.0-hbdj4                              2/2     Running   0          2m
fluentd-gcp-v3.1.0-rfnmt                              2/2     Running   0          2m
fluentd-gcp-v3.1.0-vwd8w                              2/2     Running   0          2m
fluentd-gcp-v3.1.0-wxt79                              2/2     Running   0          2m
fluentd-gcp-v3.1.0-xkt42                              2/2     Running   0          2m
heapster-v1.5.3-bc9f6bfd5-7jhqs                       3/3     Running   0          3m
kube-dns-788979dc8f-l7hch                             4/4     Running   0          4m
kube-dns-788979dc8f-pts99                             4/4     Running   0          3m
kube-dns-autoscaler-79b4b844b9-j48js                  1/1     Running   0          4m
kube-proxy-gke-mycluster-default-pool-9ad2912e-130p   1/1     Running   0          4m
kube-proxy-gke-mycluster-default-pool-9ad2912e-lfpw   1/1     Running   0          4m
kube-proxy-gke-mycluster-default-pool-9ad2912e-rt9m   1/1     Running   0          4m
kube-proxy-gke-mycluster-default-pool-b44fa389-2ds8   1/1     Running   0          4m
kube-proxy-gke-mycluster-default-pool-b44fa389-hc66   1/1     Running   0          4m
kube-proxy-gke-mycluster-default-pool-b44fa389-vh3x   1/1     Running   0          4m
kube-proxy-gke-mycluster-default-pool-d58ee1e7-2kkw   1/1     Running   0          4m
kube-proxy-gke-mycluster-default-pool-d58ee1e7-3l6r   1/1     Running   0          4m
kube-proxy-gke-mycluster-default-pool-d58ee1e7-4w18   1/1     Running   0          4m
l7-default-backend-5d5b9874d5-ms75l                   1/1     Running   0          4m
metrics-server-v0.2.1-7486f5bd67-2n6cn                2/2     Running   0          3m
```

Now assuming you have installed `byok8s` and it is located
at `~/2019-snakemake-byok8s/`, you can run the test workflow
on the kubernetes cluster:

```
# Return to our virtual environment
cd ~/2019-snakemake-byok8s/test/
source vp/bin/activate

# Export AWS keys for Snakemake
export AWS_ACCESS_KEY_ID="XXXXX"
export AWS_SECRET_ACCESS_KEY="XXXXX"

# Run byok8s
byok8s workflow-alpha params-blue --s3-bucket=mah-bukkit 
```

Once the workflow has run successfully, the results will be written
to S3 buckets and all the kubernetes containers created by snakemake
will be gone. 

If all goes well, you should see output like this:

```
$ byok8s --s3-bucket=mah-bukkit -f workflow-alpha params-blue
--------
details!
	snakefile: /home/ubuntu/2019-snakemake-byok8s/test/Snakefile
	config: /home/ubuntu/2019-snakemake-byok8s/test/workflow-alpha.json
	params: /home/ubuntu/2019-snakemake-byok8s/test/params-blue.json
	target: target1
	k8s namespace: default
--------
Building DAG of jobs...
Using shell: /bin/bash
Provided cores: 1
Rules claiming more threads will be scaled down.
Job counts:
	count	jobs
	1	target1
	1
Resources before job selection: {'_cores': 1, '_nodes': 9223372036854775807}
Ready jobs (1):
	target1
Selected jobs (1):
	target1
Resources after job selection: {'_cores': 0, '_nodes': 9223372036854775806}

[Mon Jan 28 23:49:51 2019]
rule target1:
    output: cmr-0123/alpha.txt
    jobid: 0

echo alpha blue > cmr-0123/alpha.txt
Get status with:
kubectl describe pod snakejob-1ab52bdb-903b-5506-b712-ccc86772dc8d
kubectl logs snakejob-1ab52bdb-903b-5506-b712-ccc86772dc8d
Checking status for pod snakejob-1ab52bdb-903b-5506-b712-ccc86772dc8d
Checking status for pod snakejob-1ab52bdb-903b-5506-b712-ccc86772dc8d
Checking status for pod snakejob-1ab52bdb-903b-5506-b712-ccc86772dc8d
Checking status for pod snakejob-1ab52bdb-903b-5506-b712-ccc86772dc8d
Checking status for pod snakejob-1ab52bdb-903b-5506-b712-ccc86772dc8d
[Mon Jan 28 23:50:41 2019]
Finished job 0.
1 of 1 steps (100%) done
Complete log: /home/ubuntu/2019-snakemake-byok8s/test/.snakemake/log/2019-01-28T234950.253823.snakemake.log
unlocking
removing lock
removing lock
removed all locks
```

Congratulations! You'e just run an executable Snakemake workflow
on a Google Cloud kubernetes cluster!

Delete the GKE cluster when you are done:

```
gcloud container clusters delete $CLUSTER_NAME
```

