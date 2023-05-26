class ClassBlock:
    """
    砖块类
    """

    def __init__(self, data_file: str) -> None:
        self.block_count = 0
        self.data_file = data_file
        self.map = []
        with open(data_file, 'r', encoding='utf-8') as f:
            layer_temp = f.readlines()
            for line_temp in layer_temp:
                line_list = line_temp.split()
                self.map.append(line_list)
                for block in line_list:
                    if block == '1':
                        self.block_count += 1
    
    def write(self):
        lines = []
        for line in self.map:
            lines.append(' '.join(line) + '\n')
        with open(self.data_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
