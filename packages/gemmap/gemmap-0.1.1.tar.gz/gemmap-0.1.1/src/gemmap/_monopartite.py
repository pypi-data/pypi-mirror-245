from ._netcore import Net


import networkx as nx



class Mono(Net):
    """
    """
    
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs) 
        
        self._plot_monopartite() 
        
    
    def _plot_monopartite(self):
        
        
        self.structure = {'nodes': [], 'edges': []}
        self._get_map_nx()
        
        
        if self.verbose: print(self.nx_repr)
        
        
        # draw nodes: 
        for node_id, attribs in self.nx_repr.nodes(data=True):
            
            if len(node_id)==6 and node_id.startswith('C'): 
                self._draw_kegg_node(node_id)
            else: 
                self._draw_modeled_node(node_id, onlymod=attribs['onlymod'])
        
        
        # draw edges: 
        for source_id, target_id, attribs in self.nx_repr.edges(data=True):
            self._draw_edge(source_id, target_id, 
                # attributes:
                attribs['rid'], 
                attribs['recovered'],
                attribs['to_include'],
                attribs['edge_id'])
                    
                
        self._set_cyto_style()
        if self.fluxes: self._set_fba_edge_style()
        
        
        self.set_layout(name='preset')
        
        
    def _get_map_nx(self):
        """
        """
        # Get a networkx representation of the current map (pathway/module). 

        self.added_m = set()
        self.added_m_annots = set()
        
        
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
                    if (self._is_common(mr.id) or
                        self._is_common(mp.id) or
                        mr.compartment not in self.compartments or 
                        mp.compartment not in self.compartments ):
                        continue
                   
                    
                    if mr.id not in self.added_m:
                        self._add_node(mr)
                        
                    if mp.id not in self.added_m:
                        self._add_node(mp)
                    
                    
                    # these attribs are automatically passed to graphviz_layout(): 'len'
                    self.nx_repr.add_edge(mr.id, mp.id, 
                        # attributes: 
                        rid = r.id, 
                        recovered = is_recovered,
                        to_include = to_include,
                        edge_id = f'M_{mr.id}-->M_{mp.id}',
                        flux = r.flux, # get FBA data
                        len='1.00',
                    )
                    
        
        if self.unmatched: 
            self._add_unmatched()
                
        
        # A parameter in https://graphviz.org/docs/layouts/neato/
        # can be applied to Graphs, Nodes or Edges. We can set it in the 
        # node/edge networkx attributes or prepening a 'G' if applied globally. 
        self.pos = nx.nx_agraph.graphviz_layout(
            self.nx_repr,
            prog='neato',
            args='-Ginputscale=0 -Gmode="KK"'
        )
        
    
    def _add_node(self, m):
        
        self.added_m.add(m.id)

        m_annots = self._get_m_annots(m)
        m_matched = m_annots != None and self._is_mapped(m_annots, self.mkegg.keys())

        if m_matched:

            init_x = self._get_m_x(m)
            init_y = self._get_m_y(m)
            
            # these attribs are automatically passed to graphviz_layout(): 'pos', 'pin'
            self.nx_repr.add_node(m.id, 
                onlymod = False, 
                pos = f'{init_x},{init_y}', 
                pin = 'true')
            
        else: 
            self.nx_repr.add_node(m.id, 
                onlymod = True)
        
        if m_annots != None: 
            for annot in m_annots: 
                self.added_m_annots.add(annot)
    
    
    def _add_unmatched(self):
        
        for cpd in self.mkegg.keys(): 
            if cpd not in self.added_m_annots:
                
                init_x = self._get_m_x(cpd, kegg=True)
                init_y = self._get_m_y(cpd, kegg=True)
                
                self.added_m.add(cpd)
                
                # these attribs are automatically passed to graphviz_layout(): 'pos', 'pin'
                self.nx_repr.add_node(cpd, 
                    pos=f'{init_x},{init_y}', 
                    pin='true')
    
    
    def _draw_kegg_node(self, cpd): 


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
    
    
    def _draw_modeled_node(self, mid, onlymod):
        
        
        m = self.model.metabolites.get_by_id(mid)
        
        node_name = self._get_metabolite_label(m)
        
        self.structure['nodes'].append({ 
        'position': {
             'x': self.pos[m.id][0],
             'y': self.pos[m.id][1]
        } , 
        'data': { 
            'classes': 'onlymod' if onlymod else None,
            'id': m.id, 
            'name': node_name, 
            'tooltip': self._get_tooltip(m),   
        }
        })

    
    def _draw_edge(self, mr_id, mp_id, r_id, is_recovered, to_include, edge_id):
        
        mr = self.model.metabolites.get_by_id(mr_id)
        mp = self.model.metabolites.get_by_id(mp_id)
        r  = self.model.reactions.get_by_id(r_id)
        
        
        edge_class = None
        if to_include: edge_class = 'include'
        elif is_recovered: edge_class = 'recovered'
        
            
        name = self._get_reaction_label(r)
        
        
        self.structure['edges'].append({ 
        'data': { 
            'classes': edge_class, 
            'id': edge_id,
            'source': mr.id, 
            'target': mp.id, 
            'name': name,
            'tooltip': self._get_r_tooltip(r), 
        }
        })
        

                 
    
        
    
    
            
        