extends Node2D

# ---------------------- 全局共享数据（供其他模块访问） ----------------------
var block_positions: Dictionary = {} # 方块位置（ExcelParser填充）
var block_types: Dictionary = {} # 方块类型（ExcelParser填充）
var outer_edges: Array[Array] = [] # 外边缘（OutlineGenerator填充）
var outer_vertices: Array = [] # 轮廓顶点（OutlineGenerator填充）
var all_thruster: Array[Array] = [] # 推进器参数（VehicleBuilder填充）
var v_rb: RigidBody2D = null # 载具刚体（VehicleBuilder生成）
var hooked: bool = false # 挂钩状态（PlayerInput修改）
var hooked_rb: RigidBody2D = null # 被挂钩的刚体（PlayerInput修改）
var move: bool = false # 推进器开关（PlayerInput修改）
# ---------------------- 全局常量（统一管理） ----------------------
const EXCEL_PATH = "res://DESIGN.xlsx"
const BLOCK_SIZE = 20.0
# ---------------------- 模块引用（通过子节点获取） ----------------------
@onready var excel_parser = $ExcelParser # 挂载ExcelParser脚本的子节点
@onready var outline_generator = $OutlineGenerator # 挂载OutlineGenerator的子节点
@onready var vehicle_builder = $VehicleBuilder # 挂载VehicleBuilder的子节点

func _ready():
	# 1. Excel解析：填充block_positions/block_types
	excel_parser.parse(EXCEL_PATH, self) # 传入Root引用，让解析器填充数据
	# 2. 轮廓生成：基于方块数据生成outer_edges/outer_vertices
	outline_generator.generate(self, BLOCK_SIZE) # 传入Root引用和方块尺寸
	# 3. 载具生成：基于轮廓顶点生成刚体和推进器
	if outer_vertices.size() >= 3:
		vehicle_builder.build(self) # 传入Root引用，生成载具并填充all_thruster
	else:
		print("顶点数量不足，无法生成载具")


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
