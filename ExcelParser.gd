extends Node2D

# 接收Root引用，解析Excel后填充Root的block_positions和block_types
func parse(excel_path: String, root: Node2D) -> void:
	var excel = ExcelReader.ExcelFile.open(excel_path)
	var workbook = excel.get_workbook()
	var sheet_data = workbook.get_sheet_by_name("Sheet2")
	print(JSON.stringify(sheet_data["data"], "\t"))
	
	# 解析行列数据，转换为方块坐标
	for row_str in sheet_data["data"]:
		var row = int(row_str)
		var cols = sheet_data["data"][row_str]
		for col_str in cols:
			var col = int(col_str)
			var block_info = cols[col_str]
			if block_info.begins_with("###"):
				# 行列转坐标（原点左上角，中心坐标 = (列-0.5)*方块尺寸）
				var x = (col - 0.5) * root.BLOCK_SIZE
				var y = (row - 0.5) * root.BLOCK_SIZE
				var pos_key = str(x) + "," + str(y)
				root.block_positions[pos_key] = true
				root.block_types[pos_key] = block_info
	print("Excel解析完成，共", root.block_positions.size(), "个方块")
