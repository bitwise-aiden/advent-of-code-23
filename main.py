from challenge import *
from common import runner


def main() -> None:
    try:
        runner(24)
    except KeyboardInterrupt:
        print('\rexiting...')


if __name__ == '__main__':
    main()
