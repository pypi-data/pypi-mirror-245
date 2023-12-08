from .utils import parse_cw
import os

def read_pops_data(folder_path,quick):
    print('reading pops data')
    pops_folder_path = os.path.join(folder_path, 'common/history/pops')
    pops_data = {}
    for file_name in os.listdir(pops_folder_path):
        if file_name == '100_pops_example.txt':
            continue
        if file_name.endswith(".txt"):
            file_path = os.path.join(pops_folder_path, file_name)
            print(file_path)
            pop_raw_data = parse_cw(file_path)['POPS']
            for key, substates in pop_raw_data.items():
                state_name = key.replace("s:", "")
                pop_state_data = {}
                for substate_key, substate_data in substates.items():
                    country_name = substate_key.replace("region_state:", "")
                    if 'create_pop' in substate_data and isinstance(substate_data['create_pop'], list):
                        pops = [dict(i) for i in substate_data['create_pop']]
                    elif 'create_pop' in substate_data:
                        pops = [dict(substate_data['create_pop'])]
                    else:
                        pops = []

                    pop_state_data[country_name] = pops
                
                pops_dict = {
                    'pops':pop_state_data,
                    'pops_path':file_path
                }
                pops_data[state_name] = pops_dict
        if quick:
            break
    return pops_data

def read_states_data(folder_path):
    print('reading states data')
    states_path = os.path.join(folder_path, 'common/history/states/00_states.txt')
    print(states_path)
    states_raw_data = parse_cw(states_path)['STATES']
    states_data = {}
    for key, value in states_raw_data.items():
        state_name = key.replace("s:", "")
        state_data = {}

        # Check if 'homelands', 'claims' and 'substates' are present and are lists
        if 'add_homeland' in value and isinstance(value['add_homeland'], list):
            state_data['homelands'] = value['add_homeland']
        elif 'add_homeland' in value:
            state_data['homelands'] = [value['add_homeland']]
        else:
            state_data['homelands'] = []

        if 'add_claim' in value and isinstance(value['add_claim'], list):
            state_data['claims'] = value['add_claim']
        elif 'add_claim' in value:
            state_data['claims'] = [value['add_claim']]
        else:
            state_data['claims'] = []

        if 'create_state' in value and isinstance(value['create_state'], list):
            substates = value['create_state']
        elif 'create_state' in value:
            substates = [value['create_state']]
        else:
            substates = []
        
        for ss in substates:
            ss['country'] = ss['country'].replace('c:','')
        state_data['substates'] = {ss['country']:dict(ss) for ss in substates}
        state_data['states_path'] = states_path

        states_data[state_name] = state_data
    return states_data

def read_map_data(folder_path,quick):
    map_data_folder_path = os.path.join(folder_path, 'map_data/state_regions')
    print('reading map data')
    states_dict = {}
    for file_name in os.listdir(map_data_folder_path):
        if file_name.endswith(".txt"):
            state_path = os.path.join(map_data_folder_path, file_name)
            print(state_path)
            state_data = parse_cw(state_path)
            for key, value in state_data.items():
                states_dict[key] = {
                    'id':value['id'],
                    'provinces':value['provinces']
                }
            if quick:
                break
    return states_dict


def read_buildings_data(folder_path,quick):
    print('reading buildings data')
    buildings_folder_path = os.path.join(folder_path, 'common/history/buildings')
    buildings_data = {}
    for file_name in os.listdir(buildings_folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(buildings_folder_path, file_name)
            print(file_path)
            building_raw_data = parse_cw(file_path)['BUILDINGS']
            for key, substates in building_raw_data.items():
                state_name = key.replace("s:", "")
                building_state_data = {}
                for substate_key, substate_data in substates.items():
                    country_name = substate_key.replace("region_state:", "")
                    if 'create_building' in substate_data and isinstance(substate_data['create_building'], list):
                        buildings = [dict(i) for i in substate_data['create_building']]
                    elif 'create_building' in substate_data:
                        buildings = [dict(substate_data['create_building'])]
                    else:
                        buildings = []

                    building_state_data[country_name] = buildings
                
                buildings_dict = {
                    'buildings':building_state_data,
                    'buildings_path':file_path
                }
                buildings_data[state_name] = buildings_dict
        if quick:
            break
    return buildings_data

def read_routes_data(folder_path):
    print('reading routes data')
    routes_path = os.path.join(folder_path, 'common/history/trade_routes/00_trade_routes.txt')
    print(routes_path)
    routes_raw_data = parse_cw(routes_path)['TRADE_ROUTES']

    routes_data = {}
    for key, value in routes_raw_data.items():
        country_name = key.replace("c:", "")
        country_data = []
        
        if 'create_trade_route' in value and isinstance(value['create_trade_route'], list):
            raw_routes = value['create_trade_route']
        elif 'create_trade_route' in value:
            raw_routes = [value['create_trade_route']]
        else:
            raw_routes = []
        
        for raw_route in raw_routes:
            raw_route['target'] = raw_route['target'].replace('c:','').replace('.market','')
            if raw_route['direction'] == 'import':
                raw_route['level'] *= -1
            raw_route.pop('direction')
            country_data.append(dict(raw_route))
        routes_data[country_name] = country_data
    
    return {'routes':routes_data, 'routes_path':routes_path}

def read_countries_data(folder_path):
    print('reading countries data')
    countries_path = os.path.join(folder_path, 'common/country_definitions/00_countries.txt')
    print(countries_path)
    countries_raw_data = parse_cw(countries_path,hsv_changer=True)

    countries_data = {key:dict(value) for key, value in countries_raw_data.items()}
    
    return countries_data