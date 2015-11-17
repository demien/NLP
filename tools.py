def get_column_index(column):
    columns = _get_A_to_Z()
    columns += ['A'+i for i in _get_A_to_Z()]
    columns += ['B'+i for i in _get_A_to_Z(22)]
    return columns.index(column)


def _get_A_to_Z(n=26):
    return [unichr(i) for i in range(65, 65+n)]


if __name__ == '__main__':
    print get_column_index('O')
