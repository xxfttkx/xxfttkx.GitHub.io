# 定义路径和数量
path = "free"
num_images = 32
suffix = "jpg"

# 打开文件并写入内容
with open("figures.txt", "w") as file:
    for i in range(1, num_images + 1):
        figure_text = f'{{{{< figure src="/{path}/{i}.{suffix}" title="" caption="" >}}}}\n'
        file.write(figure_text)

print("figures.txt 文件生成成功！")
