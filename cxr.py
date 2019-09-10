import sys

class camper:
	def __init__(self,age,gender,grade,firstName,lastName):
		self.age=age
		self.gender=gender
		self.grade=grade
		self.firstName=firstName
		self.lastName=lastName
	def toString(self):
		return "age:"+self.age+" gender:"+self.gender+" grade:"+str(self.grade)+" name:"+self.firstName+" "+self.lastName
	def printString(self):
		print(self.toString())

filename="/storage/emulated/0/Download/RegistrationForm.csv"
myfile=open(filename)
myfile.readline() #remove header line

mCamperDict={}
mCamperDict[9]=[]
mCamperDict[10]=[]
mCamperDict[11]=[]
mCamperDict[12]=[]
mCamperDict[13]=[]

fCamperDict={}
fCamperDict[9]=[]
fCamperDict[10]=[]
fCamperDict[11]=[]
fCamperDict[12]=[]
fCamperDict[13]=[]

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
		count=str(len(myDict[grade]))
		dictByCount[grade]=[]
		dictByCount[grade]=count
	return dictByCount

def isBalanced(myDict):
	dictByCount=getCountDict(myDict)
	#check if all grades balanced within 1
	hi=int(dictByCount[max(dictByCount)])
	lo=int(dictByCount[min(dictByCount)])
	if hi-lo>=1:
		return False
	else:
		print("hi:"+hi+" lo:"+lo)
		print("balanced within 1")
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

#load data
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
		mCamperDict[grade].append(record)
	else:
		fCamperDict[grade].append(record)

#do rebalance
print(getCountDict(mCamperDict))
for i in range(0,10):
	#balance downward
	for grade in mCamperDict:
		if grade!=9:
			newDict=rebalance(mCamperDict,grade,True)
			mCamperDict=newDict
	#check balance
	if isBalanced(mCamperDict):
		break

print(getCountDict(mCamperDict))

for i in range(0,10):
	#balance upward
	for grade in mCamperDict:
		if grade!=13:
			newDict=rebalance(mCamperDict,grade,False)
			mCamperDict=newDict
	#check balance
	if isBalanced(mCamperDict):
		break

print(getCountDict(mCamperDict))

#rebalance(fCamperDict)