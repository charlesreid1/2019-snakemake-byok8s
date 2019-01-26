"""
Command line interface driver for snakemake workflows
"""
import argparse
import os.path
import snakemake
import sys
import pprint
import json
import subprocess

from . import _program


thisdir = os.path.abspath(os.path.dirname(__file__))
cwd = os.getcwd()

def main(sysargs = sys.argv[1:]):

    descr = ''
    usg = '''byok8s [--FLAGS] <workflowfile> <paramsfile> [<target>]

byok8s: run snakemake workflows on your own kubernetes 
cluster, using the given workflow name & parameters file.

byok8s requires an S3 bucket be used for file I/O. Set
AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env vars.

'''

    parser = argparse.ArgumentParser(
            prog = _program, 
            description=descr,
            usage = usg
    )

    parser.add_argument('workflowfile')
    parser.add_argument('paramsfile')

    parser.add_argument('-k', '--k8s-namespace',default='default',   help='Namespace of Kubernetes cluster, if not "default"')
    parser.add_argument('-s', '--snakefile',    default='Snakefile', help='Relative path to Snakemake Snakefile, if not "Snakefile"')
    parser.add_argument('-b', '--s3-bucket',                         help='Name of S3 bucket to use for Snakemake file I/O (REQUIRED)')
    parser.add_argument('-n', '--dry-run',      action='store_true', help='Do a dry run of the workflow commands (no commands executed)')
    parser.add_argument('-f', '--force',        action='store_true', help='Force Snakemake rules to be re-run')
    # NOTE: You MUST use S3 buckets, GCS buckets are not supported.
    # That's because GCP requires credentials to be stored in a file,
    # and we can only pass environment variables into k8s containers.

    args = parser.parse_args(sysargs)

    # find the Snakefile
    s1 = os.path.join(cwd,args.snakefile)
    if os.path.isfile(s1):
        # user has provided a relative path
        # to a Snakefile. top priority.
        snakefile = os.path.join(cwd,args.snakefile)

    else:
        msg = 'Error: cannot find Snakefile at {}\n'.format(s1)
        sys.stderr.write(msg)
        sys.exit(-1)

    # find the workflow config file
    w1 = os.path.join(cwd,args.workflowfile)
    w2 = os.path.join(cwd,args.workflowfile+'.json')
    # TODO: yaml
    if os.path.isfile(w1):
        # user has provided the full filename
        workflowfile = w1
    elif os.path.isfile(w2):
        # user has provided the prefix of the
        # json filename
        workflowfile = w2
    else:
        msg = ['Error: cannot find workflowfile (workflow configuration file) at any of the following locations:\n']
        msg += ['{}'.format(j) for j in [w1,w2]]
        sys.stderr.write(msg)
        sys.exit(-1)

    # find the workflow params file
    p1 = os.path.join(cwd,args.paramsfile)
    p2 = os.path.join(cwd,args.paramsfile+'.json')
    # TODO: yaml
    if os.path.isfile(p1):
        paramsfile = p1
    elif os.path.isfile(p2):
        paramsfile = p2
    else:
        msg = ['Error: cannot find paramsfile (workflow parameters file) at any of the following locations:\n']
        msg += ['{}'.format(j) for j in [p1,p2]]
        sys.stderr.write(msg)
        sys.exit(-1)

    with open(paramsfile,'r') as f:
        config = json.load(f)

    with open(workflowfile, 'r') as fp:
        workflow_info = json.load(fp)

    # get the kubernetes namespace
    kube_ns = 'default'
    if args.k8s_namespace is not None and len(args.k8s_namespace)>0:
        kube_ns = args.k8s_namespace

    # verify the user has set the AWS env variables
    if not (os.environ['AWS_ACCESS_KEY_ID'] and os.environ['AWS_SECRET_ACCESS_KEY']):
        msg = 'Error: the environment variables AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set to allow the k8s cluster to access an S3 bucket for i/o.'
        sys.stderr.write(msg)
        sys.exit(-1)

    # verify the user has provided a bucket name
    if not args.s3_bucket:
        msg = 'Error: no S3 bucket specified with --s3-bucket. This must be set to allow the k8s cluster to access an S3 bucket for i/o.'
        sys.stderr.write(msg)
        sys.exit(-1)
    else:
        mah_bukkit = args.s3_bucket


    target = workflow_info['workflow_target']

    print('--------')
    print('details!')
    print('\tsnakefile: {}'.format(snakefile))
    print('\tconfig: {}'.format(workflowfile))
    print('\tparams: {}'.format(paramsfile))
    print('\ttarget: {}'.format(target))
    print('\tk8s namespace: {}'.format(kube_ns))
    print('--------')

    # Note: we comment out configfile=paramsfile below,
    # because we have problems passing files into k8s clusters.

    # run byok8s!!
    status = snakemake.snakemake(snakefile, 
                                 #configfile=paramsfile,
                                 assume_shared_fs=False,
                                 default_remote_provider='S3',
                                 default_remote_prefix=mah_bukkit,
                                 kubernetes_envvars=['AWS_ACCESS_KEY_ID','AWS_SECRET_ACCESS_KEY'],
                                 targets=[target], 
                                 printshellcmds=True,
                                 verbose = True,
                                 dryrun=args.dry_run, 
                                 forceall=args.force,
                                 kubernetes=kube_ns,
                                 config=config)

    if status: # translate "success" into shell exit code of 0
       return 0
    return 1


if __name__ == '__main__':
    main()

