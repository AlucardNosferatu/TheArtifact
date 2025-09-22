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
		# 4. 排序顶点并生成多边形碰撞体
	if outer_vertices.size() >= 3:
		var sorted_vertices = sort_vertices()
		generate_collision_shape(self, sorted_vertices)
		# 生成可视化方块（可选）
	else:
		print("顶点数量不足，无法生成多边形")


# 对顶点进行排序（按顺时针方向排列，确保多边形闭合）
func sort_vertices() -> Array:
	if outer_vertices.size() < 3:
		return []
	# 步骤1：找到最左侧的顶点（起始点）
	var start_vertex = outer_vertices[0]
	for v in outer_vertices:
		if v.x < start_vertex.x or (v.x == start_vertex.x and v.y < start_vertex.y):
			start_vertex = v
	# 步骤2：按顺时针顺序遍历相邻顶点
	var sorted = []
	var current = start_vertex
	var visited = {}
	while current != null and not visited.has(str(current.x) + "," + str(current.y)):
		sorted.append(current)
		visited[str(current.x) + "," + str(current.y)] = true
		# 寻找下一个相邻顶点（优先向右，其次向下、向左、向上）
		var next_vertex = null
		var directions = [
			Vector2(1, 0), # 右
			Vector2(0, 1), # 下
			Vector2(-1, 0), # 左
			Vector2(0, -1) # 上
		]
		for dir in directions:
			var candidate = current + dir * block_size
			for v in outer_vertices:
				if v.distance_to(candidate) < 1e-6 and not visited.has(str(v.x) + "," + str(v.y)):
					next_vertex = v
					break
			if next_vertex:
				break
		current = next_vertex
	return sorted

# 生成多边形碰撞体
func generate_collision_shape(root: Node2D, sorted_vertices: Array) -> void:
	var rigid_body = RigidBody2D.new()
	rigid_body.name = "VehicleRigidBody"
	rb_vehicle = RigidBody2D.new()
	rb_vehicle.name = 'Vehicle'
	rb_vehicle.gravity_scale = 0
	rb_vehicle.mass = 1.0
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
		var x = pos_parts[0].to_float() - 10
		var y = pos_parts[1].to_float() + 10
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
				100.0, # 默认推力
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
var vertices = [] # 存储多边形顶点
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
				var x = (col - 1) * block_size # 列从1开始，转换为0基准X坐标
				var y = (row - 1) * block_size # 行从1开始，转换为0基准Y坐标
				# 用字符串拼接替代vstr()
				block_positions[str(x) + "," + str(y)] = true
				block_types[str(x) + "," + str(y)] = cols[col_str]

func detect_outer_edges() -> void:
	for pos_str in block_positions:
		var pos_str_array = pos_str.split(",")
		var pos = []
		for s in pos_str_array:
			pos.append(int(s))
		var x = pos[0]
		var y = pos[1]
		
		# 定义当前方块的四条边和四个角落的位置检测键
		var edges = {
			"top": str(x) + "," + str(y - block_size),
			"bottom": str(x) + "," + str(y + block_size),
			"left": str(x - block_size) + "," + str(y),
			"right": str(x + block_size) + "," + str(y)
		}
		var corners = {
			"top_right": str(x + block_size) + "," + str(y),
			"bottom_right": str(x + block_size) + "," + str(y + block_size),
			"bottom_left": str(x) + "," + str(y + block_size),
			"top_left": str(x) + "," + str(y)
		}
		
		# 检测上边是否为外部边
		if not block_positions.has(edges["top"]):
			outer_vertices.append(Vector2(x, y))
			outer_vertices.append(Vector2(x + block_size, y))
		
		# 检测下边是否为外部边
		if not block_positions.has(edges["bottom"]):
			outer_vertices.append(Vector2(x, y + block_size))
			outer_vertices.append(Vector2(x + block_size, y + block_size))
		
		# 检测左边是否为外部边
		if not block_positions.has(edges["left"]):
			outer_vertices.append(Vector2(x, y))
			outer_vertices.append(Vector2(x, y + block_size))
		
		# 检测右边是否为外部边
		if not block_positions.has(edges["right"]):
			outer_vertices.append(Vector2(x + block_size, y))
			outer_vertices.append(Vector2(x + block_size, y + block_size))
		
		# 检测四个角落是否为外部顶点（无相邻方块时添加）
		if not block_positions.has(corners["top_right"]):
			outer_vertices.append(Vector2(x + block_size, y))
		if not block_positions.has(corners["bottom_right"]):
			outer_vertices.append(Vector2(x + block_size, y + block_size))
		if not block_positions.has(corners["bottom_left"]):
			outer_vertices.append(Vector2(x, y + block_size))
		if not block_positions.has(corners["top_left"]):
			outer_vertices.append(Vector2(x, y))
	
	# 去重顶点
	outer_vertices = array_unique(outer_vertices)

# 自定义数组去重方法（针对Vector2类型）
func array_unique(arr: Array) -> Array:
	var unique_arr = []
	var seen = {} # 用Dictionary记录已出现的元素
	for item in arr:
		# 将Vector2转换为字符串作为键（如"x,y"）
		var key = str(item.x) + "," + str(item.y)
		if not seen.has(key):
			seen[key] = true
			unique_arr.append(item)
	return unique_arr
