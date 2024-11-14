---
title: "记一次磁盘清理经历"
description: 
date: 2024-11-14T12:40:24+08:00
comments: true
draft: false
tags: ["disk"]
---
### 起因

{{< figure src="/live/1.png" title="" caption="" >}}

好恐怖的见红，记得前几天还是30G的。

### Dism++

{{< figure src="/live/2.png" title="" caption="" >}}

之前电脑送去修收到时获得的软件。感觉以前用的时候有找相同文件功能的，不知道是我记错还是这个版本问题。还算行，看起来删了不少临时文件。这里显示有4G多临时文件却只释放了3.58G不知道是为什么。

{{< figure src="/live/3.png" title="" caption="" >}}

### CCleaner

gpt推荐的，一下载发现好商业化啊，用的恶心，难用，也确实没什么用，赶紧卸载了。

### 自己去C盘排查

我也不知道为什么，大小在面板上不显示，但自己去文件夹看属性，能得出大小。

结果就发现 `C:\Users\MR\AppData`里有快70G文件。

{{< figure src="/live/4.png" title="" caption="" >}}

进入 `C:\Users\MR\AppData\Local`发现里面我已经卸载的卡拉彼丘，却有文件夹保存着700MB以上的数据（忘了具体多少，或许也只有100多），这是你的失职吗，卸载程序。这miHoYo我卸完了里面也还有36.5MB，打开看看发现是 `QtWebEngine`相关的一些东西。

然后这看看，那看看。Docker15.7G，Google2.93G，Microsoft7.41G，npm-cache1.02G，NVIDIA4.17G，Packages2.95G，Unity6.36G，Yarn760MB。

现在就是看看这些里面的内容是什么，有没有机会移走的问题了。

### 问GPT

看起来你的 `AppData` 文件夹占用了大量空间，这些文件通常是由程序生成的缓存、配置文件和临时数据。你可以按照以下步骤进一步检查和清理：

1. **Docker**：Docker 会在 `C:\Users\MR\AppData\Local` 下存储大量的镜像和容器数据。可以通过 Docker 命令清理未使用的镜像和容器：

   ```bash
   docker system prune -a
   ```

   这将清理所有不再使用的镜像和容器。
2. **npm 和 Yarn 缓存**：这两个文件夹会存储已安装包的缓存，可以通过以下命令清理：

   ```bash
   npm cache clean --force
   yarn cache clean
   ```
3. **Google 和 Microsoft**：这些通常是与应用程序和浏览器相关的缓存数据，可以考虑清理浏览器缓存，或者使用 CCleaner 等工具来清理它们。
4. **Unity 和 QtWebEngine**：这些可能是与某些开发工具或游戏相关的缓存。如果你确定不再需要这些内容，可以手动删除。
5. **`AppData\Local` 中的其他内容**：在清理时，确保不删除一些必要的配置文件。比如你提到的 `miHoYo` 和 `QtWebEngine` 的数据，确认是否是卸载软件后遗留的垃圾文件。

定期清理这些缓存和临时文件可以释放很多磁盘空间，同时保持系统的健康。如果不确定某些文件是否可以删除，最好先备份或者移到其他地方以避免丢失重要数据。

### Docker

打开Docker一清，磁盘空间更少了，变成了10.9G，明明它讲 `Total reclaimed space: 4.632GB`。

{{< figure src="/live/5.png" title="" caption="" >}}

看到设置这里有能改路径的东西，打开一看，这部分还真是大头，15.7G/15.8G。

改完"Apply & restart"就好了。最终 `C:\Users\MR\AppData\Local\Docker\wsl` 的大小变成了1.22GB/1.25GB。明明改了路径这原路径还有用吗，我也不敢删。

最终

{{< figure src="/live/6.png" title="" caption="" >}}

就先这样了吧。

### 结论

我不会写结论。
