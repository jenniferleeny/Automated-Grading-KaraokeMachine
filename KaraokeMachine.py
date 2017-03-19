#!/usr/bin/python
import sys
import aubio
from aubio import source, pitch, sink, digital_filter
from os import path
from scipy.io import wavfile
import threading
import pyaudio
import wave
import time
from tkinter import *
import PIL
from PIL import ImageTk, Image

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 11025
RECORD_SECONDS = 240

AUDIO_FILE = "record2.wav"

##song image constants
GRAVITY_GIF = "gif/Gravity_SaraBareilles.gif"
SUNDAYMORNING_GIF = "gif/SundayMorning_Maroon5.gif"
GOLDDIGGER_GIF = "gif/GoldDigger_KanyeWest.gif"
GRENADE_GIF = "gif/Grenade_BrunoMars.gif"
IMMORTALS_GIF = "gif/Immortals_FallOutBoy.gif"
REHAB_GIF = "gif/Rehab_AmyWinehouse.gif"
WHOKNEW_GIF = "gif/WhoKnew_P!nk.gif"
FLYMETOTHEMOON_GIF = "gif/FlyMeToTheMoon_FrankSinatra.gif"
##song wav files
GRAVITY_WAV = "Gravity_SaraBareilles.wav"
SUNDAYMORNING_WAV = "SundayMorning_Maroon5.wav"
GOLDDIGGER_WAV = "GoldDigger_KanyeWest.wav"
GRENADE_WAV = "Grenade_BrunoMars.wav"
IMMORTALS_WAV = "Immortals_FallOutBoy.wav"
REHAB_WAV = "Rehab_AmyWinehouse.wav"
WHOKNEW_WAV = "WhoKnew_P!nk.wav"
FLYMETOTHEMOON_WAV = "FlyMeToTheMoon_FrankSinatra.wav"

#############################################BUTTON CLASS############################################################
#####################################################################################################################
root=Tk()
class Button(object):
	def __init__(self, text, xstart, ystart, width, height):
		self.text = text
		self.x = xstart
		self.y = ystart
		self.width = width
		self.height = height

	def printButton(self, canvas, w=3):
		canvas.create_rectangle(self.x, self.y, self.x+self.width, self.y+self.height, fill ='dim gray')
		canvas.create_text(self.x+self.width//2, self.y+self.height//2, text=self.text, fill='white',font='Helvetica 15 bold')
		
	def getBounds(self):
		return (self.x, self.y, self.x+self.width, self.y + self.height)

	def isClicked(self, x, y):
		if (self.x < x < self.x+self.width and self.y<y<self.y+self.height):
			return True
		return False

##############################################TKINTER###############################################
####################################################################################################

def init(data):
	data.homeScreenHeight = 0
	data.buttonWidth = 120
	data.buttonHeight = 50
	data.margin = 25
	data.songButtonWidth = (data.width-6*data.margin)//2
	data.songButtonHeight = (data.height-10*data.margin-50)//4
	data.buttons = []
	data.mode = 'home'
	data.play = False
	data.songFilename = ""
	data.seconds = 0
	data.timing = []
	data.lyrics = []
	data.score = None
	data.index = 0
	#IMAGE IMPORT
	width = 90
	data.gravImg = PIL.Image.open(GRAVITY_GIF)
	data.grenImg = PIL.Image.open(GRENADE_GIF)
	data.sunImg = PIL.Image.open(SUNDAYMORNING_GIF)
	data.rehabImg = PIL.Image.open(REHAB_GIF)
	data.goldImg = PIL.Image.open(GOLDDIGGER_GIF)
	data.flyImg = PIL.Image.open(FLYMETOTHEMOON_GIF)
	data.immImg = PIL.Image.open(IMMORTALS_GIF)
	data.whoImg = PIL.Image.open(WHOKNEW_GIF)

	wpercent = width/float(data.gravImg.size[0])
	hpercent=int(float(data.gravImg.size[1])*float(wpercent))
	data.gravImage = PIL.ImageTk.PhotoImage(data.gravImg.resize((width, hpercent), PIL.Image.ANTIALIAS))
	data.grenImage = PIL.ImageTk.PhotoImage(data.grenImg.resize((width, hpercent), PIL.Image.ANTIALIAS))
	data.sunImage = PIL.ImageTk.PhotoImage(data.sunImg.resize((width, hpercent), PIL.Image.ANTIALIAS))
	data.rehabImage = PIL.ImageTk.PhotoImage(data.rehabImg.resize((width, hpercent), PIL.Image.ANTIALIAS))
	data.goldImage = PIL.ImageTk.PhotoImage(data.goldImg.resize((width, hpercent), PIL.Image.ANTIALIAS))
	data.flyImage = PIL.ImageTk.PhotoImage(data.flyImg.resize((width, hpercent), PIL.Image.ANTIALIAS))
	data.immImage = PIL.ImageTk.PhotoImage(data.immImg.resize((width, hpercent), PIL.Image.ANTIALIAS))
	data.whoImage = PIL.ImageTk.PhotoImage(data.whoImg.resize((width, hpercent), PIL.Image.ANTIALIAS))


def keyPressed(event, data):
	if data.mode == 'play': playKeyPressed(event, data)

def mousePressed(event, data):
    if (data.mode == "home"): homeScreenMousePressed(event, data)
    elif (data.mode == "play"): playScreenMousePressed(event, data)
    elif (data.mode == "songSelection"): songSelectionMousePressed(event, data)
    elif (data.mode == "help"): helpMousePressed(event, data)

def timerFired(data):
	if (data.mode == 'play'): playScreenTimerFired(data)

def redrawAll(canvas, data):
	if (data.mode == "home"): homeScreen(data, canvas)
	elif (data.mode == "play"): playScreen(data, canvas)
	elif (data.mode == "songSelection"): songSelectionScreen(data, canvas)
	elif (data.mode == "help"): helpScreen(data, canvas)

###Homescreen###
def homeScreen(data, canvas):
	canvas.create_rectangle(0, 0, data.width, data.height, fill='black')
	canvas.create_text(data.width//2, data.height//3-30, text='AUTOMATED GRADING', fill = 'white', font = 'Verdana 45 bold')
	canvas.create_text(data.width//2, data.height//3+30, text = 'KARAOKE MACHINE', fill = 'white', font = 'Verdana 45 bold')
	startButton = Button("S T A R T", data.width//2-data.buttonWidth//2 - 100, 
		data.height//2-data.buttonHeight//2+50, data.buttonWidth, data.buttonHeight)
	helpButton = Button("H E L P", data.width//2-data.buttonWidth//2 + 100, 
		data.height//2-data.buttonHeight//2 + 50, data.buttonWidth, data.buttonHeight)
	data.buttons=[startButton, helpButton]
	for i in data.buttons:
		i.printButton(canvas)
	
###Help###
def helpScreen(data, canvas):
	backButton = Button("B A C K", 2*data.margin, data.height - data.buttonHeight - data.margin, data.buttonWidth, data.buttonHeight)
	canvas.create_rectangle(0, 0, data.width, data.height, fill = 'dark slate gray')
	data.buttons = [backButton]
	for i in data.buttons:
	 	i.printButton(canvas)
	instructions="Like most karaoke machines, this program will let you choose a song to play for you to sing along \nwith."
	instructions += "However, there's a slight catch: YOU WILL RECEIVE A GRADE FOR YOUR SINGING!"
	instructions+="(Yes, \neven your singing is graded and judged at CMU)."
	instructions+="See how well of a singer you are whether you're \nsinging during your study breaks or just on your own time.\n\n"
	instructions+="Navigate through the different pages using the buttons and start the karaoke session just by \nclicking anywhere on the screen. "
	instructions+="Make sure to use \nheadphones when using this program."
	instructions+="At the end of the song, you will receive a grade out of a 100."
	canvas.create_text(2*data.margin, 2*data.margin, text="How Do I Use This Karaoke Machine?",
	fill = "peach puff", font="Veranda 40 bold", anchor = NW)
	canvas.create_text(2*data.margin, 5*data.margin, text=instructions, 
		fill = "peach puff", font="Veranda 20", anchor = NW)
	canvas.create_text(2*data.margin, 13*data.margin, text="What Am I Graded On?", 
		fill = "peach puff", font="Veranda 30 bold", anchor = NW)
	grading = "The grade will be based off of pitch."
	canvas.create_text(2*data.margin, 15*data.margin, text=grading, 
		fill = "peach puff", font="Veranda 20", anchor = NW)

def helpMousePressed(event, data):
	if len(data.buttons) == 1:
		if (data.buttons[0].isClicked(event.x, event.y)):
			data.mode = 'home'

def homeScreenMousePressed(event, data):
	if len(data.buttons) == 2:
		if (data.buttons[0]).isClicked(event.x, event.y):
			data.mode = 'songSelection'
		elif (data.buttons[1]).isClicked(event.x, event.y):
			data.mode = 'help'

###Song Selection###
def songSelectionScreen(data, canvas):
	canvas.create_rectangle(0, 0, data.width, data.height, fill = 'black')
	canvas.create_text(2*data.margin, data.margin, anchor = NW,text="SONG SELECTION", fill = "white", font = "Verdana 40 bold")
	canvas.create_line(0, 2*data.margin+50, data.width, 2*data.margin+50, fill='white', width=4)
	#first column
	gravityButton = Button('Gravity - Sara Bareilles', 2*data.margin, 50+3*data.margin, 
		data.songButtonWidth, data.songButtonHeight)
	grenadeButton = Button("Grenade - Bruno Mars", 2*data.margin, 
		50+4*data.margin+data.songButtonHeight, data.songButtonWidth, data.songButtonHeight)
	sundayMorningButton= Button('Sunday Morning - Maroon5', 2*data.margin, 
		50+5*data.margin+2*data.songButtonHeight, data.songButtonWidth, data.songButtonHeight)
	rehabButton=Button('Rehab - Amy Winehouse', 2*data.margin,
		50+6*data.margin+3*data.songButtonHeight, data.songButtonWidth, data.songButtonHeight)
	#second column
	goldDiggerButton=Button('Gold Digger - Kanye West', 3*data.margin + data.songButtonWidth,
		50+3*data.margin, data.songButtonWidth, data.songButtonHeight)
	flyMeToTheMoonButton=Button('\tFly Me To The Moon - Frank Sinatra', 3*data.margin + data.songButtonWidth,
		50+4*data.margin+data.songButtonHeight, data.songButtonWidth, data.songButtonHeight)
	immortalsButton=Button('Immortals - Fall Out Boy', 3*data.margin + data.songButtonWidth,
		50+5*data.margin+2*data.songButtonHeight, data.songButtonWidth, data.songButtonHeight)
	whoKnewButton=Button('Who Knew - P!nk', 3*data.margin + data.songButtonWidth,
		50+6*data.margin+3*data.songButtonHeight, data.songButtonWidth, data.songButtonHeight)

	backButton = Button("B A C K", 2*data.margin, data.height-data.margin-data.buttonHeight, data.buttonWidth, data.buttonHeight)
	data.buttons=[gravityButton,grenadeButton,sundayMorningButton, rehabButton, 
	goldDiggerButton, flyMeToTheMoonButton, immortalsButton, whoKnewButton, backButton]
	for i in data.buttons:
	 	i.printButton(canvas)
	printAlbumCover(data,canvas)

def printAlbumCover(data, canvas):
	increment_x = 52
	increment_y = 1
	#left column
	canvas.create_image(data.buttons[0].x+increment_x, 
		data.buttons[0].y+data.buttons[0].height//2+increment_y, image= data.gravImage)
	canvas.create_image(data.buttons[1].x+increment_x, 
		data.buttons[1].y+data.buttons[1].height//2+increment_y, image= data.grenImage)
	canvas.create_image(data.buttons[2].x+increment_x, 
		data.buttons[2].y+data.buttons[2].height//2+increment_y, image= data.sunImage)
	canvas.create_image(data.buttons[3].x+increment_x, 
		data.buttons[3].y+data.buttons[3].height//2+increment_y, image= data.rehabImage)
	#right column
	canvas.create_image(data.buttons[4].x+increment_x, 
		data.buttons[4].y+data.buttons[4].height//2+increment_y, image= data.goldImage)
	canvas.create_image(data.buttons[5].x+increment_x, 
		data.buttons[5].y+data.buttons[5].height//2+increment_y, image= data.flyImage)
	canvas.create_image(data.buttons[6].x+increment_x, 
		data.buttons[6].y+data.buttons[6].height//2+increment_y, image= data.immImage)
	canvas.create_image(data.buttons[7].x+increment_x, 
		data.buttons[7].y+data.buttons[7].height//2+increment_y, image= data.whoImage)


def songSelectionMousePressed(event, data):
	for i in data.buttons:
		if (i.isClicked(event.x, event.y)):
			if i.text == 'B A C K': data.mode = 'home'
			else:
				data.mode = 'play'
				data.score = None
				data.songFilename = i.text.replace(" ", "").replace("-", "_").replace('\t',"") + '.wav'

###Play Screen###
def playScreen(data, canvas):
	print(data.index)
	backButton = Button("Back to Song Selection", 2*data.margin, data.height 
		-data.buttonHeight-data.margin, data.buttonWidth*2, data.buttonHeight)
	data.buttons = [backButton]
	canvas.create_rectangle(0, 0, data.width, data.height, fill='dark slate grey')
	if data.play == True:
		if data.index == 0:
			canvas.create_text(data.width//2, data.height//2, text='[Instrumentals]', fill = 'white', font="Veranda 30")
		elif data.score != None:
			data.buttons[0].printButton(canvas)
			canvas.create_text(data.width//2, data.height//2 - 4*data.margin,text="S C O R E:", fill = "white", font="Veranda 70")
			canvas.create_text(data.width//2, data.height//2, text=str(round(data.score)), fill = 'white', font = "Veranda 70")
		else:
			canvas.create_text(data.width//2, data.height//2,
			justify=CENTER,text=data.lyrics[data.index], fill = 'white', font="Veranda 30")	
	elif data.play == False and data.score == None:
		data.buttons[0].printButton(canvas)
		canvas.create_text(data.width//2, data.height//2, text="Press anywhere to start", fill = 'white', font = "Veranda 30")

def playKeyPressed(event, data):
	pass

def playScreenTimerFired(data):
	if data.play==True and data.index < len(data.lyrics)-1:
		seconds = data.timing[data.index+1]-data.timing[data.index]
		#print(seconds)
		start = end = time.time()
		while(end - start < seconds):
			end = time.time()
		data.index += 1
	elif data.play == True and (threading.active_count() < 3):
		calculateScore(data)

def calculateScore(data):
	userPitches = getPitch(AUDIO_FILE)
	realPitches = getPitch(data.songFilename)
	realNotes = convertPitchesToNotes(realPitches)
	userNotes = convertPitchesToNotes(userPitches)
	data.score = min(100, round(pitchAlgorithm(userPitches, realPitches)))

def playScreenMousePressed(event, data):
	if (data.play==False and data.buttons[0].isClicked(event.x, event.y)):
		data.mode = "songSelection"
	elif (data.play==False and 0<=event.x<=data.width and 0<=event.y<=data.height):
		data.play = True
		playSong(data)
	elif data.play==True and (threading.active_count() < 3) and data.buttons[0].isClicked(event.x, event.y):
		data.mode="songSelection"
		data.score=None
		data.play=False
		data.lyrics=[]
		data.seconds = 0
		data.timing = []
		data.index = 0

#should only be called once
def playSong(data):
	if data.play == True:
		Lyrics(data)
		threading.Thread(target=thread_record, args = (AUDIO_FILE,)).start()
		threading.Thread(target=thread_play, args = (data.songFilename, )).start()
	print("Done!")

def run(width=1000, height=800):
	def redrawAllWrapper(canvas, data):
		canvas.delete(ALL)
		redrawAll(canvas, data)
		canvas.update()    
	def mousePressedWrapper(event, canvas, data):
		mousePressed(event, data)
		redrawAllWrapper(canvas, data)
	def keyPressedWrapper(event, canvas, data):
		keyPressed(event, data)
		redrawAllWrapper(canvas, data)
	def timerFiredWrapper(canvas, data):
		timerFired(data)
		redrawAllWrapper(canvas, data)
		# pause, then call timerFired again
		canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
	class Struct(object): pass
	data = Struct()
	data.width = width
	data.height = height
	data.timerDelay = 100 # milliseconds
	init(data)
	# create the root and the canvas
	#root = Tk()
	canvas = Canvas(root, width=data.width, height=data.height)
	canvas.pack()
    # set up events
	root.bind("<Button-1>", lambda event:
							mousePressedWrapper(event, canvas, data))
	root.bind("<Key>", lambda event:
							keyPressedWrapper(event, canvas, data))
	timerFiredWrapper(canvas, data)
	# and launch the app
	root.mainloop()  # blocks until window is closed
	print("bye!")

##################################################################################################################
##################################################################################################################
def gravity(data, lyrics):
	i = lyrics.index('Gravity_SaraBareilles.wav\n')
	gravitylyrics=lyrics[i:]
	try:
		e = gravitylyrics.index('\n')
		gravitylyrics = gravitylyrics[:e]
	except:
		print("Assume it's the last song in the list")
	gravitylyrics = ''.join(gravitylyrics)
	gravitylyrics = gravitylyrics.split('@\n')
	data.lyrics = gravitylyrics
	data.seconds = 3*60+53
	data.timing = [0, 13, 39, 62, 93, 118, 120+30, 180+25]

def goldDigger(data, lyrics):
	i = lyrics.index('GoldDigger_KanyeWest.wav\n')
	goldDiggerlyrics=lyrics[i+1:]
	try:
		e = goldDiggerlyrics.index('\n')
		goldDiggerlyrics=goldDiggerlyrics[:e]
	except:
		print("assume it's the last element in the list")
	goldDiggerlyrics = ''.join(goldDiggerlyrics)
	goldDiggerlyrics = goldDiggerlyrics.split('@\n')
	data.lyrics = goldDiggerlyrics
	data.seconds = 3*60+30
	data.timing = [0, 0, 16, 37,50,70,79,100,110,131,141,162,177,194]

def sundayMorning(data, lyrics):
	i = lyrics.index('SundayMorning_Maroon5.wav\n')
	sundayMorninglyrics=lyrics[i+1:]
	try:
		e = sundayMorninglyrics.index('\n')
		sundayMorninglyrics=sundayMorninglyrics[:e]
	except:
		print("assume it's the last element in the list")
	sundayMorninglyrics = ''.join(sundayMorninglyrics)
	sundayMorninglyrics = sundayMorninglyrics.split('@\n')
	data.lyrics = sundayMorninglyrics
	data.seconds = 3*60+58
	data.timing = [0, 7, 15, 36, 58, 60+21, 60+42, 120+18, 120+21,120+42, 180+9]

def grenade(data, lyrics):
	i = lyrics.index('Grenade_BrunoMars.wav\n')
	grenadelyrics=lyrics[i+1:]
	try:
		e = grenadelyrics.index('\n')
		grenadelyrics=grenadelyrics[:e]
	except:
		print("assume it's the last element in the list")
	grenadelyrics = ''.join(grenadelyrics)
	grenadelyrics = grenadelyrics.split('@\n')
	data.lyrics = grenadelyrics
	data.seconds = 3*60+43
	data.timing = [0, 4,21,37, 54,73,95,111,127,144,166,184]

def immortals(data, lyrics):
	i = lyrics.index('Immortals_FallOutBoy.wav\n')
	immortallyrics=lyrics[i+1:]
	try:
		e = immortallyrics.index('\n')
		immortallyrics=immortallyrics[:e]
	except:
		print("assume it's the last element in the list")
	immortallyrics = ''.join(immortallyrics)
	immortallyrics = immortallyrics.split('@\n')
	data.lyrics = immortallyrics
	data.seconds = 3*60+10
	data.timing = [0, 4, 25, 47, 80, 100, 123, 145]

def rehab(data, lyrics):
	i = lyrics.index('Rehab_AmyWinehouse.wav\n')
	rehablyrics=lyrics[i+1:]
	try:
		e = rehablyrics.index('\n')
		rehablyrics=rehablyrics[:e]
	except:
		print("assume it's the last element in the list")
	rehablyrics = ''.join(rehablyrics)
	rehablyrics = rehablyrics.split('@\n')
	data.lyrics = rehablyrics
	data.seconds = 3*60+32
	data.timing = [0,0,13,26,52,78,92,132,146,173,183,198]

def whoKnew(data, lyrics):
	i = lyrics.index('WhoKnew_P!nk.wav\n')
	whoKnewlyrics=lyrics[i+1:]
	try:
		e = whoKnewlyrics.index('\n')
		whoKnewlyrics=whoKnewlyrics[:e]
	except:
		print("assume it's the last element in the list")
	whoKnewlyrics = ''.join(whoKnewlyrics)
	whoKnewlyrics = whoKnewlyrics.split('@\n')
	data.lyrics = whoKnewlyrics
	data.seconds = 3*60+42
	data.timing = [0,6,33,65,91,119,142,158,164,171,184]

def flyMeToTheMoon(data, lyrics):
	i = lyrics.index('FlyMeToTheMoon_FrankSinatra.wav\n')
	flyMelyrics=lyrics[i+1:]
	try:
		e = flyMelyrics.index('\n')
		flyMelyrics=flyMelyrics[:e]
	except:
		print("assume it's the last element in the list")
	flyMelyrics = ''.join(flyMelyrics)
	flyMelyrics = flyMelyrics.split('@\n')
	data.lyrics = flyMelyrics
	data.seconds = 2*60+33
	data.timing = [0,7,40,70,105]

def Lyrics(data):
	with open('lyrics.txt', 'r') as myfile:
		lyrics = myfile.readlines()
	if (data.songFilename == GRAVITY_WAV):
		gravity(data, lyrics)
	elif (data.songFilename == GOLDDIGGER_WAV):
		goldDigger(data, lyrics)
	elif (data.songFilename == SUNDAYMORNING_WAV):
		sundayMorning(data, lyrics)
	elif (data.songFilename == GRENADE_WAV):
		grenade(data, lyrics)
	elif (data.songFilename == IMMORTALS_WAV):
		immortals(data, lyrics)
	elif (data.songFilename == REHAB_WAV):
		rehab(data, lyrics)
	elif (data.songFilename == WHOKNEW_WAV):
		whoKnew(data, lyrics)
	elif (data.songFilename == FLYMETOTHEMOON_WAV):
		flyMeToTheMoon(data, lyrics)
	else:
		print("Error in finding lyrics")

def getPitch(filename):
	from aubio import source, pitch
	downsample = 1
	samplerate = RATE//downsample
	win_s = 4096 // downsample # fft size
	hop_s = 512  // downsample # hop size
	s = source(filename, samplerate, hop_s)
	samplerate = s.samplerate
	tolerance = 0.8
	pitch_o = pitch("yin", win_s, hop_s, samplerate)
	pitch_o.set_unit("midi")
	pitch_o.set_tolerance(tolerance)
	pitches, confidences = [], []
	# total number of frames read
	total_frames = 0
	while True:
		samples, read = s()
		pitch = pitch_o(samples)[0]
		pitch = round(pitch, 3)
		confidence = pitch_o.get_confidence()
		if confidence < 0.40: pitch = 0
		pitches += [pitch]
		confidences += [confidence]
		total_frames += read
		if read < hop_s: break
	concat = 4
	pitches=pitches[concat:]
	confidences=confidences[concat:]
	return pitches

def convertPitchesToNotes(pitches):	
	pitchDict = makePitchMap()
	notes = []
	for pitch in pitches:
		if int(round(pitch)) in pitchDict.values():
			for key in pitchDict:
				if int(round(pitch))==pitchDict[key]:
					notes += [key]
		else: notes += [0]
	return notes

#used for both pitches and notes
def reduceWhiteNoise(userArray, realArray):
	#20 samples per second
	interval = 10
	#beginning case
	if (userArray[0]!=0 and userArray[1:5] != [0]*4): 
		userArray[0]=0
	#end case
	if (userArray[-1]!=0 and userArray[-5:-1] != [0]*4):
		userArray[-1]=0
	for i in range(len(userArray)-interval):
		if (userArray[i:i+interval//2-1] == [0]*(interval//2-1) and userArray[i+interval//2+1: i+interval]==[0]*(interval//2-1)):
			if userArray[i+interval//2-1:i+interval//2+1] != realArray[i+interval//2-1:i+interval//2+1]:
				userArray[i+interval//2-1] = 0
				userArray[i+interval//2] = 0
	return userArray

#input: array of user notes and real notes
def pitchAlgorithm(userPitches, realPitches):
	interval = round(len(realPitches)/(RECORD_SECONDS*4))
	userPitches = reduceWhiteNoise(userPitches, realPitches)
	#concatenate extra frames
	begin, end = 0, 0
	for i in range(len(userPitches) -1):
		if int(userPitches[i]) == 0 and int(userPitches[i+1]!=0):
			begin = i + 1
			break
	for j in range(len(userPitches) - 1, begin, -1):
		if int(userPitches[j-1]) != 0 and int(userPitches[j])==0:
			end = j
			break
	userPitches = userPitches[begin:end]
	realPitches = realPitches[begin:end]
	userNotes = convertPitchesToNotes(userPitches)
	realNotes = convertPitchesToNotes(realPitches)
	score = 0
	total = min(len(userNotes), len(realNotes))
	
	for i in range(0, len(realNotes)-interval, interval):
		#window for freq: 1/3 of a second
		for j in range(-1*interval//2, interval//2, 1):
			if realNotes[i+j] == 0 and userNotes[i+j]==0:
				score+=1
			elif realNotes[i+j] ==0 or userNotes[i+j]==0:
				score+=1
			elif ( compareNotes(realNotes[i], userNotes[i+j]) ):
				score += 1
	#for i in range(min(len(userNotes), len(realNotes) )):
		#if (not isinstance(userNotes[i], str) and isinstance(realNotes[i], str)):
		#	total -=1
		#if compareNotes(realNotes[i], userNotes[i]):
		#	score+=1
	return score/total*100

def compareNotes(A, B):
	if isinstance(A, float): A = int(A)
	if isinstance(B, float): B = int(B)
	if (A ==0 and B == 0):
		return True
	elif isinstance(A,str) and isinstance(B, str) and A[0:2] == B[0:2]:
		return True
	return False

#################################################PYAUDIO#################################################
#########################################################################################################

def play(outputFile):
	wf = wave.open(outputFile, 'rb')
	p = pyaudio.PyAudio()
	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
	                channels=wf.getnchannels(),
	                rate=wf.getframerate(),
	                output=True)
	data = wf.readframes(CHUNK)
	while len(data) > 0:
	    stream.write(data)
	    data = wf.readframes(CHUNK)
	stream.stop_stream()
	stream.close()
	p.terminate()

def record(inputFile):
	p = pyaudio.PyAudio()
	stream = p.open(format=FORMAT,
					channels = CHANNELS,
					rate = RATE,
					input = True,
					frames_per_buffer=CHUNK)
	print("* recording")
	frames = []
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)
	print('* done recording')

	stream.stop_stream()
	stream.close()
	p.terminate()

	wf = wave.open(inputFile, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()

####THREADING####
def thread_record(inputFile):
	print("thread_record...")
	return record(inputFile)

def thread_play(outputFile):
	print('thread_play...')
	return play(outputFile)

def makePitchMap():
	dictionary = {}
	for i in range(0, 7):
		key = 'C' + str(i + 1)
		dictionary[key] = 24 + i*12
		key = 'C#' + str(i + 1)
		dictionary[key] = 25 + i*12
		key = 'D' + str(i + 1)
		dictionary[key] = 26 + i*12
		key = 'D#' + str(i + 1)
		dictionary[key] = 27 + i*12
		key = 'E' + str(i + 1)
		dictionary[key] = 28 + i*12
		key = 'F' + str(i + 1)
		dictionary[key] = 29 + i*12
		key = 'F#' + str(i + 1)
		dictionary[key] = 30 + i*12
		key = 'G' + str(i + 1)
		dictionary[key] = 31 + i*12
		key = 'G#' + str(i + 1)
		dictionary[key] = 32 + i*12
		key = 'A' + str(i + 1)
		dictionary[key] = 33 + i*12
		key = 'A#' + str(i + 1)
		dictionary[key] = 34 + i*12
		key = 'B' + str(i + 1)
		dictionary[key] = 35 + i*12
	dictionary['C8'] = 108
	return dictionary

def testFunction():
    pitches =[24,27, 36.43, 70.05, 108.3]
    notes = convertPitchesToNotes(pitches)
    assert(notes, ['C1', 'A1', 'C2', 'A#4', 'C8'])
    assert(compareNotes('C#8', 'C#1'), True)


def main():
    testFunction()
	run(1000, 700)

if __name__ == '__main__':
    main()