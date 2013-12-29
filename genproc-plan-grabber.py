# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# genproc-plan-grabber.py
# Author: Maxim Dubinin (sim@gis-lab.info)
# About: Grab http://plan.genproc.gov.ru/plan2014 data on ����������, creates two tables linked with unique id, policemen and locations they are responsible for.
# Created: 22:05 28.12.2013
# Usage example: python genproc-plan-grabber.py
# ---------------------------------------------------------------------------

import urllib
import urllib2
from bs4 import BeautifulSoup
import sys
import os
import ucsv as csv
from datetime import datetime
import time

def download_org(link,id):
    numtries = 5
    for i in range(1,numtries+1):
        try:
            #user_agent = "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)"
            #headers = { 'User-Agent' : user_agent }
            #values = {'name' : 'John Doe','language' : 'Python' }
            #data = urllib.urlencode(values)
            #req = urllib2.Request(link, data, headers)
            #u = urllib2.urlopen(req)
            u = urllib2.urlopen(link)
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server for ID:' + id + ' Reason: ' + str(e.reason) + '.' + ' Attempt: ' + str(i)
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request for ID: ' + id + ' Error code: ' + str(e.code) + '.' + ' Attempt: ' + str(i)
            success = False
            time.sleep(3)
        else:
            f = open("data/" + id + ".html","wb")
            f.write(u.read())
            f.close()
            print("Listing for id " + id + " was downloaded")
            success = True
            break
    
    return success
    
def parse_org(id):
    id_data = open("data/" + id + ".html")
    soup = BeautifulSoup(''.join(id_data.read()))
    maintable = soup.find("table", { "class" : "plan_filter" })
    if str(maintable) == 'None':
        name = addrloc_jur = addrloc_ip = addr_act = addr_obj = ogrn = inn = goal = osn_datestart = osn_dateend = osn_datestart2 = osn_other = check_month = check_days = check_hours = check_form = check_org = "EMPTY"
        f_errors.write(id + "," + link + ", id is empty" + "\n")
    else:
        tds = maintable.findAll("td")
        
        if len(tds) < 33:
            name = addrloc_jur = addrloc_ip = addr_act = addr_obj = ogrn = inn = goal = osn_datestart = osn_dateend = osn_datestart2 = osn_other = check_month = check_days = check_hours = check_form = check_org = "ERROR"
            f_errors.write(id + "," + link + ", incorrect data" + "\n")
        else:
            name = list(tds[1].strings)[0]
            addrloc_jur = list(tds[3].strings)[0]
            addrloc_ip = list(tds[5].strings)[0]
            addr_act = list(tds[7].strings)[0]
            addr_obj = list(tds[9].strings)[0]
            ogrn = list(tds[11].strings)[0]
            inn = list(tds[13].strings)[0]
            goal = list(tds[15].strings)[0]
            osn_datestart = list(tds[17].strings)[0]
            osn_dateend = list(tds[19].strings)[0]
            osn_datestart2 = list(tds[21].strings)[0]
            osn_other = list(tds[23].strings)[0]
            check_month = list(tds[25].strings)[0]
            check_days = list(tds[27].strings)[0]
            check_hours = list(tds[29].strings)[0]
            check_form = list(tds[31].strings)[0]
            check_org = list(tds[33].strings)[0]
            
    #write to id file
    csvwriter.writerow(dict(ID=id,
                            URL=link,
                            NAME=name,
                            ADDRLOC_JUR=addrloc_jur.strip(),
                            ADDRLOC_IP=addrloc_ip.strip(),
                            ADDR_ACT=addr_act.strip(),
                            ADDR_OBJ=addr_obj.strip(),
                            OGRN=ogrn.strip(),
                            INN=inn.strip(),
                            GOAL=goal.strip(),
                            OSN_DATESTART=osn_datestart.strip(),
                            OSN_DATEEND=osn_dateend.strip(),
                            OSN_DATESTART2=osn_datestart2.strip(),
                            OSN_OTHER=osn_other.strip(),
                            CHECK_MONTH=check_month.strip(),
                            CHECK_DAYS=check_days.strip(),
                            CHECK_HOURS=check_hours.strip(),
                            CHECK_FORM=check_form.strip(),
                            CHECK_ORG=check_org.strip()))

if __name__ == '__main__':
    args = sys.argv[1:]
    start_id = int(args[0])
    end_id = int(args[1]) + 1
    
    f_errors = open("errors" + "_" + str(start_id) + "_" + str(start_id) + ".csv","a")
    if not os.path.exists("data"): os.makedirs("data")
    
    fieldnames_data = ("ID","URL","NAME","ADDRLOC_JUR","ADDRLOC_IP","ADDR_ACT","ADDR_OBJ","OGRN","INN","GOAL","OSN_DATESTART","OSN_DATEEND","OSN_DATESTART2","OSN_OTHER","CHECK_MONTH","CHECK_DAYS","CHECK_HOURS","CHECK_FORM","CHECK_ORG")
    f_data = open("data" + "_" + str(start_id) + "_" + str(start_id) + ".csv","wb")
    csvwriter = csv.DictWriter(f_data, fieldnames=fieldnames_data)
    
    for id in range(start_id,end_id):
        id = str(id)
        link = "http://plan.genproc.gov.ru/plan2014/detail.php?ID=" + id
        
        success = download_org(link,id)
        if success == True:
            parse_org(id)
        else:
            f_errors.write(id + "," + link + ", unavailable" + "\n")
        
    f_data.close()
    f_errors.close()