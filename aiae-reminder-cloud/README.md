# AIAE 课程每日提醒 · 云端部署指南

电脑关机也能收到微信提醒。GitHub Actions 每天北京时间 20:30 触发，通过 **Server酱** 推送到微信。

## 文件说明

| 文件 | 作用 |
|---|---|
| `plan.json` | 学习计划数据（10/8-10/17 每天学第几节到第几节） |
| `remind.py` | 推送脚本，读取计划并调用 Server酱 |
| `.github/workflows/remind.yml` | GitHub Actions 定时任务配置（北京时间 20:30 = UTC 12:30） |

---

## 你需要准备什么

只需要 **Server酱 SendKey**（你已注册 ✅），不需要再注册 PushPlus。

两者区别（为什么 Server酱 就够了）：

| | Server酱 | PushPlus |
|---|---|---|
| 每天免费额度 | 5 条 | 200 条 |
| 本项目每天用量 | 1 条 | 1 条 |
| 要否实名 | 否 | 是（1 元）|
| 消息格式 | Markdown | HTML |

我们每天只发 1 条，Server酱 的 5 条完全够用，且免实名、更省事。

---

## 第 1 步：取 SendKey

1. 登录 https://sct.ftqq.com/
2. 页面右上角「SendKey」→ 点复制，形如 `SCTxxxxxxxxxxxxxxxx`
3. 存好这串字符

> SendKey 相当于密码，不要发到公开地方。它只会存在 GitHub 的 Secret 里。

---

## 第 2 步：创建 GitHub 仓库（2 分钟）

1. 打开 https://github.com/new
2. 仓库名填 `aiae-reminder`
3. **勾选** `Add a README file`
4. 点 `Create repository`

---

## 第 3 步：上传文件（3 分钟）

把本目录的 3 个文件按以下结构上传：

```
aiae-reminder/
├── plan.json
├── remind.py
└── .github/
    └── workflows/
        └── remind.yml
```

**上传步骤**：
1. 进入刚建的仓库 → `Add file` → `Create new file`
2. 输入路径 `plan.json`，粘贴内容，`Commit changes`
3. 重复创建 `remind.py`
4. 创建 `.github/workflows/remind.yml`

> `.github` 开头是点目录，直接在文件名框输入完整路径 `.github/workflows/remind.yml` 即可自动创建目录。

---

## 第 4 步：配置 SendKey（2 分钟）

1. 仓库顶部工具栏 → `Settings`
2. 左侧菜单 → `Secrets and variables` → `Actions`
3. 点 `New repository secret`
4. 填写：
   - Name：`SERVERCHAN_KEY`
   - Secret：粘贴你的 SendKey
5. 点 `Add secret`

---

## 第 5 步：手动测试一次（1 分钟）

1. 仓库顶部 `Actions` 标签
2. 左侧选 `AIAE 课程每日提醒`
3. 右侧点 `Run workflow` → 确认 → 等 1 分钟
4. **看手机微信有没有收到消息**
   - 收到 → 配置完成，等 20:30 自动推送
   - 没收到 → 点进失败的那次运行看日志，把报错发我

---

## 第 6 步：确认定时生效

- 每天北京时间 **20:30** 自动推送
- 对应 GitHub UTC 时间 `12:30`（已配好）
- 中国不实行夏令时，不用调时区

---

## 常见问题

**Q：为什么 Server酱 收到的消息是卡片样式的？**
Server酱 走微信服务号模板消息，是卡片形式，带标题和正文，点击可跳转链接。这跟普通聊天消息不同，但内容完整、能加链接，够用。

**Q：额度够吗？**
免费会员每天 5 条，本项目每天发 1 条，够用。如果某天失败重试多次也不会超。

**Q：GitHub Actions 会收费吗？**
个人账号对公开仓库免费。私有仓库每月2000 分钟免费额度，本项目每次运行约 10 秒，可用几万次。

**Q：能改推送时间吗？**
编辑 `.github/workflows/remind.yml` 里的 `cron`。北京时间 = UTC + 8，UTC 时间要减 8：
- 北京 20:30 → UTC `30 12 * * *`
- 北京 08:00 → UTC `0 0 * * *`

**Q：10/11 和 10/17 收到的是"休息"提醒？**
设计如此。休整日推"今天不学"，避免你误以为漏学了。

**Q：10/18 之后会怎样？**
会收到"AIAE 课程计划已结束"。想彻底停掉就在 Actions 页面禁用 workflow。

**Q：能不能"打了卡就不提醒"？**
不能。云端脚本够不到 WorkBuddy 的打卡数据（需要本机身份认证）。
需要这个功能就保留 WorkBuddy 里那个 20:30 的定时任务，它能查库判断。

---

## 安全说明

- SendKey 只存在 GitHub 仓库的加密 Secret 里，不在代码里
- `plan.json` 只是学习计划，不含个人信息
- 脚本只调用 Server酱 一个外部接口