extends Node2D

@onready var root = get_parent() # 父节点是根节点（挂载Root.gd）

func _process(_delta: float) -> void:
	# 处理挂钩拉力
	if root.hooked and root.hooked_rb:
		_apply_hook_force()
	
	# 处理推进器推力
	if root.move and root.all_thruster.size() > 0:
		_apply_thruster_force()

# 子函数：施加挂钩拉力
func _apply_hook_force() -> void:
	var mouse_pos = get_global_mouse_position()
	var direction = mouse_pos - root.hooked_rb.global_position
	var distance = direction.length()
	
	if distance < 20.0:
		root.hooked_rb.linear_velocity = Vector2.ZERO
		return
	
	# 归一化方向并施加拉力
	direction = direction.normalized()
	var force = direction * distance * 100.0
	root.hooked_rb.apply_force(force, Vector2.ZERO)
	
	# 限制最大速度
	root.hooked_rb.linear_velocity = root.hooked_rb.linear_velocity.clamp(
		Vector2(-200.0, -200.0),
		Vector2(200.0, 200.0)
	)

# 子函数：施加推进器推力
func _apply_thruster_force() -> void:
	for thruster in root.all_thruster:
		var vehicle_rb: RigidBody2D = thruster[0]
		var local_pos: Vector2 = thruster[1] # 推进器局部位置（方块中心）
		var face: String = thruster[2]
		var force_strength: float = thruster[3]
		var center_offset: Vector2 = thruster[4]
		
		# 转换为刚体中心原点的局部坐标
		var rb_local_pos = local_pos - center_offset
		
		# 计算推力方向（随刚体旋转）
		var angle = vehicle_rb.global_rotation
		var dir = Vector2.ZERO
		match face:
			'↑': dir = Vector2(cos(angle - PI / 2), sin(angle - PI / 2))
			'→': dir = Vector2(cos(angle), sin(angle))
			'↓': dir = Vector2(cos(angle + PI / 2), sin(angle + PI / 2))
			'←': dir = Vector2(cos(angle + PI), sin(angle + PI))
		
		# 计算施力点的全局偏移（匹配apply_force的参数要求）
		var global_offset = rb_local_pos.rotated(angle)
		
		# 施加推力
		vehicle_rb.apply_force(dir * force_strength, global_offset)
