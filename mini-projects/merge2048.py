import unittest

def merge_padding(line):
    tmp_line = []
    for elem in line:
        if elem != 0:
            tmp_line.append(elem)
    tmp_line += [0] * (len(line) - len(tmp_line)) # padding with zeros
    return tmp_line

def merge(line):
    tmp_line = merge_padding(line)
    line_index = 0
    while line_index < len(tmp_line) - 1:
        a = tmp_line[line_index]
        b = tmp_line[line_index+1]
        if a == b:
            tmp_line[line_index] = a+b
            tmp_line[line_index+1] = 0
            line_index += 2
        if a != b:
            line_index += 1
    return merge_padding(tmp_line)

class test_2048_merge(unittest.TestCase):
    """Test class
    """
    def test(self):
        case1 = merge([2,0,2,4])
        case2 = merge([8,16,16,8])
        self.assertEqual(case1, [4,4,0,0])
        self.assertEqual(case2, [8,32,8,0])

if __name__ == '__main__':
    unittest.main()
