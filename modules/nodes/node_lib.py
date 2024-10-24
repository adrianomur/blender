from modules.nodes.constants import SPACING_X, SPACING_Y


def align_nodes(func):
    def wrapper(*args, **kwargs):
        nodes = func(*args, **kwargs)
        for row_index, row in enumerate(nodes):
            for column_index, node in enumerate(row):
                if node:
                    node.location.x = column_index * SPACING_X
                    node.location.y = - row_index * SPACING_Y
        return nodes
    return wrapper
