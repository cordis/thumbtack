#!/usr/bin/env python

from thumbtack.storage import Storage
from thumbtack.runtime import Runtime
from thumbtack.runner import RuntimeRunner


def main():
    storage = Storage()
    runtime = Runtime(storage)
    runtime_runner = RuntimeRunner(runtime)
    runtime_runner.run()


if __name__ == '__main__':
    main()
