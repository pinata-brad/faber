from faber import *
import yaml
import logging
import re 
import os

logger = logging.getLogger(__name__)

def show_node(node):
    node_display=f"""
    ** NAME:   {node['function'].__name__}
    ** INPUT:  {node['inputs']}
    ** OUTPUT: {node['outputs']}
    ** TAGS:   {node['tags']}
    """
    return node_display

def trace_dependencies(pipeline,initial_state):
    dt={
        'start':{},
        'inputs':{},
        'created':{},
    }
    for i in list(initial_state):
        dt['start'][i]=0

    for i,p in reversed(list(enumerate(pipeline))):
        for j in p['inputs']:
            dt['inputs'][j] = i
        for j in p['outputs']:
            dt['created'][j] = i
    dt['created'].update(dt['start'])

    for k in dt['inputs']:
        if k in list(dt['created']):
            if dt['created'][k] >= dt['inputs'][k]:
                print(f'{k} is not in state and will not be created by this pipeline')
        else:
            print(f'{k} is not in state and will not be created by this pipeline')

def build_catalog(state={}, path=f'{os.getcwd()}/conf'):
    """
    read in yaml files into state and catalog
    """
    try:
        state.update({'user': os.environ['USER']})
    except:
        pass
    catalog={}
    fnames=[]
    for root, _, fname in os.walk(path):
        for f in fname:
            if os.path.splitext(f)[1] == '.yaml':
                fnames.append(os.path.join(root, f))
            else:
                pass
            
    fnames=[f for f in fnames if 'ipynb' not in f]
    logger.warning(f'files to load: {fnames}')
    
    file = [x for x in fnames if 'config/config.yaml' in x][0]
    print(file)
    if file in fnames:
        t=yaml.load(open(file), Loader=yaml.FullLoader)
        state.update(t)
        fnames.remove(file)
        
    for tfile in fnames: 
        print(tfile)
        if 'config' in os.path.dirname(tfile):
            s=format_yml_str(open(tfile).read(), state)
            t=yaml.load(s, Loader=yaml.FullLoader)
            state.update(t)
        else:
            continue

    for cfile in fnames:
        if 'config' in os.path.dirname(cfile):
            continue
        else:
            s=format_yml_str(open(cfile).read(), state)
            t=yaml.load(s, Loader=yaml.FullLoader)
            catalog.update(t)


    return state, catalog

def replacer(s, index_pair, new_val):
    """
    """
    s1 = s[:index_pair[0][0]]
    s2 = s[index_pair[1][1]:]
    new_s = f'''{s1}{new_val}{s2}'''
    return new_s

def format_yml_str(s, state):
    """
    """
    locs = [x for x in zip([(a.start(), a.end()) for a in list(re.finditer('{{',s))], [(a.start(), a.end()) for a in list(re.finditer('}}',s))] )]
    tot = len(locs)
    i=0
    while i<tot:
        locs = [x for x in zip([(a.start(), a.end()) for a in list(re.finditer('{{',s))], [(a.start(), a.end()) for a in list(re.finditer('}}',s))] )]
        paras_l = [s[loc[0][1]:loc[1][0]] for loc in locs]
        v=paras_l[0]
        s=replacer(s, locs[0], state[v])
        i+=1
    return s

def show_pipeline(pipeline):
    for i, p in enumerate(pipeline):
        print('****************')
        print(f'** NODE: {i+1}')
        print(show_node(p))




















