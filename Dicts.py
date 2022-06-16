contain_dict = {
    'huge': ['large', 'medium', 'small'],
    'large': ['medium', 'small'],
    'medium': ['small'],
    'small': [],
}

part_bonus_neighbor = {
    'crane': ['lab', 'factory'],
    'lab': ['command', 'factory'],
    'factory': ['warehouse', 'airport'],
    'command': ['airport', 'radar']
}

part_bonus_radius = {
    'crane': 1,
    'lab': 1,
    'factory': 2,
    'command': 2
}

armed_list = ['gun', 'cannon', 'flame']
scavenger_dict = {
    'drill': ['ore'],
    'TBM': ['ore', 'oil'],
    'saw': ['wood'],
    'pump': ['oil']
}
initial_personnel = {'dorm': 100, 'cabin': 10}
container_list = ['bay', 'hangar']
connector_list = ['dock', 'slide_mount']
