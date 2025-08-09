# GTA5中配模组说明书

作者：[B站-Cyber蝈蝈总](https://space.bilibili.com/37706580)、[3DM-DJ小良](https://mod.3dmgame.com/u/7715845)

> **[警告]**
>
> **该MOD免费，只在[GTAMODX](https://www.gtamodx.com)和[3DM](https://mod.3dmgame.com/)发布。**
>
> **严禁未授权的转载**。**严禁倒卖，用于盈利将承担相应责任！**

## 介绍

我们为GTA5制作了汉语配音模组，内容如下：

| 类型     | 内容                                                         |
| -------- | ------------------------------------------------------------ |
| 主角配音 | [必选]真人配音，常见角色包括三主角在大世界中的触发式语音     |
| 剧情配音 | [必选]真人配音，部分前期剧情任务的语音、大世界事件           |
| 视频配音 | [必选]真人配音，部分电视节目；启动动画；部分剧情涉及的贴图汉化 |
| 配套字幕 | [可选]剧情任务配音的定制字幕，如果你的游戏语言不支持简体中文，安装此项会导致乱码。安装后位于mods/update |
| NPC配音  | [可选]AI配音，覆盖几乎所有路人NPC的语音(7万+条)，但是质量一般，安装后位于mods/x64/audio/sfx/，以S_FULL和S_MINI开头的rpf文件 |

## 安装方法

> **[注意]**
>
> 安装任何模组后，GTA5可能因BattleEye(反作弊程序)检测到额外加载项而无法正常启动，请尝试**在R星启动器中禁用BE反作弊，或在exe的“启动选项”的里添加-nobattleye参数**。禁用后无法使用线上功能。也就是说模组只能线下玩，不能与OL共存。

| 自动安装（推荐）                                             | 懒人压缩包（包体巨大）                                       |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 请直接使用MOD自带的安装器一键安装，兼容增强版，如遇问题优先联系作者或Q群解决。 | 请到作者B站置顶动态的资源网盘下载懒人压缩包，解压后，将所有内容直接粘贴到增强版游戏目录，使得`.asi`文件与`GTA5.exe`处于同一级目录，那么就安装对了。 |

传承版和增强版理论上都可以分别通过OpenIV和CodeWalker手动安装，但是对普通人来说流程太复杂，增强版还需要dev48及以上的版本的CodeWalker才能编辑，故不再提供手动安装的办法，只提供安装器与懒人压缩包。

## 卸载方法

> **[注意]**
>
> 中配模组包含这些组件：`mod本体`、`mod加载器.asi`、`asi加载器.dll`，如果你之前安装过别的模组，那你大概率已经有`mod加载器.asi`和`asi加载器.dll`了，一般是`OpenIV.asi`、`OpenRPF.asi`、`dinput8.dll`、`dsound.dll`，这些文件酌情删除即可。如果要恢复线上功能，请删除asi loader，即`dinput8.dll`、`dsound.dll`等文件。
>
> 中配模组**不依赖于ScriptHookV**，任何与ScriptHookV有关的报错均与本MOD无关。

| 传承版(老版)                                                 | 增强版                                                       |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| 如果使用安装器一键卸载(直接删除mods文件夹中与中配相关的RPF文件)，请注意防止其他处于同一RPF文件内的已安装模组被一起误删。如果要精细地删除中配内容，请使用[OpenIV](https://www.gta5-mods.com/tools/openiv)操作。过于详细的方法不再赘述。 | 如果直接删除mods文件夹中与中配相关的RPF文件，请注意防止其他处于同一RPF文件内的已安装模组被一起误删。如果要精细地删除中配内容，请使用**大于等于dev48版**的[CodeWalker](https://discord.com/channels/329138547833700352/351357358460370944)操作，旧版CodeWalker与OpenIV都不兼容增强版。过于详细的方法不再赘述。 |

## 制作人员

策划：Cyber蝈蝈总、小湿帝JokiJoki、DJ小良

工具研发：Cyber蝈蝈总、[鼠子](https://space.bilibili.com/435502585)

文案：[蓝风](https://space.bilibili.com/45274270)、[tails](https://space.bilibili.com/15283)、阿笑-Seichi，CACOLAZY 、Cyber蝈蝈总、鸢鸣_Official、小湿帝JokiJoki、kagamiKILL、密申罗69号干员、幕雪风鸣、Agera

| 主要角色                     | 配音演员                                               |
| ---------------------------- | ------------------------------------------------------ |
| 麦克、网球教练               | [祈衍](https://space.bilibili.com/366596518)           |
| 崔佛、拉玛                   | [阿笑-Seichi](https://space.bilibili.com/425177357)    |
| 富兰克林                     | [Cyber蝈蝈总](https://space.bilibili.com/37706580)     |
| 吉米、丹尼斯                 | [小湿帝JokiJoki](https://space.bilibili.com/158625239) |
| 莱斯特                       | [工新河](https://space.bilibili.com/99708316)          |
| 布莱德、玛德拉索、费兰德医生 | [九日草方](https://space.bilibili.com/322276032)       |

配音：JasonSmudge老琪、阿尔戈-Argo、阿笑-Seichi、CACOLAZY 、Cricket影音博物馆、Cyber蝈蝈总、 Goldship、Hertz、进击的魔界人、小湿帝JokiJoki、蓝风、祈衍、鸢鸣_Official、崴脚小面包、封狼、T.K.Q、SCC、工新河、八百棒冰奔被窝、九日草方、为师の大可爱日奈、HA桑、幕雪风鸣、屑老板、不列(比亚迪) 、初夏翎成、柠檬

测试/校对：志存高远之人、斐波那契数列参观者

## 更新日志

请关注作者[B站主页](https://space.bilibili.com/37706580)，获取最新版本。

| 版本     | 新内容                                                       |
| -------- | ------------------------------------------------------------ |
| 0.1      | [已弃用]使用sovits-svc配音的主线任务：序章，配套字幕         |
| 0.2-0.11 | 真人主线任务：序章、难兄难弟、有借有还、节外生枝、其父其子、婚姻咨询、好友请求、侦查珠宝店、小查、掌上明珠、序章重制，配套字幕 |
| 1.0      | 主要角色的大世界触发式语音；部分常见大世界事件如切换主角、报警、飞行驾校；配套字幕；部分电视节目配音与本土化；部分真人配音的警察NPC；使用SenseVoice + DeepSeek V3 + CosyVoice2，识别、翻译并配音了几乎所有路人NPC的大世界语音 |

## 未来计划[到2.0]

1. [主要]继续推进主线任务中配，如抢劫珠宝店
2. [次要]继续推进大世界事件中配，如主角之间的邀请事件
3. 基于演员报名数量，将部分由AI配音的NPC改为真人配音

## 鸣谢

1. 徽信支付

2. 鼠子

3. 銮为延器

4. kagamiKILL

5. 志存高远之人

6. VLxMuTe

## 开源软件清单

1. CodeWalker: [https://github.com/dexyfex/CodeWalker](https://github.com/dexyfex/CodeWalker)
2. 罪恶都市次时代版启动器：[https://github.com/gtamodxcom/GTA-Vice-City-Nextgen-Edition-Launcher](https://github.com/gtamodxcom/GTA-Vice-City-Nextgen-Edition-Launcher)
3. 本安装器：[https://github.com/Katock-Cricket/GTAV-CNDub-Setup](https://github.com/Katock-Cricket/GTAV-CNDub-Setup)

## 赞助

赞助地址：[爱发电-Cyber蝈蝈总](https://ifdian.net/a/Katock)

MOD免费，但是如果得到了您的赞助，将会直接按劳分配给参与制作的人员。

我们会公开鸣谢您的赞助

## BUG反馈/建议/参与模组制作

请联系我的[B站账号]((https://space.bilibili.com/37706580))或闲聊Q群：939762012
