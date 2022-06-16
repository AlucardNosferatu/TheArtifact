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
max_range = {'gun': 50, 'cannon': 100, 'flame': 25}
rof = {'gun': 50, 'cannon': 25, 'flame': 100}
damage = {'gun': 25, 'cannon': 50, 'flame': 100}
acc = {'gun': 50, 'cannon': 25, 'flame': 0}
# example:
# flame: range=25-0 acc=0-100
# gun: range=50-0 acc=50-100
scavenger_dict = {
    'drill': ['ore'],
    'TBM': ['ore', 'oil'],
    'saw': ['wood'],
    'pump': ['oil']
}
scavenger_perf = {
    'drill': [100, 5],
    'TBM': [100, 10],
    'saw': [200, 2],
    'pump': [200, 10]
}
initial_garrison = {'dorm': 100, 'cabin': 10}
garrison_firepower = {'dorm': 100, 'cabin': 10}
container_list = ['bay', 'hangar']
connector_list = ['dock', 'slide_mount']

hp = {
    'command': 2000,
    'thruster': 20,
    'wing': 20,
    'ctrl_surface': 20,
    'drill': 20
}
mass = {
    'command': 2000,
    'thruster': 20,
    'wing': 20,
    'ctrl_surface': 20,
    'drill': 20
}
