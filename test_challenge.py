import pytest
import os,sys,re,random,string

class TestClass:
    gone_ticket = ""
    return_ticket = ""

    def negative_test(self,obj):
        self.gone_ticket = "39A"
        self.return_ticket = "60E"
        obj.chooseSeat(self.gone_ticket,self.return_ticket)
        assert "Invalid seat. I couldn't book your round-trip" in obj.gone_seat
        assert "Invalid seat. I couldn't book your round-trip" in obj.return_seat
        
    def positive_test(self,obj):
        self.gone_ticket = "25J"
        self.return_ticket = "32E"
        obj.chooseSeat(self.gone_ticket,self.return_ticket)
        assert self.gone_ticket in obj.go_seat
        assert self.return_ticket in obj.re_seat
        
    def multiple_test(self,obj,num):
        for i in range(num):
            self.gone_ticket = self.generateSeat()
            self.return_ticket = self.generateSeat()
            while(self.gone_ticket == self.return_ticket):
                self.return_ticket = self.generateSeat()
            obj.chooseSeat(self.gone_ticket,self.return_ticket)
            assert self.gone_ticket in obj.go_seat
            assert self.return_ticket in obj.re_seat                

    def generateSeat(self):
        number = random.randint(18,62)
        letter =  random.choice([l for l in string.ascii_uppercase if l <= 'K'])
        return str(number)+letter   