from logging import FileHandler
import struct
import os


def file_hash(name):
    """
    source: https://trac.opensubtitles.org/projects/opensubtitles/wiki/HashSourceCodes#Python
    """
    try:

        longlongformat = '<q'  # little-endian long long
        bytesize = struct.calcsize(longlongformat)

        f = open(name, "rb")

        filesize = os.path.getsize(name)
        hash = filesize

        if filesize < 65536 * 2:
            return "SizeError"

        for x in range(int(65536/bytesize)):
            buffer = f.read(bytesize)
            (l_value,) = struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF  # to remain as 64bit number

        f.seek(max(0, filesize-65536), 0)
        for x in range(int(65536/bytesize)):
            buffer = f.read(bytesize)
            (l_value,) = struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF

        f.close()
        returnedhash = "%016x" % hash
        return returnedhash

    except(IOError):
        return "IOError"


def _test_file_hash():
    """
    Test 1
    http://www.opensubtitles.org/addons/avi/breakdance.avi
    ​AVI file (12 909 756 bytes)
    hash: 8e245d9679d31e12
    =====
    Test 2
    http://www.opensubtitles.org/addons/avi/dummy.rar
    ​DUMMY RAR file (2 565 922 bytes, 4 295 033 890 after RAR unpacking, test on UNPACKED file)
    hash: 61f7751fc2a72bfb (for UNPACKED file)
    """
    print('Test 1:')
    hash1 = file_hash('breakdance.avi')
    print(f'hash: {hash1}, result: {hash1 == "8e245d9679d31e12"}')

    print('Test 2:')
    hash2 = file_hash('dummy.bin')
    print(f'hash: {hash2}, result: {hash2 == "61f7751fc2a72bfb"}')
    """
    Test 1:
    hash: 8e245d9679d31e12, result: True
    Test 2:
    hash: 61f7751fc2a72bfb, result: True
    """


def file_size(path):
    file_stats = os.stat(path)
    byte_size = file_stats.st_size
    return byte_size


def _test_file_size():
    """
    Test 1
    http://www.opensubtitles.org/addons/avi/breakdance.avi
    ​AVI file (12 909 756 bytes)
    =====
    Test 2
    http://www.opensubtitles.org/addons/avi/dummy.rar
    ​DUMMY RAR file (2 565 922 bytes, 4 295 033 890 after RAR unpacking, test on UNPACKED file)
    """
    print('Test 1:')
    size_1 = file_size('breakdance.avi')
    print(f'size: {size_1}, result: {size_1 == 12_909_756}')

    print('Test 2.1:')
    size_2_1 = file_size('dummy.rar')
    print(f'size: {size_2_1}, result: {size_2_1 == 2_565_922}')

    print('Test 2.2:')
    size_2_2 = file_size('dummy.bin')
    print(f'size: {size_2_2}, result: {size_2_2 == 4_295_033_890}')
    """
    Test 1:
    size: 12909756, result: True
    Test 2.1:
    size: 2565922, result: True
    Test 2.2:
    size: 4295033890, result: True
    """


if __name__ == '__main__':
    _test_file_hash()
    _test_file_size()
