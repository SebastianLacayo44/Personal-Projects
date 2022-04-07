# Projects

This repository stores some personal projects! Unlike my work repository, all programs and code in this repository should be easily reproducable.

# Projects

1. [Trade Flows Generator](#Trade Flows)

## Trade Flows

flows



    This function converts international trade data (SITC, Rev.2) raw trade data provided 
    by the Harvard Dataverse into a more digestible excel notebook for SMEs. 
    
    Ideally, this function is used to compare a single country's trade flows with 
    one or more countries. For every country passed via the source country argument, it will
    produce an excel file with aggregate trade data with the list of partner countries. The countries
    should be provided in alpha-3 or ISO 3166-1 format. 
    
    All figures are adjusted for inflation in (CPI 2010 = 100 ; shorturl.at/ceCS4).
    
    Data sources:
        raw trade data - https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/H8SFD2
        cpi data - shorturl.at/ceCS4 (data.worldbank.org)
        sitc product data - https://unstats.un.org/unsd/classifications/Econ (SITC Rev. 2)
        GDP data - https://www.worldbank.org/en/home
