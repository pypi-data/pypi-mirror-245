#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 18:51:07 2023

@author: dylangrant
"""

import xml.etree.ElementTree as et
import urllib.request
import xarray as xr


def read_netcdf(file):
    """Read in netCDF file to xarray object
    
    Parameters
    ----------
    file (string) : string netCDF file location
    
    Returns
    -------
    xr.open_dataset(file) (xarray object) : NetCDF file converted to xarray object
    
    """

    return xr.open_dataset(file)


def get_search_words(root):
    """Pull key terms from xarray attributes to search the NCAR Climate Data Guide
    
    Parameters
    ----------
    root (xarray object) : xarray object of the user NetCDF file
    
    Returns
    -------
    search_list_unique (list of strings) : List of key terms to search the NCAR database
    
    """
    
    stopwords = ['i','me','my','myself','we','our','ours','ourselves','you','you\'re','you\'ve',
                     'you\'ll','you\'d','your','yours','yourself','yourselves','he','him','his',
                     'himself','she','she\'s','her','hers','herself','it','it\'s','its','itself',
                     'they','them','their','theirs','themselves','what','which','who','whom','this',
                     'that','that\'ll','these','those','am','is','are','was','were','be','been','being',
                     'have','has','had','having','do','does','did','doing','a','an','the','and','but','if',
                     'or','because','as','until','while','of','at','by','for','with','about','against','between',
                     'into','through','during','before','after','above','below','to','from','up','down','in','out',
                     'on','off','over','under','again','further','then','once','here','there','when','where','why',
                     'how','all','any','both','each','few','more','most','other','some','such','no','nor','not',
                     'only','own','same','so','than','too','very','s','t','can','will','just','don','don\'t',
                     'should','should\'ve','now','d','ll','m','o','re','ve','y','ain','aren','aren\'t','couldn',
                     'couldn\'t','didn','didn\'t','doesn','doesn\'t','hadn','hadn\'t','hasn','hasn\'t','haven',
                     'haven\'t','isn','isn\'t','ma','mightn','mightn\'t','mustn','mustn\'t','needn','needn\'t',
                     'shan','shan\'t','shouldn','shouldn\'t','wasn','wasn\'t','weren','weren\'t','won','won\'t',
                     'wouldn','wouldn\'t','data','set','author']

    

    
    #Separate attributes into a list of keys, 
    #a list of words from the text, and a dictionary with the words separated into individual strings
    
    attr_keys = []
    attr_dict = {}
    
    for key in list(root.attrs.keys()):
        attr_value = root.attrs[key]
        
        # Check the data type of the attribute value
        if isinstance(attr_value, str):
            # If it's a string, split it
            attr_value = attr_value.split()
            attr_keys.append(key)
            attr_dict[key] = attr_value
    
    attr_list = [word for words in attr_dict.values() for word in words]
    

    #Check for duplicate words and removes small words and stop words
    check_dup={}
    dup_dict = {i:attr_list.count(i) for i in attr_list}
    dup_temp = dict(dup_dict)
    
    for i in dup_temp:
        if dup_temp[i]==1 or len(i)<3 or i.lower() in stopwords:
            del dup_dict[i]
    
    dup_dict_sorted = dict(sorted(dup_dict.items(), key=lambda item: item[1], reverse=True))
    
    #Convert duplicates dictionary into list
    dup_list = [i for i in dup_dict_sorted]
    
    #Check if any of the top search terms are in the attributes
    key_terms = ["hadisst", "era5", 'ersst','gpm','imerg', 'gpcp', 'gpcc', 'mswep', 'persiann','reanalysis','sst']
    attr_key_terms = []
    for i in attr_list:
        if i.lower() in key_terms:
            attr_key_terms.append(i)
    attr_key_terms_unique = [x for i, x in enumerate(attr_key_terms) if x not in attr_key_terms[:i]]
    
    #get title words
    title_terms = []

    attr_keys_lower = [key.lower() for key in attr_keys]
    if "title" in attr_keys_lower:
        title_terms = [term for term in attr_dict[attr_keys[attr_keys_lower.index("title")]] if term not in stopwords]
    
    #check if title words are seen more than once, if so, highly ranked
    rank1_terms = [i for i in title_terms if i in dup_dict]
    
    #rank all terms
    search_list = rank1_terms + attr_key_terms_unique + dup_list
    search_list_unique = [x for i, x in enumerate(search_list) if x not in search_list[:i]]
    
    #Checks if the final list is empty. If so, add all terms from the attributes not in stopwords
    if len(search_list_unique)<1:
        search_list_unique = [i for i in attr_list if i not in stopwords]

    #Return the first five terms in the search list
    max_terms=5
    if len(search_list_unique)<max_terms:
        return search_list_unique
    else:
        return search_list_unique[0:max_terms]



def search_NCAR(terms,xarr_file):
    """Search the NCAR database for relevant information to the netCDF file
    
    Parameters
    ----------
    terms (list of strings) : List of search terms to search the NCAR database
    xarr_file (xarray object) : xarray object of original netCDF file
    
    Returns
    -------
    filter_results(xarr_file,data,terms) (list of dictionaries) : Ordered list of result attributes from the NCAR CDG database
    
    """
    
    
    #Iterate through the search terms.
    #If the search provides no results, go to the next term
    for i in terms:
        xml_data = get_xml_file(i)
        data = xml_to_dict(xml_data)
        if len(data)>0:
            break
    
    
    def check_time_similarity(xarr,xml_input):
        """Check the similarity of the time bounds of the netCDF file with the NCAR database results
        
        Parameters
        ----------
        xarr (xarray object) : xarray object of user NetCDF file
        xml_input (list of dictionaries) : list of dictionaries pulled from NCAR CDG database from search terms
        
        Returns
        -------
        results (list of dictionaries) : Revised list of dictionaries that have a time parameter within 50 years of the original dataset in the user NetCDF file.
        
        """
        
        results = xml_input.copy()
        
        if 'time' in xarr.dims:
            time_coords = xarr.coords['time'].values.astype('datetime64[Y]').astype(int)+1970
            time_span = [time_coords[0], time_coords[-1]]
            
            res_time=[]
            none_res=[]
            for i, j in enumerate(results):
                if j['years_of_record_start'] is None:
                    none_res.append(i)
                else:
                    res_time.append([j["years_of_record_start"],j["years_of_record_end"]])
            
            for i in reversed(none_res):
                del results[int(i)]
    
            
        #compare the years in the results vs the dataset to determine how different they are
            tolerance = 50 #years
                
            del_index = [i for i, (start, end) in enumerate(res_time) if abs(time_span[0] - start) > tolerance or abs(time_span[1] - end) > tolerance]
    
            for i in reversed(del_index):
                del results[i]
                
        return results
    
    
    def check_key_terms(terms,results):
        """Check if the NCAR database results contain multiple of the search terms
        
        Parameters
        ----------
        terms (list of strings) : list of search terms derived from the user NetCDF file
        results (list of dictionaries) : list of dictionaries pulled from NCAR CDG database from search terms
        
        Returns
        -------
        check_dict (dictionary) : Dictionary of counts of how many words from the terms input are included in each of the results input
        
        """
    
        check_dict = {i: 0 for i in range(len(results))}

        for i, item in enumerate(results):
            item_words = []
            for key, value in item.items():
                item_words.extend(str(value).split())
    
            for word in item_words:
                if word.lower() in terms:
                    check_dict[i] += 1

        return check_dict

    
    
    def filter_results(xarr,results,terms):
        """Call the filtering functions and sorts the results from the most to least important. Return 3 results max.
        
        Parameters
        ----------
        xarr (xarray object) : xarray object of user NetCDF file
        results (list of dictionaries) : list of dictionaries pulled from NCAR CDG database from search terms
        terms (list of strings) : list of search terms derived from the user NetCDF file
        
        Returns
        -------
        filtered_list (list of dictionaries) : List of dictionaries of search results ordered by how many key terms from the 
        check_key_terms function each result contains as well as filtered for time similarity per the 
        check_time_similarity function.
        
        """
        
        check_results = check_time_similarity(xarr,results)
        key_list = check_key_terms(terms,check_results)
        
        value_key_pairs = ((value, key) for (key,value) in key_list.items())
        sorted_value_key_pairs = sorted(value_key_pairs, reverse=True)
        key_list_sorted = {k: v for v, k in sorted_value_key_pairs}
        
        filtered_list = [check_results[i] for i in key_list_sorted]
        
        if len(filtered_list)<3:
            return filtered_list
        else:
            return filtered_list[0:3]
        
    #If none of the searches provided any results, return integer 0
    try:
        return filter_results(xarr_file,data,terms)
    except UnboundLocalError as e:
        return 0


def xml_to_dict(file):
    """Read in the xml file result from the NCAR database and return it as a list of dictionaries
    
    Parameters
    ----------
    file (string) : xml file converted to a string - search results from NCAR CDG website returned as a string
    
    Returns
    -------
    data dict (list of dictionaries) : List of dictionaries of search results, converted from the xml string
    
    """
    
    #Read in xml
    tree = et.fromstring(file)
    root = list(tree)
    
    
    #initialize dataframe with know attributes in search results
    data_dict = []
    
    for node in root:
        key = node.attrib.get("key")
        title = node.find("title").text
        key_limitations = node.find("field_key_limitations").text
        if(key_limitations is None):
            key_limitations = "None"
        key_strengths = node.find("field_key_strengths").text
        if key_strengths is None:
            key_strengths = "None"
        
        years = node.find("field_years_of_record").text
        if years is not None:
            years_start = int(years[5:9])
            years_end = int(years[-11:-7])
        else:
            years_start = None
            years_end = None

        collections = node.find("field_dataset_collections").text
        data_type = node.find("field_data_type").text
        ins = node.find("field_institution_and_pis")
        
        data_dict.append({"key":key, "title":title,"key_limitations":key_limitations,"key_strengths":key_strengths,
                    "years_of_record_start":years_start,"years_of_record_end":years_end,"dataset_collections":collections,
                    "data_type":data_type,"institution_and_pis":ins})
        
    return data_dict


def get_xml_file(search_term):
    """Perform a search at the NCAR climate data guide and return a python xml text object
    
    Parameters
    ----------
    search_term (string) : search term derived from the user NetCDF file
    
    Returns
    -------
    xml_content (string) : xml file converted to string - search results from NCAR CDG website returned as a string
    
    """
    
    url = f"https://climatedataguide.ucar.edu/xarray?title={search_term}"

    try:
        with urllib.request.urlopen(url) as response:
            content_type = response.getheader("Content-Type")
            if "xml" in content_type.lower():
                xml_content = response.read().decode("utf-8")
                return xml_content
            else:
                print("The response does not contain XML content.")
    except urllib.error.URLError as e:
        print(f"Error: {e}")
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e}")
    
    return None  # Return None if an error occurs or if the content is not XML

    

def print_results(res_list):
    """Print the results from the NCAR database to the terminal
    
    Parameters
    ----------
    res_list (list of dictionaries) : list of dictionaries of filtered results from the NCAR CDG database
    
    """
    
    if type(res_list) is not int and len(res_list)>0:
        print("\n\nNCAR Helpful Resources")
        
        count = 1
        for i in res_list:
            print ("\n\nResult " +str(count))
            print("\n\033[4mTitle:\033[0m\n"+i["title"])
            print("\n\033[4mKey Strengths:\033[0m\n" + i["key_strengths"].replace("::BR::", "\n"))
            print("\033[4mKey Weaknesses:\033[0m\n" + i["key_limitations"].replace("::BR::", "\n"))
            count+=1
        
        print("\nFor more information, search these results on the climate data section of the NCAR Climate Data Guide: https://climatedataguide.ucar.edu/")
    else:
        print("\nThe netCDF file did not return any close results from the NCAR Climate Data Guide.")
    return 0


class cdg_reader:

    def check_NCAR(netCDF_file):
        """Print to the screen up to (3) pages from the NCAR Climate Data Guide with relevant data to the netCDF file
    
        Parameters
        ----------
        netCDF_file (string): string path of netCDF file
        """
        
        #Read in netCDF file
        xarray_data = read_netcdf(netCDF_file)
        
        #Use netCDF to find important words in the attributes
        #These will be used as search terms to NCAR
        search_list=get_search_words(xarray_data)
        
        #Search the NCAR database and return a list of results, including title, key strengths, and key limitations
        res_list = search_NCAR(search_list,xarray_data)
        
        #Print the results
        print_results(res_list)
    
