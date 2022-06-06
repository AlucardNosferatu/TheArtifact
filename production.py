import xlrd

from designs import Design


def read_pipeline_from_xls(filename):
    workbook = xlrd.open_workbook(filename=filename)
    table: xlrd.sheet.Sheet = workbook.sheets()[0]
    size = table.name.split('-')
    size = [int(item) for item in size]
    wid, hei = size
    p = Pipeline(wid, hei)
    for i in range(wid):
        for j in range(hei):
            cell_str = table.cell_value(j, i)
            if cell_str != '':
                if cell_str in Pipeline.conv_dict:
                    src_xy = Pipeline.conv_dict[cell_str][0]
                    dst_xy = Pipeline.conv_dict[cell_str][1]
                    p.set_block(
                        i,
                        j,
                        {'type': 'conv', 'src_xy': src_xy, 'dst_xy': dst_xy}
                    )
                else:
                    params = cell_str.split(':')
                    type_str = params.pop(0)
                    p.set_block(
                        i,
                        j,
                        {'type': type_str, 'params': params}
                    )
    return p


def upper_cell(x, y):
    return x, y - 1


def lower_cell(x, y):
    return x, y + 1


def left_cell(x, y):
    return x - 1, y


def right_cell(x, y):
    return x + 1, y


class Pipeline:
    width = None
    height = None
    matrix = None
    requirement = None
    conv_dict = {
        '↑': [lower_cell, upper_cell],
        '↓': [upper_cell, lower_cell],
        '←': [right_cell, left_cell],
        '→': [left_cell, right_cell],

        '↑→': [lower_cell, right_cell],
        '↓←': [right_cell, lower_cell],
        '→↓': [left_cell, lower_cell],
        '←↑': [lower_cell, left_cell],

        '↑←': [right_cell, upper_cell],
        '↓→': [upper_cell, right_cell],
        '←↓': [upper_cell, left_cell],
        '→↑': [left_cell, upper_cell]
    }

    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.matrix = []
        for r_index in range(h):
            row = []
            for c_index in range(self.width):
                row.append(None)
            self.matrix.append(row)

    def set_requirement(self, design: Design):
        self.requirement = design

    def set_block(self, x, y, block_dict):
        self.matrix[y][x] = block_dict

    def update_graph
if __name__ == '__main__':
    pipe = read_pipeline_from_xls('pipeline.xls')
    print('Done')
