import pandapower as pp
import pandapower.plotting as plot


class PandapowerNetwork:

    def __init__(self):
        self.net = pp.create_empty_network()

    def build_pandapower(self, ac_line_segment_list_topology, busbar_section_list_topology,
                          power_transformer_list_topology, synchronous_machine_list_topology,
                          shunt_compensator_list_topology, energy_consumer_list_topology, breaker_list_topology):

        # Create buses in pandapower network from the internal data structure
        for bb_top in busbar_section_list_topology:
            pp.create_bus(self.net, bb_top.u_nom_kv, name=bb_top.name)

        # Create lines in pandapower network from the internal data structure
        for al_top in ac_line_segment_list_topology:
            for bb_top in busbar_section_list_topology:
                if bb_top.id_ == al_top.bus_1_id:
                    from_bus = pp.get_element_index(self.net, 'bus', bb_top.name)
                if bb_top.id_ == al_top.bus_2_id:
                    to_bus = pp.get_element_index(self.net, 'bus', bb_top.name)
            pp.create_line_from_parameters(self.net, from_bus, to_bus, al_top.length_km, al_top.r_ohm,
                                           al_top.x_ohm, 0.0, al_top.i_max_ka,
                                           name=al_top.name)

        # Create transformers in pandapower network from the internal data structure
        for tr_top in power_transformer_list_topology:
            for bb_top in busbar_section_list_topology:
                if bb_top.id_ == tr_top.bus_hv_id:
                    hv_bus = pp.get_element_index(self.net, 'bus', bb_top.name)
            for bb_top in busbar_section_list_topology:
                if bb_top.id_ == tr_top.bus_lv_id:
                    lv_bus = pp.get_element_index(self.net, 'bus', bb_top.name)
            # From the transformer documentation
            power_transformer_z = (tr_top.r ** 2 + tr_top.x ** 2) ** 0.5
            power_transformer_vsc = 100 * power_transformer_z * tr_top.s_nom_mva
            power_transformer_vscr = 100 * tr_top.r * tr_top.s_nom_mva
            # Neglect the iron losses
            if ('hv_bus' or 'lv_bus') in locals():
                pp.create_transformer_from_parameters(self.net, hv_bus, lv_bus, tr_top.s_nom_mva,
                                                      tr_top.hv_nom_kv, tr_top.lv_nom_kv,
                                                      power_transformer_vscr, power_transformer_vsc, 0, 0,
                                                      name=tr_top.name)
                del hv_bus
                del lv_bus

        # Create generators in pandapower network from the internal data structure
        for sm_top in synchronous_machine_list_topology:
            for bb_top in busbar_section_list_topology:
                if bb_top.id_ == sm_top.bus_id:
                    sm_bus = pp.get_element_index(self.net, 'bus', bb_top.name)
            pp.create_gen(self.net, sm_bus, sm_top.p_rated, name=sm_top.name)

        # Create shunt in pandapower network from the internal data structure
        for sh_top in shunt_compensator_list_topology:
            for bb_top in busbar_section_list_topology:
                if bb_top.id_ == sh_top.bus_id:
                    sh_bus = pp.get_element_index(self.net, 'bus', bb_top.name)
            pp.create_shunt(self.net, sh_bus, sh_top.q_rated_mvar, vn_kv=sh_top.u_nom_kv, name=sh_top.name)

        # Create loads in pandapower network from the internal data structure
        for ec_top in energy_consumer_list_topology:
            for bb_top in busbar_section_list_topology:
                if bb_top.id_ == ec_top.bus_id:
                    ec_bus = pp.get_element_index(self.net, 'bus', bb_top.name)
            pp.create_load(self.net, ec_bus, ec_top.p, ec_top.q, name=ec_top.name)

        # Comment this part if the extended XML files are used
        # Create switches
        for br_top in breaker_list_topology:
            for bb_top in busbar_section_list_topology:
                if bb_top.id_ == br_top.bus_id:
                    br_bb = pp.get_element_index(self.net, 'bus', bb_top.name)
                    for al_top in ac_line_segment_list_topology:
                        if al_top.id_ == br_top.element_id:
                            br_el = pp.get_element_index(self.net, 'line', al_top.name)
                            pp.create_switch(self.net, br_bb, br_el, et='l', name=br_top.name)
                    for tr_top in power_transformer_list_topology:
                        if tr_top.id_ == br_top.element_id:
                            br_el = pp.get_element_index(self.net, 'trafo', tr_top.name)
                            pp.create_switch(self.net, br_bb, br_el, et='t', name=br_top.name)
        print('Pandapower network has been created')

    def plot_network(self, plot_filename):
        self.plot_filename = plot_filename
        plot.to_html(self.net, self.plot_filename)

    def print_network(self):
        print(self.net)
        print(self.net.bus)
        print(self.net.gen)
        print(self.net.line)
        print(self.net.trafo)
        print(self.net.load)
        print(self.net.shunt)
        print(self.net.switch)