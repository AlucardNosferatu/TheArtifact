extends Node2D

var vehicle_script = load("res://Vehicle.gd")
# 生成载具刚体和碰撞体，填充Root的v_rb和all_thruster
func build(root: Node2D) -> void:
	# 步骤1：创建载具刚体
	#var vehicles:Array[RigidBody2D]=[]
	# 步骤4：初始化推进器参数（从block_types中筛选推进器）
	root.all_thruster.clear()
	var joints: Dictionary = {}
	var joints_pos_str: Array = []
	var pivot_global_position: Vector2 = Vector2.ZERO
	var pivot_vertices_center: Vector2 = Vector2.ZERO
	var base_offset = Vector2.ZERO
	for i in range(root.outer_vertices.size()):
		var rb_vehicle = RigidBody2D.new()
		rb_vehicle.name = "Vehicle_" + str(i)
		rb_vehicle.gravity_scale = 0.0
		rb_vehicle.collision_layer = 1
		rb_vehicle.collision_mask = 1
		var relative_offset = Vector2.ZERO
		var vertices_center = get_bounding_box_center(root.outer_vertices[i])
		if pivot_global_position.length() <= 0:
			rb_vehicle.global_position = Vector2(200.0, 200.0)
			pivot_global_position = rb_vehicle.global_position
			pivot_vertices_center = vertices_center
			base_offset = get_min_xy(root.outer_vertices[i])
		else:
			relative_offset = vertices_center - pivot_vertices_center
			rb_vehicle.global_position = relative_offset + pivot_global_position
		# 步骤2：创建碰撞多边形（基于轮廓顶点）
		var collision_shape = CollisionPolygon2D.new()
		var centered_vertices = []
		for v in root.outer_vertices[i]:
			centered_vertices.append(v - base_offset - relative_offset)
		collision_shape.polygon = centered_vertices
		var area = calculate_polygon_area(collision_shape)
		print(rb_vehicle.name, ' Area:', area)
		rb_vehicle.mass = 0.01 * area # 质量与方块数量成正比
		rb_vehicle.add_child(collision_shape)
			
		# 步骤3：计算中心偏移量（几何中心相对于左上角的偏移）
		var center_offset = _calculate_center_offset(root.outer_vertices[i])
		for pos_str in root.block_types:
			var block_info: String = root.block_types[pos_str]
			var pos_parts = pos_str.split(",")
			if pos_parts.size() != 2:
				continue
			var x = float(pos_parts[0])
			var y = float(pos_parts[1])
			var center_pos = Vector2(x, y)
			if 'JOINT' in block_info or 'RAIL' in block_info:
				#无归属block初始化，还没写，先用pass占个位
				if 'JOINT' in block_info:
					if pos_str not in joints_pos_str:
						var params = block_info.rsplit('###', true)[1].rsplit('#')
						if params[1] not in joints.keys():
							joints[params[1]] = {}
						var global_pos = pivot_global_position + center_pos - base_offset
						var joint_rb = RigidBody2D.new()
						joint_rb.gravity_scale = 0.0
						joint_rb.mass = 0.1
						joint_rb.collision_layer = 1
						joint_rb.collision_mask = 1
						joint_rb.global_position = global_pos
						var small_square_cs = CollisionShape2D.new()
						var small_square_rs = RectangleShape2D.new()
						small_square_rs.size = Vector2(root.BLOCK_SIZE, root.BLOCK_SIZE)
						small_square_cs.shape = small_square_rs
						joint_rb.add_child(small_square_cs)
						root.add_child(joint_rb)
						joints[params[1]]['joint_rb'] = joint_rb
						joints_pos_str.append(pos_str)
			else:
				if is_point_in_polygon(Vector2(x, y), root.outer_vertices[i]):
					if "THRUSTER" in block_info:
					# 解析推进器朝向
						var thruster_face = block_info.right(1)
						if thruster_face not in ["↑", "↓", "←", "→"]:
							print("无效朝向：", thruster_face)
							continue
						# 构建推进器参数（[刚体, 位置, 朝向, 推力, 中心偏移]）
						root.all_thruster.append([
							rb_vehicle,
							center_pos - base_offset - relative_offset,
							thruster_face,
							200.0, # 默认推力
							center_offset
						])
					elif "JBIND" in block_info:
						var params = block_info.rsplit('###', true)[1].rsplit('#')
						if params[1] not in joints.keys():
							joints[params[1]] = {}
						if 'node' not in joints[params[1]].keys():
							joints[params[1]]['node'] = []
						joints[params[1]]['node'].append(rb_vehicle)
		# 步骤6：添加到场景并更新Root引用
		rb_vehicle.set_script(vehicle_script)
		root.add_child(rb_vehicle)
		print("载具生成完成，推进器数量：", root.all_thruster.size())
	for joint_id in joints.keys():
		var params = joints[joint_id]
		var joint_rb = params['joint_rb']
		var node_a = params['node'][0]
		var node_b = params['node'][1]
		var j_p_1 = PinJoint2D.new()
		var j_p_2 = PinJoint2D.new()
		j_p_1.position = Vector2.ZERO
		j_p_2.position = Vector2.ZERO
		j_p_1.node_a = NodePath(joint_rb.get_path())
		j_p_2.node_a = NodePath(joint_rb.get_path())
		j_p_1.node_b = NodePath(node_a.get_path())
		j_p_2.node_b = NodePath(node_b.get_path())
		j_p_1.bias = 0.0
		j_p_2.bias = 0.0
		joint_rb.add_child(j_p_1)
		joint_rb.add_child(j_p_2)
# 射线法：判断点是否在多边形内（局部坐标）
# 参数：point - 待检测点（刚体局部坐标）；polygon - 多边形顶点数组（刚体局部坐标）
# 返回：bool - 点在多边形内返回true，否则false
func is_point_in_polygon(point: Vector2, polygon: Array) -> bool:
	var n = polygon.size()
	if n < 3:
		return false # 无效多边形
	var inside = false
	for i in range(n):
		var j = (i + 1) % n # 下一个顶点索引
		var vi = polygon[i]
		var vj = polygon[j]
		# 检测射线与边的交点
		var vi_y_cond = (vi.y > point.y)
		var vj_y_cond = (vj.y > point.y)
		# 边的两端点在射线两侧（y方向）
		if vi_y_cond != vj_y_cond:
			# 计算交点的x坐标
			var x_intersect = ((point.y - vi.y) * (vj.x - vi.x)) / (vj.y - vi.y) + vi.x
			# 交点在点的右侧，计数+1
			if point.x < x_intersect:
				inside = !inside # 奇数次为内，偶数次为外
	return inside

# 计算多边形外接矩形（轴对齐）的中心点坐标
# 参数：vertices - 顶点数组（支持Vector2、(x,y)元组、[x,y]数组）
# 返回：Vector2 - 外接矩形中心点；顶点为空时返回(0,0)
func get_bounding_box_center(vertices: Array) -> Vector2:
	if vertices.size() <= 0:
		return Vector2.ZERO
	# 初始化最值（取第一个顶点的坐标）
	var min_x = vertices[0].x
	var max_x = min_x
	var min_y = vertices[0].y
	var max_y = min_y
	# 遍历所有顶点，更新最值
	for v in vertices:
		var x = v.x
		var y = v.y
		if x < min_x:
			min_x = x
		if x > max_x:
			max_x = x
		if y < min_y:
			min_y = y
		if y > max_y:
			max_y = y
	# 计算外接矩形中心点（(max+min)/2）
	return Vector2(
		(max_x + min_x) / 2.0,
		(max_y + min_y) / 2.0
	)

# 辅助函数：获取顶点数组的min_x（最左）和min_y（最上）
func get_min_xy(vertices: Array) -> Vector2:
	if vertices.size() <= 0:
		return Vector2.ZERO
	# 初始化min_x和min_y（取第一个顶点）
	var min_x = vertices[0].x
	var min_y = vertices[0].y
	# 遍历所有顶点，找到真正的min_x和min_y
	for v in vertices:
		var x = v.x
		var y = v.y
		if x < min_x:
			min_x = x
		if y < min_y:
			min_y = y
	return Vector2(min_x, min_y)
	
# 计算CollisionPolygon2D的面积
func calculate_polygon_area(polygon: CollisionPolygon2D) -> float:
	var vertices = polygon.polygon # 获取碰撞体的顶点数组（PoolVector2Array类型）
	var n = vertices.size()
	if n < 3:
		return 0.0 # 少于3个顶点无法形成多边形，面积为0
	
	var area_sum = 0.0
	for i in range(n):
		var x_i = vertices[i].x
		var y_i = vertices[i].y
		# 下一个顶点（最后一个顶点的下一个是第一个顶点）
		var x_next = vertices[(i + 1) % n].x
		var y_next = vertices[(i + 1) % n].y
		
		area_sum += (x_i * y_next) - (x_next * y_i)
	
	# 取绝对值的一半，得到最终面积
	return abs(area_sum) * 0.5
# 子函数：计算中心偏移量
func _calculate_center_offset(vertices: Array) -> Vector2:
	if vertices.size() <= 0:
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
