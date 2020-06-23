# ParseXMLPowerSystem
This program is created to parse two power system XML files, namely XML files for equipment and XML files for steady-state hypothesis. The parsing results are used to create and store elements using the classes defined in the Python program. Next, the topology of the network is determined using a depth first search based algorithm based on the connectivity of the elements. Finally, based on the topology, pandapower netwok is created.

# Files
This project contains five files:
* Main.py: the main file used to run the program
* GUI.py: graphical user interface (GUI), generates graphic user interface and all its widgets.
* Elements.py: contains classes of each element and generate the elements from the parsing results
* Topology.py: runs the traversal algorithm to determine the network topology based on the connectivity of the elements
* PandapowerNetwork.py: contains a function to create the pandapower network ased on the topology.
