# Version 0.1 to be loaded onto GitHub

import datetime



class day():
    def __init__(self,theday,themonth,theyear,higherpriority=None):
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
    def isday(self,theday):
        """ return true if self equals the day of week"""
        """ Monday equals zero"""
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
        retval = False
        try:
            theday = datetime.date(self.year,self.month,self.day).weekday()
        except:
            return False
        if theday == 5 or theday == 6 :
            return True
        if(self.isgoodfriday(jurisdiction)) : return True
        if(self.isJeanB(jurisdiction)) : return True
        if(self.islabour()) : return True
        return retval
    def isgoodfriday(self,jurisdiction):
        if (datetime.date(2016,3,25) == datetime.date(self.year,self.month,self.day)
            and jurisdiction == "Que"): return True
    def isestMon(self,jurisdiction):
        if (datetime.date(2016,3,28) == datetime.date(self.year,self.month,self.day)
            and jurisdiction == "Que"): return True
    def isJeanB(self,jurisdiction):
        if (datetime.date(2016,6,24) == datetime.date(self.year,self.month,self.day)
            and jurisdiction == "Que"): return True
    def isVicDay(self,jurisdiction):
        if (datetime.date(2016,5,23) == datetime.date(self.year,self.month,self.day)
            and jurisdiction == "Que"): return True 
    def islabour(self):
        if (datetime.date(2016,9,5) == datetime.date(self.year,self.month,self.day)):
            return True
    def isCanday(self):
        if (datetime.date(2016,7,1) == datetime.date(self.year,self.month,self.day)):
            return True
    def isTGving(self):
        if (datetime.date(2016,10,10) == datetime.date(self.year,self.month,self.day)):
            return True
    def isRembrance(self):
        if (datetime.date(2016,11,11) == datetime.date(self.year,self.month,self.day)):
            return True
    def isXmas(self):
        if (datetime.date(2016,12,25) == datetime.date(self.year,self.month,self.day)):
            return True
    def hasconflict(self,highpriority = None):
        if(highpriority == None) :
            return False
        retval = highpriority.isavail(self.year,self.month,self.day)
        if retval == True :
            return False
        else:
            return True
    
        
    

class person():
    def __init__(self,pname):
        self.thename = pname
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
        # check if holiday
        a_holiday = self.isstat("Que")
    def __repr__(self):
        return "A day of work by "+ self.worker.getname()

class project():
    def __init__(self,projname,HigherPriority = None):
        """creates a project object"""
        self.projname = projname
        self.daydict = []
        self.daynum = 0
        # this represents another project that claims priority
        # over any given day
        self.higherPriority = HigherPriority
        self.listsorted = False
        self.firstday = None
        self.lastday = None
    def __repr__(self):
        return "Project "+ self.projnam 


    def add_day(self,theperson,theday,themon,theyear,comment=""):
        """ adds day to daydict for the person if possible """
        # add day to daydict if it is not a statutory holiday
        # or has a higher priority
        # or does not exist
        newday = workday(theperson,theday,themon,theyear,comment)
        # if day is a holiday do not add into list
        if newday.isstat("Que") :
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

    def isavail(self,theyear,themonth,theday):
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
                isadded = self.add_day(me,daycnt,monthcnt,2016)
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
                newday = day(daycnt,monthcnt,2016)
                if not newday.isday(dayofweek):
                    continue
                isadded = self.add_day(me,daycnt,monthcnt,2016,comment)
                if isadded : daynum += 1
                if daynum >= maxdays : return daynum
            # want to start at day one for next month
            initday = 1
        # should equal maxdays
        return daynum            
                

def loaddata():
    me = person('Harold Henson')
    Vac2016 = project('Vacation for HH')
    
    
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

    Vac2016.listdays()
    thetot = Vac2016.get_total()
    print("Total Days Used", thetot)

    ESDC2016 = project('90 day contract',Vac2016)
        
    ESDC2016.loaddays(me,88,2016,1,18)
    ESDC2016.listdays()
    thetot = ESDC2016.get_total()
    print("Total Days Used", thetot)
    
        
