---
title: "《星痕共鸣》自动挂机"
description: 
date: 2025-07-20T21:20:27+08:00
comments: true
draft: false
tags: ["Python", "自动化", "游戏脚本", "pyautogui", "PostMessage"]
categories: ["tech"]
---
《星痕共鸣》的生活职业养成十分麻烦，要不断进行重复的采集工作，看到b站上有使用按键精灵且配上`用别怕，怕别用`的标语后，就想自己写程序了，虽说不知道会不会被检测，但能自己控制总不会是坏事。

## 📌 项目背景

- 游戏：《星痕共鸣》
- 目标：定时点击F键，实现自动采集
- 环境：Windows + Python 脚本

## 🧪 尝试方法一：`pyautogui`

优点：

- 模拟用户层操作，所见即所得

```python
target_window.activate()
pyautogui.press('f')
```

这种用户层的操作会打断自己正在做的事，且自己正在做的输入有可能影响一瞬聚焦的游戏，体验并不好。另外还无法在息屏状态下运行。

## 🧪 尝试方法二：`PostMessage`

优点：

* 不需要激活窗口。
* 在理论上更隐蔽、更系统层。


```python
    win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, vk_code, lparam_down)
    # time.sleep(0.2)
    win32gui.PostMessage(hwnd, win32con.WM_KEYUP, vk_code, lparam_up)
```

但经过实测，在我窗口模式的情况下，仍需`win.activate()`才能成功`PostMessage`。

根据GPT的说法：

> 《星痕共鸣》可能使用了 **Raw Input / DirectInput** 等底层输入机制，导致它**无法正常响应 PostMessage 发送的按键消息**。

且在我切换回原来窗口之后（`original_win.activate()`），仍能通过鼠标控制游戏，即转视角和普通攻击会被我的鼠标操作引出，导致脱离原本采集范围。且预想的息屏状态下能运行也只是我的幻想。


```
    pyautogui.keyDown('alt')
    pyautogui.press('tab')
    pyautogui.keyUp('alt')
```

使用这能解决鼠标能控制游戏的问题，但这alt+tab的点击会导致画面闪烁，画面表现也变得和使用`pyautogui`一样了。原本使用`PostMessage`的目的就是想解决`pyautogui`的当前操作和游戏内操作可能互相影响的问题，这一来就又可能出问题了。

## ✅ 最终方案

没有捏。

## 🏁 总结

万策尽喵。

## 🧩 代码

[auto_click](https://github.com/xxfttkx/auto_click)
