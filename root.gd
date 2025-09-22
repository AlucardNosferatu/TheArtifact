extends Node2D

var hooked = false
var hooked_rb: RigidBody2D = null
var v_rb: RigidBody2D = null
const EXCEL_PATH = "res://DESIGN.xlsx"

func _ready():
	var excel = ExcelReader.ExcelFile.open(EXCEL_PATH)
	var workbook = excel.get_workbook()
	var sheet_data = workbook.get_sheet_by_name("Sheet2")
	print(JSON.stringify(sheet_data["data"], "\t"))
	parse_block_positions(sheet_data["data"])
	# 3. 检测外部边缘并收集顶点
	detect_outer_edges()
	generate_outer_vertices()
		# 4. 排序顶点并生成多边形碰撞体
	if outer_vertices.size() >= 3:
		generate_collision_shape(self, outer_vertices)
	else:
		print("顶点数量不足，无法生成多边形")

# 遍历外边缘生成闭合轮廓顶点
func generate_outer_vertices() -> void:
	outer_vertices.clear()
	# 检查外边缘是否为空
	if outer_edges.size() <= 0:
		print("警告：外边缘列表为空，无法生成顶点")
		return
	# 1. 复制外边缘列表（避免修改原始数据）
	var remaining_edges = outer_edges.duplicate()
	# 2. 随机选择起始边
	var start_edge = remaining_edges[randi() % remaining_edges.size()]
	remaining_edges.erase(start_edge) # 从剩余边中移除起始边
	# 3. 初始化遍历变量
	var current_point = start_edge[1] # 起始边的终点作为第一个当前点
	outer_vertices.append(current_point) # 记录第一个顶点（终点）
	var start_point = start_edge[0] # 起始边的起点（用于判断闭合）
	# 4. 遍历所有外边缘形成闭合轮廓
	while not remaining_edges.empty():
		var found = false
		# 查找起点与当前点匹配的边
		for i in range(remaining_edges.size()):
			var edge = remaining_edges[i]
			var edge_start = edge[0]
			var edge_end = edge[1]
			# 浮点数比较需要容错（避免精度问题导致匹配失败）
			if is_point_equal(edge_start, current_point):
				# 找到匹配的边，记录其终点
				current_point = edge_end
				outer_vertices.append(current_point)
				# 移除已处理的边
				remaining_edges.erase_at(i)
				found = true
				break
		# 如果找不到匹配的边，说明轮廓不闭合（处理异常）
		if not found:
			print("警告：未找到匹配的边，轮廓可能不闭合")
			break
	# 5. 检查是否闭合（最后一个点应与起始边的起点重合）
	if outer_vertices.size() > 0 and not is_point_equal(outer_vertices[-1], start_point):
		print("警告：轮廓未闭合，手动补充起始点")
		outer_vertices.append(start_point)

# 辅助函数：比较两个点是否相等（处理浮点数精度问题）
func is_point_equal(p1: Vector2, p2: Vector2, epsilon: float = 0.01) -> bool:
	return abs(p1.x - p2.x) < epsilon and abs(p1.y - p2.y) < epsilon
	
# 生成多边形碰撞体
func generate_collision_shape(root: Node2D, sorted_vertices: Array) -> void:
	var rigid_body = RigidBody2D.new()
	rigid_body.name = "VehicleRigidBody"
	rb_vehicle = RigidBody2D.new()
	rb_vehicle.name = 'Vehicle'
	rb_vehicle.gravity_scale = 0
	rb_vehicle.mass = 1.0 * block_positions.size()
	rb_vehicle.collision_layer = 1
	rb_vehicle.collision_mask = 1
	var collision_shape = CollisionPolygon2D.new()
	collision_shape.polygon = sorted_vertices
	var center_offset = calculate_center_offset(sorted_vertices)
	rb_vehicle.add_child(collision_shape)
	rb_vehicle.global_position = Vector2(200.0, 200.0)
	root.add_child(rb_vehicle)
	v_rb = rb_vehicle
	for pos_str in block_types:
		# 1. 解析位置：从"x,y"字符串转换为Vector2
		var pos_parts = pos_str.split(",") # 分割为["x", "y"]
		if pos_parts.size() != 2:
			continue # 跳过格式错误的键
		var x = pos_parts[0].to_float()
		var y = pos_parts[1].to_float()
		var thruster_pos: Vector2 = Vector2(x, y)
		# 2. 解析朝向：从值字符串中提取最后一个字符（假设朝向是最后一位）
		var block_info = block_types[pos_str]
		if 'THRUSTER' in block_info:
			var thruster_face: String = block_info.right(1) # 取最后一个字符（如"→"）
			# 3. 验证朝向是否合法（仅处理上下左右）
			if thruster_face not in ["↑", "↓", "←", "→"]:
				print("无效的推进器朝向：", thruster_face)
				continue
			# 4. 构建推进器参数并添加到全局列表
			var thruster_params = [
				rb_vehicle, # 载具刚体
				thruster_pos, # 推进器位置
				thruster_face, # 推进器朝向
				200.0, # 默认推力
				center_offset
			]
			all_thruster.append(thruster_params)
	var vehicle_script = load("res://vehicle.gd") # 替换为实际脚本路径
	rb_vehicle.script = vehicle_script # 挂载脚本
	print("生成载具碰撞体，顶点数：", sorted_vertices.size())
	
func calculate_center_offset(sorted_vertices: Array) -> Vector2:
	if sorted_vertices.size() <= 0:
		print("警告：碰撞框顶点为空，返回默认偏移量")
		return Vector2.ZERO
	
	# 1. 找出X轴和Y轴的最小/最大值（确定碰撞框边界）
	var min_x = sorted_vertices[0].x
	var max_x = sorted_vertices[0].x
	var min_y = sorted_vertices[0].y
	var max_y = sorted_vertices[0].y
	
	for vert in sorted_vertices:
		min_x = min(min_x, vert.x)
		max_x = max(max_x, vert.x)
		min_y = min(min_y, vert.y)
		max_y = max(max_y, vert.y)
	
	# 2. 计算碰撞框的宽和高
	var width = max_x - min_x # X方向长度（宽）
	var height = max_y - min_y # Y方向长度（高）
	
	# 3. 计算左上角原点（min_x, min_y）到中心的偏移量
	# 中心坐标 = (min_x + width/2, min_y + height/2)
	# 偏移量 = 中心坐标 - 左上角坐标（min_x, min_y）= (width/2, height/2)
	var center_offset = Vector2(width / 2, height / 2)
	
	return center_offset

var move = false

func _input(event: InputEvent) -> void:
	if event is InputEventMouseButton:
		var event_mb: InputEventMouseButton = event
		if event_mb.pressed:
			var click_pos = get_global_mouse_position()
			if event.button_index == MOUSE_BUTTON_LEFT:
				var rb = RigidBody2D.new()
				rb.gravity_scale = 1.0
				rb.mass = 1.0
				rb.collision_layer = 1
				rb.collision_mask = 1
				
				var cs = CollisionShape2D.new()
				var square = RectangleShape2D.new()
				square.size = Vector2(20.0, 20.0)
				cs.shape = square
				rb.add_child(cs)
				
				rb.global_position = click_pos
				self.add_child(rb)
			elif event.button_index == MOUSE_BUTTON_RIGHT:
				if not hooked:
					var state = get_world_2d().direct_space_state
					var query = PhysicsPointQueryParameters2D.new()
					query.position = click_pos
					query.collision_mask = 1
					var results = state.intersect_point(query)
					for result in results:
						var node = result.get('collider')
						if node is RigidBody2D:
							hooked_rb = node
							print(hooked_rb.name)
							hooked = true
							break
				else:
					hooked_rb = null
					hooked = false
	elif event is InputEventKey:
		var event_kb: InputEventKey = event
		if event_kb.pressed:
			if event_kb.keycode == KEY_SPACE:
				if not move:
					move = true
				else:
					move = false

var all_thruster: Array[Array] = []
			
								
func _process(_delta: float) -> void:
	if hooked:
		var mouse_pos = get_global_mouse_position()
		var direction = mouse_pos - hooked_rb.global_position
		var distance = direction.length()
		direction = direction / distance
		if distance > 20:
			hooked_rb.apply_force(direction * distance * 100, Vector2.ZERO)
			hooked_rb.linear_velocity = hooked_rb.linear_velocity.clamp(Vector2(-200.0, -200.0), Vector2(200.0, 200.0))
		else:
			hooked_rb.linear_velocity = Vector2.ZERO
	if move:
		for thruster_params in all_thruster:
			var vehicle_rb: RigidBody2D = thruster_params[0]
			var pos: Vector2 = thruster_params[1]

			var face: String = thruster_params[2]
			var force: float = thruster_params[3]
			var center_offset: Vector2 = thruster_params[4]
			#face有四种，上下左右，要根据vehicle_rb本身的rotation算出相对方向
			#vehicle_rb.draw_circle(pos, 2, Color.RED)
			# 2. 计算力的方向向量（复用之前的方向计算逻辑）
			var angle = vehicle_rb.global_rotation
			var dir = Vector2.ZERO
			match face:
				'↑': dir = Vector2(cos(angle - PI / 2), sin(angle - PI / 2))
				'→': dir = Vector2(cos(angle), sin(angle))
				'↓': dir = Vector2(cos(angle + PI / 2), sin(angle + PI / 2))
				'←': dir = Vector2(cos(angle + PI), sin(angle + PI))
			# 3. 绘制力的方向（蓝色线段，长度与力大小成正比）
			pos = pos - center_offset
			var global_pos = pos.rotated(vehicle_rb.global_rotation) # 旋转偏移量以匹配实体角度
			print(dir * force, '\t\t', pos)
			vehicle_rb.apply_force(dir * force, global_pos)
			
		
var block_size = 20 # 每个方块尺寸为20px
var rb_vehicle: RigidBody2D = null


# 用Dictionary模拟集合（键："x,y"字符串，值：true）
var block_positions: Dictionary = {}
# 用Dictionary模拟集合（键："x,y"字符串，值："###TAIL#→"）
var block_types: Dictionary = {}
# 存储外部边缘顶点（去重后）
var outer_vertices: Array = []


# 解析JSON数据，记录所有方块的位置（行列转换为坐标）
func parse_block_positions(json_data: Dictionary) -> void:
	# 假设JSON结构：{"行号": {"列号": "###TAIL#→"}}
	for row_str in json_data:
		var row = int(row_str)
		var cols = json_data[row_str]
		for col_str in cols:
			var col = int(col_str)
			if cols[col_str].begins_with("###"):
				# 转换行列到坐标（原点在左上角，行=Y，列=X）
				var x = (col - 0.5) * block_size # 列从1开始，转换为0基准X坐标
				var y = (row - 0.5) * block_size # 行从1开始，转换为0基准Y坐标
				# 用字符串拼接替代vstr()
				block_positions[str(x) + "," + str(y)] = true
				block_types[str(x) + "," + str(y)] = cols[col_str]
				
# 模块的边，每个元素是[起点，终点]
var edges: Array[Array] = []
var outer_edges: Array[Array] = []
func detect_outer_edges() -> void:
	for pos_str in block_positions:
		var pos_str_array = pos_str.split(",")
		var pos = []
		for s in pos_str_array:
			pos.append(int(s))
		var x = float(pos[0])
		var y = float(pos[1])
		#这里的x和y是模块的中心坐标（相对于载具整体的左上角）
		var offset = float(block_size) / 2
		var c1 = Vector2(x + offset, y - offset) # 右上角
		var c2 = Vector2(x - offset, y - offset) # 左上角
		var c3 = Vector2(x - offset, y + offset) # 左下角
		var c4 = Vector2(x + offset, y + offset) # 右下角
		edges.append([c1, c2])
		edges.append([c2, c3])
		edges.append([c3, c4])
		edges.append([c4, c1])
		#剩下的部分你来完成（去重，注意边是双向匹配）
	# 2. 边去重处理（核心逻辑）
	# 用字典统计边的出现次数（键：标准化的边字符串，值：出现次数）
	var edge_counter: Dictionary = {}
	for edge in edges:
		var p1: Vector2 = edge[0]
		var p2: Vector2 = edge[1]
		
		# 标准化边的表示：确保起点 <= 终点（按坐标排序，解决双向匹配问题）
		var std_edge = standardize_edge(p1, p2)
		var standard_p1 = std_edge[0]
		var standard_p2 = std_edge[1]
		
		# 生成唯一键（将Vector2转换为字符串，精确到小数点后2位避免浮点数误差）
		var edge_key: String = "{0},{1}|{2},{3}".format(
			[standard_p1.x, standard_p1.y, standard_p2.x, standard_p2.y]
			)
		# 统计出现次数
		edge_counter[edge_key] = edge_counter.get(edge_key, 0) + 1
	# 3. 筛选外边缘（只出现一次的边）
	for edge in edges:
		var p1: Vector2 = edge[0]
		var p2: Vector2 = edge[1]
		# 标准化边的表示：确保起点 <= 终点（按坐标排序，解决双向匹配问题）
		var std_edge = standardize_edge(p1, p2)
		var standard_p1 = std_edge[0]
		var standard_p2 = std_edge[1]
		# 生成唯一键（将Vector2转换为字符串，精确到小数点后2位避免浮点数误差）
		var edge_key: String = "{0},{1}|{2},{3}".format(
			[standard_p1.x, standard_p1.y, standard_p2.x, standard_p2.y]
			)
		# 只保留出现次数为1的边（外边缘）
		if edge_counter[edge_key] == 1:
			outer_edges.append(edge)
	
# 辅助函数：标准化边的起点和终点顺序（确保p1 <= p2）
func standardize_edge(p1: Vector2, p2: Vector2) -> Array[Vector2]:
	# 排序规则：先比较x坐标，x相等则比较y坐标
	if p1.x < p2.x:
		return [p1, p2]
	elif p1.x > p2.x:
		return [p2, p1]
	else:
		# x相等时比较y坐标
		if p1.y <= p2.y:
			return [p1, p2]
		else:
			return [p2, p1]
