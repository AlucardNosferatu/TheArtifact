extends RigidBody2D

func _ready():
	contact_monitor = true
	max_contacts_reported = 10


func _draw():
	for thruster in get_tree().root.get_child(0).all_thruster:
		var rb: RigidBody2D = thruster[0]
		if rb == self:
			var pos: Vector2 = thruster[1] # 发力点（局部坐标）
			var face: String = thruster[2]
			var force: float = thruster[3]
			# 1. 绘制发力点（红色小点）
			draw_circle(pos, 2, Color.RED)
			# 2. 计算力的方向向量（复用之前的方向计算逻辑） 
			var angle = rb.global_rotation
			var dir = Vector2.ZERO
			match face:
				'↑': dir = Vector2(cos(angle - PI / 2), sin(angle - PI / 2))
				'→': dir = Vector2(cos(angle), sin(angle))
				'↓': dir = Vector2(cos(angle + PI / 2), sin(angle + PI / 2))
				'←': dir = Vector2(cos(angle + PI), sin(angle + PI))
			# 3. 绘制力的方向（蓝色线段，长度与力大小成正比）
			draw_line(pos, pos + dir * force * 5, Color.BLUE, 2.0) # 0.1是缩放系数，避免线太长

func _integrate_forces(state: PhysicsDirectBodyState2D) -> void:
	var cc = state.get_contact_count()
	if cc > 0:
		for i in range(cc):
			var normal_vec = state.get_contact_local_normal(i)
			var body = state.get_contact_collider_object(i)
			if body is RigidBody2D:
				var bullet_vec: Vector2 = state.get_contact_collider_velocity_at_position(i)
				var incident_ang = 90.0 - abs(rad_to_deg(normal_vec.angle_to(bullet_vec)))
				print(incident_ang)
