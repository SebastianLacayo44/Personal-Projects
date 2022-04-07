#!/usr/bin/env python
# coding: utf-8

# # Import Modules and Data

# In[1]:


# import pandas 

import pandas as pd
import numpy as np
pd.set_option("display.max_rows", None)
pd.options.display.float_format = '{:20,.2f}'.format # format currency 
pd.options.mode.chained_assignment = None

# import raw data 

datafile = 'Desktop/data/country_partner_sitcproduct2digit_year.dta'

col = ['year','export_value',
       'import_value','location_code',
       'partner_code', 'sitc_product_code']

df = pd.read_stata(datafile, columns = col)

# import cpi data

cpi = pd.read_excel('Desktop/data/CPI_Conversion.xlsx')

# import SITC product data

sitc_pc = pd.read_excel('Desktop/data/SITC_Conv.xlsx')

# import GDP data

gdp_data = pd.read_csv('Desktop/data/GDP(Constant).csv')


# # Create the Excel Generator Function

# In[2]:


def raw_to_excel(df, source_countries, partner_countries):
    """
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
     
    """
    assert type(source_countries) is list, "Please provide {} in a list".format(source_countries)
    assert type(partner_countries) is list, "Please provide {} in a list".format(partner_countries)
    
    cpi = pd.read_excel('Desktop/data/CPI_Conversion.xlsx')
    
    for source in source_countries:
        # iterate through all source countries 
        
        assert len(source) == 3, "Please provide countries in alpha-3 or ISO 3166-1 format"
        
        # create a df with source country and partner countries

        source_partner = df[df.location_code.isin([source]) & df.partner_code.isin(partner_countries)]
        
        # reformat year 
        
        source_partner['year'] = pd.to_datetime(source_partner['year'], format='%Y').dt.year
        
        # adjust cpi data
        
        cpi['CPI 2020'] = cpi['CPI 2020'].astype(int)
        cpi['CPI 2020'] = pd.to_datetime(cpi['CPI 2020'], format='%Y').dt.year
        cpi.rename(columns = {'Year ':'CPI 2020', 'CPI 2020':'year'}, inplace = True)
        
        # import SITC product code data
        
        sitc = sitc_pc[sitc_pc['Commodity Code'].apply(lambda x: str(x).isdigit())] # remove non-numerical codes
        sitc['Commodity Code'] = sitc['Commodity Code'].astype(int)
        sitc.rename(columns = {'Commodity Code':'sitc_product_code'}, inplace = True)
        
        # merge cpi and SITC product data
        
        source_partner['sitc_product_code'] = source_partner['sitc_product_code'].astype(int)
        sp_sitc_code = source_partner.merge(cpi, on ='year', how = 'left')
        sp_cpi = sp_sitc_code.merge(sitc, on ='sitc_product_code', how = 'left')
        
        # adjust for inflation 
        
        adjusted_df = sp_cpi.copy()
        adjusted_df['Adjusted Exports'] = (115.157 / sp_cpi['CPI 2020']) * sp_cpi['export_value']
        adjusted_df['Adjusted Imports'] = (115.157 / sp_cpi['CPI 2020']) * sp_cpi['import_value']
        
        ### This portion begins the analysis
        
        # Average yearly trade 
        
        avg_df = adjusted_df.copy()
        avg_df = avg_df.groupby(['year']).mean()
        
        # Net trade flows
        
        net_df = adjusted_df.copy()
        net_df = net_df.groupby(['year']).sum()
        net_df['net exports'] = net_df['Adjusted Exports'] - net_df['Adjusted Imports']
        net_df['Export percentage']= (net_df['Adjusted Exports']/net_df['Adjusted Exports'].sum())*100
        net_df['Import percentage']= (net_df['Adjusted Imports']/net_df['Adjusted Imports'].sum())*100
        
        # Commodity average
        
        comm_avg = adjusted_df.copy()
        comm_avg = comm_avg.groupby(['Commodity description']).mean()
        
        # Commodity sum
        
        comm_sum = adjusted_df.copy()
        comm_sum = comm_sum.groupby(['Commodity description']).sum()
        comm_sum['net exports'] = comm_sum['Adjusted Exports'] - comm_sum['Adjusted Imports']
        percentage_ex = comm_sum['Adjusted Exports']/comm_sum['Adjusted Exports'].sum()
        percentage_im = comm_sum['Adjusted Imports']/comm_sum['Adjusted Imports'].sum()
        comm_sum['Export percentage']= (percentage_ex)*100
        comm_sum['Import percentage']= (percentage_im)*100
        
        # Net country and year 
        
        ncy = adjusted_df.copy()
        ncy = ncy.groupby(['partner_code','year']).sum()
        ncy['net exports'] = ncy['Adjusted Exports'] - ncy['Adjusted Imports']
        
        # Granular 
        
        gran = adjusted_df.copy()
        gran = gran.groupby(['partner_code','year','Commodity description']).sum()
        gran['net exports'] = gran['Adjusted Exports'] - gran['Adjusted Imports']
        
        ### Percent of GDP
        
        gdp = gdp_data.replace({'..':np.nan})
        gdp_source = gdp[['year',source]]
        gdp_source[source] = gdp[source].astype(float)
        gdp_source = gdp_source.dropna(subset = [source], axis = 0, how = 'all') # drop missing years
        
        # Merge with CPI
        
        gdp_adjusted = pd.merge(gdp_source, cpi, on = 'year', how = 'left')
        gdp_adjusted['Adjusted GDP'] = (115.157 / gdp_adjusted['CPI 2020']) * gdp_adjusted[source]
        
        # Merge with Adjusted Data
        
        adj = adjusted_df.groupby('year').sum()
     
        pogdp = adj.merge(gdp_adjusted, on = 'year', how = 'left')
        pogdp['Imports + Exports'] = pogdp['Adjusted Exports'] + pogdp['Adjusted Imports']
        pogdp['% of GDP'] = (pogdp['Imports + Exports']/pogdp['Adjusted GDP']) * 100 
        
        # To excel 
        
        with pd.ExcelWriter('{}_TradeLogs.xlsx'.format(source)) as writer:  
            avg_df.to_excel(writer, sheet_name='Yearly Averages')
            net_df.to_excel(writer, sheet_name='Yearly Sums and Net')
            comm_avg.to_excel(writer, sheet_name='Commodity Averages')
            comm_sum.to_excel(writer, sheet_name='Commodity Sums and Net')
            ncy.to_excel(writer, sheet_name='Net Country and Year')
            gran.to_excel(writer, sheet_name='Full Trade Log')
            pogdp.to_excel(writer, sheet_name='PercentofGDP.xlsx')
        
        print("Success! Please look for a file called {}_TradeLogs.xlsx in your current directory".format(source))


# In[5]:


raw_to_excel(df,['IRN'],['EGY','SWZ'])

