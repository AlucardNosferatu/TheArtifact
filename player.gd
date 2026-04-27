extends CharacterBody2D

@export var move_speed = 280.0
@export var bullet_speed = 600.0
@export var bullet_lifetime = 1.0

func _physics_process(delta):
	var input = Input.get_vector("left","right","up","down")
	velocity = input * move_speed
	move_and_slide()

func _process(delta):
	if Input.is_action_just_pressed("shoot"):
		_shoot_bullet()

func _shoot_bullet():
	var mouse_world = get_global_mouse_position()
	var dir = (mouse_world - global_position).normalized()

	# 1. 先加载脚本！
	var bullet_script = load("res://bullet.gd")

	# 2. 创建子弹并直接附加脚本
	var bullet = Area2D.new()
	bullet.set_script(bullet_script)
	bullet.name = "Bullet"
	bullet.global_position = global_position

	# 3. 现在赋值 100% 成功！
	bullet.direction = dir
	bullet.speed = bullet_speed
	bullet.lifetime = bullet_lifetime

	# 加入场景
	get_parent().add_child(bullet)

	# 外观
	var sprite = Sprite2D.new()
	sprite.texture = _create_circle_texture(6, Color(1, 0.2, 0.2))
	bullet.add_child(sprite)

	# 碰撞
	var col = CollisionShape2D.new()
	col.shape = CircleShape2D.new()
	col.shape.radius = 4
	bullet.add_child(col)

func _create_circle_texture(size, color):
	var img = Image.create(size, size, false, Image.FORMAT_RGBA8)
	img.fill(Color(0,0,0,0))
	for x in range(size):
		for y in range(size):
			var dx = x - size/2
			var dy = y - size/2
			if dx*dx + dy*dy <= (size/2)*(size/2):
				img.set_pixel(x, y, color)
	return ImageTexture.create_from_image(img)
