---
title: "自适应gamma"
description: 
date: 2025-05-20T10:54:55+08:00
comments: true
draft: false
tags: ["anime"]
categories: ["anime"]
image: "/makeine/181.jpg"
---
{{< figure src="/makeine/181.jpg" title="" caption="" >}}

# 引言

我有一张绝美的蓝毛女子，奈何她看起来太过悲伤，我想让画面明亮一点。

我要使用自适应gamma。

**自适应 Gamma（Adaptive Gamma Correction）** 是一种图像增强技术，用于根据图像的亮度分布动态地调整伽玛值（gamma），以增强图像的亮度、对比度或细节，特别是暗部区域的细节。

---

### ✅ 先看普通 Gamma 校正

**普通 Gamma 校正** 是一种非线性亮度变换，用公式表达如下：

$$
I_{\text{out}} = I_{\text{in}}^{\gamma}
$$

* γ < 1：增强暗部，图像变亮
* γ > 1：抑制亮部，图像变暗

但普通 gamma 是固定的，不能针对图像内容自适应。

---

### 🧠 自适应 Gamma 的核心思想

> 根据图像的亮度分布（如直方图或累积分布函数 CDF），**为不同亮度区域设计不同的 γ 值**，使图像暗部增强、亮部不过曝。

一种典型策略是：

$$
\gamma(x) = 1 - \text{CDF}(x)
$$

* CDF 是图像灰度直方图的累积分布函数，反映每个亮度值在图像中出现的“亮度百分位”。
* 暗部像素的 CDF 值小（例如 0.1），那么 γ ≈ 0.9 → 增强亮度。
* 亮部像素的 CDF 值大（例如 0.9），那么 γ ≈ 0.1 → 抑制亮度。

---

### 🔬 图像增强过程简述

1. 把图像转为灰度图。
2. 计算直方图 → 得到 CDF。
3. 使用 `gamma = 1 - CDF` 为每个亮度值生成一张查找表（LUT）。
4. 用这张 LUT 对每个像素应用自适应 γ 校正。

---

### 🎯 优势

* **暗图提亮**：自动把黑暗区域提亮。
* **防止过曝**：亮部区域不会被压得太亮或太白。
* **无须手动调 γ**：不需要人为选择参数，适合图像预处理。

---

### 📌 举例代码片段（关键行）

```python
# 计算灰度图直方图
hist = cv2.calcHist([gray], [0], None, [256], [0, 1])
cdf = hist.cumsum() / hist.sum()

# 自适应 gamma LUT
gamma_lut = 1.0 - cdf
lut = np.power(np.linspace(0, 1, 256), gamma_lut)
```

---

### 🧩 自适应 Gamma 的应用场景

* 图像预处理（比如 OCR、医学图像）
* 黑暗图像增强（如夜拍）
* 对比度提升
* HDR 映射替代方案

---

# 实践
上面是gpt的解释，跟着它做吧。

## 🟫 1. 灰度图（grayscale image）

灰度图是一个只有亮度信息的图像，每个像素值范围在 `[0, 255]`（8位）或 `[0.0, 1.0]`（归一化后）。

灰度值越大像素越亮。

```python
img = cv2.imread('181.jpg').astype(np.float32) / 255.0
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```

{{< figure src="/makeine/181_gray.jpg" title="" caption="" >}}

## 📊 2. `hist` —— 直方图（Histogram）

**直方图**是表示图像中像素亮度分布的统计图。它统计每个灰度值出现了多少次：

* 横轴：灰度值（0\~255）
* 纵轴：该灰度值在图像中出现的次数

```python
hist = cv2.calcHist([gray], [0], None, [256], [0, 1])
```

{{< figure src="/makeine/181_hist.jpg" title="" caption="" >}}

全暗的像素这也太多了，不过是没问题的

## 📈 3. `cdf` —— 累积分布函数（Cumulative Distribution Function）

**CDF** 是直方图的“累加和归一化”形式。也就是说：

```python
cdf = hist.cumsum() / hist.sum()
```

含义：

* `hist.cumsum()` 是每个灰度等级以下像素的总数（累加）
* 除以 `hist.sum()` 是为了归一化到 `[0, 1]`

{{< figure src="/makeine/181_cdf.jpg" title="" caption="" >}}

## ✅ 4. **自适应 Gamma 校正**

```python
gamma_lut = 1.0 - cdf
lut = np.power(np.linspace(0, 1, 256), gamma_lut).clip(0, 1)
```

解释：

* 明亮区域的 `cdf` 值大 → gamma 趋近于 0 → `x^0 = 1` → 亮度抬得少
* 黑暗区域的 `cdf` 值小 → gamma 趋近于 1 → `x^1 = x` → 亮度提升大

→ 所以 `1 - cdf` 作为 gamma，就是**根据图像暗亮分布，自动调节亮度的程度**，叫 **自适应 Gamma 修正**。

{{< figure src="/makeine/181_lut.jpg" title="" caption="" >}}

在心里用y=x对比发现所有像素都要变亮

## ✅ **将自适应 gamma 校正应用到每个颜色通道（B、G、R）**

详细解释如下：

---

### 🔧 函数：`apply_gamma(img, lut)`

```python
def apply_gamma(img, lut):
    img_255 = (img * 255).astype(np.uint8)
    return cv2.LUT(img_255, (lut * 255).astype(np.uint8)).astype(np.float32) / 255.0
```

这段函数的每一步做了什么？

1. **`img * 255`**
   将归一化的图像值 `[0.0, 1.0]` 变回 `[0, 255]` 的整数像素值。

2. **`cv2.LUT(img_255, lut)`**
   用 OpenCV 的查找表（LUT）函数对每个像素值进行 gamma 映射。
   也就是说，每个像素值 `x` 被替换成 `lut[x]`，实现非线性亮度调整。

3. **`.astype(np.float32) / 255.0`**
   再次将输出结果归一化回 `[0.0, 1.0]`，以便后续继续使用浮点图像。

---

### 🎨 应用到每个通道（R、G、B）

```python
result = np.zeros_like(img)
for c in range(3):
    result[..., c] = apply_gamma(img[..., c], lut)
```

这部分表示：

* 对输入图像的每个颜色通道（0:蓝，1:绿，2:红）分别执行 `apply_gamma`
* 把每个通道调整后的结果，保存进 `result` 图像中。

---

### 📌 总结一句话：

你这段代码 **把根据亮度直方图计算出的自适应 Gamma 映射 LUT 应用到每个颜色通道上**，从而实现自动亮度增强/抑制，让整张图更清晰自然。

### 完了

{{< figure src="/makeine/181_output.jpg" title="" caption="" >}}

会不会太亮了，能怎么改