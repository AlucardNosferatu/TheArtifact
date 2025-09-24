extends Node2D

# ---------------------- 全局共享数据（供其他模块访问） ----------------------
var block_positions: Dictionary = {} # 方块位置（ExcelParser填充）
var block_types: Dictionary = {} # 方块类型（ExcelParser填充）
var outer_edges: Array[Array] = [] # 外边缘（OutlineGenerator填充）
var outer_vertices: Array[Array] = [] # 轮廓顶点（OutlineGenerator填充）
var all_thruster: Array[Array] = [] # 推进器参数（VehicleBuilder填充）
var hooked: bool = false # 挂钩状态（PlayerInput修改）
var hooked_rb: RigidBody2D = null # 被挂钩的刚体（PlayerInput修改）
var move: bool = false # 推进器开关（PlayerInput修改）
var rotate_1: bool = false
var rotate_2: bool = false
# ---------------------- 全局常量（统一管理） ----------------------
const EXCEL_PATH = "res://DESIGN.xlsx"
const BLOCK_SIZE = 20.0
# ---------------------- 模块引用（通过子节点获取） ----------------------
@onready var excel_parser = $ExcelParser # 挂载ExcelParser脚本的子节点
@onready var outline_generator = $OutlineGenerator # 挂载OutlineGenerator的子节点
@onready var vehicle_builder = $VehicleBuilder # 挂载VehicleBuilder的子节点
@onready var player_input = $PlayerInput # 挂载PlayerInput的子节点
@onready var thruster_controller = $ThrusterController # 挂载ThrusterController的子节点

func _ready():
	# 1. Excel解析：填充block_positions/block_types
	excel_parser.parse(EXCEL_PATH, self) # 传入Root引用，让解析器填充数据
	# 2. 轮廓生成：基于方块数据生成outer_edges/outer_vertices
	outline_generator.generate(self, BLOCK_SIZE) # 传入Root引用和方块尺寸
	# 3. 载具生成：基于轮廓顶点生成刚体和推进器
	vehicle_builder.build(self) # 传入Root引用，生成载具并填充all_thruster
