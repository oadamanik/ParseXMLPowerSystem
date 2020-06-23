from tkinter import *
import os
from tkinter import filedialog
import tkinter.scrolledtext as tkst


class MainPage:

    def __init__(self, master, grid_elements, topology, pandapower):
        self.master = master
        self.grid_elements = grid_elements
        self.topology = topology
        self.pandapower = pandapower

        self.canvas = Canvas(self.master, height=500, width=500)
        self.canvas.pack()

        self.frame = Frame(self.master)
        self.frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.7)

        self.about_frame = Frame(self.master)
        self.about_frame.place(relx=0.0, rely=0.75, relwidth=1, relheight=0.25)

        code_about = "KTH Royal Institute of Technology\n" \
                "EH2745 Computer Applications in Power Systems\n" \
                  "Assignment 1\n" \
                  "Created by oadamanik\n" \
                  "Version 1.0\n"

        self.code_about = Label(self.about_frame, text=code_about,
                                font=("Arial", "10"), justify="center")
        self.code_about.place(relheight=1, relwidth=1, relx=0.0, rely=0.0)

        self.exit_button = Button(self.frame, text='EXIT',
                                font=("Arial", "10"), command=self.canvas.quit)
        self.exit_button.place(relheight=0.05, relwidth=1, relx=0.0, rely=0.95)

        self.filename_eq = ''
        self.filename_ssh = ''

        # Selecting the equipment file
        self.openfile_eq_button = Button(self.frame, text="Select equipment file",
                                    command=self.add_file_eq, font=("Arial", "10"))
        self.openfile_eq_button.place(relheight=0.05, relwidth=0.4, relx=0.0, rely=0.0)
        self.eq_filename_label = Label(self.frame, text='Selected equipment file (*.xml)',
                                  font=("Arial", "10", "italic"), relief="sunken")
        self.eq_filename_label.place(relheight=0.05, relwidth=0.6, relx=0.4, rely=0.0)

        # Selecting the SSH file
        self.openfile_ssh_button = Button(self.frame, text="Select ssh file",
                                     command=self.add_file_ssh, font=("Arial", "10"))
        self.openfile_ssh_button.place(relheight=0.05, relwidth=0.4, relx=0.0, rely=0.05)
        self.ssh_filename_label = Label(self.frame, text='Selected SSH file (*.xml)',
                                   font=("Arial", "10", "italic"), relief="sunken")
        self.ssh_filename_label.place(relheight=0.05, relwidth=0.6, relx=0.4, rely=0.05)

        # Parsing the selected files
        self.parse_button = Button(self.frame, text="Parse XML files",
                                   command=self.parse_xml)
        self.parse_button.place(relheight=0.1, relwidth=1, relx=0.0, rely=0.10)

        # Create internal datastructures
        self.create_datastructures_button = Button(self.frame, text="Create internal datastructures",
                                   command=self.create_elements)
        self.create_datastructures_button.place(relheight=0.1, relwidth=0.75, relx=0.0, rely=0.30)
        self.create_elements_label = Label(self.frame, text=None, font=("Arial", "10", 'italic'),
                                           fg='white', relief='sunken')
        self.create_elements_label.place(relheight=0.1, relwidth=0.25, relx=0.75, rely=0.30)

        # Generate topology
        self.generate_topology_button = Button(self.frame, text="Generate topology",
                                                   command=self.generate_topology)
        self.generate_topology_button.place(relheight=0.1, relwidth=0.75, relx=0.0, rely=0.5)
        self.generate_topology_label = Label(self.frame, text=None, font=("Arial", "10", 'italic'),
                                             fg='white', relief='sunken')
        self.generate_topology_label.place(relheight=0.1, relwidth=0.25, relx=0.75, rely=0.5)

        # Build the pandapower network
        self.build_pandapower_button = Button(self.frame, text="Build network using pandapower",
                                               command=self.build_pandapower_network)
        self.build_pandapower_button.place(relheight=0.1, relwidth=0.75, relx=0.0, rely=0.6)
        self.build_pandapower_label = Label(self.frame, text=None, font=("Arial", "10", 'italic'),
                                            fg='white', relief='sunken')
        self.build_pandapower_label.place(relheight=0.1, relwidth=0.25, relx=0.75, rely=0.6)

    def add_file_eq(self):
        self.filename_eq = os.path.split(filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=((
            "XML Files", "*.xml"), ("All files", "*.*"))))[1]
        self.eq_filename_label = Label(self.frame, text=self.filename_eq, font=("Arial", "10"), relief="sunken")
        self.eq_filename_label.place(relheight=0.05, relwidth=0.6, relx=0.4, rely=0.0)

    def add_file_ssh(self):
        self.filename_ssh = os.path.split(filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=((
            "XML Files", "*.xml"), ("All files", "*.*"))))[1]
        self.ssh_filename_label = Label(self.frame, text=self.filename_ssh, font=("Arial", "10"), relief="sunken")
        self.ssh_filename_label.place(relheight=0.05, relwidth=0.6, relx=0.4, rely=0.05)

    def parse_xml(self):
        self.grid_elements.parse_xml(self.filename_eq, self.filename_ssh)
        self.parse_info = Label(self.frame, text='Successfully parse the files!', font=("Arial", "9", 'italic'),
                                borderwidth=2)
        self.parse_info.place(relheight=0.05, relwidth=1, relx=0.0, rely=0.20)

    def create_elements(self):
        self.grid_elements.create_elements()
        self.create_elements_label = Label(self.frame, text='Success', font=("Arial", "10", 'italic'),
                                              bg='green', fg='white', relief='sunken')
        self.create_elements_label.place(relheight=0.1, relwidth=0.25, relx=0.75, rely=0.30)
        self.internal_data_window_button = Button(self.frame, text='Component details and configuration',
                                           command=self.open_internal_data_window)
        self.internal_data_window_button.place(relheight=0.05, relwidth=1, relx=0.0, rely=0.4)

    def generate_topology(self):
        if any(self.disconnected_elements):
            for de in self.disconnected_elements:
                for ce in self.grid_elements.conducting_equipment_list:
                    if de == ce.name:
                        for i in range(len(self.grid_elements.breaker_list)):
                            if ce.id_ == self.grid_elements.breaker_list[i].element_id:
                                self.grid_elements.breaker_list[i].pos = True

        self.topology.generate_topology(self.grid_elements.conducting_equipment_id_list,
                                        self.grid_elements.terminal_id_list,
                                        self.grid_elements.connectivity_node_id_list,
                                        self.grid_elements.synchronous_machine_id_list,
                                        self.grid_elements.terminal_list,
                                        self.grid_elements.breaker_list,
                                        self.grid_elements.busbar_section_list,
                                        self.grid_elements.ac_line_segment_list,
                                        self.grid_elements.power_transformer_list,
                                        self.grid_elements.synchronous_machine_list,
                                        self.grid_elements.energy_consumer_list,
                                        self.grid_elements.shunt_compensator_list)
        self.generate_topology_label = Label(self.frame, text='Success', font=("Arial", "10", 'italic'),
                                              bg='green', fg='white', relief='sunken')
        self.generate_topology_label.place(relheight=0.1, relwidth=0.25, relx=0.75, rely=0.5)

    def build_pandapower_network(self):
        self.pandapower.build_pandapower(self.topology.ac_line_segment_list_topology,
                                         self.topology.busbar_section_list_topology,
                                         self.topology.power_transformer_list_topology,
                                         self.topology.synchronous_machine_list_topology,
                                         self.topology.shunt_compensator_list_topology,
                                         self.topology.energy_consumer_list_topology,
                                         self.topology.breaker_list_topology)
        self.pandapower_network_label = Label(self.frame, text='Success', font=("Arial", "10", 'italic'),
                                              bg='green', fg='white', relief='sunken')
        self.pandapower_network_label.place(relheight=0.1, relwidth=0.25, relx=0.75, rely=0.6)
        # Print pandapower network at the console
        self.print_network_button = Button(self.frame, text='Print the pandapower network in the console',
                                             command=self.pandapower.print_network)
        self.print_network_button.place(relheight=0.05, relwidth=1, relx=0.0, rely=0.7)
        self.plot_network_button = Button(self.frame, text='Plot network',
                                             command=self.plot_pandapower_network)
        self.plot_network_button.place(relheight=0.05, relwidth=0.4, relx=0.0, rely=0.8)
        self.plot_network_label = Label(self.frame, relief='sunken')
        self.plot_network_label.place(relheight=0.05, relwidth=0.6, relx=0.4, rely=0.8)

    def plot_pandapower_network(self):
        filename = 'my_plot.html'
        self.pandapower.plot_network(filename)
        self.plot_network_label = Label(self.frame, text=filename + ' is created',
                                              font=("Arial", "10"), relief='sunken')
        self.plot_network_label.place(relheight=0.05, relwidth=0.6, relx=0.4, rely=0.8)

    def open_internal_data_window(self):
        self.indata_window = Toplevel(self.master, height=600, width=750)

        self.indata_frame = Frame(self.indata_window)
        self.indata_frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

        self.details_label = Label(self.indata_frame, text="Component details", font=("Arial", "10"),
                                   borderwidth=1, relief="solid")
        self.details_label.place(relheight=0.1, relwidth=1, relx=0.0, rely=0.0)

        self.busbar_button = Button(self.indata_frame, text="Busbar",
                                     command=self.show_details_busbar, font=("Arial", "10"))
        self.busbar_button.place(relheight=0.05, relwidth=0.4, relx=0.0, rely=0.1)

        self.sm_button = Button(self.indata_frame, text="Synchronous machine",
                                    command=self.show_details_sm, font=("Arial", "10"))
        self.sm_button.place(relheight=0.05, relwidth=0.4, relx=0.0, rely=0.15)

        self.trafo_button = Button(self.indata_frame, text="Transformer",
                                     command=self.show_details_trafo, font=("Arial", "10"))
        self.trafo_button.place(relheight=0.05, relwidth=0.4, relx=0.0, rely=0.2)

        self.ac_line_button = Button(self.indata_frame, text="AC Line",
                                     command=self.show_details_ac_line, font=("Arial", "10"))
        self.ac_line_button.place(relheight=0.05, relwidth=0.4, relx=0.0, rely=0.25)

        self.ec_button = Button(self.indata_frame, text="Load",
                                command=self.show_details_ec, font=("Arial", "10"))
        self.ec_button.place(relheight=0.05, relwidth=0.4, relx=0.0, rely=0.3)

        self.sh_button = Button(self.indata_frame, text="Shunt compensator",
                                command=self.show_details_sh, font=("Arial", "10"))
        self.sh_button.place(relheight=0.05, relwidth=0.4, relx=0.0, rely=0.35)

        self.cb_button = Button(self.indata_frame, text="CB",
                                command=self.show_details_breaker, font=("Arial", "10"))
        self.cb_button.place(relheight=0.05, relwidth=0.4, relx=0.0, rely=0.4)

        self.component_scrollbar = tkst.ScrolledText(self.indata_frame,
                                                           wrap=WORD)
        self.component_scrollbar.place(relheight=0.35, relwidth=0.6, relx=0.4, rely=0.1)

        self.config_label = Label(self.indata_frame, text="Configuration", font=("Arial", "10"),
                                  borderwidth=1, relief="solid")
        self.config_label.place(relheight=0.1, relwidth=1, relx=0.0, rely=0.5)

        self.config_component_label = Label(self.indata_frame, text="Connect",
                                            font=("Arial", "10"))
        self.config_component_label.place(relheight=0.05, relwidth=0.4, relx=0.0, rely=0.6)

        self.config_disconnect_label = Label(self.indata_frame, text="Disconnect",
                                             font=("Arial", "10"))
        self.config_disconnect_label.place(relheight=0.05, relwidth=0.4, relx=0.6, rely=0.6)

        self.config_listbox = Listbox(self.indata_frame)
        for i in range(len(self.grid_elements.disconnectable_list)):
            self.config_listbox.insert(i, self.grid_elements.disconnectable_list[i].name)
        self.config_listbox.place(relheight=0.35, relwidth=0.4, relx=0.0, rely=0.65)

        self.config_selected_listbox = Listbox(self.indata_frame)
        self.config_selected_listbox.place(relheight=0.35, relwidth=0.4, relx=0.6, rely=0.65)

        self.config_add_button = Button(self.indata_frame, text='>>>>>',
                                               command=self.add_selected_listbox)
        self.config_add_button.place(relheight=0.05, relwidth=0.2, relx=0.4, rely=0.7)

        self.config_delete_button = Button(self.indata_frame, text='<<<<<',
                                               command=self.delete_selected_listbox)
        self.config_delete_button.place(relheight=0.05, relwidth=0.2, relx=0.4, rely=0.9)

        self.config_confirm_button = Button(self.indata_frame, text='OK',
                                           command=self.config_confirm)
        self.config_confirm_button.place(relheight=0.15, relwidth=0.2, relx=0.4, rely=0.75)
        print(self.config_listbox.get(0, END))
        print(self.config_selected_listbox.get(0, END))

    def delete_selected_listbox(self):
        anchor = self.config_selected_listbox.get(ANCHOR)
        self.config_selected_listbox.delete(ANCHOR)
        self.config_listbox.insert(END, anchor)

    def config_confirm(self):
        self.disconnected_elements = list(self.config_selected_listbox.get(0, ANCHOR))
        print(self.disconnected_elements)
        self.indata_window.destroy()

    def add_selected_listbox(self):
        anchor = self.config_listbox.get(ANCHOR)
        self.config_listbox.delete(ANCHOR)
        self.config_selected_listbox.insert(END, anchor)

    def show_details_busbar(self):
        details = '\n'
        for bb in self.grid_elements.busbar_section_list:
            details = details + 'Name = ' + bb.name + '\n'
            details = details + 'Nominal voltage (kV) = ' + str(bb.u_nom_kv) + '\n\n'
        self.component_scrollbar.delete("1.0", END)
        self.component_scrollbar.insert(INSERT, details)

    def show_details_sm(self):
        details = '\n'
        for sm in self.grid_elements.synchronous_machine_list:
            details = details + 'Name = ' + sm.name + '\n'
            details = details + 'S, rated (MVA) = ' + str(sm.s_rated_kva) + '\n'
            details = details + 'P, rated (MW) = ' + str(sm.p_rated) + '\n'
            details = details + 'r0 (ohm) = ' + str(sm.r0) + '\n'
            details = details + 'x0 (ohm) = ' + str(sm.x0) + '\n\n'
        self.component_scrollbar.delete("1.0", END)
        self.component_scrollbar.insert(INSERT, details)

    def show_details_trafo(self):
        details = '\n'
        for tr in self.grid_elements.power_transformer_list:
            details = details + 'Name = ' + tr.name + '\n'
            details = details + 'S, nominal (MVA) = ' + str(tr.s_nom_mva) + '\n'
            details = details + 'HV-side (kV) = ' + str(tr.hv_nom_kv)+ '\n'
            details = details + 'LV-side (kV) = ' + str(tr.lv_nom_kv) + '\n'
            details = details + 'r (ohm) = ' + str(tr.r) + '\n'
            details = details + 'x (ohm) = ' + str(tr.x) + '\n\n'
        self.component_scrollbar.delete("1.0", END)
        self.component_scrollbar.insert(INSERT, details)

    def show_details_ac_line(self):
        details = '\n'
        for al in self.grid_elements.ac_line_segment_list:
            details = details + 'Name = ' + al.name + '\n'
            details = details + 'Length (km) = ' + str(al.length_km) + '\n'
            details = details + 'r (ohm) = ' + str(al.r_ohm) + '\n'
            details = details + 'x (ohm) = ' + str(al.x_ohm) + '\n\n'
        self.component_scrollbar.delete("1.0", END)
        self.component_scrollbar.insert(INSERT, details)

    def show_details_breaker(self):
        details = '\n'
        for br in self.grid_elements.breaker_list:
            details = details + 'Name = ' + br.name + '\n'
            if br.normal_open:
                details = details + 'Operation = Normally close\n'
            else:
                details = details + 'Operation = Normally open\n'
            if br.pos:
                details = details + 'Current position = Open\n'
            else:
                details = details + 'Current position = Close\n'
        self.component_scrollbar.delete("1.0", END)
        self.component_scrollbar.insert(INSERT, details)

    def show_details_ec(self):
        details = '\n'
        for ec in self.grid_elements.energy_consumer_list:
            details = details + 'Name = ' + ec.name + '\n'
            details = details + 'P (MW) = ' + str(ec.p) + '\n'
            details = details + 'Q (MVAr) = ' + str(ec.q) + '\n\n'
        self.component_scrollbar.delete("1.0", END)
        self.component_scrollbar.insert(INSERT, details)

    def show_details_sh(self):
        details = '\n'
        for sh in self.grid_elements.shunt_compensator_list:
            details = details + 'Name = ' + sh.name + '\n'
            details = details + 'U, nominal (kV) = ' + str(sh.u_nom_kv) + '\n'
            details = details + 'Q, rated (MVAr) = ' + str(sh.q_rated_mvar) + '\n\n'
        self.component_scrollbar.delete("1.0", END)
        self.component_scrollbar.insert(INSERT, details)

