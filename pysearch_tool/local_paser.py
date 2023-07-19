"""parser"""

class Node:
    """base config for node"""
    def __init__(self, name, path, tree, des):
        """
        A single node definition.

        Parameters
        -----------
        name : str
            Node name
        path : str
            Node file path
        tree : list
            Tree path of the node
        """
        self._name = name
        self._path = path
        self._tree = tree
        self._des = des
    
    def name(self):
        return self._name
    
    def path(self):
        return self._path
    
    def tree(self):
        return self._tree
    
    def des(self):
        return self._des
    

class Method(Node):
    pass 


class Application(Node):
    pass


class Example(Node):
    pass
