# An example labelling for CoFI methods

#     cofi_simple_newton <- simple Newton step <- InLab 
# <- non-linear <- optimization <- parameter estimation <- CoFI



# An example labelling for Espresso problems

#     magnetotelluric_1D <- magnetotelluric <- 
#  370602 Electrical and electromanetic methods in geophysics <- 
#  3706 Geophysics <- 37 Earth Sciences



# An example labelling for CoFI examples: pygimli_dcip_century_tri_mesh.ipynb

#     Application domain: pygimli_dcip_century_tri_mesh.ipynb <- DCIP 
#   <- 370602 Electrical and electromanetic methods in geophysics 
#   <- 3706 Geophysics <- 37 Earth Sciences
#     Methods domain: pygimli_dcip_century_tri_mesh.ipynb <- Newton conjugate gradient trust-region algorithm (trust-ncg) <- scipy.optimize.minimize <- non-linear <- optimization <- parameter estimation <- CoFI



# Another example labelling for CoFI examples

#     Application domain: pygimli_dcip.ipynb <- DCIP <- 370602 Electrical and electromanetic methods in geophysics <- 3706 Geophysics <- 37 Earth Sciences
#     Methods domain:
#         pygimli_dcip.ipynb <- Newton conjugate gradient trust-region algorithm (trust-ncg) <- scipy.optimize.minimize <- non-linear <- optimization <- parameter estimation <- CoFI
#         pygimli_dcip.ipynb <- RAdam <- torch.optim <- non-linear <- optimization <- parameter estimation <- CoFI


class hirc_tree:
    def __init__(self, me):
        """
        relationship tree for as parsing result

        Parameters
        ----------------
        me : str
            current leaf name
       
        child : [hirc_tree]
            current leaf's children
        """
        self._me = me
        self._children = []
        self._parent = None
        self._path = None
        self._description = None

        #---graphics property
        self.x = None
        self.y = None
        self.modifier = 0
        self.width = max(220,len(me) * 22)
        self.ch_width = 0

    def me(self):
        return self._me
    
    def children(self):
        return self._children
    
    def parent(self):
        return self._parent
    
    def add_child(self, node):
        self._children.append(node)

    def add_parent(self, node):
        self._parent = node
    
    def add_description(self, des):
        self._description = des
    
    def add_path(self, path):
        self._path = path
    
    def description(self):
        return self._description
    
    def path(self):
        return self._path

    def to_pos(self):
        return [self.x, self.y,0,0]

def insert(tre, node):
        lst = node.tree()
        if len(lst)!= 1:
            token = lst.pop(0)
            if token == tre.me():
                flag = False
                child = lst[0]
                for tok in tre.children():
                    if child == tok.me():
                        insert(tok, node)
                        flag = True
                if not flag:
                    btree = hirc_tree(child)
                    btree.add_parent(token)
                    insert(btree, node)
                    tre.add_child(btree)
        else:
            tre.add_description(node.des())
            tre.add_path(node.path())
            
        return tre


def relation_dict(node):
    return relation_pack(node)

def relation_pack(node):
    node_dict = {}
    node_dict["name"] = node.me()
    node_dict["link_git"] = node.path()
    node_dict["link_doc"] = "www.google.com.au"
    node_dict["children"] = []
    node_dict["description"] = node.description()
    if node.children():
        for j in node.children():
            node_dict["children"].append(relation_pack(j))
    return node_dict


#------------------------

