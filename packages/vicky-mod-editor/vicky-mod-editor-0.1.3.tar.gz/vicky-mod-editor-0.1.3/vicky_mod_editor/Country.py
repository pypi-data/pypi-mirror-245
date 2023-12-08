from .DataWriter import write_routes_data

class Country:
    def __init__(self,country_tag,editor):
        # obligatory data
        self.country_tag = country_tag
        cd = editor.countries_data[country_tag]
        self.color = cd['color']
        self.tier = cd['tier']
        self.cultures = cd['cultures']
        self.capital = cd['capital']

        self.is_named_from_capital = cd.get('is_named_from_capital')
        self.religion = cd.get('religion')
        self.country_type = cd.get('country_type')
        self.valid_as_home_country_for_separatists = cd.get('valid_as_home_country_for_separatists')

        self.routes = editor.routes_data['routes'].get(country_tag,[])

        self.routes_path = editor.routes_data['routes_path']
        
    def add_route(self,target,goods,level):
        assert type(level) == int, 'route level must be integer'
        if level == 0:
            #nothing do do here
            return

        route_found = False
        for route in self.routes:
            if (target,goods) == (route['target'],route['goods']):
                # route exists, just edit the level
                route['level'] += level
                route_found = True
                break

        if not route_found:
            new_route = {
                'goods':goods,
                'level':level,
                'target':target,
            }
            self.routes.append(new_route)
        
        # clean 0 value routes
        self.routes = [route for route in self.routes if route['level'] != 0]
        write_routes_data(self)

    def clear_routes_by_good(self,goods):
        self.routes = [route for route in self.routes if route['goods'] != goods]
        write_routes_data(self)
    
    def clear_routes_by_target(self,target):
        self.routes = [route for route in self.routes if route['target'] != target]
        write_routes_data(self)
    
    def clear_all_routes(self):
        self.routes = []
        write_routes_data(self)
    
    def clear_route(self,target,goods):
        self.routes = [route for route in self.routes if (route['goods'],route['target']) != (goods,target)]
        write_routes_data(self)


