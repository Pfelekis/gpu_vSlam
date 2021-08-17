import time



class Timer(object):
    #A class keeping and updating the time for each of sub-functions
    def __init__(self,frames):

        self.totalTime= 0
        self.extractTime= 0
        self.matchTime=0
        self.triangulateTime=0
        self.frameNum=frames
        self.totalList=[]
        self.extractList=[]
        self.matchList=[]
        self.triangulateList=[]

    def totalTimer(self, startT):

        if startT:
            self.totalTime=time.time()
            return
        else:
            endTime=time.time()
            self.totalTime= endTime- self.totalTime
            self.totalList.append(float(self.totalTime))

    def extractionTimer(self, startExT):
        
        if startExT:
            self.exStartTime= time.time()
        else:
            endExTime= time.time()
            self.extractTime= endExTime- self.exStartTime
            self.extractList.append(float(self.extractTime))
            

    def matchTimer(self, startMatchT):

        if startMatchT:
            self.startMatchTime= time.time()
        else:
            endMatchTime= time.time()
            self.matchTime= endMatchTime - self.startMatchTime - 0.013
            self.matchList.append(float(self.matchTime))
    
    def triangulateTimer(self, startTriT):

        if startTriT:
            self.startTriTime= time.time()
        else:
            endTriTime= time.time()
            self.triangulateTime=endTriTime-self.startTriTime
            self.triangulateList.append(self.triangulateTime)
    
    def getAverage(self,lst):
        return 1000 * sum(lst) / (len(lst) +1)

    def printTime(self):
        

        print('Total time:',"%.2f" %self.totalList[0], 'second')
        print('Average extract time:',"%.2f" %self.getAverage(self.extractList), 'ms')
        print('Average matchTimer:',"%.2f" %self.getAverage(self.matchList), 'ms')
        print('Average Triangulate Time:',"%.2f" %self.getAverage(self.triangulateList), 'ms')
        
    
