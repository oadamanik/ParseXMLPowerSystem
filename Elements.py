import xml.etree.ElementTree as et


class ACLineSegment:

    def __init__(self, id_, length_km, r_ohm, x_ohm, bch=0.0,
                 name='', base_voltage_kv=0.0, i_max_ka=0.0, bus_1_id='', bus_2_id=''):
        self.id_ = id_
        self.length_km = length_km
        self.r_ohm = r_ohm
        self.x_ohm = x_ohm
        self.bch = bch
        self.name = name
        self.base_voltage_kv = base_voltage_kv
        self.bus_1_id = bus_1_id
        self.bus_2_id = bus_2_id
        self.i_max_ka = i_max_ka


class BaseVoltage:

    def __init__(self, id_, u_base_kv, name=''):
        self.id_ = id_
        self.u_base_kv = u_base_kv
        self.name = name


class Breaker:

    def __init__(self, id_, normal_open=False, pos=False, name=''):
        self.id_ = id_
        self.normal_open = normal_open
        self.pos = pos
        self.name = name
        self.bus_id = None
        self.element_id = None

    def open(self):
        if not self.pos:
            self.pos = True

    def close(self):
        if self.pos:
            self.pos = False


class BusbarSection:

    def __init__(self, id_, u_nom_kv, name=''):
        self.id_ = id_
        self.u_nom_kv = u_nom_kv
        self.name = name


class ConnectivityNode:

    def __init__(self, id_, container, name=''):
        self.id_ = id_
        self.container = container
        self.name = name


class CurrentLimit:

    def __init__(self, id_, current_amp, operational_limit_set_id, name=''):
        self.id_ = id_
        self.name = name
        self.current_amp = current_amp
        self.operational_limit_set_id = operational_limit_set_id


class EnergyConsumer:

    def __init__(self, id_, p=0.0, q=0.0, name='', bus_id=''):
        self.id_ = id_
        self.name = name
        self.p = p
        self.q = q
        self.bus_id = bus_id


class GeneratingUnit:

    def __init__(self, id_, p_nom, name=''):
        self.id_ = id_
        self.name = name
        self.p_nom = p_nom


class OperationalLimitSet:

    def __init__(self, id_, terminal, name='', current_limit_amp_list=None):
        self.id_ = id_
        self.name = name
        self.terminal = terminal
        self.current_limit_amp_list = current_limit_amp_list if current_limit_amp_list is not None else []
        if any(self.current_limit_amp_list):
            self.min_current_limit_amp = min(self.current_limit_amp_list)


class PowerTransformer:

    def __init__(self, id_, r=0.0, x=0.0, b=0.0, g=0.0, r0=0.0, x0=0.0, b0=0.0,
                 g0=0.0, s_nom_mva=0.0, hv_nom_kv=0.0, lv_nom_kv=0.0, bus_hv_id='', bus_lv_id='', name=''):
        self.id_ = id_
        self.r = r
        self.x = x
        self.b = b
        self.g = g
        self.r0 = r0
        self.x0 = x0
        self.b0 = b0
        self.g0 = g0
        self.s_nom_mva = s_nom_mva
        self.hv_nom_kv = hv_nom_kv
        self.lv_nom_kv = lv_nom_kv
        self.bus_hv_id = bus_hv_id
        self.bus_lv_id = bus_lv_id
        self.name = name


class ShuntCompensator:

    def __init__(self, id_, b=0.0, g=0.0, b0=0.0, g0=0.0, u_nom_kv=0.0, bus_id='', name=''):
        self.id_ = id_
        self.b = b
        self.g = g
        self.b0 = b0
        self.g0 = g0
        self.u_nom_kv = u_nom_kv
        self.bus_id = bus_id
        self.q_rated_mvar = self.b * self.u_nom_kv**2
        self.name = name


class SynchronousMachine:

    def __init__(self, id_, s_rated_kva=0.0, pf_rated=0.0,
                 r0=0.0, r2=0.0, x0=0.0, x2=0.0, generating_unit_id='', bus_id='', name=''):
        self.id_ = id_
        self.name = name
        self.s_rated_kva = s_rated_kva
        self.pf_rated = pf_rated
        self.p_rated = s_rated_kva*pf_rated
        self.r0 = r0
        self.r2 = r2
        self.x0 = x0
        self.x2 = x2
        self.generating_unit_id = generating_unit_id
        self.bus_id = bus_id


class Terminal:

    def __init__(self, id_, sequence_number, ce, cn, name=''):
        self.id_ = id_
        self.name = name
        self.sequence_number = sequence_number
        self.ce = ce
        self.cn = cn


class VoltageLevel:

    def __init__(self, the_id, name=''):
        self.the_id = the_id
        self.name = name
        self.u_kv = float(name)


def get_id(id_list, object_list):
    for i in range(len(object_list)):
        id_list.append(object_list[i].id_)


class GridElements:

    def __init__(self):
        self.eq_tree = None
        self.ssh_tree = None
        self.eq = None
        self.ssh = None

        self.ac_line_segment_list = []
        self.base_voltage_list = []
        self.busbar_section_list = []
        self.breaker_list = []
        self.connectivity_node_list = []
        self.current_limit_list = []
        self.energy_consumer_list = []
        self.generating_unit_list = []
        self.synchronous_machine_list = []
        self.power_transformer_list = []
        self.shunt_compensator_list = []
        self.terminal_list = []
        self.operational_limit_set_list = []
        self.voltage_level_list = []

        self.connectivity_node_id_list = []
        self.terminal_id_list = []
        self.synchronous_machine_id_list = []
        self.busbar_section_id_list = []
        self.power_transformer_id_list = []
        self.breaker_id_list = []
        self.ac_line_segment_id_list = []
        self.energy_consumer_id_list = []
        self.shunt_compensator_id_list = []
        self.conducting_equipment_id_list = []
        self.conducting_equipment_list = []

    def parse_xml(self, filename_eq, filename_ssh):
        self.eq_tree = et.parse(filename_eq)
        self.ssh_tree = et.parse(filename_ssh)
        self.eq = self.eq_tree.getroot()
        self.ssh = self.ssh_tree.getroot()
        print("Successfully parse the files")

    def create_elements(self):

        ns = {'cim': 'http://iec.ch/TC57/2013/CIM-schema-cim16#',
              'entsoe': 'http://entsoe.eu/CIM/SchemaExtension/3/1#',
              'rdf': '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'}

        # ConnectivityNode
        for cn in self.eq.findall('cim:ConnectivityNode', ns):
            self.connectivity_node_list.append(ConnectivityNode(cn.attrib.get(
                ns['rdf'] + 'ID'), cn.find(
                'cim:ConnectivityNode.ConnectivityNodeContainer', ns).attrib.get(
                ns['rdf'] + 'resource').replace('#', ''), name=cn.find('cim:IdentifiedObject.name', ns).text))
        get_id(self.connectivity_node_id_list, self.connectivity_node_list)

        # Terminal
        for te in self.eq.findall('cim:Terminal', ns):
            self.terminal_list.append(Terminal(te.attrib.get(
                ns['rdf'] + 'ID'), te.find('cim:ACDCTerminal.sequenceNumber', ns).text, te.find(
                'cim:Terminal.ConductingEquipment', ns).attrib.get(ns['rdf'] + 'resource').replace('#', ''),
                te.find('cim:Terminal.ConnectivityNode', ns).attrib.get(ns['rdf'] + 'resource').replace('#', ''),
                name=te.find('cim:IdentifiedObject.name', ns).text, ))
        get_id(self.terminal_id_list, self.terminal_list)

        for cl in self.eq.findall('cim:CurrentLimit', ns):
            # Push every object created to the list
            self.current_limit_list.append(CurrentLimit(cl.attrib.get(
                ns['rdf'] + 'ID'), cl.find('cim:IdentifiedObject.name', ns).text,
                float(cl.find('cim:CurrentLimit.value', ns).text), cl.find(
                    'cim:OperationalLimit.OperationalLimitSet', ns).attrib.get(
                    ns['rdf'] + 'resource').replace('#', '')))

        # OperationalLimitSet
        for ol in self.eq.findall('cim:OperationalLimitSet', ns):
            # Create object using the obtained information from the xml file
            operational_limit_set = OperationalLimitSet(ol.attrib.get(
                ns['rdf'] + 'ID'), ol.find('cim:IdentifiedObject.name', ns).text,
                ol.find('cim:OperationalLimitSet.Terminal', ns).attrib.get(
                    ns['rdf'] + 'resource').replace('#', ''))
            # Obtain the list of current limit to the operational limit set
            for cl in self.current_limit_list:
                if cl.operational_limit_set_id == operational_limit_set.id_:
                    operational_limit_set.current_limit_amp_list.append(cl.current_amp)
            # Push every object created to the list
            self.operational_limit_set_list.append(operational_limit_set)

        # ACLineSegment
        for al in self.eq.findall('cim:ACLineSegment', ns):
            ac_line_segment = ACLineSegment(al.attrib.get(ns['rdf'] + 'ID'),
                                            float(al.find('cim:Conductor.length', ns).text),
                                            float(al.find('cim:ACLineSegment.r', ns).text),
                                            float(al.find('cim:ACLineSegment.x', ns).text),
                                            name=al.find('cim:IdentifiedObject.name', ns).text)
            for bv in self.eq.findall('cim:BaseVoltage', ns):
                if al.find('cim:ConductingEquipment.BaseVoltage', ns).attrib.get(ns['rdf'] + 'resource').replace(
                        '#', '') == bv.attrib.get(ns['rdf'] + 'ID'):
                    ac_line_segment.base_voltage_kv = float(bv.find('cim:BaseVoltage.nominalVoltage', ns).text)
            # Connection to buses
            for te in self.eq.findall('cim:Terminal', ns):
                if al.attrib.get(ns['rdf'] + 'ID') == te.find(
                        'cim:Terminal.ConductingEquipment', ns).attrib.get(ns['rdf'] + 'resource').replace('#', ''):
                    if te.find('cim:ACDCTerminal.sequenceNumber', ns).text == '1':
                        # Find the connectivity node and take the container association
                        for cn in self.eq.findall('cim:ConnectivityNode', ns):
                            if cn.attrib.get(ns['rdf'] + 'ID') == te.find(
                                    'cim:Terminal.ConnectivityNode', ns).attrib.get(
                                ns['rdf'] + 'resource').replace('#', ''):
                                # Find the busbar section inside this container
                                # The busbar is where the line's terminal is connected
                                for bb in self.eq.findall('cim:BusbarSection', ns):
                                    if bb.find('cim:Equipment.EquipmentContainer', ns).attrib.get(
                                            ns['rdf'] + 'resource').replace('#', '') == cn.find(
                                        'cim:ConnectivityNode.ConnectivityNodeContainer', ns).attrib.get(
                                            ns['rdf'] + 'resource').replace('#', ''):
                                        ac_line_segment.bus_1_id = bb.attrib.get(ns['rdf'] + 'ID')
                            # Current limit
                            # for ol in operational_limit_set_list:
                            #     if ol.terminal
                            #         ac_line_segment.i_max_ka = float(cl.find('cim:CurrentLimit.value', ns).text)
                    elif te.find('cim:ACDCTerminal.sequenceNumber', ns).text == '2':
                        # Find the connectivity node and take the container association
                        for cn in self.eq.findall('cim:ConnectivityNode', ns):
                            if cn.attrib.get(ns['rdf'] + 'ID') == te.find(
                                    'cim:Terminal.ConnectivityNode', ns).attrib.get(
                                    ns['rdf'] + 'resource').replace('#', ''):
                                # Find the busbar section inside this container
                                # The busbar is where the line's terminal is connected
                                for bb in self.eq.findall('cim:BusbarSection', ns):
                                    if bb.find('cim:Equipment.EquipmentContainer', ns).attrib.get(
                                            ns['rdf'] + 'resource').replace('#', '') == cn.find(
                                        'cim:ConnectivityNode.ConnectivityNodeContainer', ns).attrib.get(
                                        ns['rdf'] + 'resource').replace('#', ''):
                                        ac_line_segment.bus_2_id = bb.attrib.get(ns['rdf'] + 'ID')
            self.ac_line_segment_list.append(ac_line_segment)
        get_id(self.ac_line_segment_id_list, self.ac_line_segment_list)

        # BaseVoltage
        for bv in self.eq.findall('cim:BaseVoltage', ns):
            self.base_voltage_list.append(BaseVoltage(bv.attrib.get(ns['rdf'] + 'ID'),
                                                      float(bv.find('cim:BaseVoltage.nominalVoltage', ns).text),
                                                      name=bv.find('cim:IdentifiedObject.name', ns).text))

        # BusbarSection
        for bb in self.eq.findall('cim:BusbarSection', ns):
            for vl in self.eq.findall('cim:VoltageLevel', ns):
                if bb.find('cim:Equipment.EquipmentContainer', ns).attrib.get(
                        ns['rdf'] + 'resource').replace('#', '') == vl.attrib.get(ns['rdf'] + 'ID'):
                    u_nom_kv = float(vl.find('cim:IdentifiedObject.name', ns).text)
                    busbar_section = BusbarSection(bb.attrib.get(ns['rdf'] + 'ID'), u_nom_kv, name=bb.find(
                        'cim:IdentifiedObject.name', ns).text)
                    self.busbar_section_list.append(busbar_section)
        get_id(self.busbar_section_id_list, self.busbar_section_list)

        # EnergyConsumer
        for ec in self.eq.findall('cim:EnergyConsumer', ns):
            energy_consumer = EnergyConsumer(ec.attrib.get(
                ns['rdf'] + 'ID'), name=ec.find('cim:IdentifiedObject.name', ns).text)
            for ec_ssh in self.ssh.findall('cim:EnergyConsumer', ns):
                if ec_ssh.attrib.get(ns['rdf'] + 'about').replace('#', '') == ec.attrib.get(ns['rdf'] + 'ID'):
                    energy_consumer.p = float(ec_ssh.find('cim:EnergyConsumer.p', ns).text)
                    energy_consumer.q = float(ec_ssh.find('cim:EnergyConsumer.q', ns).text)
            # Connection to buses
            for te in self.eq.findall('cim:Terminal', ns):
                if ec.attrib.get(ns['rdf'] + 'ID') == te.find(
                        'cim:Terminal.ConductingEquipment', ns).attrib.get(ns['rdf'] + 'resource').replace('#', ''):
                    # Find the connectivity node and take the container association
                    for cn in self.eq.findall('cim:ConnectivityNode', ns):
                        if cn.attrib.get(ns['rdf'] + 'ID') == te.find('cim:Terminal.ConnectivityNode', ns).attrib.get(
                                ns['rdf'] + 'resource').replace('#', ''):
                            # Find the busbar section inside this container
                            # The busbar is where the line's terminal is connected
                            for bb in self.eq.findall('cim:BusbarSection', ns):
                                if bb.find('cim:Equipment.EquipmentContainer', ns).attrib.get(
                                        ns['rdf'] + 'resource').replace('#', '') == cn.find(
                                    'cim:ConnectivityNode.ConnectivityNodeContainer', ns).attrib.get(
                                        ns['rdf'] + 'resource').replace('#', ''):
                                    energy_consumer.bus_id = bb.attrib.get(ns['rdf'] + 'ID')
            self.energy_consumer_list.append(energy_consumer)
        get_id(self.energy_consumer_id_list, self.energy_consumer_list)

        # GeneratingUnit
        for gen in self.eq.findall('cim:GeneratingUnit', ns):
            self.generating_unit_list.append(GeneratingUnit(gen.attrib.get(ns['rdf'] + 'ID'),
                                                       float(gen.find('cim:GeneratingUnit.nominalP', ns).text),
                                                            name=gen.find('cim:IdentifiedObject.name', ns).text))

        # SynchronousMachine
        for sm in self.eq.findall('cim:SynchronousMachine', ns):
            synchronous_machine = SynchronousMachine(sm.attrib.get(ns['rdf'] + 'ID'),
                                                           float(sm.find('cim:RotatingMachine.ratedS', ns).text),
                                                           float(sm.find(
                                                               'cim:RotatingMachine.ratedPowerFactor', ns).text),
                                                           float(sm.find('cim:SynchronousMachine.r0', ns).text),
                                                           float(sm.find('cim:SynchronousMachine.r2', ns).text),
                                                           float(sm.find('cim:SynchronousMachine.x0', ns).text),
                                                           float(sm.find('cim:SynchronousMachine.x2', ns).text),
                                                     name=sm.find('cim:IdentifiedObject.name', ns).text)
            # Connection to bus
            for te in self.eq.findall('cim:Terminal', ns):
                if sm.attrib.get(ns['rdf'] + 'ID') == te.find(
                        'cim:Terminal.ConductingEquipment', ns).attrib.get(ns['rdf'] + 'resource').replace('#', ''):
                    # Find the connectivity node and take the container association
                    for cn in self.eq.findall('cim:ConnectivityNode', ns):
                        if cn.attrib.get(ns['rdf'] + 'ID') == te.find('cim:Terminal.ConnectivityNode', ns).attrib.get(
                                ns['rdf'] + 'resource').replace('#', ''):
                            # Find the busbar section inside this container
                            # The busbar is where the line's terminal is connected
                            for bb in self.eq.findall('cim:BusbarSection', ns):
                                if bb.find('cim:Equipment.EquipmentContainer', ns).attrib.get(
                                        ns['rdf'] + 'resource').replace('#', '') == cn.find(
                                    'cim:ConnectivityNode.ConnectivityNodeContainer', ns).attrib.get(
                                        ns['rdf'] + 'resource').replace('#', ''):
                                    synchronous_machine.bus_id = bb.attrib.get(ns['rdf'] + 'ID')
            self.synchronous_machine_list.append(synchronous_machine)
        get_id(self.synchronous_machine_id_list, self.synchronous_machine_list)

        # PowerTransformer and PowerTransformerEnd are combined in a class
        for tr in self.eq.findall('cim:PowerTransformer', ns):
            power_transformer = PowerTransformer(tr.attrib.get(ns['rdf'] + 'ID'))
            power_transformer.name = tr.find('cim:IdentifiedObject.name', ns).text
            for tr_end in self.eq.findall('cim:PowerTransformerEnd', ns):
                # Find the side of the power transformer
                if power_transformer.id_ == tr_end.find(
                        'cim:PowerTransformerEnd.PowerTransformer', ns).attrib.get(
                    ns['rdf'] + 'resource').replace('#', ''):
                    # HV side
                    if tr_end.find('cim:TransformerEnd.endNumber', ns).text == '1':
                        # Take the information of the transformer
                        # Power rating of the transformer in kVA
                        power_transformer.s_nom_mva = float(tr_end.find('cim:PowerTransformerEnd.ratedS', ns).text)
                        # Voltage rating of the HV side
                        power_transformer.hv_nom_kv = float(tr_end.find('cim:PowerTransformerEnd.ratedU', ns).text)
                        power_transformer.r = float(tr_end.find('cim:PowerTransformerEnd.r', ns).text)
                        power_transformer.x = float(tr_end.find('cim:PowerTransformerEnd.x', ns).text)
                        power_transformer.b = float(tr_end.find('cim:PowerTransformerEnd.b', ns).text)
                        power_transformer.g = float(tr_end.find('cim:PowerTransformerEnd.g', ns).text)
                        power_transformer.r0 = float(tr_end.find('cim:PowerTransformerEnd.r0', ns).text)
                        power_transformer.x0 = float(tr_end.find('cim:PowerTransformerEnd.x0', ns).text)
                        power_transformer.b0 = float(tr_end.find('cim:PowerTransformerEnd.b0', ns).text)
                        power_transformer.g0 = float(tr_end.find('cim:PowerTransformerEnd.g0', ns).text)
                        # Connection to bus
                        for te in self.eq.findall('cim:Terminal', ns):
                            if te.attrib.get(ns['rdf'] + 'ID') == tr_end.find(
                                    'cim:TransformerEnd.Terminal', ns).attrib.get(
                                ns['rdf'] + 'resource').replace('#', ''):
                                # Find the connectivity node and take the container association
                                for cn in self.eq.findall('cim:ConnectivityNode', ns):
                                    if cn.attrib.get(ns['rdf'] + 'ID') == te.find('cim:Terminal.ConnectivityNode',
                                                                                  ns).attrib.get(
                                            ns['rdf'] + 'resource').replace('#', ''):
                                        # Find the busbar section inside this container
                                        # The busbar is where the line's terminal is connected
                                        for bb in self.eq.findall('cim:BusbarSection', ns):
                                            if bb.find('cim:Equipment.EquipmentContainer', ns).attrib.get(
                                                    ns['rdf'] + 'resource').replace('#', '') == cn.find(
                                                'cim:ConnectivityNode.ConnectivityNodeContainer', ns).attrib.get(
                                                ns['rdf'] + 'resource').replace('#', ''):
                                                power_transformer.bus_hv_id = bb.attrib.get(ns['rdf'] + 'ID')
                    # LV side
                    elif tr_end.find('cim:TransformerEnd.endNumber', ns).text == '2':
                        power_transformer.lv_nom_kv = float(tr_end.find('cim:PowerTransformerEnd.ratedU', ns).text)
                        for te in self.eq.findall('cim:Terminal', ns):
                            if te.attrib.get(ns['rdf'] + 'ID') == tr_end.find(
                                    'cim:TransformerEnd.Terminal', ns).attrib.get(
                                ns['rdf'] + 'resource').replace('#', ''):
                                # Find the connectivity node and take the container association
                                for cn in self.eq.findall('cim:ConnectivityNode', ns):
                                    if cn.attrib.get(ns['rdf'] + 'ID') == te.find('cim:Terminal.ConnectivityNode',
                                                                                  ns).attrib.get(
                                        ns['rdf'] + 'resource').replace('#', ''):
                                        # Find the busbar section inside this container
                                        # The busbar is where the line's terminal is connected
                                        for bb in self.eq.findall('cim:BusbarSection', ns):
                                            if bb.find('cim:Equipment.EquipmentContainer', ns).attrib.get(
                                                    ns['rdf'] + 'resource').replace('#', '') == cn.find(
                                                'cim:ConnectivityNode.ConnectivityNodeContainer', ns).attrib.get(
                                                ns['rdf'] + 'resource').replace('#', ''):
                                                power_transformer.bus_lv_id = bb.attrib.get(ns['rdf'] + 'ID')
            self.power_transformer_list.append(power_transformer)
        get_id(self.power_transformer_id_list, self.power_transformer_list)

        # ShuntCompensator
        for sh in self.eq.findall('cim:LinearShuntCompensator', ns):
            shunt_compensator = ShuntCompensator(
                sh.attrib.get(ns['rdf'] + 'ID'),
                float(sh.find('cim:LinearShuntCompensator.bPerSection', ns).text),
                float(sh.find('cim:LinearShuntCompensator.gPerSection', ns).text),
                float(sh.find('cim:LinearShuntCompensator.b0PerSection', ns).text),
                float(sh.find('cim:LinearShuntCompensator.g0PerSection', ns).text),
                float(sh.find('cim:ShuntCompensator.nomU', ns).text),
                name=sh.find('cim:IdentifiedObject.name', ns).text)
            for te in self.eq.findall('cim:Terminal', ns):
                if sh.attrib.get(ns['rdf'] + 'ID') == te.find(
                        'cim:Terminal.ConductingEquipment', ns).attrib.get(ns['rdf'] + 'resource').replace('#', ''):
                    for cn in self.eq.findall('cim:ConnectivityNode', ns):
                        if cn.attrib.get(ns['rdf'] + 'ID') == te.find(
                                'cim:Terminal.ConnectivityNode', ns).attrib.get(
                            ns['rdf'] + 'resource').replace('#', ''):
                            # Find the busbar section inside this container
                            # The busbar is where the line's terminal is connected
                            for bb in self.eq.findall('cim:BusbarSection', ns):
                                if bb.find('cim:Equipment.EquipmentContainer', ns).attrib.get(
                                        ns['rdf'] + 'resource').replace('#', '') == cn.find(
                                    'cim:ConnectivityNode.ConnectivityNodeContainer', ns).attrib.get(
                                    ns['rdf'] + 'resource').replace('#', ''):
                                    shunt_compensator.bus_id = bb.attrib.get(ns['rdf'] + 'ID')
            self.shunt_compensator_list.append(shunt_compensator)
        get_id(self.shunt_compensator_id_list, self.shunt_compensator_list)

        # VoltageLevel
        for vl in self.eq.findall('cim:VoltageLevel', ns):
            self.voltage_level_list.append(VoltageLevel(vl.attrib.get(ns['rdf'] + 'ID'),
                                                   name=vl.find('cim:IdentifiedObject.name', ns).text))

        # Breakers
        for br in self.eq.findall('cim:Breaker', ns):
            breaker = Breaker(br.attrib.get(ns['rdf'] + 'ID'), name=br.find('cim:IdentifiedObject.name', ns).text)
            if br.find('cim:Switch.normalOpen', ns).text == 'true':
                breaker.normal_open = True
            for br_ssh in self.ssh.findall('cim:Breaker', ns):
                if br_ssh.find('cim:Switch.open', ns).text == 'true':
                    breaker.pos = True
            # Find the bus to where the breaker is connected
            breaker_bus_list = []
            for te in self.terminal_list:
                # There will be two terminals that fulfill the condition below
                if te.ce == breaker.id_:
                    # Find the terminal which has the same CN as the breaker
                    for te_ in self.terminal_list:
                        if te_.cn == te.cn:
                            # If there is a bus
                            if te_.ce in self.busbar_section_id_list:
                                breaker.bus_id = te_.ce
                                breaker_bus_list.append(te_.ce)
            print(breaker_bus_list)
            # Find the element to where the breaker is connected
            for te in self.terminal_list:
                # There will be two terminals that fulfill the condition below
                if te.ce == breaker.id_ and breaker.element_id is None:
                    # Find the terminal which has the same CN as the breaker
                    # Put it into the list below
                    breaker_element_list = []
                    # Iterate terminal which has the same CN as the breaker
                    for te_ in self.terminal_list:
                        if te_.cn == te.cn:
                            breaker_element_list.append(te_.ce)
                    if any(i in breaker_element_list for i in self.busbar_section_id_list) \
                            and len(breaker_bus_list) == 1:
                        breaker_element_list.clear()
                    else:
                        breaker_element_list.remove(breaker.id_)
                        for be in breaker_element_list:
                            if be in (self.ac_line_segment_id_list + self.power_transformer_id_list):
                                breaker.element_id = be
            print(breaker.name)
            print(breaker.element_id)
            print(breaker.bus_id)
            self.breaker_list.append(breaker)
        print(len(self.breaker_list))
        get_id(self.breaker_id_list, self.breaker_list)

        self.conducting_equipment_id_list = self.synchronous_machine_id_list + self.busbar_section_id_list + \
                                            self.breaker_id_list + self.power_transformer_id_list + \
                                            self.ac_line_segment_id_list + self.energy_consumer_id_list + \
                                            self.shunt_compensator_id_list

        self.conducting_equipment_list = self.synchronous_machine_list + self.busbar_section_list + \
                                         self.breaker_list + self.power_transformer_list + self.ac_line_segment_list + \
                                         self.energy_consumer_list + self.shunt_compensator_list

        self.disconnectable_list = self.power_transformer_list + self.ac_line_segment_list

        print('Network elements have been created')