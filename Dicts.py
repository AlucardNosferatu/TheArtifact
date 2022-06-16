contain_dict = {
    'huge': ['large', 'medium', 'small'],
    'large': ['medium', 'small'],
    'medium': ['small'],
    'small': [],
}

part_bonus_neighbor = {
    'crane': ['lab', 'factory'],
    'lab': ['command', 'factory'],
    'factory': ['warehouse', 'hangar']
}

part_bonus_radius = {
    'crane': 2,
    'lab': 1,
    'factory': 2
}
