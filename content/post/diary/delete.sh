#!/bin/bash

# 要遍历的目标目录路径
target_directory="./"  # 根据你的项目路径修改

# 遍历目录，处理每个文件
find "$target_directory" -type f -name "*.md" | while read file; do
    # 删除 "hidden: false" 行并保存
    sed -i '/hidden: false/d' "$file"
    echo "更新文件: $file"
done
