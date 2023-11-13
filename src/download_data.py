"""
This file is for downloading and uncompressing the Lakh Million Song Dataset (lmd) data

Credits for data - Garvey Li
"""

"""
**IMPORTANT** 

Download these files (INTO THE resources/ FOLDER)
    http://hog.ee.columbia.edu/craffel/lmd/lmd_aligned.tar.gz
    http://hog.ee.columbia.edu/craffel/lmd/lmd_matched_h5.tar.gz
                     
**IMPORTANT**
"""

import requests
import tarfile

# Links and destinations for compressed data
url1 = 'http://hog.ee.columbia.edu/craffel/lmd/lmd_aligned.tar.gz'
url2 = 'http://hog.ee.columbia.edu/craffel/lmd/lmd_matched_h5.tar.gz'
target_path1 = 'lmd_aligned.tar.gz'
target_path2 = 'lmd_matched_h5.tar.gz'
        
# Download our compressed Files
def download_lmd_data(out_destination="../resources/"):
    
    response = requests.get(url1, stream=True)
    if response.status_code == 200:
        with open(out_destination+target_path1, 'wb') as f:
            f.write(response.raw.read())
            
    response = requests.get(url2, stream=True)
    if response.status_code == 200:
        with open(out_destination+target_path2, 'wb') as f:
            f.write(response.raw.read())

# Decompress our files
def decompress_lmd_data(out_destination="../data/"):
    f = tarfile.open("../resources/lmd_aligned.tar.gz")
    f.extractall(out_destination)
    f.close

    f = tarfile.open("../resources/lmd_matched_h5.tar.gz")
    f.extractall(out_destination)
    f.close