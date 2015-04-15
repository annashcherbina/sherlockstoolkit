# Import the graph_tool modules
import graph_tool
import graph_tool.stats
import graph_tool.draw
import cPickle
import random 
from Node import * 
#from ete2 import Tree, NodeStyle, TreeStyle 
import pygraphviz as PG 
from second_degree_imputation import * 

class PedigreeGraph: 
    def __init__(self,rel_dict,combo_dict,gender_dict,ancestry_dict): 
        #input data for the pedigree
        #index->[person1,person2,truth,predicted,correct, minor_shared,expected_minor_shared] 
        #index->[ma00,ma01,ma02,ma11,ma12,ma22,ibs0,kinc]
        print "ancestry_dict:"+str(ancestry_dict) 
        print "gender_dict:"+str(gender_dict) 
        self.rel_dict=dict() 
        self.combo_dict=dict() 
        for i in rel_dict: 
            p1=rel_dict[i][0] 
            p2=rel_dict[i][1] 
            key1=tuple([p1,p2]) 
            key2=tuple([p2,p1]) 
            self.rel_dict[key1]=rel_dict[i][2::] 
            self.rel_dict[key2]=rel_dict[i][2::] 
            self.combo_dict[key1]=combo_dict[i]
            self.combo_dict[key2]=combo_dict[i] 
        self.colors=['#ffffff','#000000','#ab82ff','#1c86ee','#ff2400','#228b22','#20b2aa','#ffa500','#99cc32','#838b83','#ffa07a']
        self.gender_dict=gender_dict
        self.gender_color=dict() 
        self.gender_color['m']='#99ffff'
        self.gender_color['f']='#ffcccc'

        self.ancestry_dict=ancestry_dict
        self.ancestry_color=dict() 
        self.ancestry_color['EUROPE']='#d60000'
        self.ancestry_color['AMERICA']='#b2b2f9'
        self.ancestry_color['MIDDLE EAST']='#348e00'
        self.ancestry_color['EAST ASIA']='#fb7200'
        self.ancestry_color['SOUTH ASIA']='#ffd700'
        self.ancestry_color['AFRICA']='#1a1f71' 
        self.ancestry_color['EUROPE,AMERICA']='#d0000'
        self.ancestry_color['NONE']='#000000'
        self.ancestry_color['global']='#D3D3D3'
        #initialized edge and vertex properties 
        self.g=graph_tool.Graph(directed=False) 
        self.v_name=self.g.new_vertex_property("string") 
        self.e_mashared=self.g.new_edge_property("float")
        self.e_predicted=self.g.new_edge_property("int")
        self.e_color=self.g.new_edge_property("string") 
        self.v_color=self.g.new_vertex_property("string") 
        self.e_direction=self.g.new_edge_property("string") 
        
        #additional data structures to map node/edge names and relationships 
        self.vertices=dict() # vertex name --> vertex object 
        self.first_degree_edges=dict() #p1->[p_n with d=1] 
        self.second_degree_edges=dict() 
        self.third_degree_edges=dict() 

        self.siblings=dict() 
        self.high_degree_edges=dict() #p1->[p_n with d>=2] 
        self.specific_edges=dict() #tuple([p1,p2])--> edge 
        self.all_edges=dict() #p1->[p_n with any degree] 

        self.married_in=dict() 
        self.connectivity=dict() 
        self.second_third=dict() 

    def draw_graph(self): 
        self.g.vertex_properties["name"]=self.v_name 
        self.g.edge_properties["mashared"]=self.e_mashared 
        self.g.edge_properties["predicted"]=self.e_predicted 
        self.g.edge_properties["direction"]=self.e_direction
        self.g.vertex_properties["color"]=self.v_color 
        vprops = {'label' : self.v_name,'voro_margin':0.01,'margin':0,'resolution':400,'fontsize':10,'truecolor':True,'shape':'plaintext'}
        eprops={'overlap':False,'splines':'curved',"dir":self.e_direction,"arrowType":"normal","style":"solid"}
        #graph_tool.draw.graph_draw(g, vprops=vprops, eprops=eprops, vertex_font_size=5, vertex_shape="plaintext", output="pedigree.png")
        graph_tool.draw.graphviz_draw(self.g,size=tuple([50,60]),splines=True,vprops=vprops,eprops=eprops,elen=self.e_mashared,ecolor=self.e_color,vcolor=self.v_color, layout="neato",output="pedigree_graph.png")

    def create_vertices(self): 
        subjects=set([]) 
        for key in self.rel_dict: 
            s1=key[0] 
            s2=key[1] 
            subjects.add(s1) 
            subjects.add(s2) 
        for s in subjects: 
            v=self.g.add_vertex() 
            self.v_name[v]=s
            self.vertices[s]=v 
            gender=self.gender_dict[s] 
            ancestry=self.ancestry_dict[s] 
            gender_color=self.gender_color[gender] 
            ancestry_color=self.ancestry_color[ancestry] 
            self.v_color[v]=gender_color 
            #self.v_color[v]=ancestry_color 

    def add_edges(self): 
        added=dict() 
        for key in self.rel_dict: 
            s_name=key[0] 
            t_name=key[1] 
            if tuple([s_name,t_name]) in added: 
                continue 
            if tuple([t_name,s_name]) in added: 
                continue 
           
            added[tuple([s_name,t_name])]=1 
            added[tuple([t_name,s_name])]=1 
            degree=int(self.rel_dict[key][1]) 
            ###print str(degree) 
            if degree==-1: 
                continue #unrelated 
            source=self.vertices[s_name] 
            target=self.vertices[t_name] 
            e=self.g.add_edge(source,target) 
            self.e_mashared[e]=1/float(self.rel_dict[key][3])
            self.e_predicted[e]=int(self.rel_dict[key][1])
            self.e_color[e]=self.colors[self.e_predicted[e]]
            self.e_direction[e]="none" 
            self.specific_edges[tuple([s_name,t_name])]=e 
            self.specific_edges[tuple([t_name,s_name])]=e 
            if s_name not in self.all_edges: 
                self.all_edges[s_name]=[t_name] 
            else: 
                self.all_edges[s_name].append(t_name) 
            if t_name not in self.all_edges: 
                self.all_edges[t_name]=[s_name]
            else: 
                self.all_edges[t_name].append(s_name) 
            ###print str(self.all_edges) 
            if degree==1: 
                ###print str(degree) 
                if s_name not in self.first_degree_edges: 
                    self.first_degree_edges[s_name]=[t_name] 
                else: 
                    self.first_degree_edges[s_name].append(t_name) 
                if t_name not in self.first_degree_edges: 
                    self.first_degree_edges[t_name]=[s_name] 
                else: 
                    self.first_degree_edges[t_name].append(s_name) 
            else: 
                if s_name not in self.high_degree_edges: 
                    self.high_degree_edges[s_name]=[t_name ]
                else: 
                    self.high_degree_edges[s_name].append(t_name) 
                if t_name not in self.high_degree_edges: 
                    self.high_degree_edges[t_name]=[s_name] 
                else: 
                    self.high_degree_edges[t_name].append(s_name)
            if degree==2: 
                if s_name not in self.second_degree_edges: 
                    self.second_degree_edges[s_name]=[t_name] 
                else: 
                    self.second_degree_edges[s_name].append(t_name) 
                if t_name not in self.second_degree_edges: 
                    self.second_degree_edges[t_name]=[s_name] 
                else: 
                    self.second_degree_edges[t_name].append(s_name) 
            if degree==3: 
                if s_name not in self.third_degree_edges: 
                    self.third_degree_edges[s_name]=[t_name] 
                else: 
                    self.third_degree_edges[s_name].append(t_name) 
                if t_name not in self.third_degree_edges: 
                    self.third_degree_edges[t_name]=[s_name] 
                else: 
                    self.third_degree_edges[t_name].append(s_name) 


    def connect_nuclear(self,tree): 
        #get the set of undirected 2nd degree edges 
        undirected_edges=dict() 
        for p1 in self.second_degree_edges: 
            for p2 in self.second_degree_edges[p1]: 
               e_p1_p2=self.specific_edges[tuple([p1,p2])] 
               if self.e_direction[e_p1_p2]=="none": 
                   undirected_edges[tuple([p1,p2])]=e_p1_p2 
        improvement = True 
        while improvement: 
            #print "iterating improvement" 
            print "undirected edges:"+str(undirected_edges) 
            improvement=False 
            toremove=[] 
            for e in undirected_edges: 
                p1=e[0] 
                p2=e[1]
                print "testing p1:"+str(p1) 
                print "testing p2:"+str(p2) 
                updated_tree,errors=test_second_tree_rels(tree,p1,p2,self.rel_dict,self.combo_dict,self.married_in,self.connectivity) 
                #print "errors:"+str(errors) 
                
                if errors !=-1: 
                    #the optimal relationship between p1 and p2 can be determined 
                    tree=updated_tree 
                    toremove.append(e)
                    improvement=True 
            for e in toremove: 
                undirected_edges.__delitem__(e) 
        #print "DONE WITH CONNECTING NUCLEAR FAM's" 
        return tree 
    
            
            
    def get_nuclear_families(self): 
        families=[]
        expanded=set([]) 
        for vertex in self.vertices: 
            if (vertex not in self.first_degree_edges) and (vertex not in self.high_degree_edges): 
                continue #singleton 
            if vertex in expanded:
                continue 
            newfam=set([vertex]) 
            newfam_expanded=set([]) 
            while len(newfam)!=len(newfam_expanded): 
               toexpand=newfam - newfam_expanded 
               for v in toexpand:
                   for target_name in self.all_edges[v]:
                       edge=self.specific_edges[tuple([v,target_name])]
                       target=edge.target()
                       source=edge.source() 
                       t_name=self.v_name[target]
                       s_name=self.v_name[source] 
                       #is the edge a first degree 
                       if self.e_predicted[edge]==1: 
                           newfam.add(t_name)
                           newfam.add(s_name) 
               newfam_expanded.add(v) 
               ###print "newfam:"+str(newfam) 
               ###print "newfam_expanded:"+str(newfam_expanded) 
            expanded=expanded.union(newfam_expanded) 
            families.append(newfam) 
        ##print str(families)
        return families

    def get_married_in_parents(self,family): 
        multiple_possible_directions=dict() 
        for p in family: 
            if p in self.first_degree_edges: 
                if (len(self.first_degree_edges[p])>0) and (p not in self.high_degree_edges): 
                    #this is a married in parent:
                    ##print "married in:"+str(p)
                    self.married_in[p]=True  
                    for child in self.first_degree_edges[p]: 
                        #impose direction 
                        e_to_direct=self.specific_edges[tuple([p,child])] 
                        source=e_to_direct.source()
                        s_name=self.v_name[source] 
                        target=e_to_direct.target() 
                        t_name=self.v_name[target] 
                        dir_existing=None 
                        if self.e_direction[e_to_direct]!="none": 
                            dir_existing=self.e_direction[e_to_direct] 
                        if s_name==p: 
                            self.e_direction[e_to_direct]="forward" 
                        else: 
                            self.e_direction[e_to_direct]="back" 
                        if dir_existing!=None: 
                            multiple_possible_directions[tuple([p,child])]=[dir_existing,self.e_direction[e_to_direct]]
        return multiple_possible_directions

    
    def get_siblings(self,family): 
        multiple_possible_directions=dict() 
        for p1 in family: 
            if p1 not in self.first_degree_edges: 
                continue 
            potential_sibs=self.first_degree_edges[p1] 
            for p2 in potential_sibs: 
                mashared=self.combo_dict[tuple([p1,p2])] 
                if float(mashared[4])==0: 
                    continue 
                ratio_12_over_02=float(mashared[6])/float(mashared[4]) 
                if ratio_12_over_02<5: 
                    e_to_direct=self.specific_edges[tuple([p1,p2])] 
                    if self.e_direction[e_to_direct]!="none": 
                        multiple_possible_directions[tuple([p1,p2])]=[self.e_direction[e_to_direct],"both"]
                    self.e_direction[e_to_direct]="both" 
                    if p1 not in self.siblings: 
                        self.siblings[p1]=set() 
                    if p2 not in self.siblings: 
                        self.siblings[p2]=set() 
                    self.siblings[p1].add(p2) 
                    self.siblings[p2].add(p1) 
        return multiple_possible_directions 
    
    def get_trios(self,family):
        multiple_possible_directions=dict() 
        for p1 in family:
                if p1 not in self.first_degree_edges: 
                    continue 
                connections=list(set(self.first_degree_edges[p1])) 
                potential_parents=[] 
                #do all the connections have a first degree edge? 
                for ind_c1 in range(len(connections)): 
                    for ind_c2 in range(ind_c1+1,len(connections)): 
                        c1=connections[ind_c1] 
                        c2=connections[ind_c2] 
                        if c2 not in self.first_degree_edges[c1]: 
                            #is the number of minor alleles shared high? 
                            mashared_p1_c1=float(self.rel_dict[tuple([p1,c1])][3])
                            mashared_p1_c2=float(self.rel_dict[tuple([p1,c2])][3])
                            ###print str(mashared_p1_c1) 
                            if mashared_p1_c1 > .40 and mashared_p1_c2 > 0.4: 
                                #check for an inheritance pattern 
                                mashared_c1_c2=float(self.rel_dict[tuple([c1,c2])][3])
                                if mashared_c1_c2 <0.30:
                                    potential_parents.append([c1,c2]) 
                if len(potential_parents)==1:
                    c1=potential_parents[0][0] 
                    c2=potential_parents[0][1] 
                    e1=self.specific_edges[tuple([p1,c1])]
                    e2=self.specific_edges[tuple([p1,c2])] 
                    if self.e_direction[e1]!="none": 
                        multiple_possible_directions[tuple([p1,c1])]=[self.e_direction[e1]]
                    if self.e_direction[e2]!="none": 
                        multiple_possible_directions[tuple([p1,c2])]=[self.e_direction[e2]] 
                    if self.v_name[e1.source()]==c1: 
                        self.e_direction[e1]="forward" 
                    else: 
                        self.e_direction[e1]="back" 
                    if tuple([p1,c1]) in multiple_possible_directions: 
                        multiple_possible_directions[tuple([p1,c1])].append(self.e_direction[e1])
                    if self.v_name[e2.source()]==c2: 
                        self.e_direction[e2]="forward" 
                    else: 
                        self.e_direction[e2]="back" 
                    if tuple([p1,c2]) in multiple_possible_directions: 
                        multiple_possible_directions[tuple([p1,c2])].append(self.e_direction[e2]) 
        return multiple_possible_directions         
        
    def get_inheritance_groups(self,family): 
        chains=[] 
        for p1 in family: 
            if p1 not in self.first_degree_edges: 
                continue 
            connections=list(set(self.first_degree_edges[p1])) 
            for ind_c1 in range(len(connections)): 
                for ind_c2 in range(ind_c1+1,len(connections)): 
                    c1=connections[ind_c1] 
                    c2=connections[ind_c2] 
                    show=True
                    if c2 not in self.first_degree_edges[c1]:
                            #is the number of minor alleles shared high? 
                            mashared_p1_c1=float(self.rel_dict[tuple([p1,c1])][3])
                            mashared_p1_c2=float(self.rel_dict[tuple([p1,c2])][3])
                            if mashared_p1_c1 > .40 and mashared_p1_c2 > 0.4: 
                                #check for an inheritance pattern 
                                mashared_c1_c2=float(self.rel_dict[tuple([c1,c2])][3])
                                ratio=mashared_c1_c2/max([mashared_p1_c1,mashared_p1_c2])
                                if ratio>0.6: #inheritance!
                                    chain=[c1,p1,c2]
                                    chains.append(chain) 
        #iterate until no new directional information can be added 
        ignore_first_pass=[] 
        for chain in chains: 
            c1=chain[0] 
            p1=chain[1] 
            c2=chain[2] 
            e1=self.specific_edges[tuple([c1,p1])] 
            e2=self.specific_edges[tuple([p1,c2])] 
            if self.e_direction[e1]=="none" and self.e_direction[e2]=="none": 
                ignore_first_pass.append(chain) 
                
        delta=0
        firstpass=True 
        while (delta >0) or (firstpass==True): 
            delta=0 
            for chain in chains: 
                c1=chain[0] 
                p1=chain[1]
                c2=chain[2] 
                e1=self.specific_edges[tuple([c1,p1])] 
                e2=self.specific_edges[tuple([p1,c2])]
                num_none=0 
                if self.e_direction[e1]=="none": 
                    num_none+=1 
                else: 
                    directed_edge=e1
                if self.e_direction[e2]=="none": 
                    num_none+=1 
                else: 
                    directed_edge=e2
                if num_none==1:
                    if firstpass==True and chain in ignore_first_pass: 
                        continue 
                    #we can impose direction on the other edge! 
                    parent_name = self.v_name[directed_edge.source()]
                    direction=self.e_direction[directed_edge]
                    if parent_name==c1 and direction=="forward" : 
                        #direction should be p1--> c2 
                        if self.v_name[e2.source()]==p1: 
                            self.e_direction[e2]="forward"
                        else: 
                            self.e_direction[e2]="back" 
                        delta+=1 
                    elif parent_name==c1 and direction=="back": 
                        #direction should be c2-->p1-->c1
                        if self.v_name[e2.source()]==p1: 
                            self.e_direction[e2]="back" 
                        else: 
                            self.e_direction[e2]="forward" 

                        delta+=1 
                    elif parent_name==c2 and direction=="forward": 
                        #direction should be p1--> c1 
                        if self.v_name[e1.source()]==p1: 
                            self.e_direction[e1]="forward" 
                        else: 
                            self.e_direction[e2]="back" 
                        delta+=1             
                    elif parent_name==c2 and direction=="back": 
                        #direction shoud be c1 -->p1-->c2
                        if self.v_name[e1.source()]==c1: 
                            self.e_direction[e1]="forward" 
                            
                        else: 
                            self.e_direction[e1]="back" 
                        delta+=1 
                    elif parent_name==p1: 
                        target_name=self.v_name[directed_edge.target()]
                        if target_name==c1 and direction=="forward": 
                            #direction should be c2-->p1-->c1
                            if self.v_name[e2.source()]==c2: 
                                self.e_direction[e2]="forward" 
                            else: 
                                self.e_direction[e2]="back" 
                            delta+=1 
                        elif target_name==c1 and direction=="back": 
                            #direction should be c1-->p1-->c2 
                            if self.v_name[e2.source()]==p1: 
                                self.e_direction[e2]="forward" 
                            else: 
                                self.e_direction[e2]="back" 
                            delta+=1 
                        elif target_name==c2 and direction=="forward" : 
                            #direction should be c1-->p1-->c2 
                            if self.v_name[e1.source()]==c1: 
                                self.e_direction[e1]="forward" 
                            else: 
                                self.e_directoin[e1]="back" 
                            delta+=1 
                        elif target_name==c2 and direction=="back": 
                            #direction should be c2-->p1-->c1 
                            if self.v_name[e1.source()]==p1: 
                                self.e_direction[e1]="forward"
                            else: 
                                self.e_direction[e1]="back" 
                            delta+=1
            firstpass=False
        for chain in chains: #impose direction on 2nd degree edges!
            c1=chain[0] 
            p1=chain[1]  
            c2=chain[2]
            if tuple([c1,c2]) not in self.specific_edges: 
                ##print "skipping!" 
                continue 
            e1=self.specific_edges[tuple([c1,p1])] 
            e2=self.specific_edges[tuple([p1,c2])]
            e1_dir=self.e_direction[e1] 
            e2_dir=self.e_direction[e2] 
            if tuple([c1,c2]) in self.specific_edges: 
                e3=self.specific_edges[tuple([c1,c2])]
            else: 
                continue 
            if e1_dir == "forward" or e1_dir=="back" or e2_dir=="forward" or e2_dir=="back": 
                ##print "GETTING 2nd DEGREE DIRECTION!!" 
                e1_source=self.v_name[e1.source()] 
                e2_source=self.v_name[e2.source()] 
                parent=None 
                child=None
                if e1_source==c1 and e1_dir=="forward": 
                    #c1-->p1 
                    if parent==c2: 
                        continue 
                    parent=c1
                    child=c2
                if e1_source==c1 and e1_dir=="back": 
                    if parent==c1: 
                        continue 
                    parent=c2
                    child=c1 
                if e1_source==p1  and e1_dir=="back": 
                    if parent==c2: 
                        continue 
                    parent=c1
                    child=c2
                if e1_source==p1 and e1_dir=="forward": 
                    if parent==c1: 
                        continue 
                    parent=c2
                    child=c1
                if e2_source==c2 and e2_dir=="forward": 
                    if parent==c1: 
                        continue 
                    parent=c2 
                    child=c1
                if e2_source==c2 and e2_dir=="back": 
                    if parent==c2: 
                        continue
                    parent=c1
                    child=c2
                if e2_source==p1 and e2_dir=="forward": 
                    if parent==c2: 
                        continue
                    parent=c1
                    child=c2
                if e2_source==p1 and e2_dir=="back":
                    if parent==c1: 
                        continue
                    parent=c2 
                    child=c1 
                ###print "parent:"+str(parent) 
                ###print "child:"+str(child) 
                e3_source=self.v_name[e3.source()] 
                e3_target=self.v_name[e3.target()] 
                if e3_source==parent and e3_target==child: 
                    self.e_direction[e3]="forward"
                else:
                    self.e_direction[e3]="back" 
    def get_reverse_trios(self,family): 
        multiple_possible_directions=dict() 
        for p1 in family: 
            if p1 not in self.siblings: 
                continue 
            for s1 in self.siblings[p1]: 
                for relative in self.first_degree_edges[p1]: 
                    if relative ==p1: 
                        continue 
                    if relative==s1: 
                        continue 
                    if relative in self.siblings[p1] or relative in self.siblings[s1]: 
                        continue 
                    if relative in self.first_degree_edges[s1]:                        
                        #The relative is a parent of both p1 and s1 
                        #assign direction to both edges. 
                        e1=self.specific_edges[tuple([p1,relative])]
                        if self.e_direction[e1]!="none": 
                            multiple_possible_directions[tuple([p1,relative])]=[self.e_direction[e1]] 
                        if self.v_name[e1.source()]==p1 and self.v_name[e1.target()]==relative: 
                            self.e_direction[e1]="back" 
                        else: 
                            self.e_direction[e1]="forward" 
                        if tuple([p1,relative]) in multiple_possible_directions: 
                            multiple_possible_directions[tuple([p1,relative])].append(self.e_direction[e1])
                        e2=self.specific_edges[tuple([s1,relative])]
                        if self.e_direction[e2]!="none": 
                            multiple_possible_directions[tuple([s1,relative])]=[self.e_direction[e2]] 
                        if self.v_name[e2.source()]==s1 and self.v_name[e2.target()]==relative: 
                            self.e_direction[e2]="back" 
                        else: 
                            self.e_direction[e2]="forward" 
                        if tuple([s1,relative]) in multiple_possible_directions: 
                            multiple_possible_directions[tuple([s1,relative])].append(self.e_direction[e2])
                    else: #the relative is a child of p1! 
                        e1=self.specific_edges[tuple([p1,relative])]
                        if self.e_direction[e1]!="none": 
                            multiple_possible_directions[tuple([s1,relative])]=[self.e_direction[e1]]
                        if self.v_name[e1.source()]==p1 and self.v_name[e1.target()]==relative: 
                            self.e_direction[e1]="forward" 
                        else: 
                            self.e_direction[e1]="back" 
                        if tuple([s1,relative]) in multiple_possible_directions: 
                            multiple_possible_directions[tuple([s1,relative])].append(self.e_direction[e1])
        return multiple_possible_directions 
    def get_married_in(self,nuclear_families): 
        #people who married into the family will not have any relationships across nuclear families 
        for p in self.connectivity: 
            if self.connectivity[p]==0: 
                self.married_in[p]=True 
    def get_connectivity(self,nuclear_families):
        print str(nuclear_families) 
        for fam1 in nuclear_families: 
            for p1 in fam1: 
                connectivity=0 
                second_third=0 
                for fam2 in nuclear_families: 
                    if fam1==fam2:                         
                        continue 
                    for p2 in fam2: 
                        if tuple([p1,p2]) in self.rel_dict: 
                            degree=float(self.rel_dict[tuple([p1,p2])][1])
                            #print "p1:"+str(p1)+",p2:"+str(p2)+","+str(self.rel_dict[tuple([p1,p2])])
                            if degree > -1: 
                                weight=1/float(degree) 
                                connectivity+=weight
                            if degree==2 or degree==3: 
                                second_third+=1 
                self.connectivity[p1]=connectivity
                self.second_third[p1]=second_third 
    
    def merge_conflicts(self,conflicts1,conflicts2,conflicts3,conflicts4):
        conflicts=dict() 
        for entry in conflicts1: 
            rev_entry=tuple([entry[1],entry[0]]) 
            conflicts[entry]=set(conflicts1[entry]) 
            conflicts[rev_entry]=set(conflicts1[entry])
        for entry in conflicts2: 
            rev_entry=tuple([entry[1],entry[0]]) 
            if entry in conflicts: 
                conflicts[entry]=conflicts[entry].union(set(conflicts2[entry]))
            else: 
                conflicts[entry]=set(conflicts2[entry])
            if rev_entry in conflicts: 
                conflicts[rev_entry]=conflicts[rev_entry].union(set(conflicts2[entry]))
            else: 
                conflicts[rev_entry]=set(conflicts2[entry])
        for entry in conflicts3: 
            rev_entry=tuple([entry[1],entry[0]])
            if entry in conflicts: 
                conflicts[entry]=conflicts[entry].union(set(conflicts3[entry]))
            else: 
                conflicts[entry]=set(conflicts3[entry])
            if rev_entry in conflicts: 
                conflicts[rev_entry]=conflicts[rev_entry].union(set(conflicts3[entry]))
            else: 
                conflicts[rev_entry]=set(conflicts3[entry])
        for entry in conflicts4: 
            rev_entry=tuple([entry[1],entry[0]]) 
            if entry in conflicts: 
                conflicts[entry]=conflicts[entry].union(set(conflicts4[entry]))
            else: 
                conflicts[entry]=set(conflicts4[entry])
            if rev_entry in conflicts: 
                conflicts[rev_entry]=conflicts[rev_entry].union(set(conflicts4[entry]))
            else: 
                conflicts[rev_entry]=set(conflicts4[entry])
        return conflicts 
                

    def impute_direction(self): 
        nuclear_families=self.get_nuclear_families()
        self.get_connectivity(nuclear_families) 
        self.get_married_in(nuclear_families) 
        print "married_in:"+str(self.married_in) 
        conflicts=[] 
        for family in nuclear_families: 
            conflicts1=self.get_married_in_parents(family) 
            conflicts2=self.get_siblings(family) 
            conflicts3=self.get_reverse_trios(family) 
            conflicts4=self.get_trios(family) 
            self.get_inheritance_groups(family) #we shouldn't have conflicts here because function assumes that at least one of the edges is null 
            conflicts=self.merge_conflicts(conflicts1,conflicts2,conflicts3,conflicts4) 
        return nuclear_families,conflicts
    #figures out the older and younger generation from an edge 
    def resolve_hierarchy(self,e,person1,person2):
        person1_name=person1 
        person2_name=person2
        person1=self.vertices[person1] 
        person2=self.vertices[person2] 
        print str(self.e_direction[e]) 
        if self.e_direction[e]=="forward": 
            if e.source()==person1 and e.target()==person2: 
                return [person1_name,person2_name] #[older,younger] 
            elif e.source()==person2 and e.target()==person1: 
                return [person2_name,person1_name] 
        elif self.e_direction[e]=="back": 
            print "resolving hierarchy:"+person1_name+","+person2_name+" back case!!"
            if e.source()==person1 and e.target()==person2: 
                ##print "returning: person2, person1" 
                return[person2_name,person1_name] 
            elif e.source()==person2 and e.target()==person1: 
                return [person1_name,person2_name] 


    #resolve any conflicting edges in the tree 
    def resolve_tree_conflicts(self,tree): 
        for node in tree: 
            parents=tree[node].parents 
            children=tree[node].children 
            siblings=tree[node].siblings 
            parent_sibling_overlap=parents.intersection(siblings) 
            parent_child_overlap=parents.intersection(children) 
            child_siblings_overlap=children.intersection(siblings) 
            if len(parent_sibling_overlap) > 0: 
                #resolve the conflict  
                for person in parent_sibling_overlap: 
                    if float(self.combo_dict[tuple([person,node])][8])<0.2: 
                        #parent 
                        if person in tree[node].siblings: 
                            tree[node].siblings.remove(person) 
                        if node in tree[person].siblings: 
                            tree[person].siblings.remove(node) 
                    else: 
                        #sibling
                        if person in tree[node].parents: 
                            tree[node].parents.remove(person) 
                        if node in tree[person].children: 
                            tree[person].children.remove(node) 
            if len(child_siblings_overlap)>0: 
                #resolve the conflict: 
                for person in child_siblings_overlap: 
                    if float(self.combo_dict[tuple([person,node])][8])<0.2: 
                        #child 
                        if person in tree[node].siblings: 
                            tree[node].siblings.remove(person)
                        if node in tree[person].siblings: 
                            tree[person].siblings.remove(node) 
                    else: 
                        #sibling 
                        if person in tree[node].children: 
                            tree[node].children.remove(person) 
                        if node in tree[person].parents: 
                            tree[person].parents.remove(node) 
            if len(parent_child_overlap)>0: 
                #resolve the conflict by looking at connected degree! 
                for person in parent_child_overlap: 
                    if self.connectivity[person]>self.connectivity[node]: 
                        #the person is the parent of the node 
                        if person in tree[node].children: 
                            tree[node].children.remove(person) 
                        if node in tree[person].parents: 
                            tree[person].parents.remove(node) 
                    if self.connectivity[person] < self.connectivity[node]: 
                        #the person is the child of the node
                        if person in tree[node].parents: 
                            tree[node].parents.remove(person)
                        if node in tree[person].children: 
                            tree[person].children.remove(node)                 
        return tree

    def build_tree(self,families):
        tree=dict() 
        roots=[] # root nodes that have no parents, these will be combined in one super parent 
        #create all nodes in our pedigree 
        for vertex_name in self.vertices: 
            vertex=self.vertices[vertex_name] 
            current_name=self.v_name[vertex]
            newNode=Node()
            newNode.name=current_name 
            newNode.gender=self.gender_dict[current_name]
            roots.append(current_name) 
            tree[current_name]=newNode

        print "#########################################" 
        for current_name in self.vertices:
            current_node=tree[current_name] 
            #add all the directed relatives that aren't in the tree yet 
            if current_name not in self.first_degree_edges: 
                continue 
            for relative in self.first_degree_edges[current_name]: 
                specific_edge=self.specific_edges[tuple([relative,current_name])]
                if self.e_direction[specific_edge]=="none":
                    continue 
                    #TODO: can we somehow add in undirected edges? 
                #the edge has direction! it is useful to us
                relNode=tree[relative] 
                if self.e_direction[specific_edge]=="both": 
                    #print "adding sibling:"+str(relative)+" to current node:"+str(current_node.name) 
                    current_node.siblings.add(relative)
                    relNode.siblings.add(current_name) 
                    #merge their parents 
                    common_parents=current_node.parents.union(relNode.parents) 
                    #print "common parents:"+str(common_parents) 
                    current_node.parents=common_parents
                    relNode.parents=common_parents 
                    #merge their siblings 
                    common_sibs=current_node.siblings.union(relNode.siblings) 
                    #print "common sibs:"+str(common_sibs) 
                    current_node.siblings=common_sibs 
                    relNode.siblings=common_sibs 
                else: 
                    if relNode.name in current_node.children: 
                        continue 
                    if relNode.name in current_node.parents: 
                        continue 
                    parent,child=self.resolve_hierarchy(specific_edge,current_name,relative) 
                    if child in roots:
                        roots.remove(child) 
                    tree[child].parents.add(parent) 
                    tree[parent].children.add(child) 
                    for sibling in tree[child].siblings:
                    #    print "sibling:"+str(sibling) 
                        tree[sibling].parents.add(parent) 
                        if sibling in roots: 
                            roots.remove(sibling) 
        print "#########################################"
        
        added_unknown=0 
        toremove_roots=[] 
        for un1 in roots: 
            for un2 in roots: 
                if un1==un2: 
                    continue 
                if un1 in self.siblings: 
                    if un2 in self.siblings[un1]: 
                        #create a phantom parent node!
                        #only create a new node if no "unknown" parents already exist. 
                        #check if "unknown" parents already exist 
                        parents_to_add=2 
                        for p in tree[un1].parents: 
                            parents_to_add-=1 
                            if un2 not in tree[p].children: 
                                tree[p].children.add(un2) 
                                tree[un2].parents.add(p) 
                        for p in tree[un2].parents: 
                            parents_to_add-=1 
                            if un1 not in tree[p].children: 
                                tree[p].children.add(un1) 
                                tree[un1].parents.add(p) 
                        while parents_to_add > 0: 
                            added_unknown+=1 
                            newNode=Node()
                            newNode.name="Unknown"+str(added_unknown)  
                            newNode.gender='u'
                            roots.append(newNode.name) 
                            tree[newNode.name]=newNode 
                            newNode.children.add(un1) 
                            newNode.children.add(un2) 
                            tree[un1].parents.add(newNode.name) 
                            tree[un2].parents.add(newNode.name) 
                            parents_to_add-=1 
                        toremove_roots.append(un1) 
                        toremove_roots.append(un2) 

        for n in toremove_roots: 
            if n in roots: 
                roots.remove(n) 
        #remove self references from the tree 
        for n in tree: 
            if n in tree[n].parents: 
                tree[n].parents.remove(n)
            if n in tree[n].siblings: 
                tree[n].siblings.remove(n) 
            if n in tree[n].children: 
                tree[n].children.remove(n) 
        return tree 

    #recursively builds newick string 
    def build_newick(self,root,tree): 
        newick="" 
        if len(root.children)==0: 
            newick=root.name 
            return newick 
        else: 
            newick="(" 
            for child in root.children: 
                newick=newick+","+self.build_newick(tree[child],tree)
            newick=newick+")"+root.name 
            return newick 

    #when possible, resolve cases of multiple possible directions assigned to first degree edges 
    def resolve_conflicts(self,conflicts): 
        print "CONFLICTS:"+str(conflicts) 
        for entry in conflicts: 
            if len(conflicts[entry])>1: 
                case1=conflicts[entry].__contains__('both') and conflits[entry].__contains__('back') 
                case2=conflicts[entry].__contains__('both') and conflicts[entry].__contains__('forward') 
                if case1 or case2: 
                    if entry not in self.specific_edges: 
                        continue 
                    e1=self.specific_edges[entry]
                    #get the p(IBS=0) 
                    pibs0=float(self.combo_dict[entry][8])
                    if pibs0 < 0.2: 
                        #parent/child 
                        if case1: 
                            self.e_direction[e1]='back' 
                        elif case2: 
                            self.e_direction[e1]='forward' 
                    else: 
                        self.e_direction[e1]='both' 

        

if __name__=="__main__":
    #rel_dict=cPickle.load(open('dictionary.fam95.pkl','rb'))
    #combo_dict=cPickle.load(open('allelecombos.fam95.pkl','rb')) 
    #gender_dict=cPickle.load(open('genderdict.fam95.pkl','rb')) 
    rel_dict=cPickle.load(open('dictionary.pkl','rb'))
    combo_dict=cPickle.load(open('allelecombos.pkl','rb')) 
    gender_dict=cPickle.load(open('genderdict.pkl','rb')) 
    p=PedigreeGraph(rel_dict,combo_dict,gender_dict) 
    p.create_vertices() 
    p.add_edges() 
    nuclear_families,conflicts=p.impute_direction() 
    p.resolve_conflicts(conflicts) 
    #generate a newick string for pedigree visualization 
    tree=p.build_tree(nuclear_families) 
    tree=p.resolve_tree_conflicts(tree) 
    #connect nuclear families based on 2nd degree relationships 
    tree=p.connect_nuclear(tree) 
    p.draw_graph() 
    A=PG.AGraph(directed=True,strict=False) 
    for node in tree: 
        for child in tree[node].children: 
            A.add_edge(node,child) 
            n=A.get_node(child) 
            if child not in p.gender_dict: 
                n.attr['shape']='diamond'
                #if the child of this node has another parent with a known gender, we can infer the gender 
                temp_children=tree[child].children 
                assigned=False 
                for c_temp in temp_children: 
                    if assigned==True: 
                        break 
                    for p_temp in tree[c_temp].parents: 
                        if p_temp in p.gender_dict: 
                            if p.gender_dict[p_temp]=='m': 
                                #print "case 1: assigning circle shape to node:"+str(child)+" because child "+str(c_temp) + " has parent "+str(p_temp) 
                                n.attr['shape']='circle'
                                assigned=True 
                                break 
                            elif p.gender_dict[p_temp]=='f': 
                                #print "case 1: assigning square shape to node:"+str(child)+" because child "+str(c_temp) + " has parent "+str(p_temp) 
                                n.attr['shape']='square' 
                                assigned=True 
                                break 

            elif p.gender_dict[child]=='m': 
                n.attr['shape']='square'
            else: 
                n.attr['shape']='circle' 
            n=A.get_node(node) 
            if node not in p.gender_dict: 
                n.attr['shape']='diamond' 
                #if the child of this node has another parent with a known gender, we can infer the gender 
                temp_children=tree[node].children 
                assigned=False 
                for c_temp in temp_children: 
                    if assigned==True: 
                        break 
                    for p_temp in tree[c_temp].parents: 
                        if p_temp in p.gender_dict: 
                            #print "case 2: assigning circle shape to node:"+str(node)+" because child "+str(c_temp) + " has parent "+str(p_temp) 
                            if p.gender_dict[p_temp]=='m': 
                                n.attr['shape']='circle' 
                                assigned=True 
                            elif p.gender_dict[p_temp]=='f': 
                                #print "case 2 : assigning square shape to node:"+str(node)+" because child "+str(c_temp) + " has parent "+str(p_temp) 
                                n.attr['shape']='square' 
                                assigned=True 
                                break 
            elif p.gender_dict[node]=='m': 
                n.attr['shape']='square'
            else: 
                n.attr['shape']='circle' 
    #randomly assign gender in cases where both parent nodes are unknown 
    for node in tree: 
        unknown_parents=[] 
        for p in tree[node].parents: 
            n=A.get_node(p) 
            if n.attr['shape']=='diamond': 
                unknown_parents.append(p) 
        if len(unknown_parents)>1: 
            p1=unknown_parents[0] 
            n=A.get_node(p1) 
            n.attr['shape']='square' 
            p2=unknown_parents[1] 
            n=A.get_node(p2) 
            n.attr['shape']='circle' 
    A.write('pedigree.dot') 
    A.layout(prog='dot') 
    A.draw('pedigree.png') 
