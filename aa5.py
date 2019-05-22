__author__ = 'JIANFENG LIN (Calvin)'

import random
import pretty_midi

import pygame
import tkinter as tkr
import os

from tkinter import *
from tkinter.filedialog import askopenfilename


#2-demension to 1-demension



##Encode System
import math

cipArray = [str(i) for i in range(0, 298+1)] #define the range of numbers
decArrayTemp = []
decArray = []
#decode = ''

#for cutting definition
midi_name = 'baga01'
pm = pretty_midi.PrettyMIDI(midi_name + '.mid')
partitions = []

#1. Generate (recursive function)
resultList=[]#用于存放结果的List
A = 0 #最小随机数
B = 200 #最大随机数
COUNT = 300
randomSeed = 14 #random seed depended on the weight
random.seed(randomSeed)


# 定义要创建的目录
cataNum = 0
mkpath="d:\\Sound_Sequences_Data\\" + str(cataNum)


playlistPath = ""

#Encode function
def transpostionEncrypt(msg,key):
    size = len(msg)
    result = []
    for i in range(key):
        t = i
        while t<size:
            result.append(msg[t])
            t+=key
    #return ''.join(result)
    #return result
    global cipArray
    cipArray = result
    print(cipArray)

##Decode function
def transpostionDecrypt(msg,key):

    numOfColums = int(math.ceil(len(msg)/float(key)))
    numOfRows = key
    sharedBox = numOfColums*numOfRows - len(msg)

    row = 0
    col = 0
    result = ['']*numOfColums
    for i in msg:
        result[col] = result[col] + i + '.'
        col+=1
        if col==numOfColums or (col==numOfColums-1 and row>=numOfRows-sharedBox):
            col=0
            row+=1

    i = 0
    resultTemp = []
    while i < len(result):
        a = result[i].split('.')
        #print(a)
        j = 0
        while j < len(a):
            if a[j] != "":
                resultTemp.append(a[j])
            j = j + 1
        #resultTemp.append(result[i].split('.'))
        i = i + 1
    #print(len(result))
    #print(resultTemp)
    global decArray
    decArray = resultTemp
    print(resultTemp)
    #return resultTemp
    #return ''.join(result)

##Password Main Function
# def main():
#     #global cipArray
    
#     #global cipher
#     #cipher = transpostionEncrypt("012345",3) #The plaintext is 012345; the key is 3
#     #cipArray = transpostionEncrypt(cipArray, 23)
#     print(cipArray)
#     #print (cipher[1])
 
#     #global decArray
#     #decArray = transpostionDecrypt(cipArray,23)Parentheses
#     print(decArray)
#     #decode = transpostionDecrypt(cipher,3)
#     #print (decode) #if the right key, the decode would display the right plaintext

# if __name__=="__main__":
#     main()


#生成随机数的递归数学，参数counter表示当前准备要生成的第几个有效随机数
def generateRand(counter): 
	
	tempInt=round(random.uniform(A,B),3) # 生成一个范围内的临时随机数，
	if(counter<=COUNT): # 先看随机数的总个数是不是够了，如果不够
		if(tempInt not in resultList): # 再检查当前已经生成的临时随机数是不是已经存在，如果不存在
			resultList.append(tempInt) #则将其追加到结果List中
			counter+=1 #然后将表示有效结果的个数加1. 请注意这里，如果临时随机数已经存在，则此if不成立，那么将直接执行16行，counter不用再加1
		generateRand(counter) #不管上面的if是否成立，都要递归。如果上面的临时随机数有效，则这里的conter会加1，如果上面的临时随机数已经存在了，则需要重新再生成一次随机数,counter不能变化
generateRand(1) #调用递归函数，并给当前要生成的有效随机数的个序号置为1，因为要从第一个开始嘛
#print(resultList)

#2. Sorting
def QuickSort(myList,start,end): #快排
    #判断low是否小于high,如果为false,直接返回
	if start < end:
		i,j = start,end
        #设置基准数
		base = myList[i]

		while i < j:
            #如果列表后边的数,比基准数大或相等,则前移一位直到有比基准数小的数出现
			while (i < j) and (myList[j] >= base):
				j = j - 1

            #如找到,则把第j个元素赋值给第个元素i,此时表中i,j个元素相等
			myList[i] = myList[j]

            #同样的方式比较前半区
			while (i < j) and (myList[i] <= base):
				i = i + 1
			myList[j] = myList[i]
        #做完第一轮比较之后,列表被分成了两个半区,并且i=j,需要将这个数设置回base
		myList[i] = base

        #递归前后半区
		QuickSort(myList, start, i - 1)
		QuickSort(myList, j + 1, end)
	return myList

#Create catagory
def mkdir(path): 
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        os.makedirs(path) 
        print (path+' Succeed')
        global playlistPath
        playlistPath = path
        return True
    else:
        print (path+' Existed')
        global cataNum
        cataNum = cataNum + 1
        mkpath="d:\\Sound_Sequences_Data\\" + str(cataNum)
        mkdir(mkpath)
        return False
        # global cataNum
        # cataNum = cataNum + 1
        # print(mkpath)



def cut():
    mkdir(mkpath)
    for partition in range(len(partitions)-1):
        start_time = partitions[partition]
        end_time = partitions[partition + 1]

        new_midi= pretty_midi.PrettyMIDI()
        global pm
        for instr_num in range (len(pm.instruments)):
            instrument = (pm.instruments[instr_num])

            notes_velocity=[]
            notes_pitch=[]
            notes_start = []
            notes_end = []

        # 找出start_time之后的第一个音符编号记作note_num
            for start_note_num in range (len(instrument.notes)):
                note = instrument.notes[start_note_num]
                start = note.start
                if start >= start_time:
                    break

            for end_note_num in range (len(instrument.notes)):
                note = instrument.notes[end_note_num]
                end = note.end
                if end > end_time:
                    break
        #将原midi中，区间内的音符记下
            for k in range(start_note_num,end_note_num):
                note = instrument.notes[k]
                notes_pitch.append(note.pitch)
                notes_start.append(note.start)
                notes_end.append(note.end)
                notes_velocity.append(note.velocity)

            program = instrument.program
            is_drum = instrument.is_drum
            name = instrument.name
            inst = pretty_midi.Instrument(program=program, is_drum=is_drum, name=name)
            new_midi.instruments.append(inst)

        # 粘到新midi里
            for i in range (end_note_num - start_note_num):
                inst.notes.append(pretty_midi.Note(notes_velocity[i], notes_pitch[i], notes_start[i]-float(start_time), notes_end[i]-float(start_time)))

        new_midi.write("d:/Sound_Sequences_Data/" + str(cataNum) + '/'+str(partition)+'.mid')
        #new_midi.write("d:/Sound_Sequences_Data/" + str(cataNum) + '/segmented_part'+str(partition)+'.mid')
    playListUpdate(playlistPath);

    

#generate the random number's list
myList = resultList
QuickSort(myList,0,len(myList)-1)
#print(myList)

partitions = myList
for i in range(len(partitions)):
	partitions[i]-= partitions[0]
#print(partitions)

#Create Window
player = tkr.Tk()

#Edit Window
player.title("Cryptography")
player.geometry("250x340")
player.resizable(width=False, height=False)
player.iconbitmap('interface.ico')

#Playlist Register
os.chdir("D:/Documents/Newcastle University/(DMS8013)Advanced Creative Digital Practice/project3/Midi/4/playlist")
#print("AAAAAA",os.getcwd)
songlist = os.listdir()

#Volume Input
#VolumeLevel = tkr.Scale(player, from_=0.0, to_=1.0, orient = tkr.HORIZONTAL, resolution = 0.1)

#Playlist Input
playlist = tkr.Listbox(player, highlightcolor = "blue", selectmode = tkr.SINGLE)
#print("song list is: ",songlist)

for item in songlist:
	pos = 0
	playlist.insert(pos, item)
	pos = pos + 1


def playListUpdate(var_path):
    #Playlist Register
    global playlist
    playlist.delete(0, END)
    print("var_path = ", var_path)


    # path_list = var_path.split("\\")
    # path_str = ""
    # for i in path_list:
    #     if len(i) <= 0:
    #         continue
    #     path_str += "/" + i
    # new_str = path_str[1:]
    # print("New One:", new_str)
    os.chdir(var_path)
    songlist = os.listdir(var_path)
    songlist.sort(key=lambda x:int(x[:-4]))
    #Volume Input
    #VolumeLevel = tkr.Scale(player, from_=0.0, to_=1.0, orient = tkr.HORIZONTAL, resolution = 0.1)
    #Playlist Input
    print("New Songlist: ", songlist)

    for item in songlist:
        pos = 0
        playlist.insert(pos, item)
        pos = pos + 1
    change_btn(songlist)



#playlist.select_set(2)

#Pygame Init
pygame.init()
pygame.mixer.init()

s = pygame.mixer.Sound('E:/white1.wav')
s.play()

#global a
a = 0

#Clock
clock = pygame.time.Clock()

#button state
def change_btn(songlist):
    if len(songlist):
        button1['state'] = 'normal'
    else:
        button1['state'] = 'disabled'


#Action Event
def Play():
    Bgm()
	#pygame.mixer.music.load(playlist.get(tkr.ACTIVE))
    global a
    numberSum = len(decArray)-1

	#print(cipher)


    if(playlist.get(a) != ''):
		#pygame.mixer.music.load(playlist.get(a))
        pygame.mixer.music.load(playlist.get(decArray[numberSum - a]))

        #var.set(playlist.get(tkr.ACTIVE))
		#var.set(playlist.get(cipher[a]))
		#var.set(playlist.get(a))
        print("a:", a, " - cipher:", decArray[numberSum - a])
        pygame.mixer.music.play()
        Next()
		#print(pygame.mixer.music.get_busy())
        while pygame.mixer.music.get_busy():
			#print(clock.tick(1))
            clock.tick(60)
			
        Play()
    else:
        a = 0
        ExitPlayer()

	
	# pygame.mixer.music.set_volume(VolumeLevel.get())
	# print(pygame.mixer.music.get_volume())
	# print(VolumeLevel.get())


def ExitPlayer():
	pygame.mixer.music.stop()
	s.stop()
# def Pause():
# 	pygame.mixer.music.pause()

# def UnPause():
# 	pygame.mixer.music.unpause()	

def Next():
	global a
	a = a + 1

def Bgm():
	s.play()


def selectPath():
    path_ = askopenfilename()
    path.set(path_)
    print(path_)
    button5['state'] = 'normal'
    global pm
    pm = pretty_midi.PrettyMIDI(path_)

def getValue():
    var = entry2.get()
    v = int(var)
    transpostionEncrypt(cipArray, v)

def getValue2():
    var = entry3.get()
    v = int(var)
    global decArrayTemp
    decArrayTemp = cipArray
    transpostionDecrypt(decArrayTemp,v)



path = StringVar()
#Rigister Buttons
button1 = tkr.Button(player, width = 5, height = 3, text = "PLAY", command = Play)
change_btn(songlist)
#button2 = tkr.Button(player, width = 5, height = 3, text = "STOP", command = ExitPlayer)
#button3 = tkr.Button(player, width = 5, height = 3, text = "NEXT", command = Next)

entry1 = tkr.Entry(player, textvariable = path)
button4 = tkr.Button(player, text = "Select MIDI", command = selectPath) #original file
button5 = tkr.Button(player, text = "Cut", command = cut, state = 'disabled')

label1 = tkr.Label(player, text = "---------- ENCODE ----------")
entry2 = tkr.Entry(player)
button6 = tkr.Button(player, text = "Encode", command = getValue)  #command = transpostionEncrypt(cipArray, 25)

label2 = tkr.Label(player, text = "---------- DECODE ----------")
entry3 = tkr.Entry(player)
button7 = tkr.Button(player, text = "Decode", command = getValue2)  #command = transpostionEncrypt(cipArray, 25)

#Song Names
#var = tkr.StringVar()
#songtitle = tkr.Label(player, textvariable = var)



#Place Widgets
#songtitle.pack()

#button2.pack(fill = "x")
#button3.pack(fill = "x")
entry1.pack(fill = "x", pady = "5", padx = "5")
button4.pack(fill = "x", pady = "5", padx = "50")
button5.pack(fill = "x", pady = "5", padx = "50")

label1.pack()
entry2.pack(fill = "x", padx = "50")
button6.pack(pady = "5")

label2.pack()
entry3.pack(fill = "x", padx = "50")
button7.pack(pady = "5")

button1.pack(fill = "x", pady = "5", padx = "5")

# VolumeLevel.pack(fill = "x")
#playlist.pack(fill = "both", expand = "yes")


#Activate
player.mainloop()


# while 1:
#     if pygame.mixer.music.get_busy() == False:
#         print("播放音乐3")
#         pygame.time.delay(1000)
#         print("播放音乐2")
#         pygame.time.delay(1000)
#         print("播放音乐1")
#         break;
