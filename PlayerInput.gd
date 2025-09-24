extends Node2D

@onready var root = get_parent()  # 父节点是根节点（挂载Root.gd）

func _input(event: InputEvent) -> void:
	# 处理鼠标点击（生成物体、挂钩）
	if event is InputEventMouseButton:
		if not event.pressed:
			return
		var click_pos = get_global_mouse_position()
		
		# 左键：生成小方块刚体
		if event.button_index == MOUSE_BUTTON_LEFT:
			_spawn_small_rigidbody(click_pos)
		
		# 右键：挂钩/取消挂钩
		elif event.button_index == MOUSE_BUTTON_RIGHT:
			if not root.hooked:
				_hook_rigidbody(click_pos)
			else:
				root.hooked = false
				root.hooked_rb = null
	
	# 处理键盘输入（推进器开关）
	elif event is InputEventKey:
		if event.pressed:
			if event.keycode == KEY_SPACE:
				root.move = not root.move
				if root.move:
					print('move now!')
				else:
					print('stop!')
			elif event.keycode == KEY_Q:
				root.rotate_1 = not root.rotate_1
				root.rotate_2 = not root.rotate_1
				if root.rotate_1:
					print('rotate 1!')
				else:
					print('stop!')
			elif event.keycode == KEY_E:
				root.rotate_2 = not root.rotate_2
				root.rotate_1 = not root.rotate_2
				if root.rotate_1:
					print('rotate 2!')
				else:
					print('stop!')
			elif event.keycode == KEY_W:
				root.rotate_1 = false
				root.rotate_2 = root.rotate_1
				print('stop!')
# 子函数：生成小方块刚体
func _spawn_small_rigidbody(spawn_pos: Vector2) -> void:
	var rb = RigidBody2D.new()
	rb.name = "SmallBlock"
	rb.gravity_scale = 1.0
	rb.mass = 1.0
	rb.collision_layer = 1
	rb.collision_mask = 1
	
	# 添加碰撞形状
	var cs = CollisionShape2D.new()
	var square = RectangleShape2D.new()
	square.size = Vector2(20.0, 20.0)
	cs.shape = square
	rb.add_child(cs)
	
	rb.global_position = spawn_pos
	root.add_child(rb)

# 子函数：挂钩刚体
func _hook_rigidbody(click_pos: Vector2) -> void:
	var space_state = get_world_2d().direct_space_state
	var query = PhysicsPointQueryParameters2D.new()
	query.position = click_pos
	query.collision_mask = 1
	var results = space_state.intersect_point(query)
	
	for result in results:
		var collider = result.get("collider")
		if collider is RigidBody2D:
			root.hooked_rb = collider
			root.hooked = true
			print("挂钩：", collider.name)
			break
