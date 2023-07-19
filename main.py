"""
This is the main script for running the parser.
Please see config.py to change any of configs.
"""


from pysearch_tool import local_paser, git_link
from config import Base_config
from relation_dict import hirc_tree, insert, relation_dict
from pysearch_tool import dir_search
import json
import boto3








def main(Base_config):
    # f = dir_search.Search(Base_config)
    p = dir_search.Search(Base_config)
    p._search()
    method_tree = hirc_tree('CoFI')
    apps_tree = hirc_tree('37 Earth Sciences')
    example_tree = hirc_tree('37 Earth Sciences')
    # method_tree, application_tree, example_tree = build_tree(Base_config)

    for i in p.mds():
        method_tree = insert(method_tree,i)
    
    for i in p.aps():
        apps_tree = insert(apps_tree,i)
    
    for i in p.examples():
        example_tree = insert(example_tree,i)


    s3 = boto3.client('s3')
    bucket_name = 'jsonofthetree'
    json_key = 'data.json'


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





if __name__ == "__main__": 
    main(Base_config())