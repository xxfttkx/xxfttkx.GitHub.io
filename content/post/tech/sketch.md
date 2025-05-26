---
title: "Sketch"
description: 
date: 2025-05-26T19:32:03+08:00
comments: true
draft: false
tags: ["anime"]
categories: ["anime"]
image: "/tech/sketch/input.jpg"
---
## 引言

看到[Anime2Sketch](https://github.com/Mukosame/Anime2Sketch)，想起之前看到过使用PS将图片转成素描风格的例子，所以应该是存在不涉及深度学习就能完成类似操作的方法，遂问GPT。

{{< figure src="/tech/sketch/input.jpg" title="" caption="" >}}

## 颜色减淡法

1. **灰度化（Grayscale）**

   把原始彩色图像转为灰度图，只保留明暗信息。

```python
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
```

   {{< figure src="/tech/sketch/step1_gray.jpg" title="" caption="" >}}

2. **反相（Invert）**

   将灰度图像的像素反相（即变成“负片”效果）。

```python
inverted_image = 255 - gray_image
```

   {{< figure src="/tech/sketch/step2_inverted.jpg" title="" caption="" >}}

3. **高斯模糊（Gaussian Blur）**

   对反相后的图像进行模糊处理，使边缘柔和，看起来像手绘铅笔的阴影。

```python
blurred = cv2.GaussianBlur(inverted_image, (21, 21), sigmaX=0, sigmaY=0)
```

   {{< figure src="/tech/sketch/step3_blurred.jpg" title="" caption="" >}}

4. **颜色减淡（Color Dodge）**

   将灰度图与模糊后的反相图做“颜色减淡”混合。这个步骤是让图像看起来像用铅笔在纸上画出来的关键。

   数学表达：

   $$
   \text{Result} = \frac{\text{Gray}}{255 - \text{Blurred Inverted}} \times 255
   $$

   （并确保结果不超出 255）

```python
def dodge(front, back):
    result = cv2.divide(front, 255 - back, scale=256)
    return result

sketch = dodge(gray_image, blurred)
```
边缘 -> 不那么白

平坦 -> 白

   {{< figure src="/tech/sketch/step4_sketch.jpg" title="" caption="" >}}

## Canny 边缘检测

```python
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blurred, threshold1=50, threshold2=150)
edges = 255-edges
```

   {{< figure src="/tech/sketch/canny_edges.jpg" title="" caption="" >}}