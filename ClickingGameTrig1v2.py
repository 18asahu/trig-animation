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
from PyQt5.QtWidgets import QVBoxLayout, QSizePolicy
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
        left_button.clicked.connect(self.on_left_button_clicked)
        
        right_button = QPushButton('Plot cos graph', self)
        right_button.clicked.connect(self.on_right_button_clicked)

        self.mpl_widget = MyMplWidget(self,main_window) #I got an error when I left the contents of the parantheses empty. In lessons, it was left empty. Not sure why I got an error
        
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        
        hbox.addWidget(left_button)
        hbox.addWidget(right_button)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.mpl_widget)

        vbox.addLayout(hbox)
        vbox.addLayout(vbox)
        
        
    def on_left_button_clicked(self):
        self.main_window.statusBar().showMessage('Left button pressed')
        self.mpl_widget.plot_sin() #CHECK TO SEE IF PARAMETER DEFINITIONS NEEDED
        self.mpl_widget.update_sin() 
         
        
        
    def on_right_button_clicked(self):
        self.main_window.statusBar().showMessage('Right button pressed')
        self.mpl_widget.plot_cos()#CHECK SAME AS ABOVE
        self.mpl_widget.update_cos()
        
class MyMplWidget(FigureCanvas):
    
    def __init__(self, main_window, figsize = (4,3), dpi = 100):
        self.main_window = main_window
        self.fig = plt.figure(figsize = figsize, dpi=dpi)
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
        
        
        if (self.frame_counter*self.dt*1000)%1000 == 0:
            mes = f'animation time = {self.frame_counter*self.dt:.1f}, actual time = {t_now-self.start_time:.1f}'
            self.main_window.statusBar().showMessage(mes)
            
        self.frame_counter += 1
        
    def plot_sin(self,k):
        self.fig.clf()
        self.ax = self.fig.add_subplot(1,1,1)
        self.x = np.linspace(-1,1,301)
        self.ax.set_ylim([-1,1])
        self.line, = self.ax.plot(self.x, np.sin(k*self.x), 'purple')
        self.draw()
        
        
    def plot_cos(self,k):
        self.fig.clf()
        self.ax = self.fig.add_subplot(1,1,1)
        self.x = np.linspace(-1,1,301)
        self.ax.set_ylim([-1,1])
        self.line, = self.ax.plot(self.x, np.cos(k*self.x), 'orange')
        self.draw()
        
    def update_sin(self,k):
        self.line.set_ydata(np.sin(k*self.x))
        self.ax.draw_artist(self.ax.patch) 
        self.ax.draw_artist(self.line)
        self.fig.canvas.update()
        self.fig.canvas.flush_events()
        
    def update_cos(self,k):
        self.line.set_ydata(np.cos(k*self.x))
        self.ax.draw_artist(self.ax.patch) 
        self.ax.draw_artist(self.line)
        self.fig.canvas.update()
        self.fig.canvas.flush_events()
        
      
         
app = None

def main():
    global app
    app = QApplication(sys.argv)
    w = MyMainWindow()
    w.show()
    app.exec()
    
if __name__ == '__main__':
    main()            
            
            
        
        
