# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 19:12:00 2020

@author: mojo_jojo
"""

#this is the repo for selenium tools for use in webtools

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, StaleElementReferenceException, ElementClickInterceptedException, NoSuchElementException, NoSuchFrameException,NoAlertPresentException,UnexpectedAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

class mydriver:
    def __init__(self, download_dir):   
        self.download_dir = download_dir
    def setupbrowser(self,head=None):
         # for linux/*nix, download_dir="/usr/Public"
        options = webdriver.ChromeOptions()
        
        profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], # Disable Chrome's PDF Viewer
                       "download.default_directory": self.download_dir , "download.prompt_for_download":False,"download.directory_upgrade": True,"safebrowsing.enabled": False,'profile.default_content_setting_values.automatic_downloads': 1,"download.extensions_to_open": "applications/pdf"}
        options.add_experimental_option("prefs", profile)
        
        if head:
            options.add_argument('--headless')
        
        self.driver=webdriver.Chrome(ChromeDriverManager().install(),options=options)
        self.driver.implicitly_wait(10)
        return(self.driver)
    
class main:
    def __init__(self,driver):
        self.driver-driver
    def checkbox_check(self,idstr):
        delay=3
        myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.ID, idstr)))
        return(myElem.is_selected())
    def checkbox_mass(self,partialid):
        xpath=f'//input[contains(@id,"{partialid}")]'
        a=self.driver.find_elements_by_xpath(xpath)
        valdict=[]
        for i in a:
            if self.checkbox_check(i.get_attribute('id')):
                valdict.append(i.get_attribute('id'))
        return(valdict)
    def cf_catalog(self,classnames):
        #this function surveys a page and returns list of tuples with field id as well as labels
        valuelist=[]
        for i in classnames:
            for element in self.driver.find_elements_by_class_name(i):
                try:
                    newtup=tuple([self.driver.find_elements_by_id(element.get_attribute('id')[:-2]+'_LBL'+element.get_attribute('id')[-2:])[0].get_attribute('innerText'),element.get_attribute('id')])
                except:
                    newtup=tuple(["No label",element.get_attribute('id')])
                valuelist.append(newtup)
        return(valuelist)
    
    def cf_data_distribute(self,datadict):
        x=self.getids()
        for key, value in datadict.items():
            if key in x:
                self.waitfillid(key,value)
                sleep(.5)
                self.okay()
        
    def clear_fd(self,fieldid):
        delay = 3 
        try:
            myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.ID, fieldid)))
            myElem.clear()
            myElem.send_keys(Keys.TAB)
            sleep(0.5)
        except TimeoutException:
            print(f"{fieldid} process timed out")    
    
    def collect_span(self,spanid):
        return(self.driver.find_element_by_xpath(spanid).text)
    
    def data_collect(self,datatype):
        a = self.driver.find_elements_by_class_name(datatype)
        valdict={}
        for i in a:
            x= i.get_attribute('value')
            if type(x)=="None":
                x=i.text
            if type(x)!=None:
                y=i.get_attribute('id')
                valdict[y]=x
        return(valdict)
        
    def data_collector2(self,partialid):
        xpath=f'//span[contains(@id,"{partialid}")]'
        a=self.driver.find_elements_by_xpath(xpath)
        valdict={}
        for i in a:
            x= i.text
            if type(x)!=None:
                y=i.get_attribute('id')
                valdict[y]=x
        return(valdict)
        
    def data_distribute(self,datadict):
        for key, value in datadict.items():
            if self.windowswitch(key,0):
                try:
                    self.waitfillid(key,value)
                except StaleElementReferenceException:
                    self.waitfillid(key,value)
                except ElementClickInterceptedException:
                    self.okay2()
                    self.waitfillid(key,value)
    
    def	dropdownitembyid(self,idstr):
        select = Select(self.driver.find_element_by_id(idstr))
        selected_option = select.first_selected_option
        return(selected_option.text) 
        
    def dropdownoptions(self,idstr):
        options=[i.text for i in Select(self.driver.find_element_by_id(idstr)).options]
        return(options)
    
    def dropdownremoval(self,idstr,button):
        options=[i.text for i in Select(self.driver.find_element_by_id(idstr)).options]
        for i in options:
            print(f"Removing {i}")
            Select(self.driver.find_element_by_id(idstr)).select_by_value(i)
            self.waitid(button)
            sleep(1)
    
    
    def dropdownselector(self,idstr,selected):
        if self.windowswitch(idstr,0):
            try:
                delay=2
                select = Select(WebDriverWait(self.driver, delay).until(EC.element_to_be_clickable((By.ID, idstr))))
                select.select_by_visible_text(selected)
                select.send_keys(Keys.TAB)
                self.okay2()
            except NoSuchElementException:
                self.okay2()
                self.driver.switch_to.default_content()
                self.dropdownselector(idstr,selected)
            except ElementClickInterceptedException:
                self.okay2()
                self.dropdownselector(idstr,selected)
            except:
                pass
    
    def framenav(self,num):
        self.driver.switch_to.default_content()
        frames=self.driver.find_elements(By.TAG_NAME, 'iframe')
        self.driver.switch_to.frame(frames[num])

    def getcf(self):
        return(mydriver.cflog(self))

    def getids(self):
        ids = self.driver.find_elements_by_xpath('//*[@id]')
        idlist=[]
        for ii in ids:
            #print ii.tag_name
            idlist.append(ii.get_attribute("id"))
        return(idlist)
        
    def getvals(self,idstr):
        try:
            return(self.driver.find_element_by_id(idstr).get_attribute('value'))
        except TimeoutException:
            self.windowswitch(idstr,0)
            return(self.driver.find_element_by_id(idstr).get_attribute('value'))
            
    def gettext(self,idstr):
        try:
            return(self.driver.find_element_by_id(idstr).text)
        except TimeoutException:
            self.windowswitch(idstr,0)
            return(self.driver.find_element_by_id(idstr).text)
        
    def get_class_vals(self,classstr):    #this function should return labels
        valuelist=[]
        for element in self.driver.find_elements_by_class_name(classstr):
            valuelist.extend((element.get_attribute('id'),element.get_attribute('value')))
        return(valuelist)
    def get_class_text(self,classstr):    #this function should return labels
        valuelist=[]
        for element in self.driver.find_elements_by_class_name(classstr):
            valuelist.extend((element.get_attribute('id'),element.get_attribute('text')))
        return(valuelist)

    
    
    def grab_table(self,ID):
        table_id = self.driver.find_element(By.ID, ID)
        rows = table_id.find_elements(By.TAG_NAME, "td") # get all of the rows in the table
        return(rows)
                                
    def name_to_css(self,x):
        y=x.get_attribute('id')
        return("#"+y.split("$")[0]+"/$"+y.split("$")[1])
    
    def okay(self):
        self.wait_spin()
        if self.windowswitch("#ICOK",0):
            self.waitid("#ICOK")
        if self.windowswitch('#ALERTOK',0):
            self.waitid('#ALERTOK')

        else:
            self.driver.switch_to.parent_frame        
    def okay2(self):
        try:
            self.driver.switch_to.default_content()
            if 'ICOK' in self.driver.page_source:
                self.waitid("#ICOK")
            elif "ALERTOK" in self.driver.page_source:
                self.waitid("#ALERTOK")
        except UnexpectedAlertPresentException:
            try:
                self.driver.switch_to.alert.accept()
            except NoAlertPresentException:
                pass
    def okay3(self):
        print('looking for dialogue boxes to OK out of')
        self.wait_spin()
        try:
            self.driver.switch_to.alert.accept()
            return(True)
        except NoAlertPresentException:
            try:
               self.waitid("#ICOK")
               self.waitid("#ALERTOK")
               self.driver.find_element_by_xpath('//*[@id="#ALERTOK"]').click()
               self.driver.find_element_by_xpath('//*[@id="#ICOK"]').click()
               self.driver.find_element_by_xpath("//*[contains(@id, 'OK')]").click()
            except ElementClickInterceptedException:
                try:
                    if 'frame id' in self.driver.page_source:
                        self.driver.switch_to.frame(self.driver.page_source.split("frame id")[2].split()[0][6:-1])
                    else:
                        self.driver.switch_to.default_content()
                    self.waitid("#ICOK")
                    self.waitid("#ALERTOK")
                    self.driver.find_element_by_xpath('//*[@id="#ALERTOK"]').click()
                    self.driver.find_element_by_xpath('//*[@id="#ICOK"]').click()
                    self.driver.find_element_by_xpath("//*[contains(@id, 'OK')]").click()
                except NoSuchFrameException:
                    self.driver.switch_to.default_content()
                    self.waitid("#ICOK")
                    self.waitid("#ALERTOK")
                    self.driver.find_element_by_xpath('//*[@id="#ALERTOK"]').click()
                    self.driver.find_element_by_xpath('//*[@id="#ICOK"]').click()
                    self.driver.find_element_by_xpath("//*[contains(@id, 'OK')]").click()
            except TimeoutException:
                self.driver.switch_to.default_content()
                self.waitid("#ICOK")
                self.waitid("#ALERTOK")
                self.driver.find_element_by_xpath('//*[@id="#ALERTOK"]').click()
                self.driver.find_element_by_xpath('//*[@id="#ICOK"]').click()
                self.driver.find_element_by_xpath("//*[contains(@id, 'OK')]").click()
                try:
                    self.driver.switch_to.frame("TargetContent")
                except NoSuchFrameException:
                    pass
            except NoSuchElementException:
                pass
            except NoSuchFrameException:
                pass
    def openrecord(self,fieldtype,valuelist):
        if fieldtype=="job":
            self.waitfillid("EMPLMT_SRCH_COR_EMPLID",valuelist[0])
            self.waitfillid("EMPLMT_SRCH_COR_EMPL_RCD",valuelist[1]) 
        elif fieldtype=="pos":
            self.waitfillid("POSITION_SRCH_POSITION_NBR",valuelist[0])
        elif fieldtype=="js":
            self.waitfillid("CU_JOB_SUM_SRCH_EMPLID",valuelist[0])
        self.waitid("#ICSearch")
        try:
            self.waitid("SEARCH_RESULT1")
        except:
            pass
                    
    def openrecord_cf(self,field1,val1,field2=None,val2=None):  #deprecated in favor of openrecord
        self.waitfillid(field1,val1)
        if not field2:
            pass
        else:
            self.waitfillid(field2,val2)
        self.waitid(self.search)            
    
    def openrecordjob(self,empl,rcd):   #deprecated in favor of openrecord
        self.waitfillid("EMPLMT_SRCH_COR_EMPLID",empl)
        self.waitfillid("EMPLMT_SRCH_COR_EMPL_RCD",rcd)
        self.waitid("#ICSearch")
    
    def page_has_loaded(driver):
        #self.log.info("Checking if {} page is loaded.".format(self.driver.current_url))
        page_state = driver.execute_script('return document.readyState;')
        return page_state == 'complete'
            
    def pra_table_extract(self,rows):
        titlelist=["BA1""BA2","BA3","BD1","BD2","BD3","BD4","C/A","CAP","CCA","CET","CSA","DA1","DA2","ECA","EOA","IT","IT1","IT2","IT3","IT4","IT5","IT6","IT7","IT8","IT9","NS"]
        titledict={"BA1":"500021","BA2":"500023","BA3":"500025","BD1":"500273",
                   "BD2":"500275","BD3":"500277","BD4":"500279","C/A":"500050",
                   "CAP":"500050","CCA":"500074","CSA":"500033","DA1":"500080",
                   "DA2":"500082","DA3":"500084","EOA":"500101","ECA":"500230",
                   "IT":"500141","IT1":"500123","IT2":"500125","IT3":"500127",
                   "IT4":"500129","IT5":"500133","IT6":"500131","IT7":"500135",
                   "IT8":"500137","IT9":"500139","NS":"999999"}
        xlist=[row.text for row  in rows if row.text[0].isalpha()==False and len(row.text)>2 and len(row.text)<11 or row.text in titlelist]
        
        return([(xlist[ix],xlist[ix+1],xlist[ix+2],titledict[xlist[ix+3]],xlist[ix+4]) for ix,x in enumerate(xlist) if "/" in x])
    
    def refreshfill(self,fieldid,texts):
        delay = 3 
        try:
            myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.ID, fieldid)))
            myElem.clear()
            myElem.send_keys(Keys.TAB)
            myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.ID, fieldid)))
            myElem.send_keys(texts)
            myElem.send_keys(Keys.TAB)
            sleep(0.5)
        except TimeoutException:
            print(f"{fieldid} process timed out")   

    def return_rows(self,rows):
        return([row.text for row in rows])
    
    def save_check(self):
        delay = 1 
        fieldid='//*[@id="SAVED_win0"]'
        if self.windowswitch("SAVED_win0",0):
            try:
                myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, fieldid)))
                return(myElem.get_attribute('style'))
            except NoSuchElementException:
                self.okay2()
                self.save_check()
            except:
                return(False)   
        else:
            return(False)
        
    def saving_check(self):
        delay = 1 
        fieldid='//*[@id="WAIT_win0"]'
        if self.windowswitch("WAIT_win0",0):
            try:
                myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, fieldid)))
                return(myElem.get_attribute('style'))
            except NoSuchElementException:
                self.okay2()
                self.save_check()
            except:
                return(False)   
        else:
            return(False)
    def save_flag(self,status):
        if status==False:
            return(False)
        elif "hidden" in status:
            return('hidden')
        elif "hidden" not in status:
            return("visible")
        else:
            return(False)
    def save_now(self):
        print('now attempting to save')
        y=[]
        while True:
            x=self.save_flag(self.save_check())
            y.append(x)
            y=list(set(y))
            if 'visible' in y:
                break
            self.okay2()   
            if self.save not in self.driver.page_source:
                self.driver.switch_to.frame("TargetContent")
                try:
                    self.waitid(self.save)
                    self.driver.switch_to.default_content()
                except ElementClickInterceptedException as e:
                    print(e)
                    self.okay2()
                    self.save_now()
                except TimeoutException as e:
                    print(e)
                    self.save_now()
                except NoSuchElementException as e:
                    print(e)
                    pass
                except NoSuchFrameException as e:
                    print (e)
                    pass
            else:
                self.waitid(self.save)
                self.okay2()
        else:
            self.okay2()
    def simplesave(self):
        y=[]
        while True:
            self.okay2()
            x=self.save_flag(self.save_check())
            y.append(x)
            y=list(set(y))
            z=self.save_flag(self.saving_check())
            if 'visible' in z:
                pass
            
            if 'visible' in y:
                break
            if self.windowswitch(self.save,0):
                try:
                    self.waitid(self.save)
                except StaleElementReferenceException:
                    break
    def spinner(self):
        delay = 3 
        fieldid='//*[@id="WAIT_win0"]'
        try:
            self.windowswitch("WAIT_win0",0)
            myElem = WebDriverWait(self.driver, delay).until(EC.invisibility_of_element_located((By.XPATH, fieldid)))
            if str(type(myElem))!="<class 'NoneType'>":
                return("hidden" not in myElem.get_attribute('style'))
            else:
                return(False)
        except Exception as e:
            print(e)
            return(False)
            
    def union(elemlist1,elemlist2):
        return(len(set(elemlist1,elemlist2))>1)

    def wait_for_spinner(self):
        LONG_TIMEOUT = 30  # give enough time for loading to finish
        sleep(1)
        sstatus=""
        LOADING_ELEMENT_XPATH = "//*[@id='SAVED_win0']"
        WebDriverWait(self.driver, LONG_TIMEOUT).until(EC.invisibility_of_element_located((By.XPATH, LOADING_ELEMENT_XPATH)))
        sstatus="on"
        LOADING_ELEMENT_XPATH = "//*[@id='WAIT_win0']"
        WebDriverWait(self.driver, LONG_TIMEOUT).until(EC.invisibility_of_element_located((By.XPATH, LOADING_ELEMENT_XPATH)))
        sstatus="off"
        print(sstatus)
        #REVISIT THIS MOJO!
        
    def wait_spin(self):
        while True:
            if self.spinner()==True:
                sleep(.1)
            else:
                break               
    def waitalert(self):
        WebDriverWait(browser, 3).until(EC.alert_is_present(),'Are you sure to proceed?'+'Ar you sure to delete this timesheet?'+'This Timesheet was successfully saved')
                      
    def waitcheckbox(self,idstr):
        delay = 3 
        try:
            myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.ID, idstr)))
            myElem.isSelected()
        except TimeoutException as e:
                return(e)
    
    def waitfillid(self,fieldid,texts):
        delay = 3 
        try:
            myElem = WebDriverWait(self.driver, delay).until(EC.element_to_be_clickable((By.ID, fieldid)))
            try:
                myElem.clear()
            except:
                pass
            if 'dropdown' in myElem.get_attribute('class').lower():
                self.dropdownselector(fieldid,texts)
            else:
                myElem.send_keys(texts)
            myElem.send_keys(Keys.TAB)
            sleep(0.5)
        except TimeoutException as e:
                return(e)
        except StaleElementReferenceException:
            self.waitfillid(fieldid,texts)
        except ElementNotInteractableException:
            cssval=self.name_to_css(myElem)
            try:
                myElem = WebDriverWait(self.driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR, cssval)))
                try:
                    myElem.clear()
                except:
                    pass
                if 'dropdown' in myElem.get_attribute('class').lower():
                    self.dropdownselector(fieldid,texts)
                else:
                    myElem.send_keys(texts)
                myElem.send_keys(Keys.TAB)
                sleep(0.5)
            except TimeoutException as e:
                return(e)
            except ElementClickInterceptedException:
                self.okay()
                self.waitfillid(fieldid,texts)

    def waitid(self,idstr):
        delay = 3 
        try:
            myElem = WebDriverWait(self.driver, delay).until(EC.element_to_be_clickable((By.ID, idstr)))
            myElem.click()
        except TimeoutException as e:
                return(e)
        except ElementClickInterceptedException:
            self.okay()
            self.waitid(idstr)        
    
    def waitlink(self, linktext):
        delay = 3 
        try:
            myElem = WebDriverWait(self.driver, delay).until(EC.element_to_be_clickable((By.LINK_TEXT, linktext)))
            myElem.click()
        except TimeoutException as e:
                return(e)
    
    def windowswitch(self,elemstr,num):
        if elemstr in self.driver.page_source:
            return(True)
        if 'frame id' in self.driver.page_source:
            try:
                self.driver.switch_to.frame(self.driver.page_source.split("frame id")[2].split()[0][6:-1])
            except Exception as e:
                print(e)
                pass
        if elemstr in self.driver.page_source:
            return(True)
        else:
            self.driver.switch_to.default_content()
            try:
                self.driver.switch_to.frame(num)
            except NoSuchFrameException:
                pass
            num+=1
            try:
                self.windowswitch(elemstr,num)
            except Exception as e:
                #print(e)
                self.driver.switch_to.default_content
                self.windowswitch(elemstr,num)   
            finally:
                return(False)    

    def xpathclick(self,elem):
        self.driver.find_element_by_xpath(elem).click()

