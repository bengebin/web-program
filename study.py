"""一个简单的感谢程序：输入称呼和感谢原因，生成感谢语。"""


def main() -> None:
    name = input("请输入想感谢的人（可留空）：").strip()
    reason = input("想感谢对方什么？（可留空）：").strip()

    recipient = name or "你"
    print("\n" + "=" * 32)
    print(f"亲爱的{recipient}：")
    if reason:
        print(f"谢谢你{reason}。")
    else:
        print("谢谢你的帮助与陪伴。")
    print("因为有你的支持，我感到十分温暖。")
    print("衷心感谢！")
    print("=" * 32)


if __name__ == "__main__":
    main()
