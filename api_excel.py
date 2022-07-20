import requests
import json
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)

base_url = "https://viperdb.scripps.edu"

all_tnums_url = "/services/tnumber_index.php?serviceName=tnumbers"

tnum_members_url = "/services/tnumber_index.php?serviceName=tnumber_members&tnumber="

def tnum_url(n):
    return base_url + tnum_members_url + str(n)

#sort list of dictionaries by resolution and take the n lowest
def lowres_dictlist(dictlist, n):
    lowres = {}
    for k in dictlist.keys():
        sortres = sorted(dictlist[k], key=lambda d: (d['resolution'] is None, d['resolution']))
        lowres[k] = sortres[:n]
    return lowres


tnums_res = requests.get((base_url + all_tnums_url), verify=False)
tnums = json.loads(tnums_res.text)

tnum_members = {}
n_structures = 5
pdb_ids = []

for t in tnums:
    tnum = t['tnumber']
    members_res = requests.get(tnum_url(tnum), verify=False)
    tnum_members[tnum] = json.loads(members_res.text)

tnum_lowres = lowres_dictlist(tnum_members, n_structures)
for tnum in tnum_lowres.keys():
    for v in tnum_lowres[tnum]:
        pdb_ids.append(v['entry_id'])

###loop through ids and get coords

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

options = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "/Users/kageyamatobio/Documents/MATLAB/vpa_input"}
options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(executable_path='./chromedriver',options=options)

base_url = 'https://viperdb.scripps.edu/Info_Page.php?VDB='
for id in pdb_ids:
    try:
        res = driver.get(base_url + id)
        while True:
            try:
                dlds = driver.find_element(By.ID, "btn-downloads")
                dlds.click()
                dlbtn = driver.find_element(By.LINK_TEXT, "VIPER Coordinates")
                dlbtn.click()
                time.sleep(1)
                break
            except:
                break
    except Exception as e:
        print(e)
driver.close()

import subprocess
subprocess.check_call(['./pdb.sh', 'vpa_input'])


#run PA analysis and export to excel file

import xlwings as xw
import sys
import matlab.engine
eng = matlab.engine.start_matlab()

for pdbid in pdb_ids:
    try:
        file_url = 'vpa_input/' + pdbid + '.pdb'

        res = subprocess.check_output(['pdb_info.pl', file_url])
        app_line = res.decode().split('\n')[-2]
    
        wb = xw.Book('template.xlsx')

        ws1 = wb.sheets['1aym']

        ws1.api.copy_worksheet(after_=ws1.api)
        ws2 = wb.sheets['1aym (2)']
        try:
            ws2.name = pdbid
        except Exception as e:
            print(e)
        wb.save()
        wb.app.quit()

        script = "clear all;\n" \
                 "clc;\n" \
                 "close all\n" \
                 "" + app_line + ";\n"\
                 "pdbid = '" + pdbid + "'\n"

        with open("loadcapsid.m","w") as f:
            f.write(script)

        eng.loadcapsid(nargout=0)
        eng.SC_frankencode(nargout=0)
    except Exception as e:
        print(e)

eng.quit()

