"""把 heart_popup.py 打包成 macOS 可双击运行的 .app 应用。

用法:
    .build-venv/bin/python build_app.py

产物:
    dist/100个爱心.app   —— 双击即可运行，自带背景音乐
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP_NAME = "100个爱心"
ENTRY = os.path.join(HERE, "heart_popup.py")
ICON = os.path.join(HERE, "heart.icns")
# 优先打包 mp3（跨平台通用），Windows 也能播
MUSIC = os.path.join(HERE, "江南.mp3")
if not os.path.exists(MUSIC):
    MUSIC = os.path.join(HERE, "江南.m4a")


def run(cmd: list[str]) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=HERE)


def main() -> None:
    if not os.path.exists(ICON):
        raise SystemExit("缺少 heart.icns，请先运行 make_icon.py")
    if not os.path.exists(MUSIC):
        raise SystemExit("缺少 江南.m4a")

    # 清理上次构建
    for d in ("build", "dist"):
        shutil.rmtree(os.path.join(HERE, d), ignore_errors=True)

    run([
        sys.executable, "-m", "PyInstaller",
        "--noconfirm", "--clean",
        "--windowed",                     # macOS .app，不显示终端窗口
        "--name", APP_NAME,
        "--icon", ICON,
        "--add-data", f"{MUSIC}:.",       # 音乐打进包内 Resources
        "--osx-bundle-identifier", "com.local.heartpopup",
        "--hidden-import", "tkinter",
        ENTRY,
    ])

    app = os.path.join(HERE, "dist", f"{APP_NAME}.app")
    if not os.path.exists(app):
        raise SystemExit("打包失败：未生成 .app")

    # 确保音乐确实在 Resources 里
    res = os.path.join(app, "Contents", "Resources")
    packed = os.path.join(res, os.path.basename(MUSIC))
    if not os.path.exists(packed):
        shutil.copy(MUSIC, packed)
        print("补拷贝音乐 ->", packed)

    # ad-hoc 签名：macOS 要求 .app 有有效签名才能启动，
    # 未签名会报 "Launch failed (error 163)"。
    subprocess.run(
        ["codesign", "--force", "--deep", "--sign", "-", app],
        capture_output=True,
    )
    check = subprocess.run(
        ["codesign", "-v", "--deep", app], capture_output=True
    )
    print("签名校验:", "✓ 通过" if check.returncode == 0 else "✗ 失败")

    # 移除下载隔离标记（若从网络下载过）
    subprocess.run(["xattr", "-cr", app], capture_output=True)

    print("\n✓ 构建完成:", app)


if __name__ == "__main__":
    main()
