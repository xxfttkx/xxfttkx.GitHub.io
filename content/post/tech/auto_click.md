---
title: "《星痕共鸣》自动采集"
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

通过

```
original_win.activate()
pyautogui.moveTo(original_mouse_pos.x, original_mouse_pos.y)
```

能把窗口切换造成的影响尽量降低，但打字被打断等副作用是无能为力的。

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

`PostMessage`就是往消息队列发消息。而我手动点击游戏能触发之前的`PostMessage`，怀疑是游戏内判断了窗口激活时才能处理按键消息。所以**消息“堆积”在消息队列里，直到窗口被激活**。

根据GPT的说法：

> 《星痕共鸣》可能使用了 **Raw Input / DirectInput** 等底层输入机制，导致它**无法正常响应 PostMessage 发送的按键消息**。

且在我切换回原来窗口之后（`original_win.activate()`），仍能通过鼠标控制游戏，即转视角和普通攻击会被我的鼠标操作引出，导致脱离原本采集范围。且预想的息屏状态下能运行也只是我的幻想。

使用

```
    pyautogui.keyDown('alt')
    pyautogui.press('tab')
    pyautogui.keyUp('alt')
```

能解决鼠标能控制游戏的问题，但这alt+tab的点击会导致画面闪烁，画面表现也变得和使用`pyautogui`一样了。原本使用`PostMessage`的目的就是想解决`pyautogui`的当前操作和游戏内操作可能互相影响的问题，这一来就又可能出问题了。

上述的模拟`alt+tab的点击`其实还有平替：

```
def activate_window(hwnd):
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')  # Alt键以绕过权限问题
    # win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    time.sleep(0.1)
    win32gui.SetForegroundWindow(hwnd)
```

可惜仍是类似的表现，没能解决存在着的问题。

> Windows 从 XP 之后几乎**不允许静默地将窗口切到前台**，这是系统限制。

## 🧪 尝试方法三：`SendInput`

`SendInput`本质和`pyautogui`相同呀，且它不需要窗口句柄，等同现实点击，需要窗口在前台，那不更要active了吗。

## ✅ 最终方案

没有捏。

## 需要解决的

activate游戏后就算activate了别的窗口也仍能控制游戏

或

不activate游戏的话`PostMessage`无法生效

## 🏁 总结

万策尽喵。愿意接受副作用其实`pyautogui`和`PostMessage`都算能用。

## 🧩 代码

[auto_click](https://github.com/xxfttkx/auto_click)

## 想法

说不定使用模拟器可以发送按键消息不影响其他本地操作。

## 后记

发现按esc显示侧边栏的时候无法通过鼠标控制视角转向，那么之前`PostMessage`的相关问题可以通过这个解决，但很麻烦，需要自己手动按esc，还要担心鼠标滚轮把它滚到专注采集去。

实测体验还行，毕竟是真的完成了后台采集这个功能。

实现一边移动一边采集时尝试用`按Esc + PostMessage`时无法做到后台采集，应该因为是active窗口太久且长按操作需要焦点。
