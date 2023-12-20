from challenge import *
from common import *


def main() -> None:
    try:
        runner(20)
    except KeyboardInterrupt:
        print('\rexiting...')


if __name__ == '__main__':
    main()
