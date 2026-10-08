# -*- coding: utf-8 -*-
"""AIAE 课程每日提醒 · 云端版（GitHub Actions 运行，电脑关机也能触发）"""
import json
import os
import ssl
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

CST = timezone(timedelta(hours=8))
COURSE_URL = "http://www.chinapeixun.org.cn/login.html"


def log(msg):
    print(msg, flush=True)


def today_str():
    return datetime.now(CST).strftime("%Y-%m-%d")


def load_plan():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plan.json")
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def build_message(plan, day_key):
    """返回 (title, html, markdown)"""
    days = plan["days"]
    if day_key not in days:
        title = "AIAE 课程计划已结束"
        args = (plan["course"], plan["start"], plan["end"], plan["total_lessons"])
        html = (
            "<p>%s 的学习计划（%s 至 %s，共 %d 节）已到期。</p>"
            "<p>如需继续，可回到工作台调整计划：</p>"
            "<p><a href=\"https://www.workbuddy.cn/space/d/aURugCge1ZBUuLB7w3CDYJ\">打开学习目标管理台</a></p>"
        ) % args
        md = (
            "**%s 的学习计划（%s 至 %s，共 %d 节）已到期。**&#8203;\n\n"
            "> 如需继续，可回到工作台调整计划：\n"
            "> https://www.workbuddy.cn/space/d/aURugCge1ZBUuLB7w3CDYJ\n"
        ) % args
        return title, html, md

    item = days[day_key]
    weekday = "一二三四五六日"[datetime.strptime(day_key, "%Y-%m-%d").weekday()]

    if item.get("rest"):
        note = item.get("note", "今天不学")
        html = (
            "<p>%s（周%s）</p><p>%s</p>"
            "<p>课程进度不受影响，安心休息。</p>"
        ) % (day_key, weekday, note)
        md = (
            "**%s（周%s）**&#8203;\n\n%s\n\n"
            "课程进度不受影响，安心休息。\n"
        ) % (day_key, weekday, note)
        return "😴 %s 今日休息" % plan["course"], html, md

    title = "📚 %s 今日学习提醒" % plan["course"]
    html = (
        "<p><b>%s（周%s）今日任务</b></p>"
        "<p style='font-size:16px;margin:8px 0'>第 %d-%d 节 · 共 %d 节 · 约 %.1f 小时</p>"
        "<p style='color:#666'>%s</p>"
        "<p><a href=\"%s\">📚 打开课程网站</a></p>"
        "<p style='color:#999;font-size:12px'>学完记得回到工作台打卡</p>"
    ) % (day_key, weekday, item["from"], item["to"], item["lessons"],
         item["hours"], item["title"], COURSE_URL)
    if day_key == plan["end"]:
        html += "<p><b>今天是最后一天，加油！</b></p>"

    md = (
        "## %s（周%s）今日任务\n\n"
        "**第 %d-%d 节 · 共 %d 节 · 约 %.1f 小时**\n\n"
        "> %s\n\n"
        "[📚 打开课程网站](%s)\n\n"
        "---\n学完记得回到工作台打卡\n"
    ) % (day_key, weekday, item["from"], item["to"], item["lessons"],
         item["hours"], item["title"], COURSE_URL)
    if day_key == plan["end"]:
        md += "\n**今天是最后一天，加油！**\n"
    return title, html, md


def send_pushplus(token, title, html):
    url = "https://www.pushplus.plus/send"
    payload = json.dumps({
        "token": token, "title": title, "content": html,
        "template": "html", "topic": "",
    }).encode("utf-8")
    req = urllib.request.Request(
        url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20, context=ssl.create_default_context()) as r:
        return r.read().decode("utf-8", "replace")


def send_serverchan(key, title, desp):
    url = "https://sctapi.ftqq.com/%s.send" % key
    payload = json.dumps({"title": title, "desp": desp}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20, context=ssl.create_default_context()) as r:
        return r.read().decode("utf-8", "replace")


def main():
    plan = load_plan()
    day = today_str()
    title, html, md = build_message(plan, day)
    log("日期: %s" % day)
    log("标题: %s" % title)

    pp = os.environ.get("PUSHPLUS_TOKEN", "").strip()
    sc = os.environ.get("SERVERCHAN_KEY", "").strip()
    if not pp and not sc:
        log("错误：未配置 PUSHPLUS_TOKEN 或 SERVERCHAN_KEY，跳过推送。")
        return 2

    try:
        if sc:
            log("通道: Server酱")
            log("响应: %s" % send_serverchan(sc, title, md))
        else:
            log("通道: PushPlus")
            log("响应: %s" % send_pushplus(pp, title, html))
    except Exception as err:
        log("推送失败: %s" % err)
        return 1

    log("完成")
    return 0


if __name__ == "__&#8203;main__":
    sys.exit(main())
