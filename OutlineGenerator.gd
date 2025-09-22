extends Node2D

# 生成外边缘和轮廓顶点，填充Root的outer_edges和outer_vertices
func generate(root: Node2D, block_size: float) -> void:
	# 步骤1：生成所有方块的边
	var edges: Array[Array] = []
	for pos_str in root.block_positions:
		var pos_parts = pos_str.split(",")
		var x = float(pos_parts[0])
		var y = float(pos_parts[1])
		var offset = block_size / 2.0
		
		# 计算方块四个角（中心坐标x,y → 角坐标）
		var c1 = Vector2(x + offset, y - offset)  # 右上角
		var c2 = Vector2(x - offset, y - offset)  # 左上角
		var c3 = Vector2(x - offset, y + offset)  # 左下角
		var c4 = Vector2(x + offset, y + offset)  # 右下角
		
		edges.append([c1, c2])
		edges.append([c2, c3])
		edges.append([c3, c4])
		edges.append([c4, c1])
	
	# 步骤2：边去重（筛选外边缘）
	root.outer_edges = _filter_outer_edges(edges)
	
	# 步骤3：遍历外边缘生成轮廓顶点
	root.outer_vertices = _traverse_edges(root.outer_edges, root)
	print("轮廓生成完成，顶点数：", root.outer_vertices.size())

# 子函数：筛选外边缘（去重）
func _filter_outer_edges(all_edges: Array[Array]) -> Array[Array]:
	var edge_counter: Dictionary = {}
	# 统计边的出现次数
	for edge in all_edges:
		var p1 = edge[0]
		var p2 = edge[1]
		var std_edge = _standardize_edge(p1, p2)
		var edge_key = "{0},{1}|{2},{3}".format([std_edge[0].x, std_edge[0].y, std_edge[1].x, std_edge[1].y])
		edge_counter[edge_key] = edge_counter.get(edge_key, 0) + 1
	
	# 保留只出现一次的边（外边缘）
	var outer_edges: Array[Array] = []
	for edge in all_edges:
		var p1 = edge[0]
		var p2 = edge[1]
		var std_edge = _standardize_edge(p1, p2)
		var edge_key = "{0},{1}|{2},{3}".format([std_edge[0].x, std_edge[0].y, std_edge[1].x, std_edge[1].y])
		if edge_counter[edge_key] == 1:
			outer_edges.append(edge)
	return outer_edges

# 子函数：标准化边（解决双向匹配）
func _standardize_edge(p1: Vector2, p2: Vector2) -> Array[Vector2]:
	# 排序规则：先比较x坐标，x相等则比较y坐标
	if p1.x < p2.x:
		return [p1, p2]
	elif p1.x > p2.x:
		return [p2, p1]
	else:
		# x相等时比较y坐标，明确返回Array[Vector2]
		if p1.y <= p2.y:
			return [p1 as Vector2, p2 as Vector2]
		else:
			return [p2 as Vector2, p1 as Vector2]

# 子函数：遍历边生成轮廓顶点
func _traverse_edges(outer_edges: Array[Array], root: Node2D) -> Array:
	if outer_edges.size()<=0:
		print("警告：外边缘为空")
		return []
	
	var remaining_edges = outer_edges.duplicate()
	var start_edge = remaining_edges[randi() % remaining_edges.size()]
	remaining_edges.erase(start_edge)
	
	# 初始化遍历
	var current_point = start_edge[1]
	var vertices = [current_point]
	var start_point = start_edge[0]
	
	# 遍历匹配边
	while not remaining_edges.size()<=0:
		var found = false
		for i in range(remaining_edges.size()):
			var edge = remaining_edges[i]
			if is_point_equal(edge[0], current_point):
				current_point = edge[1]
				vertices.append(current_point)
				remaining_edges.remove_at(i)
				found = true
				break
		if not found:
			print("警告：轮廓未闭合")
			break
	
	# 确保闭合
	if not is_point_equal(vertices[-1], start_point):
		vertices.append(start_point)
	return vertices

# 辅助函数：比较两个点是否相等（处理浮点数精度问题）
func is_point_equal(p1: Vector2, p2: Vector2, epsilon: float = 0.01) -> bool:
	return abs(p1.x - p2.x) < epsilon and abs(p1.y - p2.y) < epsilon
