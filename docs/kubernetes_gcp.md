# Kubernetes on Google Cloud Platform

This document will walk you through how to start a kubernetes cluster using the
Google Kubernetes Engine (GKE) on Google Cloud Platform (GCP), run the byok8s
Snakemake workflow on the GKE kubernetes cluster, and tear down the cluster
when the workflow is complete.

## Setup

Before you can create a kubernetes cluster on Google Cloud,
you need a Google Cloud account and a Google Cloud project.
You can sign up for a Google Cloud account [here](https://cloud.google.com/).
You can create a new project from the [Google Cloud Console](https://console.cloud.google.com/).
New accounts start with 300 free hours specifically to let you
test drive features like GKE! Cool!

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
[Google Cloud Console](https://console.cloud.google.com/)
(or read on).

If you aren't sure how to use the console to enable these APIs, just start
running the commands below to create a kubernetes cluster, and the gcloud
utility will let you know if it needs APIs enabled for actions.  If it can't
enable the API for you, it will give you a direct link to the relevant Google
Cloud Console page.

## Google Kubernetes Engine (GKE)

GKE uses GCP compute nodes to run a kubernetes cluster
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

You can get more information about the containers running each step of 
the workflow using the `kubectl describe` commands printed in the output.
Here is an example:

```
$ kubectl describe pod snakejob-c91f804c-805a-56a2-b0ea-b3b74bc38001
Name:         snakejob-c91f804c-805a-56a2-b0ea-b3b74bc38001
Namespace:    default
Node:         gke-mycluster-default-pool-b44fa389-vh3x/10.138.0.7
Start Time:   Mon, 28 Jan 2019 23:55:18 -0800
Labels:       app=snakemake
Annotations:  <none>
Status:       Running
IP:           10.0.6.4
Containers:
  snakejob-c91f804c-805a-56a2-b0ea-b3b74bc38001:
    Container ID:  docker://2aaa04c34770c6088334b29c0332dc426aff2fbbd3a8af07b65bbbc2c5fe437d
    Image:         quay.io/snakemake/snakemake:v5.4.0
    Image ID:      docker-pullable://quay.io/snakemake/snakemake@sha256:f5bb7bef99c4e45cb7dfd5b55535b8dc185b43ca610341476378a9566a8b52c5
    Port:          <none>
    Host Port:     <none>
    Command:
      /bin/sh
    Args:
      -c
      cp -rf /source/. . && snakemake cmr-0123/.zetaB1 --snakefile Snakefile --force -j --keep-target-files  --keep-remote --latency-wait 0  --attempt 1 --force-use-threads --wrapper-prefix None --config 'name='"'"'blue'"'"'' -p --nocolor --notemp --no-hooks --nolock  --default-remote-provider S3 --default-remote-prefix cmr-0123  --allowed-rules target3sleepyB1
    State:          Running
      Started:      Mon, 28 Jan 2019 23:56:15 -0800
    Ready:          True
    Restart Count:  0
    Requests:
      cpu:  0
    Environment:
      AWS_ACCESS_KEY_ID:      <set to the key 'aws_access_key_id' in secret 'e077a45f-1274-4a98-a76c-d1a9718707db'>      Optional: false
      AWS_SECRET_ACCESS_KEY:  <set to the key 'aws_secret_access_key' in secret 'e077a45f-1274-4a98-a76c-d1a9718707db'>  Optional: false
    Mounts:
      /source from source (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-jmnv4 (ro)
Conditions:
  Type           Status
  Initialized    True
  Ready          True
  PodScheduled   True
Volumes:
  source:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  e077a45f-1274-4a98-a76c-d1a9718707db
    Optional:    false
  workdir:
    Type:    EmptyDir (a temporary directory that shares a pod's lifetime)
    Medium:
  default-token-jmnv4:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-jmnv4
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  <none>
Tolerations:     node.kubernetes.io/not-ready:NoExecute for 300s
                 node.kubernetes.io/unreachable:NoExecute for 300s
Events:
  Type    Reason                 Age   From                                               Message
  ----    ------                 ----  ----                                               -------
  Normal  Scheduled              63s   default-scheduler                                  Successfully assigned snakejob-c91f804c-805a-56a2-b0ea-b3b74bc38001 to gke-mycluster-default-pool-b44fa389-vh3x
  Normal  SuccessfulMountVolume  63s   kubelet, gke-mycluster-default-pool-b44fa389-vh3x  MountVolume.SetUp succeeded for volume "workdir"
  Normal  SuccessfulMountVolume  63s   kubelet, gke-mycluster-default-pool-b44fa389-vh3x  MountVolume.SetUp succeeded for volume "default-token-jmnv4"
  Normal  SuccessfulMountVolume  63s   kubelet, gke-mycluster-default-pool-b44fa389-vh3x  MountVolume.SetUp succeeded for volume "source"
  Normal  Pulling                61s   kubelet, gke-mycluster-default-pool-b44fa389-vh3x  pulling image "quay.io/snakemake/snakemake:v5.4.0"
  Normal  Pulled                 10s   kubelet, gke-mycluster-default-pool-b44fa389-vh3x  Successfully pulled image "quay.io/snakemake/snakemake:v5.4.0"
  Normal  Created                6s    kubelet, gke-mycluster-default-pool-b44fa389-vh3x  Created container
  Normal  Started                6s    kubelet, gke-mycluster-default-pool-b44fa389-vh3x  Started container
```

Congratulations! You've successfully run an executable Snakemake workflow
on a Google Cloud kubernetes cluster!

Delete the GKE cluster when you are done:

```
gcloud container clusters delete $CLUSTER_NAME
```

