# -*- coding: UTF-8 -*-

'''
Created on 21/05/2011

@author: ThiagoP
@contact: tpborion@gmail.com
'''


import sys, os

# Sets working directory to the script directory
os.chdir(os.path.abspath(os.path.realpath(__file__ + "/..")))
sys.path.append(os.path.abspath(".."))

from tools import *
from time import strftime
from DBManager import DBCursor
from objects import *
from os import path
from ConfigParser import RawConfigParser



# This function shall be called to capture jobs from a url
def jobs_search(url, post=''):
    
    if verbose == False:
        show = toLimbo
    elif verbose == True:
        show = toScreen
    elif verbose == 'log':
        show = toLog
    
    
    # Get the MAXDUPLICATE parameter in the config file
    max_duplicate = CONFIG_FILE.get('Limits', 'MAXDUPLICATE')
    duplicates = 0
    
    # Resquest the content
    if post <> '':
        html = get_url(url, post)
    else:
        html = get_url(url)

    # Configure a cursor (singleton) to the database
    DBCursor(CONFIG_FILE)
    
    # Get the advertiser
    advs = Advertiser.getFromConfig(CONFIG_FILE)
    assert len(advs) == 1
    adv = advs[0]

    # Pattern to get the links
    while "<td align='left' valign='top'><b><a href='" in html:

        # Get a link
        html = cut(html, "<td align='left' valign='top'><b><a href='", 'no', 'first', 'end')
        link = cut(html, "'", 'no', 'first', 'begin')
        
        # Mount link
        link = normalize(link)
        job = get_url(link)
        
        # Job reference code
        ref = cut(job, "Job Code:</td>", 'no', 'first', 'end')
        ref = cut(ref, "<td valign='top' class='formFieldNormal' colspan=1 width='100%'><b>", 'no', 'first', 'end')
        ref = cut(ref, '</', 'no', 'first', 'begin')
        
        
        # Get job title
        job_title = cut(job, "<td colspan=2><hr width='100%' size='1' color='silver'></td></tr><tr><td colspan=2><b>", 'no', 'first', 'end')
        job_title = cut(job_title, '</', 'no', 'first', 'begin')
        job_title = normalize(job_title)
        
        # Time of the capture
        date_time = strftime("%Y-%m-%d %H:%M:%S")
        
        # Location of the job
        location = cut(job, 'nowrap>Location:</td>', 'no', 'first', 'end')
        location = cut(location, "<td valign='top' class='formFieldNormal' colspan=1 width='100%'><b>", 'no', 'first', 'end')
        location = cut(location, '</', 'no', 'first', 'begin')
        location = normalize(location)
        
        if checkExcludes(location):
            show("Location in exclude list, skipping..")
            continue  
        
        # Location of the job
#        country = cut(job, 'nowrap>Location:</td>', 'no', 'first', 'end')
#        country = cut(country, "<td valign='top' class='formFieldNormal' colspan=1 width='100%'><b>", 'no', 'first', 'end')
#        country = cut(country, '</', 'no', 'first', 'begin')
#        country = normalize(country)
        country = CONFIG_FILE.get('Advertiser', 'COUNTRYCODE')        
        
        # Position (P = Permanent, T = Temporary, C = Contract)
#        position = cut(job, '<td class="descvalue"  align="left">', 'no', 'first', 'end')
#        position = cut(position, '</td>', 'no', 'first', 'begin')
#        position = normalize(position)
        position = 'P'
    
        # Salary
#        salary = cut(job, '<td class="descvalue"  align="left">', 'no', 'first', 'end')
#        salary = cut(position, '</td>', 'no', 'first', 'begin')
#        salary = normalize(salary)
        salary = ''
        
        # Job description
        desc = cut(job, '<b>Description</b></td></tr>', 'no', 'first', 'end')
        desc = cut(desc, "<tr><td align='left'><br>", 'no', 'first', 'begin')
        desc = sanitize(desc)
        desc = normalize(desc)
        
        # Normalize the HTML only after the capture to facilitate the stablishment of the patterns
        job = normalize(job)

        # Mount a unique string to use on check for duplicates        
        checkString = adv.adv_ref + '|' + ref
        
        # Checking
        if checkScrapeVacancy(checkString, CONFIG_FILE.get('Script', 'NAME')):
            show("Aready exists, skipping...")
            duplicates += 1
            if duplicates < max_duplicate:
                continue
            else:
                break
          
        # Print to screen
        show("\n\n=============================================================================================================================================")
        show("Link: " + link)
        show("Ref: " + ref)
        show("Job title: " + job_title)
        show("Datetime: " + date_time)
        show("Location: " + location)
        show("Country: " + country)
        show("Position: " + position)
        show("Salary: " + salary)
        show("Job:") #+ job)
        show("---------------------------------------------------------------------------------------------------------------------------------------------")
        show("Description: \n")# + desc)
        show("=============================================================================================================================================")
        
        ############################################
        # Comment on test, uncomment on production #
        # Create a new vacancy object
        v = Vacancy()
        
        delattr(v, "vac_ref") #v.vac_ref = 0
        
        v.vac_cre_dte = date_time
        v.vac_status = 1
        v.vac_job_title = job_title
        v.vac_advertiser = adv.adv_ref
        v.vac_phone = adv.adv_tel #site or adv_tel
        v.vac_contact = adv.adv_cont_1 #site or adv_cont_1
        v.vac_title = adv.adv_title #site or adv_title
        v.vac_needed = 0
        v.vac_date = None #DATETIME
        v.vac_duration = 0
        v.vac_dur_type = 1
        v.vac_wk_hours = None
        v.vac_sta_time = None
        v.vac_end_time = None
        v.vac_ot_wk = None
        v.vac_ot_sat = None
        v.vac_ot_sun = None
        v.vac_pay_rate = None
        v.vac_contract = None
        v.vac_flex = None
        v.vac_fax = None
        v.vac_add1 = adv.adv_add1
        v.vac_add2 = adv.adv_add2
        v.vac_add3 = adv.adv_add3
        v.vac_add4 = adv.adv_add4
        v.vac_pcode = adv.adv_pcode
        v.vac_machine = "Web"
        v.vac_modified = date_time
        v.vac_user = "Robot"
        v.vac_text = job
        v.vac_locn = location
        v.vac_type = "P" # P=Permanent, T=Temporary
        v.vac_email_sent = None
        v.vac_board = None
        v.vac_salary = salary
        v.vac_advjob = ref
        v.vac_effective = date_time #DATETIME
        v.vac_email = adv.adv_email #from site, if it hasn't, from adv
        v.vac_url = link
        v.vac_jd = desc
        v.vac_object = None
        v.vac_lsource = "" # TODO: Customer site?
        v.vac_f_source = 1
        v.vac_f_sector = CONFIG_FILE.get('Advertiser', 'SEC_1') #from config
        v.vac_f_sector2 = CONFIG_FILE.get('Advertiser', 'SEC_2') #from config
        v.vac_f_sector3 = CONFIG_FILE.get('Advertiser', 'SEC_3') #from config
        v.vac_f_region = None
        v.vac_agencies = None
        v.vac_job_category = None
        v.vac_country = country #from site or config file
        v.vac_county = None
        
        sv = ScrapeVacancy()
        sv.sv_our_ref = 0
        sv.sv_ref = checkString # MUST BE UNIQUE (DO NOT FORGET TO CHANGE IN 'checkScrapeVacancies()'
        sv.sv_script = CONFIG_FILE.get('Script', 'NAME') 
        sv.sv_date = date_time
                 
        v.save()
        
        v = Vacancy.get(vac_advertiser = v.vac_advertiser, vac_advjob = v.vac_advjob, vac_url = v.vac_url)[0]
        
        sv.sv_our_ref = v.vac_ref
        sv.save()
        ############################################
        
        
        

###############################################
#                   MAIN                      #
###############################################
if __name__ == "__main__":
    # Set configuration file
    CONFIG_FILE = RawConfigParser()
    CONFIG_FILE.read("./Config.ini")
    
    # To print on the screen while capturing
    verbose = True
    
    #Set Verbose
    jobs_search("http://tbe.taleo.net/NA7/ats/careers/searchResults.jsp?org=RULEFINANCIAL&cws=1")
    
    
    