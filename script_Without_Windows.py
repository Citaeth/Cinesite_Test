from os import listdir
from os.path import isfile, join

#---- Script by Clement Wallez----

def RecupPath(): #---list all filenames in path
    path=input()
    global files
    files = [f for f in listdir(path) if isfile(join(path, f))]
    
def IdSeqAnim(files): #---identify the different animated sequences
    global SeqAnim
    global countFiles
    SeqAnim=[] #--- List that will contain the name of animated sequences
    countFiles = len(files)
    for p in range(0, countFiles):
        nameTemp=files[p].rsplit('.', 2)[0] #---Keep just name, exclude .frame and .ext
        if nameTemp not in SeqAnim: #---if same file call more than one time, juste pick one 
            SeqAnim.append(nameTemp)

def ListFrameBySeq(files, SeqAnim, countFiles): #--- List Frame for each sequence
    countSeqAnim=len(SeqAnim)
    global FrameInSeq
    FrameInSeq=[] #--- Multidimensional List with one for each Sequence's Frames
    FrameTempList=[] #--- Temp List for count the Frame on actual sequence
    for f in range(0, countSeqAnim): #--- Repeat for each Sequence that was count before
        for p in range(0, countFiles):
            if files[p].rsplit('.', 2)[0] == SeqAnim[f]: #---Limit List by one Sequence
                Frame=files[p].rsplit('.', 2)[1]
                FrameTempList.append(Frame) #---Count Frame in the selected Sequence
        FrameInSeq.append(FrameTempList) #---Add a dimension to the list for the selected Sequence
        FrameTempList=[]

def checkConsecutive(testlst): #--- Check if 2 frames in the list follow each other or not
    return sorted(testlst) == list(range(min(testlst), max(testlst)+1))

def checkIfJustOneFrame(testlst, CountTest): #--- If two frames aren't consecutive, check if the previous Frame are in a series or not
    global Fr
    Fs=testlst[0]
    Fe=testlst[CountTest-1]
    if Fs==Fe: #--- If the frame are alone in the list
        Fr=str(Fs)
    if Fs != Fe: #--- If the frame aren't alone in the list, create a Frame Range
        Fr=str(Fs)+'-'+str(Fe)

def RegroupFrames(FrameInSeq): #--- Check in the List of Frames if some follow, and regroup them
    countLst = len(FrameInSeq)
    global FinalFrameList
    FinalFrameList=[] #--- List who will contain the Frames Ranges of Animated Sequences 
    for d in range(0, countLst):
        countFrame = len(FrameInSeq[d]) #--- Count Frame in Selected Sequence
        testlst = [] #--- Temp List to add frame and test if they're follow 
        keeplst = [] #--- List to Keep in order Frame Range or Alones Frames 

        for x in range (0,countFrame):
            checkInt=int(FrameInSeq[d][x]) #--- Switch the Frame number in an Integer
            if len(testlst)== 0:
                testlst.append(checkInt)
            else:
                if len(testlst) > 0:
                    testlst.append(checkInt)
                    checkConsecutive(testlst)
                    if checkConsecutive(testlst) == False: #--- If the two Frames do not follow each other
                        testlst.remove(checkInt) #--- Remove the last added Frame 
                        CountTest = len(testlst) 
                        checkIfJustOneFrame(testlst, CountTest) #--- Test if one or more frame remain, and create Frame Range if needed
                        testlst.clear()
                        testlst.append(checkInt) #--- Put back the removed frame in the test List
                        keeplst.append(Fr) #--- Put the Frame Range or the Frame in the Keep List
            
            if x==countFrame-1: #--- When we reach the last frame of the list 
                checkConsecutive(testlst) 
                if checkConsecutive(testlst) == False: #--- If the two Frames do not follow each other
                    testlst.remove(checkInt) #--- Remove the last added Frame 
                    CountTest = len(testlst)
                    checkIfJustOneFrame(testlst, CountTest) #--- Test if one or more frame remain, and create Frame Range if needed
                    keeplst.append(Fr) #--- Put the Frame Range or the Frame in the Keep List
                    keeplst.append(str(checkInt)) #--- Add the Last frame in the keep List

                else: #--- If the two Frames do follow each other
                    CountTest = len(testlst) 
                    checkIfJustOneFrame(testlst, CountTest) #--- create Frame Range 
                    keeplst.append(Fr) #--- Put the Frame Range or the Frame in the Keep List
            
        FinalFrameList.append(keeplst) #--- Add the curent Animated Sequence KeepLst in one Dimension of Final List

def PrintSeqFr(SeqAnim, FinalFrameList): #---Print All Animated Sequence and Frame Range in input directory 
    countSeqAnim=len(SeqAnim)
    for p in range (0,countSeqAnim):
        Seq = str(SeqAnim[p])
        FrameRange = str(FinalFrameList[p])
        FrameRange = FrameRange.replace('[', '')
        FrameRange = FrameRange.replace(']', '')
        FrameRange = FrameRange.replace("'", '')

        print(Seq+': '+FrameRange)

RecupPath()
IdSeqAnim(files)
ListFrameBySeq(files, SeqAnim, countFiles)
RegroupFrames(FrameInSeq)
PrintSeqFr(SeqAnim, FinalFrameList)