
import random
from splitdataloader import write_split_data, SplitDataLoader


def get_random_bytes(size_limit=16):
    size = random.randint(1, size_limit)
    data = random.randbytes(size)
    return data


def test01():
    N = 1000
    data_list = []
    for idx in range(N):
        data = get_random_bytes(400)
        data_list.append(data)

    write_split_data(
        "tmp/db", data_list, splits=32, shuffle=False, start_clean=True
    )

    loader = SplitDataLoader("tmp/db")
    assert len(loader) == len(data_list)
    loaded_data_list = []
    for idx in range(len(loader)):
        data = loader[idx]
        loaded_data_list.append(data)

    assert loaded_data_list == data_list

    data_list.sort()
    loaded_data_list = []
    for data in loader.iterate_binwise():
        loaded_data_list.append(data)

    loaded_data_list.sort()
    assert data_list == loaded_data_list
    print("All OK 🙂")


def main():
    test01()


if __name__ == "__main__":
    main()
