from Tkinter import *
import tkFileDialog, tkMessageBox
import sys, os
import pygame
from scipy.io.wavfile import read

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../examples/'))
import sineModel_example
 
class SineModel_frame:
  
    def __init__(self, parent):  
         
        self.parent = parent        
        self.initUI()
        pygame.init()

    def initUI(self):

        choose_label = "Choose an input audio file .wav:"
        Label(self.parent, text=choose_label).grid(row=0, column=0, sticky=W, padx=5, pady=(10,2))
 
        #TEXTBOX TO PRINT PATH OF THE SOUND FILE
        self.filelocation = Entry(self.parent)
        self.filelocation.focus_set()
        self.filelocation["width"] = 25
        self.filelocation.grid(row=1,column=0, sticky=W, padx=10)
        self.filelocation.delete(0, END)
        self.filelocation.insert(0, '../sounds/bendir.wav')

        #BUTTON TO BROWSE SOUND FILE
        self.open_file = Button(self.parent, text="Browse...", command=self.browse_file) #see: def browse_file(self)
        self.open_file.grid(row=1, column=0, sticky=W, padx=(220, 6)) #put it beside the filelocation textbox
 
        #BUTTON TO PREVIEW SOUND FILE
        self.preview = Button(self.parent, text=">", command=self.preview_sound, bg="gray30", fg="white")
        self.preview.grid(row=1, column=0, sticky=W, padx=(306,6))

        ## SINE MODEL

        #ANALYSIS WINDOW TYPE
        wtype_label = "Analysis window type:"
        Label(self.parent, text=wtype_label).grid(row=2, column=0, sticky=W, padx=5, pady=(10,2))
        self.w_type = StringVar()
        self.w_type.set("hamming") # initial value
        window_option = OptionMenu(self.parent, self.w_type, "rectangular", "hanning", "hamming", "blackman", "blackmanharris")
        window_option.grid(row=2, column=0, sticky=W, padx=150, pady=(10,2))

        #WINDOW SIZE
        M_label = "Analysis window size 'M':"
        Label(self.parent, text=M_label).grid(row=4, column=0, sticky=W, padx=5, pady=(10,2))
        self.M = Entry(self.parent, justify=CENTER)
        self.M["width"] = 8
        self.M.grid(row=5,column=0, sticky=W, padx=10)
        self.M.delete(0, END)
        self.M.insert(0, "2001")

        #FFT SIZE
        N_label = "FFT size 'N' (power of two, bigger than 'M'):"
        Label(self.parent, text=N_label).grid(row=6, column=0, sticky=W, padx=5, pady=(10,2))
        self.N = Entry(self.parent, justify=CENTER)
        self.N["width"] = 8
        self.N.grid(row=7,column=0, sticky=W, padx=10)
        self.N.delete(0, END)
        self.N.insert(0, "2048")

        #THRESHOLD MAGNITUDE
        t_label = "Magnitude threshold of spectral peaks 't':"
        Label(self.parent, text=t_label).grid(row=8, column=0, sticky=W, padx=5, pady=(10,2))
        self.t = Entry(self.parent, justify=CENTER)
        self.t["width"] = 8
        self.t.grid(row=9, column=0, sticky=W, padx=10)
        self.t.delete(0, END)
        self.t.insert(0, "-80")

        #MIN DURATION SINUSOIDAL TRACKS
        minSineDur_label = "Minimum duration of sinusoidal tracks:"
        Label(self.parent, text=minSineDur_label).grid(row=10, column=0, sticky=W, padx=5, pady=(10,2))
        self.minSineDur = Entry(self.parent, justify=CENTER)
        self.minSineDur["width"] = 8
        self.minSineDur.grid(row=11, column=0, sticky=W, padx=10)
        self.minSineDur.delete(0, END)
        self.minSineDur.insert(0, "0.02")

        #MAX NUMBER PARALLEL SINUSOIDS
        maxnSines_label = "Maximum number of parallel sinusoids:"
        Label(self.parent, text=maxnSines_label).grid(row=12, column=0, sticky=W, padx=5, pady=(10,2))
        self.maxnSines = Entry(self.parent, justify=CENTER)
        self.maxnSines["width"] = 8
        self.maxnSines.grid(row=13, column=0, sticky=W, padx=10)
        self.maxnSines.delete(0, END)
        self.maxnSines.insert(0, "150")

        #FREQUENCY DEVIATION ALLOWED
        freqDevOffset_label = "Frequency deviation allowed in the sinusoids from frame to frame at frequency 0:"
        Label(self.parent, text=freqDevOffset_label).grid(row=14, column=0, sticky=W, padx=5, pady=(10,2))
        self.freqDevOffset = Entry(self.parent, justify=CENTER)
        self.freqDevOffset["width"] = 8
        self.freqDevOffset.grid(row=15, column=0, sticky=W, padx=10)
        self.freqDevOffset.delete(0, END)
        self.freqDevOffset.insert(0, "10")

        #SLOPE OF THE FREQ DEVIATION
        freqDevSlope_label = "Slope of the frequency deviation, higher frequencies have bigger deviation:"
        Label(self.parent, text=freqDevSlope_label).grid(row=16, column=0, sticky=W, padx=5, pady=(10,2))
        self.freqDevSlope = Entry(self.parent, justify=CENTER)
        self.freqDevSlope["width"] = 8
        self.freqDevSlope.grid(row=17, column=0, sticky=W, padx=10)
        self.freqDevSlope.delete(0, END)
        self.freqDevSlope.insert(0, "0.001")

        #BUTTON TO COMPUTE EVERYTHING
        self.compute = Button(self.parent, text="Compute", command=self.compute_model, bg="dark red", fg="white")
        self.compute.grid(row=18, column=0, padx=5, pady=(10,2), sticky=W)

        #BUTTON TO PLAY OUTPUT
        output_label = "Output:"
        Label(self.parent, text=output_label).grid(row=19, column=0, sticky=W, padx=5, pady=(10,15))
        self.output = Button(self.parent, text=">", command=self.play_out_sound, bg="gray30", fg="white")
        self.output.grid(row=19, column=0, padx=(60,5), pady=(10,15), sticky=W)

        # define options for opening file
        self.file_opt = options = {}
        options['defaultextension'] = '.wav'
        options['filetypes'] = [('All files', '.*'), ('Wav files', '.wav')]
        options['initialdir'] = '../sounds/'
        options['title'] = 'Open a mono audio file .wav with sample frequency 44100 Hz'

    def preview_sound(self):
        
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

    def compute_model(self):
        
        try:
            M = int(self.M.get())
            N = int(self.N.get())
            t = int(self.t.get())
            minSineDur = float(self.minSineDur.get())
            maxnSines = int(self.maxnSines.get())
            freqDevOffset = int(self.freqDevOffset.get())
            freqDevSlope = float(self.freqDevSlope.get())
            
            sineModel_example.main(self.filelocation.get(), self.w_type.get(), M, N, t, minSineDur, maxnSines, freqDevOffset, freqDevSlope)

        except ValueError:
            tkMessageBox.showerror("Input values error", "Some parameters are incorrect")

    def play_out_sound(self):

        filename = 'output_sounds/' + os.path.basename(self.filelocation.get())[:-4] + '_sineModel.wav'
        if os.path.isfile(filename):
            sound = pygame.mixer.Sound(filename)
            sound.play()
        else:
            tkMessageBox.showerror("Output audio file not found", "The output audio file has not been computed yet")