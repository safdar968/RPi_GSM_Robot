import tkinter
from tkinter import filedialog

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.initTracking = None
        self.window.title(window_title)
        self.video_source = ''
        self.input_options = [
            ('CSRT',1),
            ('MIL', 2)]

        self.tracker_val = tkinter.IntVar()
        self.tracker_val.set(0)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, relief="sunken", width = 640, height = 480)
        self.canvas.bind("<Button-1>", self.set_tracker_type)
        rtsplbl = tkinter.Label(window, text="RTSP Link:")
        resultlbl = tkinter.Label(window, text="Result:")
        threshlbl = tkinter.Label(window, text="Detector Threshold:")
        self.thresh = tkinter.Entry(window)
        self.link = tkinter.Entry(window)
        self.result = tkinter.Text(window, state='disabled', width=10, height=1)
        self.btn_set_tracker=tkinter.Button(window, text="Set Tracker", width=10, command=self.set_tracker_type)
        self.btn_load_file = tkinter.Button(window, text="Load Video", width=10, command=self.load_file)
        self.btn_track = tkinter.Button(window, text="Track", width=10, command=self.track)
        # Button that lets the user take a select the object to track
        for val, tracker_type in enumerate(self.input_options):

            # Radio Button that lets the user select tracker type
            radio_tracker_type = tkinter.Radiobutton(window, 
                                        text=tracker_type[0],
                                        padx = 20, 
                                        variable=self.tracker_val, 
                                        value=val
                                        )
            radio_tracker_type.grid(column=5, row=val, sticky='NW')


        self.canvas.grid(column=0, row=0, columnspan=5, rowspan=20)
        self.link.grid(column=1, row=21, sticky='WE')
        rtsplbl.grid(column=0, row=21)
        self.result.grid(column=5, row=17, sticky='NWE')
        resultlbl.grid(column=5, row=16, sticky='SW')
        self.thresh.grid(column=5, row=12, sticky='NWE')
        threshlbl.grid(column=5, row=11, sticky='SW')
        self.btn_set_tracker.grid(column=5, row=19, sticky='WSE')
        self.btn_load_file.grid(column=5, row=18, sticky='WSE')
        

            
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 1
        self.update()

        self.window.mainloop()


    def set_tracker_type(self):
        pass

    def load_file(self):
        pass

    def track(self):
        pass

    def update(self):

        self.window.after(self.delay, self.update)


# Create a window and pass it to the Application object
App(tkinter.Tk(), "RPi_GSM_Robot")