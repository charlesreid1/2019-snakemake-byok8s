"""
Command line interface driver for snakemake workflows
"""
import argparse
import os.path
import snakemake
import sys
import pprint
import json

from . import _program


thisdir = os.path.abspath(os.path.dirname(__file__))
parentdir = os.path.join(thisdir,'..')
cwd = os.getcwd()

def main(sysargs = sys.argv[1:]):

    parser = argparse.ArgumentParser(prog = _program, description='byok8s: run snakemake workflows on your own kubernetes cluster', usage='''byok8s <workflow> <parameters> [<target>]

byok8s: run snakemake workflows on your own kubernetes cluster, using the given workflow name & parameters file.

''')

    parser.add_argument('-w', '--workflowfile', action='store_true')
    parser.add_argument('-p', '--paramsfile', action='store_true')

    parser.add_argument('-k', '--kubernetes-namespace', action='store_true')

    parser.add_argument('-n', '--dry-run', action='store_true')
    parser.add_argument('-f', '--force', action='store_true')
    args = parser.parse_args(sysargs)

    # first, find the Snakefile
    snakefile_this      = os.path.join(thisdir,"Snakefile")
    if os.path.exists(snakefile_this):
        snakefile = snakefile_this
    else:
        msg = 'Error: cannot find Snakefile at any of the following locations:\n'
        msg += '{}\n'.format(snakefile_this)
        sys.stderr.write(msg)
        sys.exit(-1)

    # next, find the workflow config file
    workflowfile = None
    w1 = os.path.join(cwd,args.workflowfile)
    w2 = os.path.join(cwd,args.workflowfile+'.json')
    # NOTE:
    # handling yaml would be nice
    if os.path.exists(w1) and not os.path.isdir(w1):
        workflowfile = w1
    elif os.path.exists(w2) and not os.path.isdir(w2):
        workflowfile = w2

    if not workflowfile:
        msg = 'Error: cannot find workflowfile {} or {} '.format(w1,w2)
        msg += 'in directory {}\n'.format(cwd)
        sys.stderr.write(msg)
        sys.exit(-1)

    # next, find the workflow params file
    paramsfile = None
    p1 = os.path.join(cwd,args.paramsfile)
    p2 = os.path.join(cwd,args.paramsfile+'.json')
    if os.path.exists(p1) and not os.path.isdir(p1):
        paramsfile = p1
    elif os.path.exists(p2) and not os.path.isdir(p2):
        paramsfile = p2

    if not paramsfile:
        msg = 'Error: cannot find paramsfile {} or {} '.format(p1,p2)
        msg += 'in directory {}\n'.format(cwd)
        sys.stderr.write(msg)
        sys.exit(-1)

    with open(workflowfile, 'rt') as fp:
        workflow_info = json.load(fp)

    # get the kubernetes namespace
    kube_ns = 'default'
    if args.kubernetes_namespace not None and len(args.kubernetes_namespace)>0:
        kube_ns = args.kubernetes_namespace

    target = workflow_info['workflow_target']
    config = dict()

    print('--------')
    print('details!')
    print('\tsnakefile: {}'.format(snakefile))
    print('\tconfig: {}'.format(workflowfile))
    print('\tparams: {}'.format(paramsfile))
    print('\ttarget: {}'.format(target))
    print('\tk8s namespace: {}'.format(kube_ns))
    print('--------')

    # run byok8s!!
    status = snakemake.snakemake(snakefile, configfile=paramsfile,
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

