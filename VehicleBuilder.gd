extends Node2D

# 生成载具刚体和碰撞体，填充Root的v_rb和all_thruster
func build(root: Node2D) -> void:
	# 步骤1：创建载具刚体
	var rb_vehicle = RigidBody2D.new()
	rb_vehicle.name = "Vehicle"
	rb_vehicle.gravity_scale = 0.0
	rb_vehicle.mass = 1.0 * root.block_positions.size()  # 质量与方块数量成正比
	rb_vehicle.collision_layer = 1
	rb_vehicle.collision_mask = 1
	rb_vehicle.global_position = Vector2(200.0, 200.0)
	
	# 步骤2：创建碰撞多边形（基于轮廓顶点）
	var collision_shape = CollisionPolygon2D.new()
	collision_shape.polygon = root.outer_vertices
	rb_vehicle.add_child(collision_shape)
	
	# 步骤3：计算中心偏移量（几何中心相对于左上角的偏移）
	var center_offset = _calculate_center_offset(root.outer_vertices)
	
	# 步骤4：初始化推进器参数（从block_types中筛选推进器）
	root.all_thruster.clear()
	for pos_str in root.block_types:
		var block_info = root.block_types[pos_str]
		if "THRUSTER" not in block_info:
			continue  # 只处理推进器方块
		
		# 解析推进器位置
		var pos_parts = pos_str.split(",")
		if pos_parts.size() != 2:
			continue
		var x = float(pos_parts[0])
		var y = float(pos_parts[1])
		var thruster_pos = Vector2(x, y)
		
		# 解析推进器朝向
		var thruster_face = block_info.right(1)
		if thruster_face not in ["↑", "↓", "←", "→"]:
			print("无效朝向：", thruster_face)
			continue
		
		# 构建推进器参数（[刚体, 位置, 朝向, 推力, 中心偏移]）
		root.all_thruster.append([
			rb_vehicle,
			thruster_pos,
			thruster_face,
			200.0,  # 默认推力
			center_offset
		])
	
	# 步骤5：挂载载具脚本（如果有）
	var vehicle_script = load("res://vehicle.gd")
	if vehicle_script:
		rb_vehicle.script = vehicle_script
	
	# 步骤6：添加到场景并更新Root引用
	root.add_child(rb_vehicle)
	root.v_rb = rb_vehicle
	print("载具生成完成，推进器数量：", root.all_thruster.size())

# 子函数：计算中心偏移量
func _calculate_center_offset(vertices: Array) -> Vector2:
	if vertices.size()<=0:
		return Vector2.ZERO
	
	var min_x = vertices[0].x
	var max_x = vertices[0].x
	var min_y = vertices[0].y
	var max_y = vertices[0].y
	
	for vert in vertices:
		min_x = min(min_x, vert.x)
		max_x = max(max_x, vert.x)
		min_y = min(min_y, vert.y)
		max_y = max(max_y, vert.y)
	
	var width = max_x - min_x
	var height = max_y - min_y
	return Vector2(width / 2.0, height / 2.0)
