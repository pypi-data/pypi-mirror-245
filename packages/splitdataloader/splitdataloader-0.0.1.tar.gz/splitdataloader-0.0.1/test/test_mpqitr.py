
import time
from splitdataloader import MpQItr


def test_mp_itr():
    itr = MpQItr(range, 10, 20)
    for val in itr:
        print(val, flush=True)
        time.sleep(2)
    for val in itr:
        print(val, flush=True)
        time.sleep(2)


def main():
    test_mp_itr()


if __name__ == "__main__":
    main()
