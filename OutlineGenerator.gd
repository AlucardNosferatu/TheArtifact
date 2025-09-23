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
		#if x==130.0 and y==70:
			#print('Catch')
		# 计算方块四个角（中心坐标x,y → 角坐标）
		var c1 = Vector2(x + offset, y - offset) # 右上角
		var c2 = Vector2(x - offset, y - offset) # 左上角
		var c3 = Vector2(x - offset, y + offset) # 左下角
		var c4 = Vector2(x + offset, y + offset) # 右下角
		
		# 获取方块类型，判断是否为SLOPE斜坡块
		var block_info = root.block_types.get(pos_str, "")
		if "SLOPE" in block_info:
			# 提取斜坡方向（格式"###SLOPE#↖"，最后1个字符是方向）
			var slope_dir = block_info.right(1)
			# 根据方向生成等腰直角三角形的3条有效边（直角边与方形边重合）
			match slope_dir:
				"↖": # 斜面朝左上，直角边朝下(c2→c3)、朝右(c2→c1)，斜边c1→c3
					edges.append([c1, c3])
					edges.append([c3, c4])
					edges.append([c4, c1])
				"↗": # 斜面朝右上，直角边朝下(c1→c4)、朝左(c1→c2)，斜边c2→c4
					edges.append([c2, c3])
					edges.append([c3, c4])
					edges.append([c4, c2])
				"↘": # 斜面朝右下，直角边朝上(c4→c1)、朝左(c4→c3)，斜边c1→c3
					edges.append([c1, c2])
					edges.append([c2, c3])
					edges.append([c3, c1])
				"↙": # 斜面朝左下，直角边朝上(c3→c2)、朝右(c3→c4)，斜边c2→c4
					edges.append([c1, c2])
					edges.append([c2, c4])
					edges.append([c4, c1])
				_: # 未知方向，降级为普通方块（避免崩溃）
					print("未知斜坡方向：", slope_dir, "，按普通方块处理")
					_add_normal_block_edges(edges, c1, c2, c3, c4)
		elif "CS" in block_info:
			var params = block_info.rsplit("###", true)[1].rsplit("#", true)
			var slope_dir = params[1]
			var row_count = int(params[2])
			var col_count = int(params[3])
			var row_index = int(params[4])
			var col_index = int(params[5])
			var hypo_y_left = 0
			var hypo_y_right = 0
			var hypo_x_up = 0
			var hypo_x_down = 0
			var local_left_x = (col_index - 1) * block_size
			var local_right_x = col_index * block_size
			var local_up_y = (row_index - 1) * block_size
			var local_down_y = row_index * block_size
			
			var R_x = c4.x - col_index * block_size
			var R_y = c4.y - row_index * block_size
			
			if slope_dir in ['↙', '↗']:
				hypo_y_left = hypo_y1(local_left_x, col_count, row_count) # 左边界x=x_min处的斜边Y
				hypo_y_right = hypo_y1(local_right_x, col_count, row_count) # 右边界x=x_max处的斜边Y
				hypo_x_up = hypo_x1(local_up_y, col_count, row_count) # 左边界x=x_min处的斜边Y
				hypo_x_down = hypo_x1(local_down_y, col_count, row_count) # 右边界x=x_max处的斜边Y
			else:
				hypo_y_left = hypo_y2(local_left_x, col_count, row_count, block_size) # 左边界x=x_min处的斜边Y
				hypo_y_right = hypo_y2(local_right_x, col_count, row_count, block_size) # 右边界x=x_max处的斜边Y
				hypo_x_up = hypo_x2(local_up_y, col_count, row_count, block_size) # 左边界x=x_min处的斜边Y
				hypo_x_down = hypo_x2(local_down_y, col_count, row_count, block_size) # 右边界x=x_max处的斜边Y
			# 穿过判断：格子Y范围与斜边Y值有交集
			var hypo_y_left_inrange = local_down_y >= hypo_y_left and hypo_y_left >= local_up_y
			var hypo_y_right_inrange = local_down_y >= hypo_y_right and hypo_y_right >= local_up_y
			var hypo_x_up_inrange = local_left_x <= hypo_x_up and hypo_x_up <= local_right_x
			var hypo_x_down_inrange = local_left_x <= hypo_x_down and hypo_x_down <= local_right_x
			var crossed = hypo_y_left_inrange or hypo_y_right_inrange or hypo_x_up_inrange or hypo_x_down_inrange
			if not crossed:
				if slope_dir in ['↖', '↗']:
					if local_up_y > hypo_y_right and local_up_y > hypo_y_left:
						# 普通方块：生成4条边
						_add_normal_block_edges(edges, c1, c2, c3, c4)
					else:
						pass
				else:
					if local_up_y > hypo_y_right and local_up_y > hypo_y_left:
						pass
					else:
						# 普通方块：生成4条边
						_add_normal_block_edges(edges, c1, c2, c3, c4)
			else:
				#这部分你来写，注意利用hypo_y_left_inrange、hypo_y_right_inrange、hypo_x_up_inrange、hypo_x_down_inrange
				# 被斜线穿过：根据穿过的边组合生成有效边
				# 1. 计算各边交点坐标（基于斜边方程）
				var p_left = null # 左边界交点 (x=c2.x, y=hypo_y_left)
				if hypo_y_left_inrange:
					p_left = Vector2(c2.x, hypo_y_left + R_y)
				
				var p_right = null # 右边界交点 (x=c1.x, y=hypo_y_right)
				if hypo_y_right_inrange:
					p_right = Vector2(c1.x, hypo_y_right + R_y)
				
				var p_up = null # 上边界交点 (x=hypo_x_up, y=c1.y)
				if hypo_x_up_inrange:
					p_up = Vector2(hypo_x_up + R_x, c1.y)
				
				var p_down = null # 下边界交点 (x=hypo_x_down, y=c4.y)
				if hypo_x_down_inrange:
					p_down = Vector2(hypo_x_down + R_x, c4.y)
				
				# 2. 根据箭头方向和边组合生成有效边
				match slope_dir:
					"↗": # 斜边方向：右下→左上（斜率为正）
						# 组合1：左边界 + 下边界 → 三角形
						if hypo_y_left_inrange and hypo_x_down_inrange:
							edges.append([p_left, c3]) # 左下顶点→左边界交点
							edges.append([c3, p_down]) # 左边界交点→下边界交点
							edges.append([p_down, p_left]) # 下边界交点→右下顶点
						
						# 组合2：上边界 + 右边界 → 五边形
						elif hypo_x_up_inrange and hypo_y_right_inrange:
							edges.append([p_up, c2]) # 左上顶点→上边界交点
							edges.append([c2, c3]) # 上边界交点→右边界交点
							edges.append([c3, c4]) # 右边界交点→右下顶点
							edges.append([c4, p_right]) # 右下顶点→左下顶点
							edges.append([p_right, p_up]) # 左下顶点→左上顶点
						
						# 组合3：上边界 + 下边界 → 梯形
						elif hypo_x_up_inrange and hypo_x_down_inrange:
							edges.append([p_up, c2]) # 左上顶点→上边界交点
							edges.append([c2, c3]) # 上边界交点→下边界交点
							edges.append([c3, p_down]) # 下边界交点→左下顶点
							edges.append([p_down, p_up]) # 左下顶点→左上顶点
						
						# 组合4：左边界 + 右边界 → 梯形
						elif hypo_y_left_inrange and hypo_y_right_inrange:
							edges.append([p_right, p_left]) # 左边界交点→左下顶点
							edges.append([p_left, c3]) # 左下顶点→右下顶点
							edges.append([c3, c4]) # 右下顶点→右边界交点
							edges.append([c4, p_right]) # 右边界交点→左边界交点
					"↖": # 斜边方向：左下→右上（斜率为负）
						# 组合1：左边界 + 下边界 → 三角形
						if hypo_y_right_inrange and hypo_x_down_inrange:
							edges.append([p_right, p_down]) # 左下顶点→左边界交点
							edges.append([p_down, c4]) # 左边界交点→下边界交点
							edges.append([c4, p_right]) # 下边界交点→右下顶点
						
						# 组合2：上边界 + 右边界 → 五边形
						elif hypo_x_up_inrange and hypo_y_left_inrange:
							edges.append([c1, p_up]) # 左上顶点→上边界交点
							edges.append([p_up, p_left]) # 上边界交点→右边界交点
							edges.append([p_left, c3]) # 右边界交点→右下顶点
							edges.append([c3, c4]) # 右下顶点→左下顶点
							edges.append([c4, c1]) # 左下顶点→左上顶点
						
						# 组合3：上边界 + 下边界 → 梯形
						elif hypo_x_up_inrange and hypo_x_down_inrange:
							edges.append([p_up, p_down]) # 左上顶点→上边界交点
							edges.append([p_down, c4]) # 上边界交点→下边界交点
							edges.append([c4, c1]) # 下边界交点→左下顶点
							edges.append([c1, p_up]) # 左下顶点→左上顶点
						
						# 组合4：左边界 + 右边界 → 梯形
						elif hypo_y_left_inrange and hypo_y_right_inrange:
							edges.append([p_right, p_left]) # 左边界交点→左下顶点
							edges.append([p_left, c3]) # 左下顶点→右下顶点
							edges.append([c3, c4]) # 右下顶点→右边界交点
							edges.append([c4, p_right]) # 右边界交点→左边界交点
					"↙": # 斜边方向：左下→右上（斜率为负）
						# 组合1：左边界 + 下边界 → 三角形
						if hypo_y_right_inrange and hypo_x_up_inrange:
							edges.append([c1, p_up]) # 左下顶点→左边界交点
							edges.append([p_up, p_right]) # 左边界交点→下边界交点
							edges.append([p_right, c1]) # 下边界交点→右下顶点
						
						# 组合2：上边界 + 右边界 → 五边形
						elif hypo_x_down_inrange and hypo_y_left_inrange:
							edges.append([c1, c2]) # 左上顶点→上边界交点
							edges.append([c2, p_left]) # 上边界交点→右边界交点
							edges.append([p_left, p_down]) # 右边界交点→右下顶点
							edges.append([p_down, c4]) # 右下顶点→左下顶点
							edges.append([c4, c1]) # 左下顶点→左上顶点
						
						# 组合3：上边界 + 下边界 → 梯形
						elif hypo_x_up_inrange and hypo_x_down_inrange:
							edges.append([c1, p_up]) # 左上顶点→上边界交点
							edges.append([p_up, p_down]) # 上边界交点→下边界交点
							edges.append([p_down, c4]) # 下边界交点→左下顶点
							edges.append([c4, c1]) # 左下顶点→左上顶点
						
						# 组合4：左边界 + 右边界 → 梯形
						elif hypo_y_left_inrange and hypo_y_right_inrange:
							edges.append([c1, c2]) # 左边界交点→左下顶点
							edges.append([c2, p_left]) # 左下顶点→右下顶点
							edges.append([p_left, p_right]) # 右下顶点→右边界交点
							edges.append([p_right, c1]) # 右边界交点→左边界交点
					"↘": # 斜边方向：左下→右上（斜率为负）
						# 组合1：左边界 + 下边界 → 三角形
						if hypo_y_left_inrange and hypo_x_up_inrange:
							edges.append([p_up, c2]) # 左下顶点→左边界交点
							edges.append([c2, p_left]) # 左边界交点→下边界交点
							edges.append([p_left, p_up]) # 下边界交点→右下顶点
						
						# 组合2：上边界 + 右边界 → 五边形
						elif hypo_x_down_inrange and hypo_y_right_inrange:
							edges.append([c1, c2]) # 左上顶点→上边界交点
							edges.append([c2, c3]) # 上边界交点→右边界交点
							edges.append([c3, p_down]) # 右边界交点→右下顶点
							edges.append([p_down, p_right]) # 右下顶点→左下顶点
							edges.append([p_right, c1]) # 左下顶点→左上顶点
						
						# 组合3：上边界 + 下边界 → 梯形
						elif hypo_x_up_inrange and hypo_x_down_inrange:
							edges.append([p_up, c2]) # 左上顶点→上边界交点
							edges.append([c2, c3]) # 上边界交点→下边界交点
							edges.append([c3, p_down]) # 下边界交点→左下顶点
							edges.append([p_down, p_up]) # 左下顶点→左上顶点
						
						# 组合4：左边界 + 右边界 → 梯形
						elif hypo_y_left_inrange and hypo_y_right_inrange:
							edges.append([c1, c2]) # 左边界交点→左下顶点
							edges.append([c2, p_left]) # 左下顶点→右下顶点
							edges.append([p_left, p_right]) # 右下顶点→右边界交点
							edges.append([p_right, c1]) # 右边界交点→左边界交点
					_:
						print("未知斜坡方向：", slope_dir, "，按普通方块处理")
						_add_normal_block_edges(edges, c1, c2, c3, c4)
		elif "JOINT" in block_info:
			pass
		else:
			# 普通方块：生成4条边
			_add_normal_block_edges(edges, c1, c2, c3, c4)
	print('所有边', '\n', edges)
	# 步骤2：边去重（筛选外边缘）
	var tmp: Array[Array] = []
	for edge in edges:
		var e_vec: Vector2 = edge[1] - edge[0]
		if e_vec.length() > 0:
			tmp.append(edge)
	edges = tmp
	root.outer_edges = _filter_outer_edges(edges)
	print('外部边', '\n', root.outer_edges)
	
	# 步骤3：遍历外边缘生成轮廓顶点
	root.outer_vertices = _traverse_edges(root.outer_edges)
	print('顶点', '\n', root.outer_vertices)
func hypo_y1(x, X_total, Y_total): return float(Y_total) / float(X_total) * float(x)
func hypo_x1(y, X_total, Y_total): return float(X_total) / float(Y_total) * float(y)
func hypo_y2(x, X_total, Y_total, block_size):
	return (float(Y_total) * float(block_size)) - (float(Y_total) / float(X_total) * float(x))
func hypo_x2(y, X_total, Y_total, block_size):
	return (float(X_total) * float(block_size)) - (float(X_total) / float(Y_total) * float(y))
# 辅助函数：添加普通方块的4条边
func _add_normal_block_edges(edges: Array, c1: Vector2, c2: Vector2, c3: Vector2, c4: Vector2) -> void:
	edges.append([c1, c2]) # 右上→左上
	edges.append([c2, c3]) # 左上→左下
	edges.append([c3, c4]) # 左下→右下
	edges.append([c4, c1]) # 右下→右上
# 子函数：筛选外边缘（去重）
func _filter_outer_edges(all_edges: Array[Array]) -> Array[Array]:
	var edge_counter: Dictionary = {}
	# 统计边的出现次数
	for edge in all_edges:
		var p1 = edge[0]
		var p2 = edge[1]
		var std_edge = _standardize_edge(p1, p2)
		var edge_key = "{0},{1}|{2},{3}".format([int(std_edge[0].x), int(std_edge[0].y), int(std_edge[1].x), int(std_edge[1].y)])
		edge_counter[edge_key] = edge_counter.get(edge_key, 0) + 1
	
	# 保留只出现一次的边（外边缘）
	var outer_edges: Array[Array] = []
	for edge in all_edges:
		var p1 = edge[0]
		var p2 = edge[1]
		var std_edge = _standardize_edge(p1, p2)
		var edge_key = "{0},{1}|{2},{3}".format([int(std_edge[0].x), int(std_edge[0].y), int(std_edge[1].x), int(std_edge[1].y)])
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
func _traverse_edges(outer_edges: Array[Array]) -> Array:
	if outer_edges.size() <= 0:
		print("警告：外边缘为空")
		return []
		
	# 初始化遍历
	var vertices_groups: Array[Array] = []
	var vertices: Array = []
	
	var remaining_edges = outer_edges.duplicate()
	var start_edge = remaining_edges[randi() % remaining_edges.size()]
	remaining_edges.erase(start_edge)
	var current_point = start_edge[1]
	var start_point = start_edge[0]
	vertices.append(current_point)
	# 遍历匹配边
	var edge_now = null
	while not remaining_edges.size() <= 0:
		var found = false
		for i in range(remaining_edges.size()):
			edge_now = remaining_edges[i]
			if is_point_equal(edge_now[0], current_point):
				current_point = edge_now[1]
			elif is_point_equal(edge_now[1], current_point):
				current_point = edge_now[0]
			else:
				continue
			vertices.append(current_point)
			remaining_edges.remove_at(i)
			found = true
			break
		if not found:
			print("检测到多个独立刚体轮廓")
			# 确保闭合
			if not is_point_equal(vertices[-1], start_point):
				vertices.append(start_point)
			vertices_groups.append(vertices.duplicate())
			vertices.clear()
			start_edge = remaining_edges[randi() % remaining_edges.size()]
			remaining_edges.erase(start_edge)
			current_point = start_edge[1]
			start_point = start_edge[0]
			vertices.append(current_point)
	vertices_groups.append(vertices.duplicate())
	return vertices_groups

# 辅助函数：比较两个点是否相等（处理浮点数精度问题）
func is_point_equal(p1: Vector2, p2: Vector2, epsilon: float = 0.01) -> bool:
	return abs(p1.x - p2.x) < epsilon and abs(p1.y - p2.y) < epsilon
