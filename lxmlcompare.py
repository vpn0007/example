import xmltodict
from deepdiff import DeepDiff
from datetime import datetime 
from deepdiff.helper import SetOrdered
import os


def wrap_single_objects_as_lists(obj):
    """
    Recursively wraps single dictionary objects as lists to ensure 
    consistency when parsing XML.
    """
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, dict):  # If value is a single dict, convert to list
                obj[key] = [wrap_single_objects_as_lists(value)]
            if isinstance(value, str):  # If value is a single string, convert to list
                obj[key] = [wrap_single_objects_as_lists(value)]
            elif isinstance(value, list):
                obj[key] = [wrap_single_objects_as_lists(v) for v in value]
    return obj

def normalize_xml(file_path):
    """Loads XML, parses it into a dictionary, and ensures lists where needed."""
    with open(file_path, "rw") as f:
        xml_dict = xmltodict.parse(f.read(), dict_constructor=dict)
    return wrap_single_objects_as_lists(xml_dict)



#comparing the two files using DeepDiff 
def compare_cda(file1, file2):
 
    """Compares two CDA XML documents after normalizing."""
    xml1 = normalize_xml(file1)
    xml2 = normalize_xml(file2)

    diff = DeepDiff(xml1, xml2, ignore_order=True)

    return diff
    
             

#method to get categories of the differences
def categories_difference(diff):
    categories = {"item added":[] , "item deleted":[],"item updated":[],"others":[]}

    for diff_type in diff :
        if diff_type  in ["iterable_item_added","dictionary_item_added"]:
            categories["item added"].append(diff[diff_type])
        elif diff_type  in ["iterable_item_removed","dictionary_item_removed"]:
            categories["item deleted"].append(diff[diff_type])
        elif diff_type =="values_changed" :
            categories["item updated"].append(diff[diff_type])
        else:
            categories["others"].append(diff[diff_type])
            
    return categories




    
