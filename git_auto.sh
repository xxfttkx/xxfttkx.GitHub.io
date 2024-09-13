#!/bin/bash
# 自动执行 Git add, commit, push

# 检查是否传入了提交信息
if [ -z "$1" ]; then
  echo "Error: No commit message provided."
  echo "Usage: ./git_auto.sh \"your commit message\""
  exit 1
fi

# 进行 Git 操作
git add .
git commit -m "$1"
git push