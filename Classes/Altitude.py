unit = 'km'
low_orbit = 4500
atmosphere = 4000
gutenberg_plane = 0

terrain = gutenberg_plane + 2900
sea_level = terrain + 100

fixed_altitude = {
    'low_orbit': low_orbit,
    'atmosphere': atmosphere,
    'gutenberg_plane': gutenberg_plane
}

default_altitude = {
    'terrain': terrain,
    'sea_level': sea_level
}

