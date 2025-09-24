extends Node2D

func _process(_delta: float) -> void:
	if get_tree().root.rotate1 or get_tree().root.rotate2:
		var joints = find_children('PJ_*', '', true, false)
		var j1: PinJoint2D = joints[0]
		var j2: PinJoint2D = joints[1]
		var node_a: RigidBody2D = get_node(j1.node_b)
		var node_b: RigidBody2D = get_node(j2.node_b)
		var vec2a: Vector2 = node_a.global_position - self.global_position
		var vec2b: Vector2 = node_b.global_position - self.global_position
		var force_dir_a = Vector2.ZERO
		var force_dir_b = Vector2.ZERO
		if get_tree().root.rotate1:
			force_dir_a = vec2a.rotated(PI / 2)
			force_dir_b = vec2b.rotated(-PI / 2)
		elif get_tree().root.rotate2:
			force_dir_a = vec2a.rotated(-PI / 2)
			force_dir_b = vec2b.rotated(PI / 2)
		node_a.apply_central_force(force_dir_a * 1)
		node_b.apply_central_force(force_dir_b * 1)
