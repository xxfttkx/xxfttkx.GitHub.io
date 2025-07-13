---
title: "处理视觉边缘：关于合成 face 与 body 图像的抗争"
date: 2025-07-13T13:12:00+08:00
comments: true
draft: false
tags: ["图像处理", "Pillow", "tlg", "游戏立绘"]
categories: ["技术笔记"]
---

在正负战争的资源中，角色立绘的 face 与 body 被拆分为两个独立的图像文件。理论上，这样可以方便动画表现或换装实现。但当我尝试将两者合并，生成完整立绘时，却遭遇了一个令人意外的障碍：face 图像的边缘总是残留一圈不自然的黑边。

## 问题初现

face 与 body 图像尺寸不同，我手动测量后算好 offset，使用 `Image.alpha_composite(body, face)` 合成。但即使完全对齐，合成结果的交界处仍有一圈黑线。

一开始我以为是 offset 算错、Pillow 渲染有误，或者颜色空间的问题。但在反复调试之后我发现，**这并不是技术细节的错**——是 **视觉边缘** 的锅。

## 调查

我打开 face.png 观察，发现它看起来并没有明显黑边。甚至用 Windows 自带的画图工具查看也正常，毫无违和。然而：

- 将 face 单独显示时，边缘过渡平滑，看起来自然。
- 将 face 贴到 body 上时，边缘出现了明显的黑线。

换句话说，**face 的边缘虽然 alpha 不为 0，但也不等于 255，而是处于某种“过渡灰阶”，造成视觉上的羽化边缘**。这在 face 单独显示时看起来很美观，但在和 body 合成时，就会变成灾难。

## 尝试过的方法

我试过以下几种常见的处理方式：

- `crop_to_alpha_bbox()`：可以裁去多余空白区域，但会**改变图像分辨率**，导致 offset 失效。
- `remove_black_outline()`：通过检测深色像素去边缘，结果**误杀了头发、眼睛的边界线**。
- `feather_alpha()`：希望通过柔化 alpha 通道消除黑边，但结果边缘仍然生硬，甚至**出现了往外“延伸”的伪影像素**。

这让我开始怀疑，**问题可能出在 tlg → png 的转换过程中**。虽然没有确凿证据，但这些边缘像素更像是某种自动处理的遗留痕迹。

## 人工测试：橡皮擦

在万般无奈下，我尝试用画图工具直接擦掉 face 图像的边缘像素，果然，黑边就消失了。于是我想，也许程序上可以实现类似的操作：**把被透明像素包围的边缘像素清除掉**。

## 实现方法 1：清除被透明包围的边缘像素

```python
def clear_hard_edge_by_alpha(img: Image.Image, radius: int = 1) -> Image.Image:
    """
    清除被透明像素包围的边缘不透明像素
    """
    img = img.convert("RGBA")
    data = np.array(img)
    alpha = data[:, :, 3]

    transparent_mask = alpha == 0
    structure = np.ones((3, 3), dtype=bool)
    dilated_transparent = scipy.ndimage.binary_dilation(transparent_mask, structure=structure, iterations=radius)

    opaque_mask = alpha > 0
    border_mask = dilated_transparent & opaque_mask

    data[border_mask, 3] = 0
    return Image.fromarray(data, "RGBA")
```

这个方法模拟“橡皮擦”行为，效果不错。但在查看日志后我发现，有大量像素的 alpha 根本就不是 255，而是 230、120 甚至 10。这些就是黑边的罪魁祸首。

于是我干脆暴力处理。

## 实现方法 2：force_hard_alpha

```
def force_hard_alpha(img: Image.Image) -> Image.Image:
    """
    将所有 alpha 不等于 255 的像素设为完全透明，去除羽化边缘。
    """
    img = img.convert("RGBA")
    data = np.array(img)
    alpha = data[:, :, 3]

    non_hard_alpha_mask = alpha != 255
    data[non_hard_alpha_mask] = [0, 0, 0, 0]

    return Image.fromarray(data, "RGBA")
```

简单粗暴，但效果非常理想。face 的边缘从此干净利落，和 body 合成后不再出现黑边，像素对齐也更加精确。

## 总结

- 问题不在合成逻辑，而是来源图片 alpha 通道中的**灰阶羽化边缘**。
- 原图像的设计是为了在独立展示时更自然，但不适用于合成。
- 解决方法是：**强制移除非 255 的 alpha 像素**，舍弃羽化带来的视觉平滑，换来合成时的干净边界。

### 后记

有时候，自动化处理的边缘润色会变成人工合成的障碍。尤其是在这种「face 和 body 是两个世界」的资源设计中，更需要我们手动打磨中间地带。
