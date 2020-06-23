# ParseXMLPowerSystem
This program is created to parse two power system XML files, namely XML files for equipment and XML files for steady-state hypothesis. The parsing results are used to create and store elements using the classes defined in the Python program. Next, the topology of the network is determined using a depth first search based algorithm based on the connectivity of the elements. 

# Files
This project contains five files:
* Main.py: the main file used to run the program
* GUI.py: graphical user interface (GUI), generates graphic user interface and all its widgets.
* Elements.py: contains classes of each element and generate the elements from the parsing results
* timeseriessim.py: time series simulation, executes the time series simulation of the pandapower network and generates excel file for the simulation results (bus voltages and angles)
* testnetwork.py: contains a function to create the given pandapower network
