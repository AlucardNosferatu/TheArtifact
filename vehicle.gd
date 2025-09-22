extends Node


func _draw():
	for thruster in get_tree().root.get_child(0).all_thruster:
		var rb: RigidBody2D = thruster[0]
		var pos: Vector2 = thruster[1] # 发力点（局部坐标）
		pos.x = pos.x + 20
		var face: String = thruster[2]
		var force: float = thruster[3]
		# 1. 绘制发力点（红色小点）
		rb.draw_circle(pos, 2, Color.RED)
		# 2. 计算力的方向向量（复用之前的方向计算逻辑）
		var angle = rb.global_rotation
		var dir = Vector2.ZERO
		match face:
			'↑': dir = Vector2(cos(angle - PI / 2), sin(angle - PI / 2))
			'→': dir = Vector2(cos(angle), sin(angle))
			'↓': dir = Vector2(cos(angle + PI / 2), sin(angle + PI / 2))
			'←': dir = Vector2(cos(angle + PI), sin(angle + PI))
		# 3. 绘制力的方向（蓝色线段，长度与力大小成正比）
		rb.draw_line(pos, pos + dir * force * 5, Color.BLUE, 2.0) # 0.1是缩放系数，避免线太长
