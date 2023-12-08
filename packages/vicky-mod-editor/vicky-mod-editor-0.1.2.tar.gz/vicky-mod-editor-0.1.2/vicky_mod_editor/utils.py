import ClauseWizard 
import colorsys
import re

def parse_cw(path,hsv_changer=False):
    with open(path, 'r', encoding='utf-8-sig') as file:
        data = file.read()
    
    if hsv_changer:
        pattern = r'hsv{\s*(\S+)\s*(\S+)\s*(\S+)\s*}'
        data = re.sub(pattern, lambda x:color_hsv_fixer(x,'hsv'), data)
        pattern = r'hsv360{\s*(\S+)\s*(\S+)\s*(\S+)\s*}'
        data = re.sub(pattern, lambda x:color_hsv_fixer(x,'hsv360'), data)
        
    tokens = ClauseWizard.cwparse(data)
    parsed = ClauseWizard.cwformat(tokens)
    return parsed

def color_hsv_fixer(match,method):
    assert method in ['hsv','hsv360']
    # Extracting values from the matched pattern
    values = match.group(1,2,3)
    
    # Converting the values to floats
    hsv_vals = [float(val) for val in values]
    if method == 'hsv360':
        hsv_vals = [hsv_vals[0]/360,hsv_vals[1]/100,hsv_vals[2]/100]
    
    rgb_vals = [str(int(i*255)) for i in colorsys.hsv_to_rgb(*hsv_vals)]
    rgb_string = ' '.join(rgb_vals)
    
    result = f'{{ {rgb_string} }}'
    return result


def consolidate_pops(pops):
    d = {}
    params = ['culture','religion','pop_type']

    for pop in pops:
        key = tuple(pop.get(param) for param in params)
        d[key] = d.get(key,0) + pop['size']

    consolidated_pops = []
    for i,v in d.items():
        c_pop = {param:x for x,param in zip(i,params) if x}
        c_pop['size'] = v
        consolidated_pops.append(c_pop)

    return consolidated_pops

def consolidate_buildings(buildings):
    d = {}
    params = ['level','reserves','activate_production_methods']
    
    for b in buildings:
        b_type = b['building']
        if b_type in d:
            d[b_type]['level'] += b['level']
        else:
            d[b_type] = {p:b[p] for p in params}
    
    consolidated_buildings = []
    for i,v in d.items():
        c_b = v
        c_b['building'] = i
        consolidated_buildings.append(c_b)

    return consolidated_buildings