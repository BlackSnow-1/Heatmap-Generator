import argparse
from typing import Optional, List
import time
import sys


class RetryArgumentParser(argparse.ArgumentParser):
    """支持重试的参数解析器"""

    def __init__(self, *args, max_retries: int = 3, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_retries = max_retries
        self.retry_count = 0
        self.last_error = None

    def parse_with_retry(self, args: Optional[List[str]] = None) -> argparse.Namespace:
        """带重试的解析"""
        self.retry_count = 0

        while self.retry_count < self.max_retries:
            try:
                # 尝试解析
                result = self.parse_args(args)
                self.last_error = None
                return result

            except (SystemExit, argparse.ArgumentError) as e:
                self.retry_count += 1
                self.last_error = str(e)

                if self.retry_count < self.max_retries:
                    print(f"⚠️  参数解析失败，正在重试 ({self.retry_count}/{self.max_retries})...")
                    print(f"   错误: {self.last_error}")

                    # 等待后重试
                    time.sleep(1)

                    # 如果是 SystemExit，需要处理退出信号
                    if isinstance(e, SystemExit):
                        # 不退出，继续重试
                        continue
                else:
                    # 达到最大重试次数
                    print(f"❌ 达到最大重试次数 ({self.max_retries})")
                    print(f"   最后错误: {self.last_error}")
                    # 重新抛出异常
                    if isinstance(e, SystemExit):
                        # 对于SystemExit，使用默认退出码
                        sys.exit(e.code if e.code else 1)
                    else:
                        raise

        # 不应该到达这里
        raise argparse.ArgumentError(None, "解析失败")

    def get_file_path(self) -> Optional[str]:
        print()

