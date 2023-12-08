import copy
import pickle
from importlib import resources


cache_annot = None



def get_dbs(model, alsoreturn=False):
    
    m_annotations = set()
    for m in model.metabolites: 
        for a in m.annotation.keys():
            m_annotations.add(a)
    m_len = len(m_annotations)
    m_annotations = sorted(m_annotations)
    m_annotations= ', '.join(m_annotations)
    print('\033[1m' +  f"M ({m_len}):   " + '\033[0m', str(m_annotations))
    
    r_annotations = set()
    for r in model.reactions: 
        for a in r.annotation.keys():
            r_annotations.add(a)
    r_len = len(r_annotations)
    r_annotations = sorted(r_annotations)
    r_annotations= ', '.join(r_annotations)
    print('\033[1m' +  f"R ({r_len}):   " + '\033[0m', str(r_annotations))
    
    if alsoreturn: return m_annotations, r_annotations
    else: return None



def _boost_annotations(x, something_to_others, mrswitch='r', overwrite=False, extraverbose=False): 
    """ 
    """
    #  Works both for metabolites and reactions.
    if mrswitch=='r': 
        mrid = x.id
        
        # correct for ModelSEED reaction ids: 
        if   mrid.startswith('rxn') and mrid[-3]=='_':  # for example "rxn11567_c0"
            mrid = mrid[ : -3]
    else: 
        mrid = x.id.rsplit('_', 1)[0]  # remove compartment

    
    cnt = 0
    if mrid in something_to_others.keys(): 
    
        # get the full annotations provided by metanetx
        full_annots = something_to_others[mrid]

        
        # format model's annotations as set: 
        if not overwrite: 
            for annot in x.annotation.keys():

                if type(x.annotation[annot]) == str: 
                    x.annotation[annot] = set([x.annotation[annot]])
                elif type(x.annotation[annot]) == list: 
                    x.annotation[annot] = set(x.annotation[annot])
                else:
                    print("WARNING: Found strange annotation type:")
                    print(type(x.annotation[annot]))
                    print(x.annotation[annot])
                    return None
        else: 
            for annot in x.annotation.keys():
                x.annotation[annot] = set()

        
        # iterate through variuos databases provided by metanetx: 
        for db in full_annots.keys():

            if db not in x.annotation.keys():
                x.annotation[db] = set()
                if extraverbose: print(f'INFO: {x.id}: added new db {db}!')
            
            for annot in full_annots[db]:
                if annot not in x.annotation[db]:
                    x.annotation[db].add(annot)
                    
                    cnt += 1
                    if extraverbose: print(f'INFO: {x.id}: added {annot} ({db})')


        # re-format annotations:
        for db in x.annotation.keys():
            x.annotation[db] = list(x.annotation[db]) 
            

    return x.annotation, cnt


def pimp_my_model(model, copyfirst=False, fromchilds=False, overwrite=False, verbose=True):
    """
    """
     

    #  Much more slow if copyfirst==True
    if copyfirst:
        if verbose: print("Creating a copy of your model... ", end='', flush=True)
        # model2 = model.copy()
        # model.copy() doesn't work for metabolites.
        # we replace it with the slower copy.deepcopy()
        model = copy.deepcopy(model)
        if verbose: print('OK.', flush=True)
    
    
    if verbose: print("Autodetecting ID system... ", end='', flush=True)
    # autodetect ID system looking for water in cytosol
    id_sys = None
    for m in model.metabolites:
        # remove cytosol annot
        mid = m.id.rsplit('_', 1)[0]
        if mid == 'h2o': 
            id_sys = 'bigg'
            break
        elif mid == 'cpd00001':
            id_sys = 'seed'
            break
    if verbose: print(f'"{id_sys}" detected.', flush=True)
    if id_sys == None: id_sys = 'bigg'
    
    
    
    if verbose: print("Loading MetaNetX... ", end='', flush=True)
    global cache_annot
    if cache_annot == None:
        with resources.path("gemmap", "annotation.gemmap_data") as fpath:
            with open(fpath, 'rb') as handler:
                cache_annot = pickle.load(handler)
    # get the right dictionary
    something_to_others_M = None
    something_to_others_extended_M = None
    something_to_others_R = None
    something_to_others_extended_R = None
    if id_sys == 'bigg':
        if not fromchilds:
            something_to_others_M = cache_annot['bigg_to_others_M']
            something_to_others_R = cache_annot['bigg_to_others_R']
        else:
            something_to_others_extended_M = cache_annot['bigg_to_others_extended_M']
            something_to_others_extended_R = cache_annot['bigg_to_others_extended_R']
    elif id_sys == 'seed': 
        if not fromchilds:
            something_to_others_M = cache_annot['seed_to_others_M']
            something_to_others_R = cache_annot['seed_to_others_R']
        else:
            something_to_others_extended_M = cache_annot['seed_to_others_extended_M']
            something_to_others_extended_R = cache_annot['seed_to_others_extended_R']
    if verbose: print("OK.", flush=True)
    
    

    m_cnt = 0
    r_cnt = 0
    
    if verbose: print("Annotating metabolites... ", end='', flush=True)
    # boost annotations!     
    for m in model.metabolites:
        if not fromchilds: 
            m.annotation, cnt = _boost_annotations(m, something_to_others_M, 'm', overwrite)
        else: 
            m.annotation, cnt = _boost_annotations(m, something_to_others_extended_M, 'm', overwrite)
        m_cnt = m_cnt + cnt
    if verbose: print(f'{m_cnt} new annots added.', flush=True)
    if verbose: print("Annotating reactions... ", end='', flush=True)
    for r in model.reactions:
        if not fromchilds: 
            r.annotation, cnt = _boost_annotations(r, something_to_others_R, 'r', overwrite)
        else: 
            r.annotation, cnt = _boost_annotations(r, something_to_others_extended_R, 'r', overwrite)
        r_cnt = r_cnt + cnt
    if verbose: print(f'{r_cnt} new annots added.', flush=True)    
        
        
        
    if copyfirst: return model
    else: return None