import ipycytoscape

import networkx as nx
import pandas as pnd
import pickle
from importlib import resources


cache_map = None


def get_default_common(idsystem):
    if idsystem=='bigg': 
        common_list = [
            'h2o', 'h',
            'pi', 'ppi',
            'atp', 'adp', 'amp',
            'nad', 'nadh',
            'nadp', 'nadph',
        ] 
    else:
        common_list = [ 
            'cpd00001', 'cpd00067',
            'cpd00009', 'cpd00012',
            'cpd00002', 'cpd00008', 'cpd00018',
            'cpd00003', 'cpd00004',
            'cpd00006', 'cpd00005',
        ]
    return common_list



class Net(ipycytoscape.cytoscape.CytoscapeWidget):
    """
    """
    
    def __init__(self, 
        model, 
        pathway=None, module=None,
        idsystem=None,
        xminfilter=None, xmaxfilter=None, yminfilter=None, ymaxfilter=None,
        expand=600, 
        unmatched=False, common=True, clonecommon=False, recovery=False, compartments=True, include=[],
        fluxes=False, relfluxes='map', maxwidth=10,
        showgpr=False, transgpr=None,
        customxy=None,
        usemnx=False, fromchilds=False,
        mnames=False,
        kegglob=False,
        verbose=False):
        """
        
        If 'idsystem' is None, the ID system will be automatically choosen between 'bigg' and 'seed'. 
        """
        
    
        super().__init__()
        
        
        
        self.model = model
        self.idsystem = idsystem
        
        
        global cache_map
        if cache_map == None:
            with resources.path("gemmap", "mapping.gemmap_data") as fpath:
                with open(fpath, 'rb') as handler:
                    cache_map = pickle.load(handler)
        self.cache = cache_map
        
        
        
        self.pathway = pathway
        self.module = module
        
        self.xminfilter = xminfilter
        self.xmaxfilter = xmaxfilter
        self.yminfilter = yminfilter
        self.ymaxfilter = ymaxfilter
        
        
        self.expand = expand
        self.unmatched = unmatched
        self.common = common
        self.clonecommon = clonecommon
        self.recovery = recovery
        self.compartments = compartments
        self.include = include
        
        
        self.fluxes = fluxes
        self.relfluxes = relfluxes # scale edge width relatively to the bigger flux.
        self.maxwidth = maxwidth
        
        
        self.showgpr = showgpr
        self.transgpr = transgpr
        
        
        self.customxy = customxy
        
        
        self.usemnx = usemnx
        self.fromchilds = fromchilds
  
        self.mnames = mnames
        
        self.kegglob = kegglob

        self.verbose = verbose
        
        
        
        
        # initialization
        
        self._correct_user_input()
        self.mkegg, self.rkegg = self._get_map_components()
        self.minx, self.maxx, self.miny, self.maxy = self._get_extreme_pos()
        
        
        self.recovered = self._perform_recovery() if self.recovery else set()
        self._filter_recovered_by_compartment()
        
        # include has priority over recovered
        self.include = set(self.include) - self.recovered
        
        
        self.nx_repr = nx.MultiDiGraph()
        self.pos = {}
        
        self._set_tooltip_style()
        

    def _get_m_x(self, m, raw=False, kegg=False):
        """
        """
        
        if kegg:
            m_annots = [m]
        else: 
            m_annots = self._get_m_annots(m)
        
        # WARNING: we are taking just the first match!
        for i in m_annots:
            try: 
                x = self.mkegg[i]['x']
                
                # custom X;Y has priority if present
                try: x = self.customxy[m.id][0]
                except: pass
                
                if raw: return x
                else: return (x - self.minx) / (self.maxx - self.minx) * self.expand - self.expand/2 
            except: 
                continue
                
        print(m_annots)
        print("_get_m_x: Strage behaviour. Contact the developer.")
        
        
    def _get_m_y(self, m, raw=False, kegg=False):
        """
        """
        
        if kegg:
            m_annots = [m]
        else: 
            m_annots = self._get_m_annots(m)
        
        # WARNING: we are taking just the first match!
        for i in m_annots:
            try: 
                y = self.mkegg[i]['y']
                
                # custom X;Y has priority if present
                try: y = self.customxy[m.id][1]
                except: pass
                
                if raw: return y
                else: return (y - self.miny) / (self.maxy - self.miny) * self.expand - self.expand/2 
            except: 
                continue
                
        print(m_annots)
        print("_get_m_y: Strage behaviour. Contact the developer.")
        
        
    def _get_r_x(self, r, raw=False, kegg=False):
        """
        """
        
        if kegg:
            r_annots = [r]
        else:
            r_annots = self._get_r_annots(r)
        
        # WARNING: we are taking just the first match!
        for i in r_annots:
            try: 
                x = self.rkegg[i]['x']
                
                # custom X;Y has priority if present
                try: x = self.customxy[r.id][0]
                except: pass
                
                if raw: return x
                else: return (x - self.minx) / (self.maxx - self.minx) * self.expand - self.expand/2 
            except: 
                continue
        
        print(r_annots)
        print("_get_r_x: Strage behaviour. Contact the developer.")
        
        
    def _get_r_y(self, r, raw=False, kegg=False):
        """
        """
        
        if kegg:
            r_annots = [r]
        else:
            r_annots = self._get_r_annots(r)
        
        # WARNING: we are taking just the first match!
        for i in r_annots:
            try: 
                y = self.rkegg[i]['y']
                
                # custom X;Y has priority if present
                try: y = self.customxy[r.id][1]
                except: pass
                
                if raw: return y
                else: return (y - self.miny) / (self.maxy - self.miny) * self.expand - self.expand/2 
            except: 
                continue
            
        print(r_annots)
        print("_get_r_y: Strage behaviour. Contact the developer.")
        
    
    def _get_extreme_pos(self):
        """
        """
        # Determine min and max X;Y coordinates in this map.
        
        
        minx, maxx, miny, maxy = None, None, None, None

        # this map can be used also without KEGG maps:
        if self.pathway!=None :
            
            minx = min([self.mkegg[key]['x'] for key in self.mkegg.keys()])
            maxx = max([self.mkegg[key]['x'] for key in self.mkegg.keys()])
            miny = min([self.mkegg[key]['y'] for key in self.mkegg.keys()])
            maxy = max([self.mkegg[key]['y'] for key in self.mkegg.keys()])

        return minx, maxx, miny, maxy
     
    
    def _correct_user_input(self):
        """
        """
        # Correct user input.
        
        
        # 0. get the annotation system for this model
        if self.idsystem not in [None, 'bigg', 'seed']:
            self.idsystem = None
            if self.verbose: 
                print("WARNING: the ID system you specified is not 'bigg' nor 'seed'. It will be autodetected.")
        if self.idsystem == None:
            for m in self.model.metabolites:
                # get m.id without compartment 
                mid_noc = m.id.rsplit('_', 1)[0]
                
                if mid_noc == 'h2o':
                    self.idsystem = 'bigg'
                    break
                if mid_noc == 'cpd00001':
                    self.idsystem = 'seed'
                    break
        
                      
                      
        # 0bis. cache "decomposition"
        if self.cache != None:   # should never be empty. 
            self.path_to_rn_to_xy_dict = self.cache['path_to_rn_to_xy_dict']
            self.path_to_cpd_to_xy_dict = self.cache['path_to_cpd_to_xy_dict']
            self.md_to_r_dict = self.cache['md_to_r_dict']
            self.md_to_c_dict = self.cache['md_to_c_dict']
            self.path_cat = self.cache['path_cat']
            self.md_cat = self.cache['md_cat']
            self.cpd_cat = self.cache['cpd_cat']
                      
            if self.idsystem == None or self.idsystem== 'bigg':
                self.something_to_kegg_M = self.cache['bigg_to_kegg_M']
                self.something_to_kegg_R = self.cache['bigg_to_kegg_R']
                self.something_to_kegg_extended_M = self.cache['bigg_to_kegg_extended_M']
                self.something_to_kegg_extended_R = self.cache['bigg_to_kegg_extended_R']
            else:
                self.something_to_kegg_M = self.cache['seed_to_kegg_M']
                self.something_to_kegg_R = self.cache['seed_to_kegg_R']
                self.something_to_kegg_extended_M = self.cache['seed_to_kegg_extended_M']
                self.something_to_kegg_extended_R = self.cache['seed_to_kegg_extended_R']
            
            self.rn_to_rns = self.cache['rn_to_rns']
            
        
        
        # 1. pathway/module
        if self.pathway != None:
            if len(self.pathway) == 5:
                self.pathway = 'map' + self.pathway
                
        if self.module != None:
            if len(self.module) == 5:
                self.module = 'M' + self.module
            
            
        
        # 2. Common metabolites
        if self.idsystem==None or self.idsystem=='bigg': 
            common_list = get_default_common('bigg')
        else:
            common_list = get_default_common('seed')
            
        if type(self.common)==bool:
            if self.common==False: 
                self.common = []
            else: self.common = common_list
            
            
            
        # 3. compartments
        if type(self.compartments)==str: 
            self.compartments = [self.compartments]
            
        elif type(self.compartments)==bool or self.compartments==[]:
            # True or False is the same
            self.compartments = list(self.model.compartments.keys())
            
            
            
        # 4. include
        if type(self.include)==str: 
            self.include = [self.include]
            
            
        # 5. fluxes
        if type(self.relfluxes)==bool and self.relfluxes==False:
            self.relfluxes = 'no'
            
            
        # 6. GPR tranlastion table
        if type(self.transgpr) == str:
            if self.transgpr.endswith('.xlsx') or self.transgpr.endswith('.xls'):
                self.transgpr = pnd.read_excel(self.transgpr, names=['gname', 'translation'], header=None)
                
            else:
                self.transgpr = pnd.read_csv(self.transgpr, sep='\t', names=['gname', 'translation'], header=None)
                
            tmp_dict = {}
            for index, row in self.transgpr.iterrows(): 
                tmp_dict[row.gname] = row.translation.split(', ')
                if len(tmp_dict[row.gname]) == 1: # no need for a list here 
                    tmp_dict[row.gname] = tmp_dict[row.gname][0]
                    
            self.transgpr = tmp_dict
                
        elif type(self.transgpr) == dict:
            pass  # we want a dict
        elif self.transgpr == None:
            pass  # user didn't use this param
        else:
            print("WARNING: strange type for 'transgpr' parameter.")
            self.transgpr = None
            
            
            
        # 7. custom XY
        if type(self.customxy) == str:
            if self.customxy.endswith('.xlsx') or self.customxy.endswith('.xls'):
                self.customxy = pnd.read_excel(self.customxy, names=['node', 'x', 'y'], header=None)
                
            else:
                self.customxy = pnd.read_csv(self.customxy,  sep='\t', names=['node', 'x', 'y'], header=None)
                
            tmp_dict = {}
            for index, row in self.customxy.iterrows(): 
                tmp_dict[row.node] = (row.x, row.y)
        
            self.customxy = tmp_dict
            
        elif type(self.customxy) == dict:
            pass  # we want a dict
        elif self.customxy == None:
            pass  # user didn't use this param
        else:
            print("WARNING: strange type for 'customxy' parameter.")
            self.customxy = None
            
            
            
        # 8. 'fromchilds'
        if self.fromchilds == True and self.usemnx==False:
            self.usemnx = True
            
       
    def _get_map_components(self):
        """
        """
        # Get components for this map (pathway/module).
        # At the end, two dicts will be present in each istance of Net: `mkegg` and `rkegg`.
        
        
        
        
        # dict of dict for metabolites and reactions
        mkegg = {}  # structure: mkegg[cpd] = {'x': x, 'y': y, 'description': description}
        rkegg = {}  # structure: rkegg[rn] = {'x': x, 'y': y}
        
        
        # this function can be used also without KEGG maps:
        if self.pathway!=None :
            
            # user could have specified also a 'module':
            if self.module!=None: 

                # get the allowed subset of reactions and compounds in this map :
                cpd_allowed = set(self.md_to_c_dict[self.module])
                rn_allowed = set(self.md_to_r_dict[self.module])
                
                
            for cpd in self.path_to_cpd_to_xy_dict[self.pathway]:
                            
                if self.module!=None and not cpd in cpd_allowed: 
                    continue # not in this module
                
                curr_x = self.path_to_cpd_to_xy_dict[self.pathway][cpd]['x'] 
                curr_y = self.path_to_cpd_to_xy_dict[self.pathway][cpd]['y']
                
                # respect selected area:
                if self.xminfilter!=None and curr_x < self.xminfilter: continue
                if self.xmaxfilter!=None and curr_x > self.xmaxfilter: continue
                if self.yminfilter!=None and curr_y < self.yminfilter: continue
                if self.ymaxfilter!=None and curr_y > self.ymaxfilter: continue
                    
                if not cpd in mkegg.keys(): # if this compound was still missing:
                    mkegg[cpd] = {'x': curr_x, 'y': curr_y, 'description': self.cpd_cat[cpd]}
            
            
            for rn in self.path_to_rn_to_xy_dict[self.pathway]:
                
                if self.module!=None and not rn in rn_allowed: 
                    continue # not in this module
                    
                curr_x = self.path_to_rn_to_xy_dict[self.pathway][rn]['x'] 
                curr_y = self.path_to_rn_to_xy_dict[self.pathway][rn]['y']
                    
                # respect selected area ? 

                if not rn in rkegg.keys(): # if this reactions was still missing: 
                    rkegg[rn] = {'x': curr_x, 'y': curr_y}
                
            
        if self.verbose: 
            if self.module != None: 
                print("Module:", self.module, self.md_cat[self.module])
            if self.pathway != None: 
                print("Pathway:", self.pathway, self.path_cat[self.pathway])
        
        return mkegg, rkegg

    
    def _get_reacs_prods(self, r): 
        """
        """
        
        lb = r.lower_bound
        ub = r.upper_bound
        prods = r.products
        reacs = r.reactants

        if lb == -1000 and ub == 1000 and r.flux < 0:
            prods, reacs = reacs, prods
        elif lb == -1000 and ub == 0: 
            prods, reacs = reacs, prods
            
        return reacs, prods
    
 
    def _get_r_annots(self, r, justmodeled=False):
        
        try:
            r_annots1 = r.annotation['kegg.reaction']
            r_annots1 = [r_annots1] if type(r_annots1)==str else r_annots1
        except:
            r_annots1 = []
        
        
        r_annots2 = []
        if not justmodeled: 
            if   self.usemnx==True and self.fromchilds==False:
                try: r_annots2 = self.something_to_kegg_R[r.id]
                except: pass
            elif self.usemnx==True and self.fromchilds==True:
                try: r_annots2 = self.something_to_kegg_extended_R[r.id]
                except: pass
   
        r_annots = list(set(r_annots1).union(set(r_annots2)))
        
        
        r_annots3 = []
        if self.kegglob:
            for rn1 in r_annots: 
                try: extra_annots = self.rn_to_rns[rn1]
                except: continue
                
                for rn2 in extra_annots: 
                    r_annots3.append(rn2)
                    
        r_annots = list(set(r_annots).union(set(r_annots3)))
                    
        
        if r_annots == []: r_annots = None
        return r_annots

                      
    def _get_m_annots(self, m, justmodeled=False): 
        
        try: 
            m_annots1 = m.annotation['kegg.compound']
            m_annots1 = [m_annots1] if type(m_annots1)==str else m_annots1
        except:
            m_annots1 = []
                      
        
        m_annots2 = []
        # get m.id without compartment 
        mid_noc = m.id.rsplit('_', 1)[0]
        if not justmodeled:         
            if   self.usemnx==True and self.fromchilds==False:
                try: m_annots2 = self.something_to_kegg_M[mid_noc]
                except: pass
            elif self.usemnx==True and self.fromchilds==True:
                try: m_annots2 = self.something_to_kegg_extended_M[mid_noc]
                except: pass
    
        
        m_annots = list(set(m_annots1).union(set(m_annots2)))
        if m_annots == []: m_annots = None
                      
        return m_annots

                      
    def _is_mapped(self, annots, mapped_ids):
        """
        """
        # Check if at least one of the annotations provided (`annot`) is present in 
        # the selected KEGG Pathway/Module. Note: this function works both for 
        # metabolites and reactions depending on the `mapped_ids` provided. 
        
        
        for a in annots: 
            if a in mapped_ids:
                return True
        return False

    
    def _get_tooltip_paragraph(self, title, content):
        
        title = '<span style="color:khaki; font-weight: 600; font-size: 13px;">' + title + ': '+ '</span>'
        
        par = '<p ' + self.tooltip_style + '>' + title + content + '</p>'
        
        return par
    
    
    def _get_tooltip_links(self, annots, color):
        
        links = []
        for annot in annots:
            link = f'<a style="color:{color};" target="_blank" href="https://www.genome.jp/entry/{annot}">{annot}</a>'
            links.append(link)
        links = ', '.join(links)
        if links == []: links = ''
        return links
    
    
    def _mix_extra_annots(self, annots, annots_extra):
        
        if annots == None: annots = []
        if annots_extra == None: annots_extra = []
        
        links = self._get_tooltip_links(annots, 'lightblue')
        
        annots_extra = list(set(annots_extra) - set(annots))
        links_extra = self._get_tooltip_links(annots_extra, 'lightsalmon')
        
        if links != '' and links_extra != '': 
            links = links + ', ' + links_extra
        else: links = links  + links_extra
        
        
        if links == '': links = 'None'
        return links
    
    
    def _get_structs(self, m_annots, m_annots_extra):
        
        if m_annots == None: m_annots = []
        if m_annots_extra == None: m_annots_extra = []
        
        m_annots_extra = list(set(m_annots_extra) - set(m_annots))
        
        structs = []
        
        for annot in (m_annots + m_annots_extra):
            struct = f'<img src="https://www.genome.jp/Fig/compound/{annot}.gif" alt="{annot}.gif">'
            structs.append(struct)
                
        return structs
    
    
    def _get_tooltip(self, m):  
        
        tooltip = ''
        
        m_annots = self._get_m_annots(m, justmodeled=True)
        m_annots_extra = self._get_m_annots(m, justmodeled=False)
        m_matched = m_annots_extra != None and self._is_mapped(m_annots_extra, self.mkegg.keys())
        
        links = self._mix_extra_annots(m_annots, m_annots_extra)
        structs = self._get_structs(m_annots, m_annots_extra)
        
        raw_x = None
        raw_y = None
        if m_matched: 
            raw_x = self._get_m_x(m, raw=True)
            raw_y = self._get_m_y(m, raw=True)
            
        
        n_involved = len(m.reactions)
        involved = ', '.join([r.id for r in list(m.reactions)[:10]]) # first 10
        if n_involved > 10: involved = involved + f', ... ({n_involved} reactions)'
            
        tt_id = self._get_tooltip_paragraph('ID', m.id)
        tt_name = self._get_tooltip_paragraph('Name', m.name)
        tt_formula = self._get_tooltip_paragraph('Formula (charge)', f'{m.formula} ({m.charge})')
        tt_annots = self._get_tooltip_paragraph('KEGG annots', links)
        tt_coords = self._get_tooltip_paragraph('Raw coords', f'X {raw_x}, Y {raw_y}')
        #tt_annots_mnx = self._get_tooltip_paragraph('MNX annots', links_mnx)
        tt_compartment = self._get_tooltip_paragraph('Compartment', f'{m.compartment} ({self.model.compartments[m.compartment]})')
        tt_involved = self._get_tooltip_paragraph('Involved in', involved)
        tt_structs = ''.join(structs)
        
        tooltip = tt_id + tt_name + tt_formula + tt_annots + tt_coords + tt_compartment + tt_involved + tt_structs
        
        return tooltip
    
  
    def _get_r_tooltip(self, r): 
        
        tooltip = ''
        
        r_annots = self._get_r_annots(r, justmodeled=True)
        r_annots_extra = self._get_r_annots(r, justmodeled=False)
        r_matched = r_annots != None and self._is_mapped(r_annots, self.rkegg.keys())
        
        links = self._mix_extra_annots(r_annots, r_annots_extra)

        raw_x = None
        raw_y = None
        if r_matched: 
            raw_x = self._get_r_x(r, raw=True)
            raw_y = self._get_r_y(r, raw=True)
        
        tt_id = self._get_tooltip_paragraph('ID', r.id)
        tt_name = self._get_tooltip_paragraph('Name', r.name)
        tt_annots = self._get_tooltip_paragraph('KEGG annots', links)
        tt_coords = self._get_tooltip_paragraph('Raw coords', f'X {raw_x}, Y {raw_y}')
        #tt_annots_mnx = self._get_tooltip_paragraph('MNX annots', links_mnx)
        tt_bounds = self._get_tooltip_paragraph('Bounds', f'{r.lower_bound}, {r.upper_bound}')
        tt_gpr = self._get_tooltip_paragraph('GPR', self._get_gpr(r, tt=True))
        tt_flux = self._get_tooltip_paragraph('Flux', str(r.flux))
        tt_equation = self._get_tooltip_paragraph('Eq', r.reaction)
        
        tooltip = tt_id + tt_name + tt_annots + tt_coords  + tt_bounds + tt_gpr +  tt_flux + tt_equation
        
        return tooltip
    
    
    def _get_kegg_tooltip(self, cpd): 
        
        
        color = 'lightsalmon'
        link = f'<a style="color:{color};" target="_blank" href="https://www.genome.jp/entry/{cpd}">{cpd}</a>'
        
        tt_id = self._get_tooltip_paragraph('KEGG ID', link)
        
        tt_name = self._get_tooltip_paragraph('KEGG Name', self.mkegg[cpd]["description"])
        
        tt_struct = f'<img src="https://www.genome.jp/Fig/compound/{cpd}.gif" alt="{cpd}.gif">'
        
        raw_x = self._get_m_x(cpd, raw=True, kegg=True)
        raw_y = self._get_m_y(cpd, raw=True, kegg=True)
        
        tt_coords = self._get_tooltip_paragraph('Raw coords', f'X {raw_x}, Y {raw_y}')
        
        tooltip = tt_id + tt_name + tt_coords + tt_struct
        
        return tooltip
    
    
    def _set_cyto_style(self):
        
        
        self.graph.add_graph_from_json(self.structure, directed=True, multiple_edges=True)
        
        self.set_style([
            
        # Nodes:
        {'selector': 'node',
            'css': {
                'content': 'data(name)',
                'height': 20,
                'width': 20,
                'text-valign': 'center',
                'font-size': 12,
                'color': 'white',
                'text-outline-width': 2,
                'text-outline-color': 'grey',
                'background-opacity': 1,
                'background-color': 'grey',
                'shape': 'square',
                'text-wrap': 'wrap', 
        }},
        {'selector': 'node[classes="unmatched"]',
            'css': {
                'content': 'data(name)',
                'height': 20,
                'width': 20,
                'text-valign': 'center',
                'font-size': 12,
                'color': 'white',
                'text-outline-width': 2,
                'text-outline-color': 'lightgrey',
                'background-opacity': 1,
                'background-color': 'lightgrey',
                'shape': 'square',
        }},
        {'selector': 'node[classes="onlymod"]',
            'css': {
                'content': 'data(name)',
                'height': 20,
                'width': 20,
                'text-valign': 'center',
                'font-size': 12,
                'color': 'white',
                'text-outline-width': 2,
                'text-outline-color': 'grey',
                'background-opacity': 1,
                'background-color': 'grey',
                'shape': 'ellipse',
        }},
        {'selector': 'node[classes="common"]',
            'css': {
                'content': 'data(name)',
                'height': 15,
                'width': 15,
                'text-valign': 'center',
                'font-size': 12,
                'color': 'white',
                'text-outline-width': 2,
                'text-outline-color': 'burlywood',
                'background-opacity': 1,
                'background-color': 'burlywood',
                'shape': 'square',
        }},
        {'selector': 'node[classes="commononlymod"]',
            'css': {
                'content': 'data(name)',
                'height': 15,
                'width': 15,
                'text-valign': 'center',
                'font-size': 12,
                'color': 'white',
                'text-outline-width': 2,
                'text-outline-color': 'burlywood',
                'background-opacity': 1,
                'background-color': 'burlywood',
                'shape': 'ellipse',
        }},
        {'selector': 'node[classes="rn"]',
            'css': {
                'content': 'data(name)',
                'height': 12,
                'width': 12,
                'text-valign': 'center',
                'font-size': 12,
                'color': 'grey',
                'text-outline-width': 2,
                'text-outline-color': 'lightgreen',
                'background-opacity': 0,
                'background-color': 'lightgreen',
                'shape': 'ellipse',
        }},
        {'selector': 'node[classes="include"]',
            'css': {
                'content': 'data(name)',
                'height': 12,
                'width': 12,
                'text-valign': 'center',
                'font-size': 12,
                'color': 'grey',
                'text-outline-width': 2,
                'text-outline-color': 'plum',
                'background-opacity': 0,
                'background-color': 'plum',
                'shape': 'ellipse',
        }},
        {'selector': 'node[classes="recovered"]',
            'css': {
                'content': 'data(name)',
                'height': 12,
                'width': 12,
                'text-valign': 'center',
                'font-size': 12,
                'color': 'grey',
                'text-outline-width': 2,
                'text-outline-color': 'orange',
                'background-opacity': 0,
                'background-color': 'orange',
                'shape': 'ellipse',
        }},
            
        # Edges:
        {'selector': 'edge',
            'css': {
                'content': 'data(name)',
                'curve-style': 'bezier', # bezier requires directed=True in add_graph_from_json()
                'color': 'grey',
                'font-size': 12,
                'text-outline-width': 0,
                'text-outline-color': 'lightgreen',
                'line-color': 'lightgreen',
                'line-style': 'solid', # solid/dashed
                'target-arrow-shape': 'triangle',
                'target-arrow-color': 'lightgreen',
                'text-wrap': 'wrap',

        }},
        {'selector': 'edge[classes="include"]',
            'css': {
                'content': 'data(name)',
                'curve-style': 'bezier', # bezier requires directed=True in add_graph_from_json()
                'color': 'grey',
                'font-size': 12,
                'text-outline-width': 0,
                'text-outline-color': 'lightgreen',
                'line-color': 'plum',
                'line-style': 'solid', # solid/dashed
                'target-arrow-shape': 'triangle',
                'target-arrow-color': 'plum',

        }},
        {'selector': 'edge[classes="recovered"]',
            'css': {
                'content': 'data(name)',
                'curve-style': 'bezier', # bezier requires directed=True in add_graph_from_json()
                'color': 'grey',
                'font-size': 12,
                'text-outline-width': 0,
                'text-outline-color': 'lightgreen',
                'line-color': 'orange',
                'line-style': 'solid', # solid/dashed
                'target-arrow-shape': 'triangle',
                'target-arrow-color': 'orange',

        }},
        ])
        
        
    def _set_fba_edge_style(self):
        
        # update with FBA results:
        
        
        
        
        # get the higher flux in order ot scale the edge width:
        all_fluxes = []
        if  self.relfluxes == 'map':
                for source_id, target_id, attribs in self.nx_repr.edges(data=True):
                    all_fluxes.append(abs(attribs['flux']))  # could be negative !
        
        elif self.relfluxes == 'model' : 
            for r in self.model.reactions:
                all_fluxes.append(abs(r.flux))  # could be negative !
                
        max_flux = max(all_fluxes)
        
            
        
        fba_style = []
        for source_id, target_id, attribs in self.nx_repr.edges(data=True):
            
            curr_id = attribs['edge_id']
            curr_flux = abs(attribs['flux'])  # could be negative !
            curr_linestyle = 'dashed' if curr_flux==0 else 'solid'
            
            if self.relfluxes != 'no': 
                curr_width = curr_flux / max_flux * self.maxwidth
            else:
                curr_width = curr_flux
            
            # make visible edges that are too thin: 
            if curr_width < 1: curr_width = 1
            
            
            fba_style.append({
                'selector': f'edge[id="{curr_id}"]',
                    'css': { 
                        'width': curr_width,
                        'line-style': curr_linestyle,
                        'line-dash-pattern': [3, 6],
                }}
            )
            
        self.set_style( self.get_style() + fba_style)   
        
        
    def get_matched_m(self): 
        """
        """
        # Get the list of modeled metabolites having KEGG annotation and
        # involved in the selected KEGG Pathway/Module. 
        # The list will be empty if no KEGG Pathway/Module is selected.
        
        
        # 'plain coverage' lists: 
        matched_m = []
        # this map can be used also without KEGG maps:
        if self.pathway != None:
            for m in self.model.metabolites:
                
                annots = self._get_m_annots(m)
                matched = annots != None and self._is_mapped(annots, self.mkegg.keys())
                if matched: 
                    matched_m.append(m.id)
                    
        return matched_m
    
    
    def get_matched_r(self): 
        """
        """
        # Get the list of modeled reactions having KEGG annotation and
        # involved in the selected KEGG Pathway/Module. 
        # The list will be empty if no KEGG Pathway/Module is selected. 
        
        
        # 'plain coverage' lists: 
        matched_r = []
        # this map can be used also without KEGG maps:
        if self.pathway != None:
            for r in self.model.reactions:
                
                annots = self._get_r_annots(r)
                matched = annots != None and self._is_mapped(annots, self.rkegg.keys())
                if matched: 
                    matched_r.append(r.id)
                    
        return matched_r
    
    
    def _perform_recovery(self):
        """
        """
        # Try to put in the map reactions that are without KEGG annotation but
        # made up of metabolites that are all KEGG annotated.
        
        
        recovered = set()
        
        if self.recovery == True:
            
            for r in self.model.reactions:
                
                # Check if the reaction is already annotated.
                # In this case, it doesn't make sense to check its metabolites. 
                r_annots = self._get_r_annots(r)
                r_matched = r_annots != None and self._is_mapped(r_annots, self.rkegg.keys())
                if r_matched:
                    continue 
                
                involved = set([m.id for m in r.metabolites])
                matches = []
                
                
                for mid in involved:
                    
                    if self._is_common(mid): continue  # !!!!!!!!!!!!!!!!!!!!
                    
                    m = self.model.metabolites.get_by_id(mid)
                    
                    m_annots = self._get_m_annots(m)
                    m_matched = m_annots != None and self._is_mapped(m_annots, self.mkegg.keys())
                    
                    matches.append(m_matched)
                    
                    
                if all(matches) and matches != []:  # WARNING: all([]) is True
                    if self.verbose: print("Recovered", r.id, r.reaction)
                    recovered.add(r.id)
        return recovered
    
    
    def _is_common(self, mid): 
        
        # remove compartment information: 
        mid_noc = mid.rsplit('_', 1)[0]
        return mid_noc in self.common
    
    
    def _filter_recovered_by_compartment(self):
        
        to_remove = set()
        for rid in self.recovered: 
            
            r = self.model.reactions.get_by_id(rid)
            
            for m in r.metabolites: 
                if m.compartment  not in self.compartments:
                    
                    to_remove.add(rid)
                    break
        
        self.recovered = self.recovered - to_remove
                    
    
    def _set_tooltip_style(self):
        
        self.tooltip_style = 'style="' + \
            'color: white !important;' + \
            'font-family: Arial !important;' + \
            'font-size: 12px !important;' + \
            'font-weight: 600 !important;' + \
            'line-height: 16px !important;' + \
            'margin-block-end: 0px !important' + \
            '"'
        
    
    def _get_gpr(self, r, tt=False):
        
        gpr = r.gene_reaction_rule
        
        if self.transgpr != None: 
            # insert spaces to facilitate gene name replacement
            gpr = ' ' + gpr + ' '
            gpr = gpr.replace('(', '( ')
            gpr = gpr.replace(')', ' )')
            
            
            
                    
            
            if type(self.transgpr) == dict: 
                for key in self.transgpr.keys():
                    translation = self.transgpr[key]
                    if type(translation) == list:
                        translation = '( ' + ' or '.join(translation) + ' )'
                    gpr = gpr.replace(' ' + key + ' ', ' ' + translation + ' ')
                    
                    
            # restore previous spacing
            gpr = gpr[1:-1]
            gpr = gpr.replace('( ', '(')
            gpr = gpr.replace(' )', ')')
        
        # colour ORs and ANDs to improve the tooltip:
        if tt:
            gpr = gpr.replace(' and ', '<span style="color:yellowgreen;">' + ' and ' + '</span>')
            gpr = gpr.replace(' or ', '<span style="color:orchid;">' + ' or ' + '</span>')
        
        return gpr
  
    
    def _strip_compartment(self, label): 
        
        putative_comp = label.rsplit('_', 1)[1]
        if putative_comp in self.model.compartments.keys():
            # "+1" is for taking into account the '_', eg "rxn00459_c0".
            label = label[ : -(len(putative_comp) +1)]
            
        return label
    
    
    def _get_reaction_label(self, r):
        
        label = r.id
        
        if self.idsystem=='seed':
            label = self._strip_compartment(label)
            
        
        # determine GPR if requested
        if self.showgpr:
            gpr = self._get_gpr(r)
            if len(gpr) > 20:
                gpr = gpr[:17] + '...'
            label = label + '\n' + gpr

        return label
    
    
    def _get_metabolite_label(self, m):
        
        if self.mnames: 
            
            label = m.name
            
            if self.idsystem=='seed':
                label = self._strip_compartment(label)
            
            
            if len(label) > 10:
                label = label[:10] + '...'
                
        else:
            label = m.id
            
        return label