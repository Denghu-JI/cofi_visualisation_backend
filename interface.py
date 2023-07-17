from relation_dict import hirc_tree, insert, assign_depth, build_pos, assign_coordinates, dict_package, description, relation_dict
from pysearch_tool import dir_search
import json
import boto3

#please specify those folder!
methods_path = "pysearch_tool/cofi/src/cofi/tools"
applications_path = "pysearch_tool/espresso/contrib"
problems_path = "pysearch_tool/cofi-examples/examples"
ignore_list = ['__init__.py', '_base_inference_tool.py']

ignore = []





def main():
    p = dir_search.pysearch(methods_path,applications_path,problems_path)
    p._search()
    method_tree = hirc_tree('CoFI')
    apps_tree = hirc_tree('37 Earth Sciences')

    for i in p.mds():
        method_tree = insert(method_tree,i)
    
    for i in p.aps():
        apps_tree = insert(apps_tree,i)

    cmd = " "
    current_node = apps_tree
    last_node = []

    cmd = " "
    current_node = apps_tree
    last_node = []

    while cmd != 'exit':
        cmd = input('Whats next?: ')
        if cmd == 'children?':
            if len(current_node.children()) == 0:
                print("you have reached a terminal")
            for i in current_node.children():
                print(i.me())
        elif cmd[:2] == 'go':
            flag = False
            for i in current_node.children():
                if i.me() == cmd [3:]:
                    last_node.append(current_node)
                    current_node = i
                    print("now you are on " + i.me() + ", its children are: ", end = '')
                    for j in i.children():
                        print(j.me() + " | ", end = '')
                    print(" ")
                    flag = True
            if not flag:
                print("no such child!")
        elif cmd == "reset":
            current_node = apps_tree
        elif cmd == "back":
            if len(last_node) == 0:
                print("cannot go back")
            else:
                current_node = last_node.pop()
        elif cmd == "path":
            print(current_node.path())
        elif cmd == "des":
            print(current_node.description())
        elif cmd == "me":
            print(current_node.me())
        elif cmd == "pt":
            print(current_node.parent())
        else:
            print("not a vaild command")

if __name__ == "__main__": 
    # main()
    p = dir_search.pysearch(methods_path,applications_path,problems_path)
    p._search()
    method_tree = hirc_tree('CoFI')
    apps_tree = hirc_tree('37 Earth Sciences')
    example_tree = hirc_tree('37 Earth Sciences')

    for i in p.mds():
        method_tree = insert(method_tree,i)
    
    for i in p.aps():
        apps_tree = insert(apps_tree,i)
    
    for i in p.examples():
        example_tree = insert(example_tree,i)

    # method_dt_key = 'data-methods.json'
    # app_dt_key = 'data-apps.json'
    # method_des_key = 'des-methods.json'
    # app_des_key = 'des-apps.json'
    # method_path_key = 'path_method.json'
    # app_path_key = 'path_apps.json'

    # with open(method_dt_key, 'w') as fp:
    #     json.dump(method_dt, fp)

    # with open(app_dt_key, 'w') as fp:
    #     json.dump(app_dt, fp)

    # with open(method_des_key, 'w') as fp:
    #     json.dump(des_method, fp)
    
    # with open(app_des_key, 'w') as fp:
    #     json.dump(des_app, fp)

    # json_methods_dt = json.dumps(method_dt)
    # json_apps_dt = json.dumps(app_dt)


    s3 = boto3.client('s3')
    bucket_name = 'jsonofthetree'
    json_key = 'data.json'

    # s3.put_object(Bucket=bucket_name, Key=method_dt_key, Body=json_methods_dt, ACL='public-read')
    # s3.put_object(Bucket=bucket_name, Key=app_dt_key, Body=json_apps_dt, ACL='public-read')

    method_rel_key = "method_relation.json"
    app_rel_key = "app_relation.json"
    example_rel_key = "example_relation.json"

    relation_method = relation_dict(method_tree)
    relation_app = relation_dict(apps_tree)
    relation_example = relation_dict(example_tree)

    with open(method_rel_key, 'w') as fp:
        json.dump(relation_method, fp)
    
    with open(app_rel_key, 'w') as fp:
        json.dump(relation_app, fp)

    with open(example_rel_key, 'w') as fp:
        json.dump(relation_example, fp)

    json_relation_method = json.dumps(relation_method)
    json_relation_app = json.dumps(relation_app)
    json_relation_example = json.dumps(relation_example)

    s3.put_object(Bucket=bucket_name, Key=method_rel_key, Body=json_relation_method, ACL='public-read')
    s3.put_object(Bucket=bucket_name, Key=app_rel_key, Body=json_relation_app, ACL='public-read')
    s3.put_object(Bucket=bucket_name, Key=example_rel_key, Body=json_relation_example, ACL='public-read')