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

    descr = 'byok8s: run snakemake workflows on your own kubernetes cluster', 
    usg = '''byok8s -w <workflow> -p <parameters> [<target>]

byok8s: run snakemake workflows on your own kubernetes cluster, using the given workflow name & parameters file.

'''

    parser = argparse.ArgumentParser(
            prog = _program, 
            description=descr,
            usage = usg
    )

    parser.add_argument('workflowfile')
    parser.add_argument('paramsfile')

    parser.add_argument('-s', '--snakefile', default='Snakefile', help='Relative path to Snakemake Snakefile')
    parser.add_argument('-k', '--kubernetes-namespace', default='default', help='Namespace of Kubernetes cluster')
    parser.add_argument('-n', '--dry-run', action='store_true', help='Do a dry run of the workflow commands (no commands executed)')
    parser.add_argument('-f', '--force', action='store_true', help='Force Snakemake rules to be re-run')
    args = parser.parse_args(sysargs)

    # first, find the Snakefile
    s1 = os.path.join(cwd,args.snakefile)
    s2 = os.path.join(cwd,'Snakefile')
    if os.path.isfile(s1):
        # user has provided a relative path
        # to a Snakefile. top priority.
        snakefile = os.path.join(cwd,args.snakefile)

    elif os.path.isfile(s2):
        # user did not specify a Snakefile,
        # but we found a file called Snakefile
        # in the current working directory.
        snakefile = os.path.join(cwd,'Snakefile')

    else:
        msg = ['Error: cannot find Snakefile at any of the following locations:\n']
        msg += ['{}'.format(j) for j in [s1,s2]]
        sys.stderr.write(msg)
        sys.exit(-1)

    # next, find the workflow config file
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

    # next, find the workflow params file
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

    with open(workflowfile, 'rt') as fp:
        workflow_info = json.load(fp)

    # get the kubernetes namespace
    kube_ns = 'default'
    if args.kubernetes_namespace is not None and len(args.kubernetes_namespace)>0:
        kube_ns = args.kubernetes_namespace

    target = workflow_info['workflow_target']

    print('--------')
    print('details!')
    print('\tsnakefile: {}'.format(snakefile))
    print('\tconfig: {}'.format(workflowfile))
    print('\tparams: {}'.format(paramsfile))
    print('\ttarget: {}'.format(target))
    print('\tk8s namespace: {}'.format(kube_ns))
    print('--------')

    # run byok8s!!
    status = snakemake.snakemake(snakefile, 
                                 #configfile=paramsfile,
                                 assume_shared_fs=False,
                                 default_remote_provider='S3Mocked',
                                 #default_remote_provider='S3',
                                 #default_remote_prefix='cmr-smk-0123',
                                 #kubernetes_envvars=['AWS_ACCESS_KEY_ID','AWS_SECRET_ACCESS_KEY'],
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

