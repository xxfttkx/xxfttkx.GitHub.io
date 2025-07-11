---
title: "三种 Canvas 实现方式的比较"
description:
date: 2025-07-11T16:15:15+08:00
comments: true
draft: false
tags: ["canvas", "前端", "图像处理"]
categories: ["技术笔记"]
---

在本篇文章中，我将展示三种不同的 `<canvas>` 图像合成方式，分别是：

1. 普通的 `drawImage` 合成
2. 双 canvas 缩图合成
3. 使用 `createImageBitmap` 的高清缩图合成

它们都绘制相同的图层，但效果有明显差异，主要体现在缩放后是否存在锯齿、模糊等现象。

---

## 1️⃣ custom-canvas：普通 `drawImage`

{{< custom-canvas >}}

这是一种最基础的写法：直接将高清图绘制到 canvas 上，然后再通过 CSS 缩小显示。  
**缺点是容易出现锯齿或模糊。**

---

## 2️⃣ custom-canvas-two：双 canvas 缩图

{{< custom-canvas-two >}}

该方法使用一个隐藏的大 canvas 进行高清绘制，然后再渲染到小 canvas 上，实现**浏览器插值缩放**，效果比第一种更锐利。

---

## 3️⃣ custom-canvas-bitmap：`createImageBitmap` 缩图

{{< custom-canvas-bitmap >}}

这是最推荐的方法，利用 `createImageBitmap()` 内建的高质量缩图插值算法，能在缩放时保留细节、消除锯齿。适合对质量有追求的场景。

---

## ✅ 总结

| 方法                 | 缩放质量 | 性能   | 兼容性           | 推荐指数 |
| -------------------- | -------- | ------ | ---------------- | -------- |
| `drawImage` + 缩 CSS | ❌ 差    | ✅ 快  | ✅ 好            | ⭐       |
| 双 canvas 缩图       | ✅ 好    | ⭘ 一般 | ✅ 好            | ⭐⭐⭐   |
| `createImageBitmap`  | ✅ 极好  | ⭘ 一般 | ✅（现代浏览器） | ⭐⭐⭐⭐ |

---

总之就是插值算法品质的不同，你可以根据浏览器兼容性与性能要求，选择最适合你的方案。
