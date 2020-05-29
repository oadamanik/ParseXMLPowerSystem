"""
Latest modified: 07 May 2020
for Assignment 1 of EH2745, KTH Royal Institute of Technology
Author: oadamanik (Oscar Aristo Damanik)
"""

from GUI import *
import tkinter as tk
from Elements import *
from Topology import *
from PandapowerNetwork import *

my_grid_elements = GridElements()
my_topology = Topology()
my_pandapower = PandapowerNetwork()

root = tk.Tk()

my_gui = MainPage(root, my_grid_elements, my_topology, my_pandapower)


root.mainloop()