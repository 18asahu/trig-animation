# -*- coding: utf-8 -*-
"""
Created on Wed May  6 16:40:42 2020

@author: NEHA
"""

import sys
import time
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel
from PyQt5.QtWidgets import QVBoxLayout, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import QTimer

class MyMainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.resize(900, 300)
        self.move(400,300)
        central_widget = MyCentralWidget(self)
        self.setCentralWidget(central_widget)
        self.setWindowTitle('Plot your chosen graph')
        self.statusBar().showMessage('Bartender')
        
        
class MyCentralWidget(QWidget):
    
    def __init__(self, main_window):
        
        super().__init__()
        self.main_window = main_window
        
        #Define what to do when each button pressed
        left_button = QPushButton('Plot sin graph', self)
        left_button.move(200,400)
        left_button.clicked.connect(self.on_left_button_clicked)
        
        right_button = QPushButton('Plot cos graph', self)
        right_button.move(700,400)
        right_button.clicked.connect(self.on_right_button_clicked)

        self.mpl_widget = MyMplWidget(self.main_window) #I got an error when I left the contents of the parantheses empty. In lessons, it was left empty. Not sure why I got an error
# STEPHEN COMMENT: the number of arguments required to create an instance of a class is given by the class'
# __init__ method, for MyMplWidget there are 3 arguments (you don't need to put "self" as an argument when
# you instantiate a class, so the required arguments are main_window, figsize and dpi. figsize and dpi have
# been given default values that they take on if you do not pass an argument for them, so to make the
# MyMplWidget you need to pass one argument, corresponding to main_window, which in this case is self.main_window.
# CHANGELOG: replaced MyMplWidget(self,main_window) with MyMplWidget(self.main_window)
        hbox = QHBoxLayout()#STEPHEN COMMENT: you forgot to import QHBoxLayout, added it back in at the top
        
        
        hbox.addWidget(left_button)
        hbox.addStretch(1)
        hbox.addWidget(right_button)
        
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.mpl_widget)
        vbox.addStretch(1)
        
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        #vbox.addLayout(vbox)
        
        
    def on_left_button_clicked(self):
        self.main_window.statusBar().showMessage('Left button pressed')
        self.mpl_widget.plot_sin(self.mpl_widget.k) #CHECK TO SEE IF PARAMETER DEFINITIONS NEEDED
        self.mpl_widget.update_sin(self.mpl_widget.k) 
         
# STEPHEN COMMENT: The MyMplWidget.mpl_widget.plot_sin() and cos methods require an argument of k, which
# change with your timer, which I guess would correspond to self.mpl_widget.k
# CHANGELOG: replaced empty sin and cos parentheses with self.mpl_widget.k
        
    def on_right_button_clicked(self):
        self.main_window.statusBar().showMessage('Right button pressed')
        self.mpl_widget.plot_cos(self.mpl_widget.k)#CHECK SAME AS ABOVE
        self.mpl_widget.update_cos(self.mpl_widget.k)
        
class MyMplWidget(FigureCanvas):
    
    def __init__(self, main_window, figsize = (2,1), dpi = 100):
        
        self.fig = plt.figure(figsize = figsize, dpi=dpi)
        #self.main_window = main_window         UNCOMMENT THIS IF IT DOESN;T WORK
        FigureCanvas.__init__(self,self.fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding,QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
       # self.MCW = MyCentralWidget()
        
        #Set parameters for how graph evolves with time 
        #(TBH, not entirely sure how this works. It works in the demo we were given so I stuck with it)
        self.frame_counter = 0
        self.k = 5
        self.dir = 1
        self.plot_sin(self.k)    #defined below
        self.plot_cos(self.k)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timed_action)
        self.dt = 0.010        
        self.timer.start(self.dt*1000)
        self.start_time = time.time()
        
    def timed_action(self):
        
        if self.frame_counter == 0:
            self.start_time = time.time()
            t_now = self.start_time
        else:
            t_now = self.start_time 
            
        self.k +=self.dir * self.dt*10 
        
        if self.k > 20:
            self.dir = -1
        elif self.k<5:
            self. dir = 1
        
        #I am suspicious about the 2 lines below because in the Canvas module, we only plotted an animation of sin
        #also, on canvas there were two separate examples - one only for the sin animation and one only for normal cos and sin graphs which were displayed depending on the button clicked
        self.update_sin(self.k)
        self.update_cos(self.k)
        
        
        '''if (self.frame_counter*self.dt*1000)%1000 == 0:
            mes = f'animation time = {self.frame_counter*self.dt:.1f}, actual time = {t_now-self.start_time:.1f}'
            self.main_window.statusBar().showMessage(mes)'''
            
        self.frame_counter += 1
        
    def plot_sin(self,k):
        self.fig.clf()
        self.ax1 = self.fig.add_subplot(1,1,1)
        self.x = np.linspace(-1,1,301)
        self.ax1.set_ylim([-1,1])
        self.line, = self.ax1.plot(self.x, np.sin(k*self.x), 'purple')
        self.draw()
        
        
    def plot_cos(self,k):
        self.fig.clf()
        self.ax2 = self.fig.add_subplot(1,1,1)
        self.x = np.linspace(-1,1,301)
        self.ax2.set_ylim([-1,1])
        self.line, = self.ax2.plot(self.x, np.cos(k*self.x), 'orange')
        self.draw()
        
    def update_sin(self,k):
        self.line.set_ydata(np.sin(k*self.x))
        self.ax1.draw_artist(self.ax1.patch) 
        self.ax1.draw_artist(self.line)
        self.fig.canvas.update()
        self.fig.canvas.flush_events()
        
    def update_cos(self,k):
        self.line.set_ydata(np.cos(k*self.x))
        self.ax2.draw_artist(self.ax2.patch) 
        self.ax2.draw_artist(self.line)
        self.fig.canvas.update()
        self.fig.canvas.flush_events()
        
'''SIDENOTE:    The error I'm getting directs me to a new file which is in the matplotlib folder in my laptop '''

app = None

def main():
    global app
    app = QApplication(sys.argv)
    w = MyMainWindow()
    w.show()
    app.exec()

'''

The __main__ file is whatever file you are running your code from, so in this case the code contained in the if statement will only run
if you run this file directly, and it wouldn't run if you included this file in a different project.
Putting the statements inside a function doesn't seem necessary, but it's necessary due to the "global app"
declaration, which cares whether app has already been defined.
'''
    
if __name__ == '__main__':
    main()
        
        
