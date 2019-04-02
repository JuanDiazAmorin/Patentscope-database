
# The following script provide 74 millions of registers about patents. This informations is retrieved from WIPO dataset.
# Variables are: 

# 'year': year that the patent was granted
# 'date': includes day, month and year
# 'country':  country office from which the patent was granted
# 'inventor': person who registered the patent. The owner
# 'insitution': inventor's affiliation

#CHANGE THE chromedriver PATH

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

chromedriver = 'C:/Users/juan.diaz/Desktop/chromedriver'
driver = webdriver.Chrome(chromedriver)

start_year=1990
end_year =2018

year = []
date = []
country = []
institution = []
code =[]
inventor = []

driver.get('https://patentscope.wipo.int/search/en/search.jsf')
wait = 100


start = time.time()
for k in range(start_year, end_year+1):

    content = BeautifulSoup(driver.page_source,'html.parser')
    year_selection = driver.find_element_by_id('simpleSearchForm:j_idt349_focus')
    year_selection.send_keys('Dates')
 
    
    put_year = driver.find_element_by_id('simpleSearchForm:fpSearch').clear()
    put_year = driver.find_element_by_id('simpleSearchForm:fpSearch')
    put_year.send_keys(str(k))
    
    driver.find_element_by_id('simpleSearchForm:commandSimpleFPSearch').click()
    driver.implicitly_wait(wait)
    
    length  = driver.find_element_by_id('resultListOptionsForm:lengthOption_focus')
    length.send_keys('200')
    driver.implicitly_wait(wait) 
    
    content = BeautifulSoup(driver.page_source,'html.parser')
    
    values = [text for text in content.find(id="resultListFormTop:page_navigator").stripped_strings]
    number = int(values[1].replace(" ","")[1:])
    
    for x in range(1,number+1):
        page = driver.find_element_by_id('resultListFormTop:inputGoToPage').clear()
        page = driver.find_element_by_id('resultListFormTop:inputGoToPage')
        page.send_keys(x)
        driver.implicitly_wait(wait) 
        
        driver.find_element_by_id('resultListFormTop:linkGoToPage').click()
        driver.implicitly_wait(wait) 
        
        tables = content.find_all(class_='ui-panelgrid ui-widget no-border no-background result-table-grid table-fit-content')
        
        for i in range(0, len(tables)):
            table = tables[i]
            m1 = table.find(id='resultListForm:resultTable:'+str(i)+':resultListTableColumnCtr').get_text()
            country.append(m1)
            m2 = table.find(id='resultListForm:resultTable:'+str(i)+':resultListTableColumnPubDate').get_text()
            date.append(m2)
            m3 = table.find(id='resultListForm:resultTable:'+str(i)+':resultListTableColumnIPC').get_text().replace('\n','')
            code.append(m3)
            m4 = table.find(id='resultListForm:resultTable:'+str(i)+':resultListTableColumnApplicant').get_text()
            institution.append(m4)
            m5 = table.find(id='resultListForm:resultTable:'+str(i)+':resultListTableColumnInventor').get_text()
            inventor.append(m5)
            m6 = k
            year.append(m6)
    
    driver.get('https://patentscope.wipo.int/search/en/search.jsf')
    driver.implicitly_wait(wait) 

    
data = {'year':year, 'date':date, 'code':code, 'country':country,
        'institution':institution,'inventor':inventor}
data = pd.DataFrame(data=data)
end = time.time()
print('Elapsed time:',end-start)


