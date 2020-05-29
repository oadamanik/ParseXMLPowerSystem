class Topology:

    def __init__(self):
        self.node_id_list = []
        self.adjacency_dict = {}
        self.ac_line_segment_list_topology = []
        self.busbar_section_list_topology = []
        self.breaker_list_topology = []
        self.energy_consumer_list_topology = []
        self.synchronous_machine_list_topology = []
        self.power_transformer_list_topology = []
        self.shunt_compensator_list_topology = []

    def generate_topology(self, conducting_equipment_id_list, terminal_id_list, connectivity_node_id_list,
                          synchronous_machine_id_list, terminal_list, breaker_list, busbar_section_list,
                          ac_line_segment_list, power_transformer_list, synchronous_machine_list,
                          energy_consumer_list, shunt_compensator_list):

        self.node_id_list = conducting_equipment_id_list + terminal_id_list + \
                            connectivity_node_id_list

        for node_id in self.node_id_list:
            if node_id in conducting_equipment_id_list:
                neighbor_list = []
                for te in terminal_list:
                    if te.ce == node_id:
                        neighbor_list.append(te.id_)
                self.adjacency_dict[node_id] = neighbor_list
            elif node_id in terminal_id_list:
                for te in terminal_list:
                    if te.id_ == node_id:
                        self.adjacency_dict[node_id] = [te.ce, te.cn]
            elif node_id in connectivity_node_id_list:
                neighbor_list = []
                for te in terminal_list:
                    if te.cn == node_id:
                        neighbor_list.append(te.id_)
                self.adjacency_dict[node_id] = neighbor_list

        # Check breaker position and take the
        eliminate_node = []
        for i in range(len(breaker_list)):
            # Find terminals of the breaker
            if breaker_list[i].pos:
                for te in terminal_list:
                    if te.ce == breaker_list[i].id_:
                        eliminate_node.append(te.id_)
    
        # Remove the connectivity node which is in the list of the value of the terminal's dictionary
        for elim in eliminate_node:
            del self.adjacency_dict[elim]
    
        for node in self.adjacency_dict:
            for elim in eliminate_node:
                if elim in self.adjacency_dict[node]:
                    self.adjacency_dict[node].remove(elim)
    
        visited_node = []
        start_node = synchronous_machine_id_list[0]
        stack = [start_node]
    
        while stack:
            current = stack.pop()
            for neighbor in self.adjacency_dict[current]:
                if neighbor not in visited_node:
                    stack.append(neighbor)
            if current not in visited_node:
                visited_node.append(current)
    
        # Build the network
        conducting_equipment_id_topology = []
        for node in visited_node:
            if node in conducting_equipment_id_list:
                conducting_equipment_id_topology.append(node)
    
        # Build the topology
    
        for bb in busbar_section_list:
            if bb.id_ in conducting_equipment_id_topology:
                self.busbar_section_list_topology.append(bb)
    
        for al in ac_line_segment_list:
            if al.id_ in conducting_equipment_id_topology:
                self.ac_line_segment_list_topology.append(al)
    
        for tr in power_transformer_list:
            if tr.id_ in conducting_equipment_id_topology:
                self.power_transformer_list_topology.append(tr)
    
        for sm in synchronous_machine_list:
            if sm.id_ in conducting_equipment_id_topology:
                self.synchronous_machine_list_topology.append(sm)
    
        for ec in energy_consumer_list:
            if ec.id_ in conducting_equipment_id_topology:
                self.energy_consumer_list_topology.append(ec)
    
        for sh in shunt_compensator_list:
            if sh.id_ in conducting_equipment_id_topology:
                self.shunt_compensator_list_topology.append(sh)

        for br in breaker_list:
            if br.id_ in conducting_equipment_id_topology:
                self.breaker_list_topology.append(br)

        print('Network topology has been created')
