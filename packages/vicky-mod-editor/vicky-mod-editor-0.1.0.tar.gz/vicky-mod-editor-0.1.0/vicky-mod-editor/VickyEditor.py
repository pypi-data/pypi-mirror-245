from State import State
from Country import Country
from DataReader import read_map_data, read_pops_data, read_states_data, read_buildings_data, read_routes_data, read_countries_data

class VickyEditor:
    def __init__(self, folder_path,quick=False):
        self.folder_path = folder_path
        self.map_data = read_map_data(folder_path,quick)
        self.states_data = read_states_data(folder_path)
        self.pops_data = read_pops_data(folder_path,quick)
        self.buildings_data = read_buildings_data(folder_path,quick)
        self.routes_data = read_routes_data(folder_path)
        self.countries_data = read_countries_data(folder_path)
        
        self.setup_states()
        self.setup_countries()
        
    def setup_states(self):
        self.states = {}
        for state_name in self.states_data:
            if (state_name in self.pops_data) and (state_name in self.map_data):
                self.states[state_name] = State(state_name,self)

    def setup_countries(self):
        self.countries = {}
        for country_tag in self.countries_data:
            self.countries[country_tag] = Country(country_tag,self)
            
    def transfer_full_state(self,state_name,target_country):
        self.states[state_name].transfer_all_provinces_to_country(target_country)
    
    def transfer_provinces(self,state_name,provinces,target_country):
        self.states[state_name].transfer_provinces_to_country(provinces,target_country)

    def transfer_substate(self,state_name,source_country,target_country):
        if source_country in self.states[state_name].substates:
            self.states[state_name].transfer_all_provinces_in_substate_to_country(source_country,target_country)    
    
    def add_route(self,source_country,target_country,goods,level):
        if source_country in self.countries:
            self.countries[source_country].add_route(target_country,goods,level)