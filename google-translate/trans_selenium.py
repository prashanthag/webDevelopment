#pip install pyyaml
#pip install
import yaml
import time
from selenium import webdriver
import selenium 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions



#input1 = " Coronaviruses are a group of related viruses that cause diseases in mammals and birds. In humans, coronaviruses cause respiratory tract infections that can be mild, such as some cases of the common cold (among other possible causes, predominantly rhinoviruses), and others that can be lethal, such as SARS, MERS, and COVID-19. Symptoms in other species vary: in chickens, they cause an upper respiratory tract disease, while in cows and pigs they cause diarrhea. There are yet to be vaccines or antiviral drugs to prevent or treat human coronavirus infections."

chrome_op = ChromeOptions()
chrome_op.add_argument('--headless')
browser = webdriver.Chrome('chromedriver')
browser = webdriver.Chrome(executable_path='chromedriver', options=chrome_op)

languages = ['it','fr','de','en','kn']

def translate(input,lang_code):
    
    url = "https://translate.google.com/?op=translate&sl=en&tl="+lang_code+'&text=' + input
    # copy google Translator link here:=>
    browser.get(url)
    # just wait for some time for translating input text:=>
    time.sleep(1)    
    #result = browser.find_elements(By.XPATH, ".//*[@lang='de']/span");#
    result= browser.find_element_by_class_name('J0lOec').text
    result = result.split('\n')[0]
    return result
    

def translateTo(keyval,tmp_dic,source,destination):
    print(source,destination)
    for k,v in keyval.items():        
        result= translate(v,destination)
        tmp_dic[k] = result
        print(v," =  ",result)
    
    return tmp_dic

def transDump(keyval):
    tmp_dic = {}
    for i in languages:
        translateTo(keyval,tmp_dic,'en',i)
        file1 = i+".yml"
        #print(file1)
        with open(file1 ,'wt') as file:       
            yaml.dump(tmp_dic, stream=file, allow_unicode=True)


with open("trial.yml", 'rt') as stream:
    try:        
        keyval = yaml.safe_load(stream)
        transDump(keyval)

    except yaml.YAMLError as exc:
        print(exc)


