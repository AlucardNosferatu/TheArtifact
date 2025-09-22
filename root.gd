extends Node2D

var hooked=false
var hooked_rb:RigidBody2D=null
var v_rb:RigidBody2D=null
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
		generate_collision_shape(self,sorted_vertices)
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
			Vector2(1, 0),    # 右
			Vector2(0, 1),    # 下
			Vector2(-1, 0),   # 左
			Vector2(0, -1)    # 上
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
func generate_collision_shape(root:Node2D,sorted_vertices: Array) -> void:
	var rigid_body = RigidBody2D.new()
	rigid_body.name = "VehicleRigidBody"
	rb_vehicle = RigidBody2D.new()
	rb_vehicle.name='Vehicle'
	rb_vehicle.gravity_scale=1.0
	rb_vehicle.mass=1.0
	rb_vehicle.collision_layer=1
	rb_vehicle.collision_mask=1
	var collision_shape = CollisionPolygon2D.new()
	collision_shape.polygon = sorted_vertices
	rb_vehicle.add_child(collision_shape)
	rb_vehicle.global_position= Vector2(200.0,200.0)
	root.add_child(rb_vehicle)
	v_rb=rb_vehicle
	print("生成载具碰撞体，顶点数：", sorted_vertices.size())


func _input(event: InputEvent) -> void:
	if event is InputEventMouseButton:
		var event_mb: InputEventMouseButton = event
		if event_mb.pressed:
			var click_pos = get_global_mouse_position()
			if event.button_index==MOUSE_BUTTON_LEFT:
				var rb = RigidBody2D.new()
				rb.gravity_scale=1.0
				rb.mass=1.0
				rb.collision_layer=1
				rb.collision_mask=1
				
				var cs = CollisionShape2D.new()
				var square = RectangleShape2D.new()
				square.size = Vector2(20.0,20.0)
				cs.shape = square
				rb.add_child(cs)
				
				rb.global_position= click_pos
				self.add_child(rb)
			elif event.button_index==MOUSE_BUTTON_RIGHT:
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
							hooked=true
							break
				else:
					hooked_rb=null
					hooked=false
						
								
func _process(_delta: float) -> void:
	if hooked:
		var mouse_pos = get_global_mouse_position()
		var direction = mouse_pos - hooked_rb.global_position
		var distance = direction.length()
		direction = direction/distance
		if distance>20:
			hooked_rb.apply_force(direction*distance*100,Vector2.ZERO)
			hooked_rb.linear_velocity = hooked_rb.linear_velocity.clamp(Vector2(-200.0,-200.0),Vector2(200.0,200.0))
		else:
			hooked_rb.linear_velocity = Vector2.ZERO

var block_size = 20  # 每个方块尺寸为20px
var vertices = []  # 存储多边形顶点
var rb_vehicle: RigidBody2D=null




# 用Dictionary模拟集合（键："x,y"字符串，值：true）
var block_positions: Dictionary = {}
# 存储外部边缘顶点（去重后）
var outer_vertices: Array = []

# 解析JSON数据，记录所有方块的位置（行列转换为坐标）
func parse_block_positions(json_data: Dictionary) -> void:
	# 假设JSON结构：{"行号": {"列号": "TST_BLOCK#"}}
	for row_str in json_data:
		var row = int(row_str)
		var cols = json_data[row_str]
		for col_str in cols:
			var col = int(col_str)
			if cols[col_str] == "TST_BLOCK#→":
				# 转换行列到坐标（原点在左上角，行=Y，列=X）
				var x = (col - 1) * block_size  # 列从1开始，转换为0基准X坐标
				var y = (row - 1) * block_size  # 行从1开始，转换为0基准Y坐标
				# 用字符串拼接替代vstr()
				block_positions[str(x) + "," + str(y)] = true

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
	var seen = {}  # 用Dictionary记录已出现的元素
	for item in arr:
		# 将Vector2转换为字符串作为键（如"x,y"）
		var key = str(item.x) + "," + str(item.y)
		if not seen.has(key):
			seen[key] = true
			unique_arr.append(item)
	return unique_arr
