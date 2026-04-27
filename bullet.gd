extends Area2D

var direction: Vector2 = Vector2.RIGHT
var speed: float = 600.0
var lifetime: float = 1.0

func _ready():
	# 开启监听碰撞
	monitoring = true
	# 连接碰撞信号
	body_entered.connect(_on_body_hit)

func _physics_process(delta):
	global_position += direction * speed * delta

	lifetime -= delta
	if lifetime <= 0:
		queue_free()

# 碰撞触发
func _on_body_hit(hit_body: Node2D):
	# 碰到墙
	if hit_body is StaticBody2D:
		queue_free()

	# 碰到敌人
	elif hit_body is CharacterBody2D and hit_body.name != "Player":
		# 从世界的敌人列表里删掉，防止报错
		get_parent().enemies.erase(hit_body)
		
		hit_body.queue_free()
		queue_free()
