# GUI frame for the hpsTransformations_function.py

from Tkinter import *
import tkFileDialog, tkMessageBox
import sys, os
import pygame
from scipy.io.wavfile import read
import numpy as np
import hpsTransformations_function as hT
 
class HpsTransformations_frame:
  
	def __init__(self, parent):  
		 
		self.parent = parent        
		self.initUI()
		pygame.init()

	def initUI(self):

		choose_label = "inputFile:"
		Label(self.parent, text=choose_label).grid(row=0, column=0, sticky=W, padx=5, pady=(10,2))
 
		#TEXTBOX TO PRINT PATH OF THE SOUND FILE
		self.filelocation = Entry(self.parent)
		self.filelocation.focus_set()
		self.filelocation["width"] = 25
		self.filelocation.grid(row=0,column=0, sticky=W, padx=(70, 5), pady=(10,2))
		self.filelocation.delete(0, END)
		self.filelocation.insert(0, '../../sounds/sax-phrase.wav')

		#BUTTON TO BROWSE SOUND FILE
		self.open_file = Button(self.parent, text="...", command=self.browse_file) #see: def browse_file(self)
		self.open_file.grid(row=0, column=0, sticky=W, padx=(280, 6), pady=(10,2)) #put it beside the filelocation textbox
 
		#BUTTON TO PREVIEW SOUND FILE
		self.preview = Button(self.parent, text=">", command=self.preview_sound, bg="gray30", fg="white")
		self.preview.grid(row=0, column=0, sticky=W, padx=(325,6), pady=(10,2))

		## HPS TRANSFORMATIONS ANALYSIS

		#ANALYSIS WINDOW TYPE
		wtype_label = "window:"
		Label(self.parent, text=wtype_label).grid(row=1, column=0, sticky=W, padx=5, pady=(10,2))
		self.w_type = StringVar()
		self.w_type.set("blackman") # initial value
		window_option = OptionMenu(self.parent, self.w_type, "rectangular", "hanning", "hamming", "blackman", "blackmanharris")
		window_option.grid(row=1, column=0, sticky=W, padx=(65,5), pady=(10,2))

		#WINDOW SIZE
		M_label = "M:"
		Label(self.parent, text=M_label).grid(row=1, column=0, sticky=W, padx=(180, 5), pady=(10,2))
		self.M = Entry(self.parent, justify=CENTER)
		self.M["width"] = 5
		self.M.grid(row=1,column=0, sticky=W, padx=(200,5), pady=(10,2))
		self.M.delete(0, END)
		self.M.insert(0, "601")

		#FFT SIZE
		N_label = "N:"
		Label(self.parent, text=N_label).grid(row=1, column=0, sticky=W, padx=(255, 5), pady=(10,2))
		self.N = Entry(self.parent, justify=CENTER)
		self.N["width"] = 5
		self.N.grid(row=1,column=0, sticky=W, padx=(275,5), pady=(10,2))
		self.N.delete(0, END)
		self.N.insert(0, "1024")

		#THRESHOLD MAGNITUDE
		t_label = "t:"
		Label(self.parent, text=t_label).grid(row=1, column=0, sticky=W, padx=(330,5), pady=(10,2))
		self.t = Entry(self.parent, justify=CENTER)
		self.t["width"] = 5
		self.t.grid(row=1, column=0, sticky=W, padx=(348,5), pady=(10,2))
		self.t.delete(0, END)
		self.t.insert(0, "-100")

		#MIN DURATION SINUSOIDAL TRACKS
		minSineDur_label = "minSineDur:"
		Label(self.parent, text=minSineDur_label).grid(row=2, column=0, sticky=W, padx=(5, 5), pady=(10,2))
		self.minSineDur = Entry(self.parent, justify=CENTER)
		self.minSineDur["width"] = 5
		self.minSineDur.grid(row=2, column=0, sticky=W, padx=(87,5), pady=(10,2))
		self.minSineDur.delete(0, END)
		self.minSineDur.insert(0, "0.1")

		#MAX NUMBER OF HARMONICS
		nH_label = "nH:"
		Label(self.parent, text=nH_label).grid(row=2, column=0, sticky=W, padx=(145,5), pady=(10,2))
		self.nH = Entry(self.parent, justify=CENTER)
		self.nH["width"] = 5
		self.nH.grid(row=2, column=0, sticky=W, padx=(172,5), pady=(10,2))
		self.nH.delete(0, END)
		self.nH.insert(0, "100")

		#MIN FUNDAMENTAL FREQUENCY
		minf0_label = "minf0:"
		Label(self.parent, text=minf0_label).grid(row=2, column=0, sticky=W, padx=(227,5), pady=(10,2))
		self.minf0 = Entry(self.parent, justify=CENTER)
		self.minf0["width"] = 5
		self.minf0.grid(row=2, column=0, sticky=W, padx=(275,5), pady=(10,2))
		self.minf0.delete(0, END)
		self.minf0.insert(0, "350")

		#MAX FUNDAMENTAL FREQUENCY
		maxf0_label = "maxf0:"
		Label(self.parent, text=maxf0_label).grid(row=2, column=0, sticky=W, padx=(330,5), pady=(10,2))
		self.maxf0 = Entry(self.parent, justify=CENTER)
		self.maxf0["width"] = 5
		self.maxf0.grid(row=2, column=0, sticky=W, padx=(380,5), pady=(10,2))
		self.maxf0.delete(0, END)
		self.maxf0.insert(0, "700")

		#MAX ERROR ACCEPTED
		f0et_label = "f0et:"
		Label(self.parent, text=f0et_label).grid(row=3, column=0, sticky=W, padx=5, pady=(10,2))
		self.f0et = Entry(self.parent, justify=CENTER)
		self.f0et["width"] = 5
		self.f0et.grid(row=3, column=0, sticky=W, padx=(45,5), pady=(10,2))
		self.f0et.delete(0, END)
		self.f0et.insert(0, "5")

		#ALLOWED DEVIATION OF HARMONIC TRACKS
		harmDevSlope_label = "harmDevSlope:"
		Label(self.parent, text=harmDevSlope_label).grid(row=3, column=0, sticky=W, padx=(110,5), pady=(10,2))
		self.harmDevSlope = Entry(self.parent, justify=CENTER)
		self.harmDevSlope["width"] = 5
		self.harmDevSlope.grid(row=3, column=0, sticky=W, padx=(210,5), pady=(10,2))
		self.harmDevSlope.delete(0, END)
		self.harmDevSlope.insert(0, "0.01")

		#DECIMATION FACTOR
		stocf_label = "stocf:"
		Label(self.parent, text=stocf_label).grid(row=3, column=0, sticky=W, padx=(275,5), pady=(10,2))
		self.stocf = Entry(self.parent, justify=CENTER)
		self.stocf["width"] = 5
		self.stocf.grid(row=3, column=0, sticky=W, padx=(315,5), pady=(10,2))
		self.stocf.delete(0, END)
		self.stocf.insert(0, "0.1")

		#BUTTON TO DO THE ANALYSIS OF THE SOUND
		self.compute = Button(self.parent, text="Analysis/Synthesis", command=self.analysis, bg="dark red", fg="white")
		self.compute.grid(row=4, column=0, padx=5, pady=(10,5), sticky=W)
		
		#BUTTON TO PLAY ANALYSIS/SYNTHESIS OUTPUT
		self.output = Button(self.parent, text=">", command=lambda:self.play_out_sound('hpsModel'), bg="gray30", fg="white")
		self.output.grid(row=4, column=0, padx=(145,5), pady=(10,5), sticky=W)

		###
		#SEPARATION LINE
		Frame(self.parent,height=1,width=50,bg="black").grid(row=5, pady=5, sticky=W+E)
		###

		#FREQUENCY SCALING FACTORS
		freqScaling_label = "Frequency scaling factors, in time-value pairs:"
		Label(self.parent, text=freqScaling_label).grid(row=6, column=0, sticky=W, padx=5, pady=(5,2))
		self.freqScaling = Entry(self.parent, justify=CENTER)
		self.freqScaling.grid(row=7, column=0, sticky=W+E, padx=5, pady=(0,2))
		self.freqScaling.delete(0, END)
		self.freqScaling.insert(0, "[0, 1.2, 2.01, 1.2, 2.679, .7, 3.146, .7]")

		#FREQUENCY STRETCHING FACTORSharmonicModelTransformation
		freqStretching_label = "Frequency stretching factors, in time-value pairs:"
		Label(self.parent, text=freqStretching_label).grid(row=8, column=0, sticky=W, padx=5, pady=(5,2))
		self.freqStretching = Entry(self.parent, justify=CENTER)
		self.freqStretching.grid(row=9, column=0, sticky=W+E, padx=5, pady=(0,2))
		self.freqStretching.delete(0, END)
		self.freqStretching.insert(0, "[0, 1, 2.01, 1, 2.679, 1.5, 3.146, 1.5]")

		#TIMBRE PRESERVATION
		timbrePreservation_label = "Timbre preservation (1 preserves original timbre, 0 it does not):"
		Label(self.parent, text=timbrePreservation_label).grid(row=10, column=0, sticky=W, padx=5, pady=(5,2))
		self.timbrePreservation = Entry(self.parent, justify=CENTER)
		self.timbrePreservation.grid(row=10, column=0, sticky=W+E, padx=(395,5), pady=(5,2))
		self.timbrePreservation.delete(0, END)
		self.timbrePreservation.insert(0, "1")

		#TIME SCALING FACTORS
		timeScaling_label = "Time scaling factors, in time-value pairs:"
		Label(self.parent, text=timeScaling_label).grid(row=11, column=0, sticky=W, padx=5, pady=(5,2))
		self.timeScaling = Entry(self.parent, justify=CENTER)
		self.timeScaling.grid(row=12, column=0, sticky=W+E, padx=5, pady=(0,2))
		self.timeScaling.delete(0, END)
		self.timeScaling.insert(0, "[0, 0, 2.138, 2.138-1.0, 3.146, 3.146]")

		#BUTTON TO DO THE SYNTHESIS
		self.compute = Button(self.parent, text="Apply Transformation", command=self.transformation_synthesis, bg="dark green", fg="white")
		self.compute.grid(row=13, column=0, padx=5, pady=(10,15), sticky=W)

		#BUTTON TO PLAY TRANSFORMATION SYNTHESIS OUTPUT
		self.transf_output = Button(self.parent, text=">", command=lambda:self.play_out_sound('hpsModelTransformation'), bg="gray30", fg="white")
		self.transf_output.grid(row=13, column=0, padx=(165,5), pady=(10,15), sticky=W)

		# define options for opening file
		self.file_opt = options = {}
		options['defaultextension'] = '.wav'
		options['filetypes'] = [('All files', '.*'), ('Wav files', '.wav')]
		options['initialdir'] = '../../sounds/'
		options['title'] = 'Open a mono audio file .wav with sample frequency 44100 Hz'

	def preview_sound(self):
		self.dummy = 2
		filename = self.filelocation.get()

		if filename[-4:] == '.wav':
			(fs, x) = read(filename)
		else:
			tkMessageBox.showerror("Wav file", "The audio file must be a .wav")
			return

		if len(x.shape) > 1 :
			tkMessageBox.showerror("Stereo file", "Audio file must be Mono not Stereo")
		elif fs != 44100:
			tkMessageBox.showerror("Sample Frequency", "Sample frequency must be 44100 Hz")
		else:
			sound = pygame.mixer.Sound(filename)
			sound.play()
 
	def browse_file(self):
		
		self.filename = tkFileDialog.askopenfilename(**self.file_opt)
 
		#set the text of the self.filelocation
		self.filelocation.delete(0, END)
		self.filelocation.insert(0,self.filename)

	def analysis(self):
		
		try:
			inputFile = self.filelocation.get()
			window =  self.w_type.get()
			M = int(self.M.get())
			N = int(self.N.get())
			t = int(self.t.get())
			minSineDur = float(self.minSineDur.get())
			nH = int(self.nH.get())
			minf0 = int(self.minf0.get())
			maxf0 = int(self.maxf0.get())
			f0et = int(self.f0et.get())
			harmDevSlope = float(self.harmDevSlope.get())

			self.inputFile, self.fs, self.hfreq, self.hmag = hT.analysis(inputFile, window, M, N, t, minSineDur, nH, minf0, maxf0, f0et, harmDevSlope)

		except ValueError:
			tkMessageBox.showerror("Input values error", "Some parameters are incorrect")

	def transformation_synthesis(self):

		try:
			inputFile = self.inputFile
			fs =  self.fs
			hfreq = self.hfreq
			hmag = self.hmag
			freqScaling = np.array(eval(self.freqScaling.get()))
			freqStretching = np.array(eval(self.freqStretching.get()))
			timbrePreservation = int(self.timbrePreservation.get())
			timeScaling = np.array(eval(self.timeScaling.get()))

			hT.transformation_synthesis(inputFile, fs, hfreq, hmag, freqScaling, freqStretching, timbrePreservation, timeScaling)

		except ValueError:
			tkMessageBox.showerror("Input values error", "Some parameters are incorrect")

		except AttributeError:
			tkMessageBox.showerror("Analysis not computed", "First you must analyse the sound!")

	def play_out_sound(self, extension):

		filename = 'output_sounds/' + os.path.basename(self.filelocation.get())[:-4] + '_' + extension + '.wav'
		if os.path.isfile(filename):
			sound = pygame.mixer.Sound(filename)
			sound.play()
		else:
			tkMessageBox.showerror("Output audio file not found", "The output audio file has not been computed yet")
