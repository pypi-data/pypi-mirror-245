
import binascii
from itertools import zip_longest

from .file import readBinaryFromPath, writeJsonToPath


class Diff:
    def __init__(self, src1_path, src2_path, diff_path=None):
        self.src1_path = src1_path
        self.src2_path = src2_path
        self.diff_path = diff_path

        self.src1_data = readBinaryFromPath(self.src1_path)
        self.src2_data = readBinaryFromPath(self.src2_path)

        self.src1_len = len(self.src1_data)
        self.src2_len = len(self.src2_data)

        self.same_sizes = True if self.src1_len == self.src2_len else False

    def diff(self):
        data1 = iter(self.src1_data)
        data2 = iter(self.src2_data)

        differences = []

        for i, (v1, v2) in enumerate(zip_longest(data1, data2)):
            if not isinstance(v1, int):
                pass

            if not isinstance(v2, int):
                pass

            if v1 != v2:
                offset = hex(i)

                v1 = v1.to_bytes(1, 'little')
                v2 = v2.to_bytes(1, 'little')

                v1 = binascii.hexlify(v1).decode('utf-8')
                v2 = binascii.hexlify(v2).decode('utf-8')

                difference = (offset, v1, v2)

                differences.append(difference)

        differences_updated = {}

        start_offset = 0
        last_offset = 0

        old_buff = ''
        new_buff = ''

        for offset, v1, v2 in differences:
            offset_int = int(offset, 16)

            if start_offset == 0:
                # First difference

                start_offset = offset_int
                last_offset = start_offset

                old_buff += v1
                new_buff += v2

                continue

            if offset_int == last_offset + 1:
                last_offset = offset_int

                old_buff += v1
                new_buff += v2

            else:
                differences_updated[hex(start_offset)] = {
                    'old': old_buff,
                    'new': new_buff
                }

                old_buff = v1
                new_buff = v2

                start_offset = offset_int
                last_offset = start_offset

            # Add the last difference

            if offset == differences[-1][0]:
                differences_updated[hex(start_offset)] = {
                    'old': old_buff,
                    'new': new_buff
                }

        return differences_updated

    def writeDiffToPath(self):
        if not self.diff_path:
            raise Exception('Please set a diff path!')

        differences = self.diff()

        writeJsonToPath(self.diff_path, differences)
