# import git
#import subprocess
#(might delete if never used) import pathlib
import os
import yaml
import json

method_headfix = "https://github.com/inlab-geo/cofi/blob/main"

application_headfix = "https://github.com/inlab-geo/espresso/tree/main"
folder_name = "contrib"


example_headfix = "https://github.com/inlab-geo/cofi-examples/tree/main/examples"

class Search:
    def __init__(self, config):
        """
        search earch repository in given path, extract the
        first line.

        Parameters
        ----------------
        method_path : str
            the folder that contains inference methods in CoFI
        app_path : str
            the folder that contains applications in espresso
        prob_path : str
            the folder that contains example problems in CoFI
            examples
        """
        self._method_path = config.search_folder + config.method_folder
        self._app_path = config.search_folder + config.application_folder
        self._prob_path = config.search_folder + config.example_folder
        self._methods = []
        self._apps = []
        self._examples = []
        self._method_to_examples = {}

    def mds(self):
        return self._methods
    
    def aps(self):
        return self._apps

    def examples(self):
        return self._examples
    
    def _search(self):
        def parse(file_path, mode):
            with open(file_path) as file:
                while True:
                    line = file.readline()
                    if line:
                        if "->" in line and "#" in line:
                            if mode == "Method":
                                method_tree = line.strip('\n')[2:].split(" -> ")
                                method_description = file.readline().strip('\n')[15:]
                                method = Method(method_headfix + file_path[18:], method_tree, method_description)
                                self._methods.append(method)
                            if mode == "Application":
                                app_tree = line.strip('\n')[2:].split(" -> ")
                                app_des = file.readline().strip('\n')[15:]
                                app_path = application_headfix + file_path[22:]
                                print(app_path)
                                self._apps.append(App(app_path, app_tree, app_des))                    
                    else:
                        break
        for _, _ , files in os.walk(self._method_path):
            for i in files:
                parse(self._method_path + '/' + i, "Method")

        for root, dirs, files in os.walk(self._app_path):
            if root == self._app_path:
                for dirr in dirs:
                    parse(self._app_path + '/' + dirr + '/' + dirr + '.py', "Application")
        

        # self.init_method_to_examples()
        for root, dirs, files in os.walk(self._prob_path):
            if root == self._prob_path:
                for dirr in dirs:
                    try:
                        path = self._prob_path + dirr + '/'
                        with open(path + 'meta.yml', 'r') as file:
                            data = yaml.safe_load(file)
                            for k in data['method'].keys():
                                gpath = "https://github.com/Denghu-JI/cofi-examples/tree/main/examples/"
                                gpath += path[37:]
                                print(k)
                                e = Example(data['title'],k,gpath + k, data['application domain'].split(" -> "),data['description'],data['method'][k])
                                self._examples.append(e)
                            #---------------------------exmaples parsing done! next is method to example


                                # try:
                                #     code_cells = self.extract_code_from_ipynb(path + file)
                                #     all_code += code_cells
                                # except Exception as e:
                                #     print(e)
                            # print(all_code)
                    except Exception as e:
                        # print(e)
                        pass

            break
        #-------------------

        for method in self._methods:
            for example in self._examples:
                if " -> ".join(method.tree()) in example.methods():
                    d = {}
                    print(example.name() + ' - ' + example.filename())
                    d['name'] = example.name() + ' - ' + example.filename()
                    d['description'] = example.des()
                    d['linkToGit'] =  example.path()
                    method.add_examples(d)
        print(self._methods[0].examples())
        print(self._methods[0].tree())
class Method:
    def __init__(self, path, tree, des):
        """
        A single Method defination.

        Parameters
        -----------
        name : str
            method name
        path : str
            method file path
        tree : list
            tree path of the method
        """
        self._path = path
        self._tree = tree
        self._des = des
        self._examples = []
    
    
    def path(self):
        return self._path
    
    def tree(self):
        return self._tree
    
    def des(self):
        return self._des

    def examples(self):
        return self._examples

    def add_examples(self, exp):
        self._examples.append(exp)
    

    
class App:
    def __init__(self, path, tree, des):
        """
        A single Method defination.

        Parameters
        -----------
        name : str
            method name
        path : str
            method file path
        tree : list
            tree path of the method
        """
        self._path = path
        self._tree = tree
        self._des = des
    
    def path(self):
        return self._path
    
    def tree(self):
        return self._tree
    
    def des(self):
        return self._des


class Example:
    def __init__(self, name, filename, path, tree, des, methods):
        """
        A single Method defination.

        Parameters
        -----------
        name : str
            method name
        path : str
            method file path
        tree : list
            tree path of the method
        """
        self._name = name
        self._filename = filename
        self._path = path
        self._tree = tree
        self._des = des
        self._methods = methods
    
    def name(self):
        return self._name

    def filename(self):
        return self._filename
    
    def path(self):
        return self._path
    
    def tree(self):
        return self._tree
    
    def des(self):
        return self._des
    
    def methods(self):
        return self._methods
            