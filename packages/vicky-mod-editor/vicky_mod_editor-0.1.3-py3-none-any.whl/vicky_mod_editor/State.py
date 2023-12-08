from .DataWriter import write_states_data, write_pops_data, write_buildings_data
from copy import copy
from .utils import consolidate_pops, consolidate_buildings

class State:
    def __init__(self,state_name,editor):
        self.state_name = state_name
        self.provinces = editor.map_data[state_name]['provinces']
        self.id = editor.map_data[state_name]['id']
        self.homelands = editor.states_data[state_name]['homelands']
        self.claims = editor.states_data[state_name]['claims']
        self.substates = editor.states_data[state_name]['substates']
        self.pops = editor.pops_data[state_name]['pops']
        self.buildings = editor.buildings_data[state_name]['buildings']
        
        self.states_path = editor.states_data[state_name]['states_path']
        self.pops_path = editor.pops_data[state_name]['pops_path']
        self.buildings_path = editor.buildings_data[state_name]['buildings_path']
        
    def get_substate_population(self,country):
        if country in self.pops:
            return sum([pop['size'] for pop in self.pops[country]])
        return 0

    def get_state_population(self):
        return sum([self.get_substate_population(country) for country in self.pops])
    
    def transfer_all_provinces_to_country(self,target_country):
        source_substates = list([ss for ss in self.substates if ss != target_country])
        for ss in source_substates:
            self.transfer_all_provinces_in_substate_to_country(ss,target_country)
    
    def transfer_all_provinces_in_substate_to_country(self,substate,target_country):
        provinces = self.substates[substate]['owned_provinces']
        self.transfer_provinces_in_substate_to_country(substate,provinces,target_country)
    
    def transfer_provinces_to_country(self,provinces,target_country):
        source_substates = list([ss for ss in self.substates if ss != target_country])
        for ss in source_substates:
            self.transfer_provinces_in_substate_to_country(ss,provinces,target_country)

    def transfer_provinces_in_substate_to_country(self,substate,provinces,target_country):
        if substate not in self.substates:
            print(f'substate {substate} not found in {self.state_name}')
            return
        
        p_in_substate = self.substates[substate]['owned_provinces']
        p_to_transfer = [p for p in provinces if p in p_in_substate]
        
        if len(p_to_transfer) == 0:
            print(f'none of the provinces to transfer from {substate} in {self.state_name}')
            return
        
        # first edit the data in the state object
        # provinces, pops, buildings
        self.transfer_provinces(p_to_transfer,substate,target_country)
        
        # provinces fraction to move, 1 means all provinces moving, 0 means no provinces move
        # should never actually be 0
        p_move_fraction = len(p_to_transfer)/len(p_in_substate)

        self.transfer_pops(p_move_fraction,substate,target_country)
        self.transfer_buildings(p_move_fraction,substate,target_country)
        
        print(f'moved {str(p_to_transfer)} from {substate} to {target_country}')
        
        # then update files by writing states and pop data again
        write_states_data(self)
        write_pops_data(self)
        write_buildings_data(self)
    
    def transfer_provinces(self,provinces,source,target):
        # remove provinces from origin
        if set(provinces) == set(self.substates[source]['owned_provinces']):
            # no provinces remaining, delete the substate
            self.substates.pop(source)
        else:
            # provinces remaining, update the substate
            p_remaining = [p for p in self.substates[source]['owned_provinces'] if p not in provinces]
            self.substates[source]['owned_provinces'] = p_remaining
        
        # add provinces to destination
        if target in self.substates:
            # substate already exists, then must just add provinces
            self.substates[target]['owned_provinces'].extend(provinces)
        else:
            # substate doesn't exist, create new substate
            self.substates[target] = {
                'country': target,
                'owned_provinces': provinces
            }
    
    def transfer_pops(self,p_move_fraction,source,target):
        # take out pops from source
        if p_move_fraction == 1:
            moving_pops = self.pops.pop(source, [])
        else:
            moving_pops = []
            remaining_pops = []
            for pop in self.pops[source]:
                n_moving = int(p_move_fraction*pop['size'])
                n_remaining = pop['size']-n_moving
                moving_pop = copy(pop)
                remaining_pop = copy(pop)
                moving_pop['size'] = n_moving
                remaining_pop['size'] = n_remaining
                moving_pops.append(moving_pop)
                remaining_pops.append(remaining_pop)
            self.pops[source] = remaining_pops
        
        # add pops to destination
        self.pops.setdefault(target, []).extend(moving_pops)
        
        #consolidating pops
        self.consolidate_pops_substate(target)

    def transfer_buildings(self,p_move_fraction,source,target):
        # take out buildings from source
        if p_move_fraction == 1:
            moving_buildings = self.buildings.pop(source, [])
        else:
            moving_buildings = []
            remaining_buildings = []
            for building in self.buildings[source]:
                n_moving = int(p_move_fraction*building['level'])
                n_remaining = building['level']-n_moving
                moving_building = copy(building)
                remaining_building = copy(building)
                moving_building['level'] = n_moving
                remaining_building['level'] = n_remaining
                moving_buildings.append(moving_building)
                remaining_buildings.append(remaining_building)
            self.buildings[source] = remaining_buildings
        
        # add buildings to destination
        self.buildings.setdefault(target, []).extend(moving_buildings)
        
        #consolidating buildings
        self.consolidate_buildings_substate(target)
    
    def consolidate_pops_substate(self,substate):
        self.pops[substate] = consolidate_pops(self.pops[substate])
    
    def consolidate_pops(self):
        for substate in self.pops:
            self.consolidate_pops_substate(substate)
    
    def consolidate_buildings_substate(self,substate):
        self.buildings[substate] = consolidate_buildings(self.buildings[substate])