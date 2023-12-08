from .BlockUtils import edit_block_content

def write_states_data(state):
    
    new_state_lines = [
        f'\ts:{state.state_name} = {{\n'
    ]
    
    for country, ss in state.substates.items():
        owned_provinces = " ".join(ss['owned_provinces'])
        new_state_lines.extend([
            '\t\tcreate_state = {\n',
            f'\t\t\tcountry = c:{country}\n',
            f'\t\t\towned_provinces = {{ {owned_provinces} }}\n',
            '\t\t}\n',
            '\t\t\n',
        ])

    # Add lines for each homeland
    homeland_lines = [f'\t\tadd_homeland = {homeland}\n' for homeland in state.homelands]
    new_state_lines.extend(homeland_lines)
    
    # Add lines for each claim
    claim_lines = [f'\t\tadd_claim = {claim}\n' for claim in state.claims]
    new_state_lines.extend(claim_lines)

    # Add the closing braces
    new_state_lines.append('\t}\n')

    edit_block_content(state.states_path,state.state_name,new_state_lines)
        
        
def write_pops_data(state):

    new_pop_lines = [
        f'\ts:{state.state_name} = {{\n'
    ]
    
    for ss, pops in state.pops.items():
        new_pop_lines.append(f'\t\tregion_state:{ss} = {{\n')

        for pop in pops:
            new_pop_lines.append('\t\t\tcreate_pop = {\n')

            if 'culture' in pop:
                new_pop_lines.append(f'\t\t\t\tculture = {pop["culture"]}\n')
            if 'religion' in pop:
                new_pop_lines.append(f'\t\t\t\treligion = {pop["religion"]}\n')
            if 'pop_type' in pop:
                new_pop_lines.append(f'\t\t\t\tpop_type = {pop["pop_type"]}\n')

            new_pop_lines.append(f'\t\t\t\tsize = {pop["size"]}\n')
            new_pop_lines.append('\t\t\t}\n')

        new_pop_lines.append('\t\t}\n')
        
    new_pop_lines.append('\t}\n')

    edit_block_content(state.pops_path,state.state_name,new_pop_lines)

def write_buildings_data(state):

    new_building_lines = [
        f'\ts:{state.state_name} = {{\n'
    ]
    
    for ss, buildings in state.buildings.items():
        new_building_lines.append(f'\t\tregion_state:{ss} = {{\n')

        for building in buildings:
            pms = " ".join(['"'+b+'"' for b in building['activate_production_methods']])
            new_building_lines.extend([
                '\t\t\tcreate_building={\n',
                f'\t\t\t\tbuilding="{building["building"]}"\n',
                f'\t\t\t\tlevel={building["level"]}\n',
                '\t\t\t\treserves=1\n',
                f'\t\t\t\tactivate_production_methods={{ {pms} }}\n',
                '\t\t\t}\n'
            ])

        new_building_lines.append('\t\t}\n')
        
    new_building_lines.append('\t}\n')

    edit_block_content(state.buildings_path,state.state_name,new_building_lines)

def write_routes_data(country):

    new_routes_lines = [
        f'\tc:{country.country_tag} = {{\n'
    ]
    
    for route in country.routes:
        if route['level'] > 0:
            direction = 'export'
        elif route['level'] < 0:
            direction = 'import'
        else:
            continue
        level = abs(route['level'])

        new_routes_lines.extend([
            '\t\tcreate_trade_route = {\n',
            f'\t\t\tgoods = {route["goods"]}\n',
            f'\t\t\tlevel = {level}\n',
            f'\t\t\tdirection = {direction}\n',
            f'\t\t\ttarget = c:{route["target"]}.market\n',
            '\t\t}\n'
        ])

    new_routes_lines.append('\t}\n')
    identifier = '\tc:'+country.country_tag

    edit_block_content(country.routes_path,identifier,new_routes_lines)