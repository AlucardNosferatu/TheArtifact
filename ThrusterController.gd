extends Node2D

@onready var root = get_parent() # 父节点是根节点（挂载Root.gd）

func _process(_delta: float) -> void:
	# 处理挂钩拉力
	#print(get_global_mouse_position())
	if root.hooked and root.hooked_rb:
		_apply_hook_force()
	
	# 处理推进器推力
	if root.move and root.all_thruster.size() > 0:
		_apply_thruster_force()
		
	if root.flip:
		root.flip = false
		flip_vehicle()
		
# 翻转整个载具（沿正中间垂线左右翻转）
func flip_vehicle():
	 #1. 获取所有载具部件（Vehicle_和Joint_前缀的RigidBody2D）
	var vehicle_parts = get_all_vehicle_parts()
	if vehicle_parts.size() <= 0:
		print("未找到载具部件")
		return
	var vertices = []
	for part: RigidBody2D in vehicle_parts:
		var part_pos_ul = part.global_position
		var shape = part.find_children('*', 'CollisionPolygon2D', true, false)
		if shape.size() <= 0:
			shape = part.find_children('*', 'CollisionShape2D', true, false)
			if shape.size() <= 0:
				return
			else:
				var width = shape[0].shape.size.x
				var height = shape[0].shape.size.y
				vertices.append(Vector2(width, 0.0) + part_pos_ul)
				vertices.append(Vector2.ZERO + part_pos_ul)
				vertices.append(Vector2(0.0, height) + part_pos_ul)
				vertices.append(shape[0].shape.size + part_pos_ul)
		else:
			for v in shape[0].polygon:
				vertices.append(v + part_pos_ul)
	print(vertices)
	var center_x = calculate_x_midpoint(vertices)
		
	
	# 3. 对每个部件执行左右翻转
	for part in vehicle_parts:
		flip_part_horizontally(part, center_x)
func calculate_x_midpoint(vertices: Array) -> float:
	if vertices.size() <= 0:
		print("数组为空，无法计算")
		return 0.0
	
	# 初始化最大和最小x值
	var xmin = vertices[0].x
	var xmax = vertices[0].x
	
	# 遍历所有顶点，更新最大和最小x
	for vec in vertices:
		if vec.x < xmin:
			xmin = vec.x
		if vec.x > xmax:
			xmax = vec.x
	
	# 计算平均值（中点）
	return (xmin + xmax) / 2.0
	
# 获取所有载具部件
func get_all_vehicle_parts() -> Array:
	var parts = []
	# 递归查找所有符合条件的RigidBody2D
	find_parts_recursive(root, parts)
	return parts

# 递归查找载具部件
func find_parts_recursive(node: Node, parts: Array):
	# 检查当前节点是否是符合条件的RigidBody2D
	for child in node.get_children():
		if child is RigidBody2D:
			var node_name = child.name
			if node_name.begins_with("Vehicle_") or node_name.begins_with("Joint_"):
				parts.append(child)


# 单个部件左右翻转（以center_x为对称轴）
func flip_part_horizontally(part: RigidBody2D, center_x: float):
	var part_width = get_part_width(part)
	if part_width <= 0:
		return
	else:
		# 4. 修正位置映射：左上角 → 对称后的右上角
		var global_pos = part.global_position
		var distance = global_pos.x - center_x # 原左上角到对称轴的距离
		# 新左上角X = 对称轴X - 距离 - 宽度（补偿宽度，实现左上角→右上角映射）
		part.global_position.x = center_x - distance - part_width
		flip_polygon_self(part)
# 翻转polygon自身（用循环替代map）
func flip_polygon_self(part: RigidBody2D):
	var polygon_nodes = part.find_children("*", "CollisionPolygon2D", true, false)
	if polygon_nodes.size() <= 0:
		print("部件 " + part.name + " 未找到CollisionPolygon2D节点")
		return false

	var polygon_node = polygon_nodes[0]
	if polygon_node.polygon.size() <= 0:
		print("部件 " + part.name + " 的碰撞多边形顶点为空")
		return false

	var local_x = []
	for vert in polygon_node.polygon:
		local_x.append(vert.x)

	var poly_min_x = local_x.min()
	var poly_max_x = local_x.max()
	var poly_center_x = (poly_min_x + poly_max_x) / 2

	var mirrored_polygon = PackedVector2Array()
	for vert in polygon_node.polygon:
		var new_x = 2 * poly_center_x - vert.x
		mirrored_polygon.append(Vector2(new_x, vert.y))

	polygon_node.polygon = mirrored_polygon
	print("部件 " + part.name + " 镜像完成，中心X: " + str(poly_center_x))
	return true
	
# 计算刚体碰撞形状的左右宽度（X方向最大跨度）
func get_part_width(part: RigidBody2D) -> float:
	var shape = part.find_children('*', 'CollisionPolygon2D', true, false)
	if shape.size() <= 0:
		shape = part.find_children('*', 'CollisionShape2D', true, false)
		if shape.size() <= 0:
			return -1.0
		else:
			return shape[0].shape.size.x
	else:
		# 对CollisionPolygon2D：局部顶点的X最大差
		var local_x: Array = []
		for vert in shape[0].polygon:
			local_x.append(vert.x)
		return local_x.max() - local_x.min()

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
