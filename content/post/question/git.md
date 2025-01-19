---
title: "Git相关"
description: 
date: 2024-11-07T20:56:39+08:00
hidden: false
comments: true
draft: false
tags: ["git","tech"]
---
> origin, main, master, 分别是什么又有什么关系

- **`origin`**：远程仓库的名称（默认远程仓库的别名）。
- **`main`**：现代 Git 项目中用于表示主分支的名称，通常是默认分支。
- **`master`**：旧版本 Git 中的默认主分支名称，已经被很多项目替换为 `main`。

>怎么创建新分支
```
git branch branch-player
git checkout branch-player
git push -u origin branch-player
```
可简化
```
git checkout -b branch-player
git push -u origin branch-player
```
这样创建的新分支是基于当前分支的，即已有commit是当前分支的commit

>怎么撤销已有commit
```
git reset --hard 1e9c6b5fde1cf7512fd6d04ab025a8844dab0e70

git push --force
```
回退到commit前的版本然后强制推送