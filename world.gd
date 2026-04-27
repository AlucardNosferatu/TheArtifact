extends Node2D

@export var wall_count = 60
@export var enemy_count = 60
@export var map_range = 1200.0
@export var wall_min_size = 40
@export var wall_max_size = 100

var walls = []
var player_node = null
var enemies = [] # 敌人列表

func _ready():
	randomize()
	player_node = $Player
	
	for i in range(wall_count):
		spawn_wall()

	player_safe_position()

	for i in range(enemy_count):
		spawn_enemy_safe()

func _physics_process(delta):
	# 【核心】所有敌人统一在这里移动，100%全跑
	for enemy in enemies:
		move_enemy(enemy, delta)

func move_enemy(enemy, delta):
	# 🔥 加这一行！如果敌人已经被删了，直接跳过
	if not is_instance_valid(enemy):
		return

	if not player_node:
		return

	var dir_to_player = (player_node.global_position - enemy.global_position).normalized()
	var dist = enemy.global_position.distance_to(player_node.global_position)

	var ray = enemy.get_node("RayCast2D")
	ray.global_rotation = dir_to_player.angle()
	ray.force_raycast_update()
	var wall_blocked = ray.is_colliding()

	var flee_speed = 180.0
	var detect_range = 300.0

	enemy.velocity = Vector2.ZERO
	if not wall_blocked and dist < detect_range:
		enemy.velocity = -dir_to_player * flee_speed

	enemy.move_and_slide()

func spawn_wall():
	var x = randf_range(-map_range, map_range)
	var y = randf_range(-map_range, map_range)
	var w = randf_range(wall_min_size, wall_max_size)
	var h = randf_range(wall_min_size, wall_max_size)

	var wall = StaticBody2D.new()
	wall.global_position = Vector2(x, y)
	add_child(wall)
	walls.append(wall)

	var s = Sprite2D.new()
	var img = Image.create(int(w), int(h), false, Image.FORMAT_RGBA8)
	img.fill(Color(0.1, 0.1, 0.1))
	var tex = ImageTexture.create_from_image(img)
	s.texture = tex
	wall.add_child(s)

	var col = CollisionShape2D.new()
	var shape = RectangleShape2D.new()
	shape.size = Vector2(w, h)
	col.shape = shape
	wall.add_child(col)

func player_safe_position():
	var pos: Vector2
	var safe = false
	for _i in 100:
		pos = Vector2(
			randf_range(-map_range, map_range),
			randf_range(-map_range, map_range)
		)
		var ok = true
		for w in walls:
			var dist = pos.distance_to(w.global_position)
			if dist < 120:
				ok = false
				break
		if ok:
			safe = true
			break
	if safe:
		$Player.global_position = pos

func spawn_enemy_safe():
	var pos: Vector2
	var safe = false
	for _i in 100:
		pos = Vector2(
			randf_range(-map_range, map_range),
			randf_range(-map_range, map_range)
		)
		var ok = true
		for w in walls:
			var dist = pos.distance_to(w.global_position)
			if dist < 120:
				ok = false
				break
		if ok:
			safe = true
			break
	if not safe:
		pos = Vector2.ZERO

	var enemy = CharacterBody2D.new()
	enemy.global_position = pos
	add_child(enemy)
	enemies.append(enemy) # 加入列表

	var sprite = Sprite2D.new()
	sprite.texture = load("res://minotaur-svgrepo-com.svg")
	sprite.scale = Vector2(0.031, 0.031)
	enemy.add_child(sprite)

	var col = CollisionShape2D.new()
	var circle = CircleShape2D.new()
	circle.radius = 12
	col.shape = circle
	enemy.add_child(col)

	var ray = RayCast2D.new()
	ray.name = "RayCast2D"
	ray.target_position = Vector2(300, 0)
	ray.enabled = true
	ray.collision_mask = 1
	enemy.add_child(ray)
