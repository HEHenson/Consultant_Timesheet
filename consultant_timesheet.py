# Version 0.2 to be loaded onto GitHub

import datetime
import unittest
import pycountry



class day():
    """
    The day stores information relevant to the project to determine if 
    it is a potential day of work.  It is not tied to the individual but 
    it is tied to the project and its jurisdiction
    """
    def __init__(self,theday=None,themonth=None,theyear=None,higherpriority=None):
        self.day = theday
        self.month = themonth
        self.year = theyear
        try:
            self.thedate = datetime.date(self.year,self.month,self.day)
            self.exists = True
        except:
            self.exists = False
        self.after = None
        self.before = None
    def isworkday(self,theday):
        """  determine if theday is a normal working day
             args theday: int (monday = 0)
             return boolean
        """
        if not self.exists :
            return False
        if self.thedate.weekday() == theday :
            return True
        else:
            return False
    def __repr__(self):
        if self.exists :
            return self.thedate
        else:
            return None
    def isstat(self,jurisdiction="Ont"):
        """
        Determines if current day is a statutory holiday
        
        """
        retval = False
        try:
            theday = datetime.date(self.year,self.month,self.day).weekday()
        except:
            return False
        if theday == 5 or theday == 6 :
            return True
        if(self.isBox()): return True
        if(self.isXmas()): return True
        if(self.isRembrance(jurisdiction)) : return True
        if(self.isgoodfriday(jurisdiction)) : return True
        if(self.isJeanB(jurisdiction)) : return True
        if(self.islabour()) : return True
        return retval
    def isgoodfriday(self,jurisdiction):
        if (datetime.date(2016,3,25) == datetime.date(self.year,self.month,self.day)
            and jurisdiction == "QC"): return True
    def isestMon(self,jurisdiction):
        if (datetime.date(2016,3,28) == datetime.date(self.year,self.month,self.day)
            and jurisdiction == "QC"): return True
    def isJeanB(self,jurisdiction):
        if (datetime.date(2016,6,24) == datetime.date(self.year,self.month,self.day)
            and jurisdiction == "QC"): return True
    def isVicDay(self,jurisdiction):
        if (datetime.date(2016,5,23) == datetime.date(self.year,self.month,self.day)
            and jurisdiction == "QC"): return True 
    def islabour(self):
        if (datetime.date(2016,9,5) == datetime.date(self.year,self.month,self.day)):
            return True
    def isCanday(self):
        if (datetime.date(2016,7,1) == datetime.date(self.year,self.month,self.day)):
            return True
    def isTGving(self):
        if (datetime.date(2016,10,10) == datetime.date(self.year,self.month,self.day)):
            return True
        if (datetime.date(2020,12,10) == datetime.date(self.year,self.month,self.day)):
            return True
    def isRembrance(self,jurisdiction):
        if jurisdiction == 'QC':
            return False
        if (datetime.date(2016,11,11) == datetime.date(self.year,self.month,self.day)):
            return True
        if (datetime.date(2020,11,11) == datetime.date(self.year,self.month,self.day)):
            return True
    def isXmas(self):
        if (self.month == 12 and self.day == 25 ):
            return True
    def isBox(self):
        # in Ontario if the 26 is a holiday then it is the Monday
        if self.year == 2020: 
            if self.month == 12 and self.day == 28 : 
                return True
            else:
                return False
        if (self.month == 12 and self.day == 26 ):
            return True
        return False
    def hasconflict(self,highpriority = None):
        if(highpriority == None) :
            return False
        retval = self.isavail(self.month,self.day,self.year)
        if retval == True :
            return False
        else:
            return True
    
        
    

class person():
    """
    Info tied to participant in the project
    """
    def __init__(self,pname,maxwk=5,dayoff=None):
        self.thename = pname
        #: maxwk maximum days of work in week
        self.maxwk = maxwk
        #: dayoff Monday = zero
        self.dayoff = dayoff
        #: days worked on project by participant
        self.daytot = 0
        #: days worked in current week
        self.curwk = 0
        
    def isavail(self,month,day,year):
        """
        Will check against personal holidays
        """
        print(f'*** 135 {month} {day} {year}')
        if self.isholiday(month,day,year):
            return False
        if self.isdayoff(month,day,year):
            return False
        return True
    
    def isdayoff(self,month,day,year):
        
        try:
            theday = datetime.date(year,month,day)
        except ValueError:
            return False
        if self.dayoff is not None:
            if self.dayoff == theday:
                return True
        if theday.weekday() >= self.maxwk:
            return True
        return False
        
    def isholiday(self,month,day,year):
        """
        Checks for person holidays
        returns True if this is a holiday
        
        """
        # check for day off during week
        print(f'*** 158 month={month} day={day} year={year}')
        try:
            theday = datetime.date(year,month,day)
        except ValueError:
            return False
        print(f'*** 160 theday={theday}')
        daynum = theday.weekday()
        print(f'*** 162 daynum = {daynum}')
        if daynum < (self.maxwk):
            print(f'***  164 in holiday theday {theday}')
            return False
        else:
            print(f'***  167 in holiday theday {theday} max={self.maxwk}')
            return True
            
    def getname(self):
        return self.thename
    def __repr__(self):
        return self.getname()
    

class workday(day):
    def __init__(self,theperson, theday,themonth,theyear,comment=""):
        """ Creates a day of work for person on day, month, year"""
        day.__init__(self,theday, themonth,theyear)
        self.worker = theperson
        self.comment = comment
    def __repr__(self):
        return "A day of work by "+ self.worker.getname()

class project():
    def __init__(self,projname,HigherPriority = None,maxworkwk=5,jur='ON'):
        """creates a project object"""
        self.projname = projname
        # dictionary of days worked on project
        self.daydict = []
        self.daynum = 0
        # this represents another project that claims priority
        # over any given day
        self.higherPriority = HigherPriority
        self.listsorted = False
        self.maxworkwk = maxworkwk
        self.firstday = None
        self.lastday = None
        self.jur = jur
    def __repr__(self):
        return "Project "+ self.projnam 


    def add_day(self,theperson,theday,themon,theyear,comment=""):
        """ adds day to daydict for the person if possible """
        # add day to daydict if it is not a statutory holiday
        # or has a higher priority
        # or does not exist
        newday = workday(theperson,theday,themon,theyear,comment)
        # if day is a holiday do not add into list
        if newday.isstat(self.jur) :
            return False
        if theperson.isavail(themon,theday,theyear) == False:
            return False
        if newday.hasconflict(self.higherPriority) :
            return False
        # check if last day of month exceed 
        if not newday.exists:
            return False
        self.daydict.append(newday)
        self.daynum += 1
        self.insertday(newday)
        return True
        

    def insertday(self,newday):
        """will insert a workday into the linked list"""
        # is this the start of a list
        if self.firstday == None and self.lastday == None :
            self.firstday = newday
            self.lastday = newday
            return
        # if before first day
        if self.firstday.thedate > newday.thedate :
            self.firstday.before = newday
            newday.after = self.firstday
            self.firstday = newday
            return
        # if after last day
        if self.lastday.thedate < newday.thedate :
            self.lastday.after = newday
            newday.before = self.lastday
            self.lastday = newday
            return
        # now I must insert in the list
        theday = self.firstday
        while theday.after != None :
            if theday.thedate >= newday.thedate :
                theafter = theday.after
                thebefore = theday.before
                theday.before.after = newday
                theday.after.before = newday
                newday.before = thebefore
                newday.after = theafter
                return
            else :
                theday = theday.after

    def isprojday(self,themonth,theday,theyear):
        """
        Work being done on project that day
        """
        retval = True
        
        for personday in self.daydict :
            if personday.year == theyear and personday.month == themonth and personday.day == theday :
                return False
        return True

 
    def listdays(self):
        """List all days where at least one day is worked, along with"""
        """a cummulative total"""

        print(self.projname)
        dayno = 1
        for month in range(1,13):
            print( "Month ",month)
            print ('-'*20)
            for day in range(1,32) :
                for personday in self.daydict :
                    if personday.month == month and personday.day == day :
                        print( day,' ', dayno,' ',personday.comment)
                        dayno += 1

    def showcal(self):
        """same as listdays but in a calendar format"""
        dayno = 1
        print(self.projname)
        for month in range(1,13):
            print( "Month ",month)
            print ('-'*20)
            for day in range(1,32) :
                for personday in self.daydict :
                    if personday.month == month and personday.day == day :
                        print( day,' ', dayno,' ',personday.comment)
                        dayno += 1

        


    def get_total(self):
        """Total number of days on project, where at least one person worked"""
        return self.daynum
    
    def loaddays(self,me,maxdays,theyear,themonth,theday) :
        """ Adds a sequence of days to the project starting at date specified"""
        daynum = 0
        initday = theday
        for monthcnt in range(themonth,13):
            for daycnt in range(initday,32):
                isadded = self.add_day(me,daycnt,monthcnt,theyear)
                if isadded : daynum += 1
                if daynum >= maxdays : return daynum
            # want to start at day one for next month
            initday = 1
        # should equal maxdays
        return daynum

    def addweekday(self,me,maxdays,theday,themonth,theyear,dayofweek,comment=""):
        """ Adds a day of week"""
        """ Monday = 0 in Python"""
        daynum = 0
        initday = theday
        for monthcnt in range(themonth,13):
            for daycnt in range(initday,32):
                newday = day(daycnt,monthcnt,theyear)
                if not newday.isworkday(dayofweek):
                    continue
                isadded = self.add_day(me,daycnt,monthcnt,theyear,comment)
                if isadded : daynum += 1
                if daynum >= maxdays : return daynum
            # want to start at day one for next month
            initday = 1
        # should equal maxdays
        return daynum            
                

def loaddata():
    me = person('Harold Henson')
    Vac2016 = project('Vacation for HH')
    Vac2020 = project('Vacation for HH')
    
    for daynum in range(10,16) :
        Vac2016.add_day(me,daynum,2,2016,"Cottage")
    Vac2016.add_day(me,16,2,2016,"Flu")
    Vac2016.add_day(me,17,2,2016,"Flu")
    Vac2016.add_day(me,23,2,2016,"Family Leave")
    Vac2016.add_day(me,11,4,2016,"Flu")
    # Vac2016.add_day(me,12,4,2016,"Family Leave")
    
    for daynum in range(27,31) :
        Vac2016.add_day(me,daynum,4,2016,"Cottage")
    for daynum in range(1,3) :
        Vac2016.add_day(me,daynum,5,2016,"Cottage")
    for daynum in range(1,5) :
        Vac2016.add_day(me,daynum,6,2016,"NFLD")
    for daynum in range(6,8) :
        Vac2016.add_day(me,daynum,6,2016,"CES Presentation") 
    for daynum in range(22,28) :
        Vac2016.add_day(me,daynum,6,2016,"Cottage")
    Vac2016.add_day(me,31,8,2016,"Cottage")
    for daynum in range(1,6) :
        Vac2016.add_day(me,daynum,9,2016,"Cottage")
    # now take every Friday off
    Vac2016.addweekday(me,50,1,1,2016,4,"Fridays off")
    Vac2020.addweekday(me,50,1,1,2020,4,"Fridays off")

    Vac2016.listdays()
    thetot = Vac2016.get_total()
    print("Total Days Used", thetot)

    ESDC2016 = project('90 day contract',Vac2016)
        
    ESDC2016.loaddays(me,88,2016,1,18)
    ESDC2016.listdays()
    thetot = ESDC2016.get_total()
    print("Total Days Used", thetot)

class Test(unittest.TestCase):        
    def test_person(self):
        print('\n','test_person_started','\n',40*'*')
        MrX = person('MrX')
        self.assertEqual(MrX.getname(),'MrX')
        self.assertEqual(MrX.maxwk,5)
        MrY= person('MrY',maxwk=4)
        self.assertEqual(MrY.maxwk,4)
        self.assertTrue(MrY.isavail(10,13,2020))
        self.assertTrue(MrY.isavail(10,15,2020))
        self.assertFalse(MrY.isavail(10,16,2020))
        print('\n','test_person_ended','\n',40*'*')
    def test_day(self):
        print('\n','test_day_started','\n',40*'*')
        XmasGen = day(theday=25,themonth=12)
        self.assertEqual(XmasGen.isXmas() ,True)
        XboxGen = day(theday=26,themonth=12)
        self.assertEqual(XboxGen.isBox() ,True)
        Xbox2020A = day(theday=26,themonth=12,theyear=2020)
        self.assertEqual(Xbox2020A.isBox() ,False)
        Xbox2020B = day(theday=28,themonth=12,theyear=2020)
        self.assertEqual(Xbox2020B.isBox() ,True)
        # check standard workweek in 2020
        

        print('\n','test_day_ended','\n',40*'*')  
    def test_Example1(self):
        print('\n','test_Example1_started','\n',40*'*')
        TB_Cas90 = person('Harold Henson',maxwk=4)
        TB_ECode = project('2020_TB_Ecode')
        TB_ECode.loaddays(TB_Cas90,90,2020,10,13)
        print(TB_ECode.listdays())
        print('\n','test_Example1_ended','\n',40*'*') 
        
        
        
        
        
        
if __name__ == '__main__':
    unittest.main()  
    
        
