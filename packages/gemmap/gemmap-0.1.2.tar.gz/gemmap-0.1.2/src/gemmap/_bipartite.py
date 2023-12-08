from ._netcore import Net


import networkx as nx
import warnings


class Bi(Net):
    """
    """
    
    
    def __init__(self, *args, **kwargs):
    
        super().__init__(*args, **kwargs)
        
        self._plot_bipartite()
        
    
    def _plot_bipartite(self):
        
        
        self.structure = {'nodes': [], 'edges': []}
        self._get_map_nx()
        
        
        if self.verbose: print(self.nx_repr)
        
        
        # draw nodes:
        for node_id, attribs in self.nx_repr.nodes(data=True):
            
            if attribs['rnclass'] == False:
                
                if len(node_id)==6 and node_id.startswith('C'): 
                    self._draw_kegg_met(node_id)
                else: 
                    self._draw_modeled_met(node_id, 
                        onlymod = attribs['onlymod'],
                        common = attribs['common'])
        
            else: 
                self._draw_modeled_reac(node_id)
        
        
        # draw edges:
        for source_id, target_id, attribs in self.nx_repr.edges(data=True):
            self._draw_edge(source_id, target_id, 
                # attributes:
                attribs['rid'],            
                attribs['recovered'],
                attribs['to_include'],
                attribs['edge_id'],
                )
        
                    
        self._set_cyto_style()
        if self.fluxes: self._set_fba_edge_style()
        
        
        self.set_layout(name='preset')
        
        
    def _get_map_nx(self): 
        """
        """
        # Get a networkx representation of the current map (pathway/module). 
        
        self.added_m = set()
        self.added_m_annots = set()
        self.added_edges = set()
        
        
        res = self.model.optimize()
        for r in self.model.reactions:
            
            
            r_annots = self._get_r_annots(r)
            r_matched = r_annots != None and self._is_mapped(r_annots, self.rkegg.keys())
            
            
            # main reaction filter
            is_recovered = r.id in self.recovered
            to_include = r.id in self.include
            if (r_matched == False and 
                is_recovered == False and 
                to_include == False ):
                continue
            
            
            reacs, prods = self._get_reacs_prods(r)
            
            
            for mr in reacs:
                
                for mp in prods:
                    
                    # main metabolite filter
                    if (mr.compartment not in self.compartments or 
                        mp.compartment not in self.compartments ):
                        continue
                        
                        
                    mr_cloneid = None
                    mp_cloneid = None
                    if self.clonecommon == False:
                        if (self._is_common(mr.id) or
                            self._is_common(mp.id) ):
                            continue
                    else:
                        if self._is_common(mr.id):
                            mr_cloneid = mr.id + '_____gemmapcommon_____' + r.id
                        
                        if self._is_common(mp.id):
                            mp_cloneid = mp.id + '_____gemmapcommon_____' + r.id
                    
        
        
                    
                    if mr.id not in self.added_m: 
                        self._add_m_node(mr, mr_cloneid)
                    
                    if mp.id not in self.added_m: 
                        self._add_m_node(mp, mp_cloneid)
                    
                    
                    self._add_r_node(r)
                    

                    self._add_edges(mr, mp, r, mr_cloneid, mp_cloneid)
                    
                    
                    
        if self.unmatched: 
            self._add_unmatched()
            
        
        
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            # Espacially with 'clonecommon' activated, it could raise something like:
            # "RuntimeWarning: Warning: Max. iterations (9900) reached on graph"
            
            # A parameter in https://graphviz.org/docs/layouts/neato/
            # can be applied to Graphs, Nodes or Edges. We can set it in the 
            # node/edge networkx attributes or prepening a 'G' if applied globally. 
            self.pos = nx.nx_agraph.graphviz_layout(
                self.nx_repr,
                prog='neato',
                args='-Ginputscale=0 -Gmode="KK"'
            )
            
        
        # to reset warning behaviour: 
        warnings.resetwarnings()
       
    
    def _add_m_node(self, m, cloneid):
        
        
        is_common = True if self._is_common(m.id) else False
        
        
        mid = m.id
        if cloneid != None: mid = cloneid
        

        
        
        self.added_m.add(mid)    
        
        m_annots = self._get_m_annots(m)
        m_matched = m_annots != None and self._is_mapped(m_annots, self.mkegg.keys())
        
        
        
        
        
        if m_matched:

            init_x = self._get_m_x(m)
            init_y = self._get_m_y(m)
            
            # these attribs are automatically passed to graphviz_layout(): 'pos', 'pin'
            
            self.nx_repr.add_node(mid ,
                rnclass = False,
                onlymod = False, 
                common = is_common, 
                pos = f'{init_x},{init_y}', 
                pin = 'true')

        else: 
            self.nx_repr.add_node(mid, 
                rnclass = False,
                onlymod = True,
                common = is_common, )
        
        if m_annots != None:
            for annot in m_annots: 
                self.added_m_annots.add(annot)
    
    
    def _add_r_node(self, r):
        
        
        r_annots = self._get_r_annots(r)
        r_matched = r_annots != None and self._is_mapped(r_annots, self.rkegg.keys())
        
            
        if r_matched:

            init_x = self._get_r_x(r)
            init_y = self._get_r_y(r)
            
            # these attribs are automatically passed to graphviz_layout(): 'pos', 'pin'
            self.nx_repr.add_node(r.id,
                rnclass = True,
                onlymod = False,
                pos = f'{init_x},{init_y}', 
                pin = 'true')
            
        else:
            self.nx_repr.add_node(r.id, 
                rnclass = True, 
                onlymod = True)
                            
    
    def _add_edges(self, mr, mp, r, mr_cloneid, mp_cloneid):
        
        
        is_recovered = r.id in self.recovered
        to_include = r.id in self.include
        
        
        mrid = mr.id
        if mr_cloneid != None: mrid = mr_cloneid
        mpid = mp.id
        if mp_cloneid != None: mpid = mp_cloneid
        
        edge_id = f'M_{mrid}-->R_{r.id}'
        
        if edge_id not in self.added_edges: 
        
            # these attribs are automatically passed to graphviz_layout(): 'len'
            self.nx_repr.add_edge(mrid, r.id, 
                # attributes:
                rid = r.id,
                recovered = is_recovered,
                to_include = to_include,
                edge_id = edge_id,
                flux = r.flux,  # get FBA data
                len='1.00',
            )
            
            self.added_edges.add(edge_id)
        
        
        edge_id = f'R_{r.id}-->M_{mpid}'
        
        if edge_id not in self.added_edges: 
        
            # these attribs are automatically passed to graphviz_layout(): 'len'
            self.nx_repr.add_edge(r.id, mpid,  
                # attributes: 
                rid = r.id,
                recovered = is_recovered,
                to_include = to_include,
                edge_id = edge_id,
                flux = r.flux,  # get FBA data
                len='1.00',
            )
            
            self.added_edges.add(edge_id)
            
    
    def _add_unmatched(self):
        
        for cpd in self.mkegg.keys(): 
            if cpd not in self.added_m_annots:
                
                init_x = self._get_m_x(cpd, kegg=True)
                init_y = self._get_m_y(cpd, kegg=True)
                
                self.added_m.add(cpd)
                
                # these attribs are automatically passed to graphviz_layout(): 'pos', 'pin'
                self.nx_repr.add_node(cpd,
                    rnclass = False, 
                    pos = f'{init_x},{init_y}', 
                    pin = 'true')
        
    
    def _draw_kegg_met(self, cpd): 


        self.structure['nodes'].append({ 
        'position': {
             'x': self.pos[cpd][0],
             'y': self.pos[cpd][1]
        } , 
        'data': { 
            'classes': 'unmatched',
            'id': cpd, 
            'name': self.mkegg[cpd]['description'][:15] + '...', 
            'tooltip': self._get_kegg_tooltip(cpd), 
        }
        })
        
        
    def _draw_modeled_met(self, mid, onlymod, common):
        
        
        
        modelid = mid
        if self.clonecommon and common:
            modelid = mid.split('_____gemmapcommon_____')[0]
            
         
        
        m = self.model.metabolites.get_by_id(modelid)

        
        metclass = ''
        if common: metclass = 'common'
        if onlymod: metclass += 'onlymod'
        
          
        node_name = self._get_metabolite_label(m)
        
        
        self.structure['nodes'].append({ 
        'position': {
             'x': self.pos[mid][0],
             'y': self.pos[mid][1]
        } , 
        'data': { 
            'classes': metclass,
            'id': mid, 
            'name': node_name, 
            'tooltip': self._get_tooltip(m),   
        }
        })
    
    
    def _draw_modeled_reac(self, rid):
        
        
        r = self.model.reactions.get_by_id(rid)
        
        is_recovered = r.id in self.recovered
        to_include = r.id in self.include
        
        
        rnclass = 'rn'
        if to_include: rnclass = 'include'
        elif is_recovered: rnclass = 'recovered'
        
        
        name = self._get_reaction_label(r)
        
        
        self.structure['nodes'].append({ 
        'position': {
             'x': self.pos[r.id][0],
             'y': self.pos[r.id][1],
        } , 
        'data': { 
            'classes': rnclass,
            'id': r.id, 
            'name': name, 
            'tooltip': self._get_r_tooltip(r), 
        }
        })
              
            
    def _draw_edge(self, source_id, target_id, rid, is_recovered, to_include, edge_id):
        
        
        r = self.model.reactions.get_by_id(rid)
        
        
        edge_class = None
        if to_include: edge_class = 'include'
        elif is_recovered: edge_class = 'recovered'
        
        
        self.structure['edges'].append({ 
        'data': { 
            'classes': edge_class,
            'id': edge_id, 
            'source': source_id, 
            'target': target_id, 
            'name': None,
            'tooltip': self._get_r_tooltip(r),
        }
        })
        
        
    
    
            