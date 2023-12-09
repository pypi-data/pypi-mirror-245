# cdg-reader
A package for climate researchers to check for information on the NCAR Climate Data Guide to compare to a user netCDF file.


## Installation 
The easiest way to install the latest version of `cdg-reader` is using `pip':  

```
pip install cdg_reader
```

## Documentation 

Check out the NCAR Climate Data Guide for a wealth of information: https://climatedataguide.ucar.edu/

## Intro 

The field of climate data is diverse and expanding.

The Climate Data Guide provides concise and reliable information on the strengths and limitations of the key observational data sets, tools and methods used to evaluate Earth system models and to understand the climate system. The Guide publishes data summaries with access links, intercomparisons, and expert commentaries on the utility of climate data for addressing a wide variety of questions in climate science. The Guide has helped over a million readers from around the world gain an insider's perspective on data ranging from simple climate indices to state-of-the-art data assimilation products (e.g. reanalysis) to paleoclimate records from tree rings and corals.

This package utilizes the xarray environment to help access key information and insights from Climate Data Guide that may be valuable to understanding the key strengths and limitations of your dataset.


'ncar_data_guide' will return up to (3) results from the database relevant to your dataset.

```
   import cdg_reader as cdg
    
   # Use your netCDF file to search the guide for relevant information.
   cdg.check_NCAR('file.nc')

```

## Function

This package utilizes xarray and standard python packages xml.etree.ElementTree and urllib.request to grab information from the NCAR Climate Data Guide. Below is the intended flow of the package for understanding of the function.

The main function is check_NCAR, which takes the argument of the file path of the user NetCDF file.
```
check_NCAR('file.nc')
```

The package will convert the file to an xarray object, and then scan the attributes of the object for key terms that will be used to find relevant information on the Climate Data Guide. It will gather these terms as a list of strings. This will contain up to 5 words to be used as search terms.

```
read_netcdf(netCDF_file_location)
get_search_words(netCDF_file_conveted_to_xarray)
```

The package will perform a search of the Climate Data Guide using the urllib.request package, utilizing one search term at a time. This will ping the website and return the result as an xml file, read into python as a string. The package then uses the xml.etree.ElementTree package to convert this string to a list of dictionaries, where each dictionary contains the attributes of a page on the Climate Data Guide. The package will then filter these search results using two methods:
1. If the user netCDF file has a time component, filter the results from the climate data guide that have similar time components.
2. Using the search words generated from the user netCDF file earlier, compare the CDG results to the search words to see where there are similarities.

```
search_NCAR(list_of_search_words, netCDF_file_conveted_to_xarray)
   get_xml_file(search_word_in_list)
   xml_to_dict(result_xml_file_as_string)

   filter_results(netCDF_file_conveted_to_xarray, list_of_dictionary_results_from_NCAR, list_of_search_words)
      check_time_similarity(netCDF_file_conveted_to_xarray, list_of_dictionary_results_from_NCAR)
      check_key_terms(list_of_search_words, list_of_dictionary_results_from_NCAR)
```
Once the two filter methods are used, the package will print to the terminal up to 3 results from the resulting list. These results can then be found on the NCAR Climate Data Guide website.

```
 print_results(filtered_list_of_results_from_NCAR)

```
