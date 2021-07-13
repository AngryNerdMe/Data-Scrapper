import  requests 
from bs4 import BeautifulSoup
import urllib
import pandas as pd
import json
import re

from datetime import datetime
job_title = 'IT skills'
country = 'london'
job_titles=[]
company=[]
summary=[]
start_position=10
date_collected=datetime.now().date().strftime("%d-%b-%Y")
posted_by=[]
today_date=[]
links=[]
salary=[]
area=[]
source='Indeed'

pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

#today=datetime.strftime("%d-%b-%Y")
#print(today)

locations=['London','Slough','South West London','Hemel Hempstead','East London','Croydon','St Albans','Uxbridge','Watford','Dartford','West London','Brentford','Redhill','England']
for location in locations:
    if location == 'London':
        page_number= 50
    if location == 'Slough':
        page_number= 5
    if location == 'south West London':
        page_number= 4
    if location == 'Hemel Hempstead':
        page_number= 4
    if location == 'East London':
        page_number= 4

    if location == 'Croydon':
        page_number = 3

    if location == 'St Albans':
        page_number=3

    if location == 'Uxbridge' :
        page_number= 3
    if location == 'Watford':
        page_number= 3
    if location == 'Dartford':
        page_number=3

    if location ==  'West London':
        page_number= 3
    if location == 'Brentford':
        page_number= 3
    if location == 'Redhill':
        page_number= 3
    if location ==  'England':
        page_number = 3

# can change range to get  more infromation each page for each page we have start parameter that determines page number
    for i in range(page_number):
        getVars = {'q' : job_title, 'l':country, 'rbl':location,'start':start_position,'sort':'date'}
        
        print("fetching information for page {0}".format(i))
        print("priting for  location {0}".format(location))
        url = ('https://www.indeed.co.uk/jobs?' + urllib.parse.urlencode(getVars))
        page = requests.get(url)
        fetched=str(page.text)
        soup = BeautifulSoup(page.content, "html.parser")
       


        # extracting ob titles

        def extract_job_title_from_result(soup,string): 
            for div in soup.find_all(name="h2", attrs={"class":"title"}):
                
                for news in div.find_all(name="a",attrs={"class":"jobtitle turnstileLink"}):
                    title=news.text
                    job_titles.append(news.text.strip())
                    #print(news.text.strip())
                    #https://www.indeed.co.uk/viewjob?jk=63fd2e2037d5ac6a&from=serp&vjs=3  ( for viewing page source)
                    links.append('https://www.indeed.co.uk'+news["href"])
                    pos=string.find(title)
                    semi_str=string[pos:]
                    soup=BeautifulSoup(semi_str,"html.parser")
                    data=soup.find(class_= "salarySnippet salarySnippetDemphasizeholisticSalary")
                    if data:
                        salary.append(data.text.strip())
                    else:
                        salary.append("not mentioned")
                                

                
            
        # extracting company
        def extract_company_indeed(job_elem):

            for companies in job_elem.find_all(name="span", attrs={"class":"company"}):
                company.append(companies.text.strip())
                area.append(location)
                #print(companies.text.strip())

            

            #print(element.text.strip())

        

        # extracting summmary
        def extract_summary(job_elem):
            for extracted_soup in  job_elem.find_all(name="div",attrs={"class":"summary"}):
                #print(extracted_soup)
                summary.append(extracted_soup.text.strip())
                #print(extracted_soup.text.strip())

        def extract_posted_by(job_elem):
            for extracted_soup in  job_elem.find_all(name="span",attrs={"class":"date"}):
                posted_by.append(extracted_soup.text.strip())

                #print(extracted_soup.text.strip())


        
        
        
        extract_job_title_from_result(soup,fetched)
        extract_company_indeed(soup)  
        extract_summary(soup)
        extract_posted_by(soup)
        #extract_salary(soup)
        start_position=start_position+10
    # job_titles,company,summary,salary,posted_by

#new_dict={"source":[source]*len(job_titles),"Date Collected":[date_collected]*len(job_titles),"job_titles":job_titles,"company":company,"summary":summary,"posted_by":posted_by,"links":links,'salary':salary,'location':area}
new_dict={"source":[source]*len(job_titles),'Region':[Region]*len(job_titles),'Industry':[Industry]*len(job_titles),"Date Collected":[date_collected]*len(job_titles),"job_titles":job_titles,"company":company,"summary":summary,"posted_by":posted_by,"links":links,'salary':salary,'Roles':[]*len(job_titles),'UG':[]*len(job_titles),'PG':[]*len(job_titles),'openings':[]*len(job_titles),'Industry Sub-Domain':[]*len(job_titles)}
dataframe = pd.DataFrame(new_dict)



# fetching more skills

#### code for soft skils
df=pd.read_csv('soft-skills.csv')
soft_skills_list=[]
charac="[ ]'" 
index=1
skills=[]
for c,v in df.iterrows():
    final_string=v['Soft Skills']
    filter=re.sub(r'[^\w+]',' ',final_string)

    for pattern in filter.split('  '):
        skills.append(pattern)

soft_skills_list=list(set(skills))
#dataframe.to_csv("uk_scrapped_data.csv")







def soft_skills_fetcher(pasted_url):
    print("fetched soft skills skills")
#https://www.indeed.co.uk/rc/clk?jk=84837a8c88af56a3&fccid=cb33bf356b899776&vjs=3
    url= pasted_url
    page = requests.get(url)
    con=str(page.content) # string
    div=con.find('<div>')

    semi=con[div:]
    soup=BeautifulSoup(semi,"html.parser")
    li=[]
    for items in soup.find_all('div'):
        li.append(items.text.strip())

    
    obt=''.join(li).replace('\n','')
    # removing footer html part
    extra=obt.find('try')
    remove=obt[extra:]
    final_string=''.join(obt.replace(remove,""))
    # filtering out extra /x/x/ character
    rectified=re.sub(r'[^\w]', ' ', final_string)
    soft_skills=[]

    for words in behaviour_skills_list:
        soft_skills.extend(re.findall(words,rectified,flags=re.IGNORECASE))
    return list(set(soft_skills))

    

# callig function for soft skills
print("fetching soft skils")
dataframe['Soft Skills'] = dataframe['links'].apply(soft_skills_fetcher)







## code for hard skills

df=pd.read_csv('hard-skills.csv')
#nested=df['Hard Skills'].tolist()
hard_skills_list=[]
charac="[ ]'" 
index=1
for c,v in df.iterrows():
    final_string=v['Hard Skills']

    for ch in charac:
        final_string=final_string.replace(ch,'')
    for items in final_string.split(','):
        hard_skills_list.append(items)


def hard_skills_fetcher(pasted_url):
#https://www.indeed.co.uk/rc/clk?jk=84837a8c88af56a3&fccid=cb33bf356b899776&vjs=3
    url= pasted_url
    page = requests.get(url)
    con=str(page.content) # string
    div=con.find('<div>')

    semi=con[div:]
    soup=BeautifulSoup(semi,"html.parser")
    li=[]
    for items in soup.find_all('div'):
        li.append(items.text.strip())

    
    obt=''.join(li).replace('\n','')
    # removing footer html part
    extra=obt.find('try')
    remove=obt[extra:]
    final_string=''.join(obt.replace(remove,""))
    # filtering out extra /x/x/ character
    rectified=re.sub(r'[^\w]', ' ', final_string)
    fetched=rectified.split(' ')
    complete=[ items.title() for items in fetched ]


    skills=[words for words in complete if words in hard_skills_list]
    skills_list=[]
    # removing spaces
    for words in skills:
        if words not in skills_list and words is not '':
            skills_list.append(words)
    return skills_list
    




  
print("fetching  hard skills")
dataframe['Hard Skills'] = dataframe['links'].apply(hard_skills_fetcher)
#dataframe.to_csv('data-with-skills.csv')
#print("data saved")

## programm for fetching behaviour skills

df=pd.read_csv('behaviour-skills.csv')
behaviour_skills_list=[]
charac="[ ]'" 
index=1
skills=[]
for c,v in df.iterrows():
    final_string=v['Behaviour Skills']
    filter=re.sub(r'[^\w+]',' ',final_string)

    for pattern in filter.split('  '):
        skills.append(pattern)

behaviour_skills_list=list(set(skills))




def  behaviour_skills_fetcher(pasted_url):
    

#https://www.indeed.co.uk/rc/clk?jk=84837a8c88af56a3&fccid=cb33bf356b899776&vjs=3
    url= pasted_url
    page = requests.get(url)
    con=str(page.content) # string
    div=con.find('<div>')

    semi=con[div:]
    soup=BeautifulSoup(semi,"html.parser")
    li=[]
    for items in soup.find_all('div'):
        li.append(items.text.strip())

    
    obt=''.join(li).replace('\n','')
    # removing footer html part
    extra=obt.find('try')
    remove=obt[extra:]
    final_string=''.join(obt.replace(remove,""))
    # filtering out extra /x/x/ character
    rectified=re.sub(r'[^\w]', ' ', final_string)
    #rectified=rectified.title()

    behav_skills=[]

    for words in behaviour_skills_list:
        behav_skills.extend(re.findall(words,rectified,flags=re.IGNORECASE))
    return list(set(behav_skills))

print("fetching behaviour skills")
dataframe['Behaviour Skills'] = dataframe['links'].apply(behaviour_skills_fetcher)







## program for fetching competecies

df=pd.read_csv('competencies.csv')
competency_skills_list=[]
charac="[ ]'" 
index=1
skills=[]
for c,v in df.iterrows():
    final_string=v['Behaviour Skills']
    filter=re.sub(r'[^\w+]',' ',final_string)

    for pattern in filter.split('  '):
        skills.append(pattern)

competency_skills_list=list(set(skills))




def  competency_skills_fetcher(pasted_url):
    

#https://www.indeed.co.uk/rc/clk?jk=84837a8c88af56a3&fccid=cb33bf356b899776&vjs=3
    url= pasted_url
    page = requests.get(url)
    con=str(page.content) # string
    div=con.find('<div>')

    semi=con[div:]
    soup=BeautifulSoup(semi,"html.parser")
    li=[]
    for items in soup.find_all('div'):
        li.append(items.text.strip())

    
    obt=''.join(li).replace('\n','')
    # removing footer html part
    extra=obt.find('try')
    remove=obt[extra:]
    final_string=''.join(obt.replace(remove,""))
    # filtering out extra /x/x/ character
    rectified=re.sub(r'[^\w]', ' ', final_string)
    #rectified=rectified.title()

    comp_skills=[]

    for words in competency_skills_list:
        comp_skills.extend(re.findall(words,rectified,flags=re.IGNORECASE))
    return list(set(comp_skills))





print("fetching  competency  skills")
dataframe['Competency'] = dataframe['links'].apply(competency_skills_fetcher)

#dataframe.to_csv("uk_data.csv")

