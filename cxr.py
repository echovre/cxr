debug=True

class camper:
   	def __init__(self,age,gender,grade,firstName,lastName):
          self.age=age
          self.gender=gender
          self.grade=grade
          self.firstName=firstName
          self.lastName=lastName
   	def toString(self):
          return "age:"+self.age+" gender:"+self.gender+" grade:"+str(self.grade)+" name:"+self.firstName+" "+self.lastName
    #def printString(self):
    #    print(self.toString())


def getGrade(grade):
   grade=grade.split()[0]
   if not grade.endswith("th"):
      grade=13
   else:
      grade=grade.split("th")[0]
   return int(grade)

def getAgeInGrade(campers,isMin):
   dictByAge={}
   for camper in campers:
      dictByAge[camper.age]=[]
      dictByAge[camper.age].append(camper)
      if isMin:
         youngest=dictByAge[min(dictByAge)]
         assert(len(youngest)==1)
         return youngest[0]
      else:
         oldest=dictByAge[max(dictByAge)]
         assert(len(oldest)==1)
         return oldest[0]

def getCountDict(myDict):
   dictByCount={}
   for grade in myDict:
      #get count per grade
      count=len(myDict[grade])
      dictByCount[grade]=[]
      dictByCount[grade]=count
   return dictByCount

def isBalanced(myDict):
   dictByCount=getCountDict(myDict)
   #check if all grades balanced within 1
   hi=max(dictByCount, key=dictByCount.get)
   lo=min(dictByCount, key=dictByCount.get)
   #if debug: print("max:",hi,dictByCount[hi],"min:",lo,dictByCount[lo])
   if dictByCount[hi]-dictByCount[lo]>1:
      return False
   else:
      if debug: print("balanced within 1")
      return True

def getAdjacentGradesCount(myDict,g):
   dictByCount=getCountDict(myDict)
   if g+1>=13:
      aboveCount=-1
   else:
      aboveCount=dictByCount[g+1]
   if g-1<=8:
      belowCount=-1
   else:
      belowCount=dictByCount[g-1]
   return int(aboveCount),int(belowCount)

def rebalance(myDict,grade,isDownward):
   if isBalanced(myDict):
      return myDict
   curr=int(getCountDict(myDict)[grade])
   #get count of grades above and below
   a,b=getAdjacentGradesCount(myDict,grade)
   if isDownward:
      if a!=-1 and a<curr:
         myDict=moveCamper(myDict,grade,isDownward)
   else:
      if b!=-1 and b<curr:
         myDict=moveCamper(myDict,grade,isDownward)
   return myDict

def moveCamper(myDict,grade,isDownward):
   y=getAgeInGrade(myDict[grade],isDownward)
   myDict[grade].remove(y)
   if isDownward:
      myDict[grade-1].append(y)
   else:
      myDict[grade+1].append(y)
   return myDict

def loadData(myfile):
   mDict={}
   mDict[9]=[]
   mDict[10]=[]
   mDict[11]=[]
   mDict[12]=[]
   mDict[13]=[]
   
   fDict={}
   fDict[9]=[]
   fDict[10]=[]
   fDict[11]=[]
   fDict[12]=[]
   fDict[13]=[]
   for line in myfile:
      data=line.split(",")
      #TODO age+grade as key?
      age=data[4]
      gender=data[5]
      grade=getGrade(data[6])
      firstName=data[2]
      lastName=data[3]
      record=camper(age,gender,grade,firstName,lastName)
      if(gender=="Male"):
         mDict[grade].append(record)
      else:
         fDict[grade].append(record)
   return [mDict,fDict]

def getTotalCampers(camperDict):
   total=0
   for key in camperDict.keys():
      total+=len(camperDict[key])
   return total

def callRebalance(camperDict,gradeLimit,isDownward):
       newDict={}
       #balance downward
       for grade in camperDict:
          if grade!=gradeLimit:
             result=rebalance(camperDict,grade,isDownward)
             newDict=result
       return newDict

def rebalEdgesInward(camperDict,loGrade,hiGrade):
   countDict=getCountDict(camperDict)
   hi=countDict[hiGrade]
   secondHighest=countDict[hiGrade-1]
   if hi>secondHighest+1:
      camperDict=moveCamper(camperDict,hiGrade,True)

   countDict=getCountDict(camperDict)
   lo=countDict[loGrade]
   secondLowest=countDict[loGrade+1]
   if lo>secondLowest+1:
      camperDict=moveCamper(camperDict,loGrade,False)
      
   return camperDict

def detectRebalWalls(camperDict):
   countDict=getCountDict(camperDict)
   lowest=0
   highest=float("inf")
   for key in countDict:
      value=countDict[key]
      if value>highest:
         highest=value
      if value<lowest:
         lowest=value
         
def rebalMax(camperDict,minGrade,maxGrade):
   dictByCount=getCountDict(camperDict)
   
   hi=max(dictByCount, key=dictByCount.get)
   if hi!=minGrade and  hi!=maxGrade:
      hiLeft=dictByCount[hi-1]
      hiRight=dictByCount[hi+1]
      if hiLeft>hiRight:
         camperDict=moveCamper(camperDict,hi,True)
      elif hiRight>hiLeft:
         camperDict=moveCamper(camperDict,hi,False)
   else:
      camperDict=moveCamper(camperDict,hi,hi==maxGrade)
      
   return camperDict

def rebalMin(camperDict,minGrade,maxGrade):
   dictByCount=getCountDict(camperDict)
   
   lo=min(dictByCount, key=dictByCount.get)
   if lo!=minGrade and lo!=maxGrade:
      loLeft=dictByCount[lo-1]
      loRight=dictByCount[lo+1]
      if loLeft>loRight:
         camperDict=moveCamper(camperDict,loLeft,False)
      elif loRight>loLeft:
         camperDict=moveCamper(camperDict,loRight,True)
   else:
      if lo==minGrade:
         camperDict=moveCamper(camperDict,lo+1,True)
      elif lo==maxGrade:
         camperDict=moveCamper(camperDict,lo-1,False)
      
   return camperDict


#filename="/storage/emulated/0/Download/RegistrationForm.csv"
filename="/home/echo/RegistrationForm.csv"
myfile=open(filename)
myfile.readline() #remove header line
[mCamperDict,fCamperDict]=loadData(myfile)

#do rebalance
totalMaleInit=getTotalCampers(mCamperDict)
print("Initial male campers:",getCountDict(mCamperDict),"Total:",totalMaleInit)

newMDict=mCamperDict
for i in range(0,9):
   newMDict=rebal(newMDict,9,13)
   """
   newMDict=rebalEdgesInward(newMDict,9,13)
   newMDict=callRebalance(newMDict,9,True)
   newMDict=callRebalance(newMDict,13,False)
   newMDict=rebalEdgesInward(newMDict,9,13)
   """
   if debug: print(getCountDict(newMDict))
   if isBalanced(newMDict):
      break

totalMaleFinal=getTotalCampers(newMDict)
assert(totalMaleInit==totalMaleFinal)
print("  Final male campers:",getCountDict(newMDict),"Total:",totalMaleFinal)



print("======================")


#do rebalance
totalFemaleInit=getTotalCampers(fCamperDict)
print("Initial Female campers:",getCountDict(fCamperDict),"Total:",totalFemaleInit)

newFDict=fCamperDict
for i in range(0,10):
   newFDict=rebalMax(newFDict,9,13)
   """
   newFDict=rebalEdgesInward(newFDict,9,13)
   newFDict=callRebalance(newFDict,9,True)
   newFDict=callRebalance(newFDict,13,False)
   newFDict=rebalEdgesInward(newFDict,9,13)
   """
   if debug: print(getCountDict(newFDict))
   if isBalanced(newFDict):
      break

totalFemaleFinal=getTotalCampers(newFDict)
assert(totalFemaleInit==totalFemaleFinal)
print("  Final Female campers:",getCountDict(newFDict),"Total:",totalFemaleFinal)
