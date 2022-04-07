# Projects

This repository stores some personal projects! Unlike my work repository, all programs and code in this repository should be easily reproducable.

# Projects

1. [Trade Flows](#Trade-Flows)

## Trade Flows

This script was developed as part of a research project with a professor of international relations from my undergraduate institution. This script converts
international trade data (SITC, Rev.2) provided by the Harvard Dataverse into a more digestible excel notebook for SMEs. This function is used 
to compare a single country's trade flows with one or more countries. For every country passed via the source country argument, it will produce an excel 
file with aggregate trade data with the list of partner countries. Arguments should be passed in alpha-3 or ISO 3166-1 format and all figures are adjusted
for inflation (CPI 2010 = 100 ; shorturl.at/ceCS4). All the data is provided except for the raw trade data which is too large to upload. However, there
is a link below to the data which is publically available.

Data sources:
- Trade flows data - https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/H8SFD2
- SITC product data - https://unstats.un.org/unsd/classifications/Econ (SITC Rev. 2)
- CPI data - shorturl.at/ceCS4 (data.worldbank.org)
- GDP data - https://www.worldbank.org/en/home
