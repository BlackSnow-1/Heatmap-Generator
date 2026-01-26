import argparse

from src.RetryArgumentParser import RetryArgumentParser


def create_parser():
    """创建支持任意参数的解析器"""
    parser = argparse.ArgumentParser(
        description='Heatmap Generator',
        add_help=True,
        # 允许未知参数（不报错）
        allow_abbrev=False
    )

    # 1. 接收任意个位置参数
    parser.add_argument(
        'items',  # 参数名
        nargs='*',  # * 表示0个或多个，+ 表示1个或多个
        default=[],  # 默认值
        type=str,  # 类型
        help='任意个参数（用空格分隔）'
    )

    return parser


def handle_arbitrary_args(args):
    """处理任意参数"""
    print("=" * 50)
    print("File lists :")
    print("=" * 50)

    # 1. 文件参数
    filepath = []
    if args.items:
        print(f"📦 位置参数 ({len(args.items)} 个):")
        for i, item in enumerate(args.items, 1):
            filepath.append(item)

    return filepath


def basic_retry_example():

    # 创建重试器
    parser = RetryArgumentParser(
        description="带重试的参数解析示例",
        max_retries=3
    )

    parser.add_argument('--input', nargs='*', type=str, required = True, help = '任意个参数（用空格分隔）')
    parser.add_argument('--output', required=True, help='输出文件路径')
    parser.add_argument('--retry-delay', type=float, default=1.0,
                        help='重试延迟（秒）')

    # 模拟错误参数
    test_args = ['--input', 'missing.txt', '--output', 'output.txt']

    try:
        args = parser.parse_with_retry(test_args)
        print(f"✅ 解析成功: {args}")
    except SystemExit as e:
        print(f"程序退出: {e}")
    except Exception as e:
        print(f"解析失败: {e}")


if __name__ == "__main__":
    basic_retry_example()

# # 程序入口
# if __name__ == '__main__':
#
#     result = main()
#
#     for i in result:
#         print(i)
#
#     print(f"\n🎉 处理完成，共 {len(result)} 个参数")
