import argparse

from src.RetryArgumentParser import RetryArgumentParser

def basic_retry_example():

    # 创建重试器
    parser = RetryArgumentParser(
        description="带重试的参数解析示例",
        max_retries=3
    )

    parser.add_argument('--input', nargs='*', type=str, required = True, help = '任意个参数（用空格分隔）')
    parser.add_argument('--output', required=True, help='输出文件路径')
    parser.add_argument('--retry-delay', type=float, default=1.0, help='重试延迟（秒）')

    try:
        args = parser.parse_with_retry()
        # 处理传入的文件列表
        print(f"解析成功: {args}")
    except SystemExit as e:
        print(f"程序退出: {e}")
    except Exception as e:
        print(f"解析失败: {e}")


if __name__ == "__main__":
    # 读取 输入参数
    basic_retry_example()

    # 输入的文件列表



