import os

input_directory = "."  # 输入目录路径
output_directory = "xy"  # 输出目录路径

# 确保输出目录存在
os.makedirs(output_directory, exist_ok=True)

# 遍历目录中的.dat文件
for filename in os.listdir(input_directory):
    if filename.endswith(".dat"):
        input_filepath = os.path.join(input_directory, filename)
        output_filepath = os.path.join(output_directory, os.path.splitext(filename)[0] + ".txt")

        # 读取.dat文件内容并提取数据
        with open(input_filepath, 'r') as input_file:
            lines = input_file.readlines()

        data = []
        for line in lines:
            if line.strip().startswith('#') or line.strip() == '':
                continue
            values = line.split()
            if len(values) >= 2:
                try:
                    th_deg = float(values[0])
                    intensity = float(values[1])
                    data.append((th_deg, intensity))
                except ValueError:
                    pass

        # 将数据保存为.txt文件
        with open(output_filepath, 'w') as output_file:
            for point in data:
                output_file.write(f"{point[0]}\t{point[1]}\n")

        os.rename(output_filepath, os.path.splitext(output_filepath)[0] + ".xy")