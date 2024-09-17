---
title: "Krkr移植"
description: 
date: 2024-09-17T20:48:52+08:00
hidden: false
comments: true
draft: false
---
看了好多篇，解包封包什么的，都去看了，但exe要怎么能在手机上用，不懂啊。

看了[KrkrExtract](https://github.com/xmoezzz/KrkrExtract)，GARbro等拆包软件，更是一头雾水，想玩的游戏的解密手段也不知道，使用[KrkrExtract](https://github.com/xmoezzz/KrkrExtract)甚至还报出

[Fatal Error Access Violation](https://github.com/xmoezzz/KrkrExtract/issues/119)，更是没能找出解决方法。

决定去看看[Kirikiroid2](https://github.com/zeas2/Kirikiroid2)，看个README就看出个大概了

```
Based on most code from Kirikiri2 and KirikiriZ

Video playback module modified from kodi

Some string code from glibc and Apple Libc.

Real-time texture codec modified from etcpak, pvrtccompressor, astcrt

Android storage accessing code from AmazeFileManager
```

在我理解，就是在手机上集成了游戏引擎，也因此能用xp3打开游戏。

把一些游戏的xp3文件拷到手机，试了试，还真能。

自己想玩游戏的xp3即使没有解密拆包再封包，直接拷到手机上，也行了。就这样得到解决了。

目前也有问题还在，plugin文件夹里都是dll，我想着手机上应该不能用吧，自己做了做变量控制实验，也没有发现差异。

另外，需要xp3filter.tjs转字符，找了同项目组以前项目的响应文件，成功了。[该网站](https://zeas2.github.io/Kirikiroid2_patch/patch/)不知道为什么没有更新。

还有，直接用[Kirikiroid2](https://github.com/zeas2/Kirikiroid2)玩刚刚弄的游戏挺卡了，看了看帧率挺低，不知原因。强制使用默认字体解决了。
