from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium import webdriver
from pathlib import Path
import time
import os,sys,re,random,string
import pytest
from webdriver_manager.chrome import ChromeDriverManager

class TestClass:
    gone_ticket = ""
    return_ticket = ""

    def negative_test(self):
        self.gone_ticket = "20B"
        self.return_ticket = "60E"
        obj.generateSeat(self.gone_ticket,self.return_ticket)
        assert self.gone_ticket in obj.gone_seat
        assert self.return_ticket in obj.return_seat
        
    def positive_test(self,obj):
        self.gone_ticket = "25J"
        self.return_ticket = "32E"
        obj.generateSeat(self.gone_ticket,self.return_ticket)
        assert self.gone_ticket in obj.go_seat
        assert self.return_ticket in obj.re_seat
        
    def multiple_test(self,obj,num):
        for i in range(num):
            self.gone_ticket = self.generateSeat()
            self.return_ticket = self.generateSeat()
            while(self.gone_ticket == self.return_ticket):
                self.return_ticket = self.generateSeat()
            obj.generateSeat(self.gone_ticket,self.return_ticket)
            assert self.gone_ticket in obj.go_seat
            assert self.return_ticket in obj.re_seat                

    def generateSeat(self):
        number = random.randint(18,62)
        letter =  random.choice([l for l in string.ascii_uppercase if l <= 'K'])
        return str(number)+letter            
class OpenWeb:
    go_seat = ""
    re_seat = ""
    def __init__(self):

        self.setup()
    
    def setup(self):
        url = "https://static.gordiansoftware.com/"
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()
        self.driver.get(url)
    
    def checkSeatValues(seat):
        reg_num = int(re.match("\d+",seat).group(0))
        reg_letter = re.match("\D+",seat).group(0)
        if reg_num <= 60 and reg_letter <= 'K':
            return True
        return False            

    def waitPage(self):
        wait = WebDriverWait(self.driver, 30)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

    def generateSeat(self,departure_seat,return_seat):
        assert f"Invalid seat:{departure_seat}. I couldn't book your round-trip",self.checkSeatValues(departure_seat)
        assert f"Invalid seat: {return_seat}. I couldn't book your round-trip",self.checkSeatValues(return_seat)
        
        script_scroll = lambda : f"scrollTo(0, 1000);"
        try:
            self.searchSeat(departure_seat)
            self.searchSeat(return_seat)
            self.waitPage()
            self.driver.execute_script(script_scroll())
            time.sleep(4)
            self.assertValues()
            self.driver.save_screenshot(f"{os.getcwd()}\screenshoot.png")
        except Exception as e:
            print(e)

        finally:
            self.driver.quit()
    def assertValues(self):
        self.go_seat = (self.driver.find_element_by_xpath('//*[@id="trigger"]/section[2]/div[1]/div/div[2]/p[1]')).text
        self.re_seat = (self.driver.find_element_by_xpath('//*[@id="trigger"]/section[2]/div[1]/div/div[2]/p[2]')).text
    def searchSeat(self,seat):
        try:
            reg_num = int(re.match("\d+",seat).group(0))
            buttons = self.driver.find_elements_by_xpath(f"//div[contains(@class,'row-{reg_num}')]//button[contains(@class,'gordian-seat')]")
            #buttons = self.driver.find_elements_by_xpath(f"//button[contains(@class,'gordian-seat')]")
            select = lambda: self.driver.find_element_by_xpath('//*[@id="select-seat"]')
            next_flight = lambda:self.driver.find_element_by_xpath('//*[@id="next-button"]')
            exit_accepted ='//*[@id="accept_exit_regulations"]'
            seat_select = lambda: (self.driver.find_element_by_xpath("//*[@id='desktop-seat-details']/div/h3")).text
            pattern_seat = r"\d{2}\w{1}"
            exit_condition = lambda:len(self.driver.find_elements_by_xpath(exit_accepted))
            found = False
            for button in buttons:
                button.click()
                if(exit_condition()>0):
                    warning = WebDriverWait(self.driver, 0.15).until(EC.visibility_of_element_located((By.XPATH,exit_accepted)))
                    warning.click()
                    time.sleep(0.1)
               
                match = re.search(pattern_seat,seat_select())
                if(match.group(0) == seat):
                    found = True
                    select().click()
                    time.sleep(0.1)
                    next_flight().click()
                    break          
                                                    
        except Exception as e:
            print(e)
            print(type(e))
            print(e.args)
        finally:
            if(not found):
                print(f"Invalid seat. I couldn't book your round-trip")

        
if __name__=="__main__":
    #seat_one,seat_two = input("Inform 2 seats for your round-trip: ex('20B 60E'): \n").split()
    obj = OpenWeb()
    #test_1 = TestClass()
    test_2 = TestClass()
    #test_1.positive_test(obj)
    test_2.multiple_test(obj,1)
    #obj.generateSeat()
