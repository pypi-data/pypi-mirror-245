# -*- coding:utf-8  -*-
# @Author: FanHongWei
# @Time: 2021-01-01
import unittest

from intervalset2 import IntervalSet, Interval


class TestParseFromStr(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(IntervalSet.empty_tvs(), IntervalSet.parse_from_str(''))
        self.assertEqual(IntervalSet.inf_tvs(), IntervalSet.parse_from_str('(-inf, inf) | 5'))
        self.assertEqual('5', str(IntervalSet.parse_from_str('5')))
        # 该用例测试 10 种子场景(外切2 远离2 右侧内切及包含3 右侧内切及包含3)
        self.assertEqual('(12, 18) | (22, 28) | (32, 39) '
                         '| [112, 118) | [122, 128) | (131, 140) '
                         '| (212, 218) | (222, 228) | (231, 238) '
                         '| (312, 318] | (322, 328] | (331, 339) '
                         '| (412, 418) | (418, 419) | (422, 429) | (432, 439) '
                         '| (513, 518) | (518, 519) | (522, 529] | (531, 538] '
                         '| (612, 615) | (618, 619) | [622, 625) | (628, 629)',
                         str(IntervalSet.parse_from_str(
                             '(12, 18) | (112, 118) | (212, 218) | (312, 318) | (412, 418) | (518, 519) | (618, 619) |'
                             '(12, 15) | [112, 115) | (213, 218) | (313, 318] | (418, 419) | (513, 518) | (612, 615) |'
                             '(22, 28) | [122, 128) | (222, 228) | (322, 328] | (422, 428) | [528, 529] | [622, 625) |'
                             '(22, 28) | (122, 128) | (222, 228) | (322, 328) | [428, 429) | (522, 528) | (628, 629) |'
                             '(32, 38) | (131, 132) | (232, 238) | (338, 339) | (432, 438] | (538, 538) |'
                             '(32, 39) | (132, 139) | (231, 238) | (331, 338) | (438, 439) | (531, 538] |'
                             '           [132, 140) |              (333, 338]',
                             # 左虚内切  左实内切+前回溯 右虚内切      右实内切+后回溯  右外切      左外切         左右远离
                         )))

    def test_inf(self):
        expected = '(-inf, inf)'
        tvs_inf = IntervalSet.parse_from_str('(-inf, inf)')
        self.assertEqual(expected, str(tvs_inf))
        self.assertEqual(tvs_inf, IntervalSet.inf_tvs())
        self.assertEqual(tvs_inf, IntervalSet.parse_from_str('(-inf, 0) | 0 | (0, inf)'))
        self.assertEqual(tvs_inf, IntervalSet.parse_from_str('(-inf, 3) | 0 | (-3, inf)'))
        self.assertEqual(tvs_inf, IntervalSet.parse_from_str('(-inf, inf) | 0 | (-3, inf)'))
        self.assertEqual(tvs_inf, IntervalSet.parse_from_str('(-inf, inf) | 0 | (-3, inf)'))

    def test_empty(self):
        self.assertEqual('', str(IntervalSet.parse_from_str('')))
        self.assertEqual('', str(IntervalSet()))
        self.assertEqual(IntervalSet.empty_tvs(), IntervalSet.empty_tvs())

    def test_other(self):
        tvs1 = IntervalSet.parse_from_str('(2, 5)')
        tvs2 = tvs1.copy()
        self.assertEqual(tvs1, tvs2)

    def test_contain(self):
        self.assertEqual(True, 3 in IntervalSet.parse_from_str('(2, 5)'))
        self.assertEqual(False, 2 in IntervalSet.parse_from_str('(2, 5)'))
        self.assertEqual(False, 5 in IntervalSet.parse_from_str('(2, 5)'))
        self.assertEqual(True, 2 in IntervalSet.parse_from_str('[2, 5)'))
        self.assertEqual(True, 5 in IntervalSet.parse_from_str('(2, 5]'))
        self.assertEqual(True, [2, 5, False, True] in IntervalSet.parse_from_str('(2, 5]'))
        self.assertEqual(True, [2, 5, False, True] in IntervalSet.parse_from_str(
            '(1, 9) | (6, 8)'))
        self.assertEqual(False, [2, 10, False, True] in IntervalSet.parse_from_str(
            '(1, 9) | (6, 8)'))
        self.assertEqual(False, [7, 8, False, True] in IntervalSet.parse_from_str(
            '(1, 5) | 7 | (8, 10)'))
        self.assertEqual(False, Interval([7, 8, False, True]) in IntervalSet.parse_from_str(
            '(1, 5) | 7 | (8, 10)'))


class TestUnion(unittest.TestCase):

    def test_basic(self):
        # 下面几个用例测试特殊情况
        self.assertEqual('(2, 8)',
                         str(IntervalSet.union(*[IntervalSet.parse_from_str(e) for e in [
                             '(2, 8)',
                         ]])))
        self.assertEqual('(-inf, inf)',
                         str(IntervalSet.union(*[IntervalSet.parse_from_str(e) for e in [
                             '(2, 8)',
                             '(-inf, inf)',
                         ] * 3])))
        self.assertEqual('(-inf, inf)',
                         str(IntervalSet.union(*[IntervalSet.parse_from_str(e) for e in [
                             '(-inf, inf)',
                             '(2, 8)',
                         ] * 3])))
        self.assertEqual('(-inf, inf)',
                         str(IntervalSet.union(*[IntervalSet.parse_from_str(e) for e in [
                             '(-inf, 2)',
                             '(0, inf)',
                         ] * 3])))
        # 该用例测试三组及以上的情况
        self.assertEqual('(-inf, -100) | (0, 9) | (10, 19) | (20, 29) | (100, inf)',
                         str(IntervalSet.union(
                             *[IntervalSet.parse_from_str(e) for e in [
                                 '(5, 9) | (15, 19) | (25, 29)',
                                 '(0, 3) | (10, 13) | (20, 23)',
                                 '(2, 6) | (12, 16) | (22, 26)',
                                 '(-inf, -100) | (100, inf)'
                             ] * 3])))
        # 该用例测试 10 种子场景(外切2 远离2 右侧内切及包含3 右侧内切及包含3)
        self.assertEqual('(12, 18) | (22, 28) | (32, 39) '
                         '| [112, 118) | [122, 128) | (131, 140) '
                         '| (212, 218) | (222, 228) | (231, 238) '
                         '| (312, 318] | (322, 328] | (331, 339) '
                         '| (412, 418) | (418, 419) | (422, 429) | (432, 439) '
                         '| (513, 518) | (518, 519) | (522, 529] | (531, 538] '
                         '| (612, 615) | (618, 619) | [622, 625) | (628, 629)',
                         str(IntervalSet.union(*[IntervalSet.parse_from_str(e) for e in [
                             '(12, 18) | (112, 118) | (212, 218) | (312, 318) | (412, 418) | (518, 519) | (618, 619)',
                             '(12, 15) | [112, 115) | (213, 218) | (313, 318] | (418, 419) | (513, 518) | (612, 615)',
                             '(22, 28) | [122, 128) | (222, 228) | (322, 328] | (422, 428) | [528, 529] | [622, 625)',
                             '(22, 28) | (122, 128) | (222, 228) | (322, 328) | [428, 429) | (522, 528) | (628, 629)',
                             '(32, 38) | (131, 132) | (232, 238) | (338, 339) | (432, 438] | (538, 538)',
                             '(32, 39) | (132, 139) | (231, 238) | (331, 338) | (438, 439) | (531, 538]',
                             '           [132, 140) |              (333, 338]',
                             # 左虚内切  左实内切+前回溯 右虚内切      右实内切+后回溯  右外切      左外切         左右远离
                         ] * 3])))

    def test_discrete(self):
        self.assertEqual('[5, 8) | [15, 19) | [25, 29) | (32, 35] | [38, 39) | (42, 47]',
                         str(IntervalSet.union(
                             *[IntervalSet.parse_from_str(e) for e in [
                                 ' 5     |  15      |  25      | (32, 35) | (42, 45)',
                                 ' 5     | (15, 17) | [25, 27) |  35      |  45     ',
                                 '(5, 7) | [16, 17) | [27, 29) | [38, 39) | (45, 47]',
                                 '(5, 8) | [17, 19)'
                             ]])))

    def test_inf(self):
        self.assertEqual('(-inf, inf)',
                         str(IntervalSet.union(
                             *[IntervalSet.parse_from_str(e) for e in [
                                 '(-inf, inf)',
                                 '(5, 8) | 9',
                                 '(2, 8) | 9',
                             ]])))
        self.assertEqual('(-inf, inf)',
                         str(IntervalSet.union(
                             *[IntervalSet.parse_from_str(e) for e in [
                                 '(-inf, inf)',
                                 '(5, 8) | 9',
                                 '(2, 8) | 9',
                                 '(-inf, inf)',
                             ]])))
        self.assertEqual('(-inf, -2) | (2, inf)',
                         str(IntervalSet.union(
                             *[IntervalSet.parse_from_str(e) for e in [
                                 '(-inf, -2) | (2, inf)',
                                 '(-inf, -5) | (8, inf)',
                                 '(-inf, -8) | (8, inf)',
                             ]])))

    def test_operator(self):
        a = IntervalSet.parse_from_str('-10')
        b = IntervalSet.parse_from_str('(-10, 2) | (5, 10)')
        c = IntervalSet.parse_from_str('(0, 6)')
        self.assertEqual('[-10, 10)', str(a | b | c))
        self.assertEqual('[-10, 10)', str(a.union(b, c)))
        self.assertEqual('-10', str(a))
        self.assertEqual('(-10, 2) | (5, 10)', str(b))
        self.assertEqual('(0, 6)', str(c))
        c.update()
        self.assertEqual('(0, 6)', str(c))
        b |= c
        a |= b
        self.assertEqual('(0, 6)', str(c))
        self.assertEqual('(-10, 10)', str(b))
        self.assertEqual('[-10, 10)', str(a))


class TestIntersection(unittest.TestCase):

    def test_basic(self):
        """

        :return:
        """
        self.assertEqual('(5, 10)',
                         str(IntervalSet.intersection(*[IntervalSet.parse_from_str(e) for e in [
                             '(-10, 10)',
                             '(5, 15)'
                         ]])))
        self.assertEqual('[5, 10)',
                         str(IntervalSet.intersection(*[IntervalSet.parse_from_str(e) for e in [
                             '(-10, 10)',
                             '[5, 15)'
                         ]])))
        self.assertEqual('(5, 10]',
                         str(IntervalSet.intersection(*[IntervalSet.parse_from_str(e) for e in [
                             '(-10, 10]',
                             '(5, 15)'
                         ]])))

        self.assertEqual('0 | (5, 8)',
                         str(IntervalSet.intersection(*[IntervalSet.parse_from_str(e) for e in [
                             '0 |(2, 4) |(5, 10]',
                             '0 |(5, 8)'
                         ]])))

    def test_operator(self):
        a = IntervalSet.parse_from_str('(-100, 100)')
        b = IntervalSet.parse_from_str('(-20, 20)')
        c = IntervalSet.parse_from_str('(-10, 10)')
        self.assertEqual('(-10, 10)', str(a & b & c))
        self.assertEqual('(-10, 10)', str(a.intersection(b, c)))
        self.assertEqual('(-100, 100)', str(a))
        self.assertEqual('(-20, 20)', str(b))
        self.assertEqual('(-10, 10)', str(c))
        c.intersection_update()
        c.intersection_update(IntervalSet.parse_from_str('(-inf, inf)'))
        self.assertEqual('(-10, 10)', str(c))
        b &= c
        a &= b
        self.assertEqual('(-10, 10)', str(c))
        self.assertEqual('(-10, 10)', str(b))
        self.assertEqual('(-10, 10)', str(a))

    def test_discrete(self):
        self.assertEqual('5',
                         str(IntervalSet.intersection(*[IntervalSet.parse_from_str(e) for e in [
                             '(-10, 5]',
                             '[5, 15)'
                         ]])))
        self.assertEqual('',
                         str(IntervalSet.intersection(*[IntervalSet.parse_from_str(e) for e in [
                             '(-10, 5)',
                             '[5, 15)'
                         ]])))

    def test_close(self):
        self.assertEqual('(5, 7]',
                         str(IntervalSet.intersection(*[IntervalSet.parse_from_str(e) for e in [
                             '(5, 7]',
                             '[5, 8)'
                         ]])))
        self.assertEqual('(5, 8)',
                         str(IntervalSet.intersection(*[IntervalSet.parse_from_str(e) for e in [
                             '[5, 8)',
                             '(5, 8)'
                         ]])))
        self.assertEqual('(5, 8]',
                         str(IntervalSet.intersection(*[IntervalSet.parse_from_str(e) for e in [
                             '[5, 8]',
                             '(5, 8]'
                         ]])))

    def test_inf(self):
        self.assertEqual('(-5, -3] | 0 | (5, 10)',
                         str(IntervalSet.intersection(*[IntervalSet.parse_from_str(e) for e in [
                             '(-inf, inf)',
                             '(-5, -3] | 0 | (5, 10)'
                         ]])))
        self.assertEqual('(-inf, -3] | 0 | (5, inf)',
                         str(IntervalSet.intersection(*[IntervalSet.parse_from_str(e) for e in [
                             '(-inf, inf)',
                             '(-inf, -3] | 0 | (5, inf)'
                         ]])))


class TestDifference(unittest.TestCase):

    def test_basic(self):
        """

        :return:
        """
        self.assertEqual('(5, 8)',
                         str(IntervalSet.parse_from_str('(5, 8)').difference()))
        self.assertEqual('',
                         str(IntervalSet.parse_from_str('(5, 8)').difference(
                             *[IntervalSet.parse_from_str(e) for e in [
                                 '(6, 9)',
                                 '(-inf, inf)',
                             ]])))
        self.assertEqual('[-2, 7)',
                         str(IntervalSet.parse_from_str('(-5, 7)').difference(
                             *[IntervalSet.parse_from_str(e) for e in [
                                 '(-20, -10) | (10, 20)',
                                 '(-20, -2) | (10, 20)',
                             ]])))
        self.assertEqual('[2, 3] | [4, 5) | (5, 6) | (7, 8] '
                         '| (22, 23] | [24, 25) | (25, 26) | (27, 28)',
                         str(IntervalSet.parse_from_str('[2, 8] | (22, 28)').difference(
                             *[IntervalSet.parse_from_str(e) for e in [
                                 '0 | (1, 2) | (3, 4) | 5 | [6, 7] | (8, 9) | (10, 11)',
                                 '20 | (21, 22) | (23, 24) | 25 | [26, 27] | (28, 29) | (30, 31)',
                             ]])))

        self.assertEqual('12 | [14, 17] | 18 | (34, 37) | [54, 57] | (74, 77)',
                         str(IntervalSet.parse_from_str('[12, 18] | [32, 38] | (52, 58) | (72, 78)').difference(
                             *[IntervalSet.parse_from_str(e) for e in [
                                 '(12, 14) | (17, 18)',
                                 '[32, 34] | [37, 38]',
                                 '(52, 54) | (57, 58)',
                                 '[72, 74] | [77, 78]',
                             ]])))

    def test_operator(self):
        a = IntervalSet.parse_from_str('(-100, 100)')
        b = IntervalSet.parse_from_str('(-20, 20)')
        c = IntervalSet.parse_from_str('(-10, 10)')
        self.assertEqual('(-100, -20] | [20, 100)', str(a - b - c))
        self.assertEqual('(-100, 100)', str(a))
        self.assertEqual('(-20, 20)', str(b))
        self.assertEqual('(-10, 10)', str(c))
        c.difference_update()
        c.difference_update(IntervalSet.parse_from_str('(10, 100)'))
        self.assertEqual('(-10, 10)', str(c))
        b -= c
        a -= b
        self.assertEqual('(-10, 10)', str(c))
        self.assertEqual('(-20, -10] | [10, 20)', str(b))
        self.assertEqual('(-100, -20] | (-10, 10) | [20, 100)', str(a))

    def test_discrete(self):
        self.assertEqual('12 | 18',
                         str(IntervalSet.parse_from_str('12 | 18 | 32 | 38').difference(
                             *[IntervalSet.parse_from_str(e) for e in [
                                 '(11, 12) | (18, 19)',
                                 '(31, 32] | [38, 39)',
                             ]])))
        self.assertEqual('10',
                         str(IntervalSet.parse_from_str('5 | 10').difference(
                             *[IntervalSet.parse_from_str(e) for e in [
                                 '(0, 8)',
                             ]])))

        self.assertEqual('5 | 8',
                         str(IntervalSet.parse_from_str('[5, 8]').difference(
                             *[IntervalSet.parse_from_str(e) for e in [
                                 '(5, 8)',
                             ]])))

    def test_close(self):
        self.assertEqual('(5, 8)',
                         str(IntervalSet.parse_from_str('[5, 8]').difference(
                             *[IntervalSet.parse_from_str(e) for e in [
                                 '5 | 8',
                             ]])))

    def test_inf(self):
        self.assertEqual('(-inf, -5] | (-3, 0) | (0, 5] | [10, inf)',
                         str(IntervalSet.parse_from_str('(-inf, inf)').difference(
                             *[IntervalSet.parse_from_str(e) for e in [
                                 '(-5, -3] | 0 | (5, 10)'
                             ]])))
        self.assertEqual('(-3, 0) | (0, 5)',
                         str(IntervalSet.parse_from_str('(-100, 100)').difference(
                             *[IntervalSet.parse_from_str(e) for e in [
                                 '(-inf, -3] | 0 | [5, inf)'
                             ]])))

        self.assertEqual('(0, 2] | [9, 10) | (100, 200]',
                         str(IntervalSet.parse_from_str('(0, 10) | (100, inf)').difference(
                             *[IntervalSet.parse_from_str(e) for e in [
                                 '(2, 7) | (200, inf)',
                                 '[4, 9) | (300, inf)',
                             ]])))


class TestSymmetricDifference(unittest.TestCase):

    def test_basic(self):
        """

        :return:
        """
        self.assertEqual('(6, 9)',
                         str(IntervalSet.parse_from_str('(6, 9)').symmetric_difference(
                             *[IntervalSet.parse_from_str(e) for e in [
                                 '',
                                 '',
                             ]])))
        self.assertEqual('(1, 2] | [3, 4) | (5, 6) | [7, 8)',
                         str(IntervalSet.parse_from_str('(2, 4) | (5, 7)').symmetric_difference(
                             *[IntervalSet.parse_from_str(e) for e in [
                                 '(1, 3) | [6, 8)',
                             ]])))
        self.assertEqual('(2, 5] | [7, 8) '
                         '| (12, 16) | [17, 19) '
                         '| (22, 29) '
                         '| (32, 37) | [38, 39) '
                         '| (42, 45) | 47 '
                         '| (52, 56) '
                         '| (62, 68) '
                         '| (72, 77) | [78, 79)',
                         str(IntervalSet.parse_from_str(
                             '(2, 5) | (12, 15) | (22, 25) | (32, 35) | (42, 45) | (52, 55) | (62, 65) | (72, 75)')
                             .symmetric_difference(*[
                             IntervalSet.parse_from_str(e) for e in [
                                 '[5, 7) | [15, 17) | [25, 27) | [35, 37) | [45, 47) | [55, 57) | [65, 67) | [75, 77)',
                                 '(5, 7) | [16, 17) | [27, 29) | [38, 39) | [45, 47] | [56, 57) | [67, 68) | [78, 79)',
                                 '(5, 8) | [17, 19)'
                             ]])))
        self.assertEqual('2 | [3, 5] | 7',
                         str(IntervalSet.parse_from_str('(2, 4) | (5, 7)').symmetric_difference(
                             *[IntervalSet.parse_from_str(e) for e in [
                                 '[2, 3) | [4, 7]',
                             ]])))
        self.assertEqual('(2, 3) | (4, 7) | (12, 13] | [14, 17)',
                         str(IntervalSet.symmetric_difference(
                             *[IntervalSet.parse_from_str(e) for e in [
                                 '(2, 7) | (12, 17)',
                                 '[3, 4] | (13, 14)',
                             ]])))

    def test_discrete(self):
        self.assertEqual('[7, 8) | [15, 16) | [17, 19) | (25, 29) | (32, 35] | [38, 39) | (42, 47]',
                         str(IntervalSet.symmetric_difference(
                             *[IntervalSet.parse_from_str(e) for e in [
                                 '(5, 5) | (15, 15) | (25, 25) | (32, 35) | (42, 45)',
                                 '(5, 5) | (15, 17) | [25, 27) | (35, 35) | (45, 45)',
                                 '(5, 7) | [16, 17) | [27, 29) | [38, 39) | (45, 47]',
                                 '(5, 8) | [17, 19)'
                             ]])))

    def test_close(self):
        self.assertEqual('(8, 9) | 15 | [18, 19) | (22, 25] | 27 | (32, 35)',
                         str(IntervalSet.symmetric_difference(
                             *[IntervalSet.parse_from_str(e) for e in [
                                 '(5, 7) | (15, 17) | (22, 27) | (32, 37]',
                                 '(5, 8] | (15, 18) | (25, 27) | [35, 37)',
                                 '(5, 9) | [15, 19) | (27, 27) | (37, 37)',
                             ]])))

    def test_inf(self):
        self.assertEqual('(-inf, 2] | [8, 9) | (9, inf)',
                         str(IntervalSet.symmetric_difference(
                             *[IntervalSet.parse_from_str(e) for e in [
                                 '(-inf, inf)',
                                 '(5, 8) | 9',
                                 '(2, 8) | 9',
                             ]])))
        self.assertEqual('',
                         str(IntervalSet.symmetric_difference(
                             *[IntervalSet.parse_from_str(e) for e in [
                                 '(-inf, inf)',
                                 '(5, 8) | 9',
                                 '(2, 8) | 9',
                                 '(-inf, inf)',
                             ]])))
        self.assertEqual('[-5, -2) | (2, 8]',
                         str(IntervalSet.symmetric_difference(
                             *[IntervalSet.parse_from_str(e) for e in [
                                 '(-inf, -2) | (2, inf)',
                                 '(-inf, -5) | (8, inf)',
                                 '(-inf, -8) | (8, inf)',
                             ]])))

    def test_operator(self):
        a = IntervalSet.parse_from_str('(-100, 100)')
        b = IntervalSet.parse_from_str('(-20, 20)')
        c = IntervalSet.parse_from_str('(-10, 10)')
        self.assertEqual('(-20, -10] | [10, 20)', str(b ^ c))
        self.assertEqual('(-100, -20] | (-10, 10) | [20, 100)', str(a ^ b ^ c))
        self.assertEqual('(-100, 100)', str(a))
        self.assertEqual('(-20, 20)', str(b))
        self.assertEqual('(-10, 10)', str(c))
        c.symmetric_difference_update(IntervalSet.parse_from_str(''))
        self.assertEqual('(-10, 10)', str(c))
        b ^= c
        a ^= b
        self.assertEqual('(-10, 10)', str(c))
        self.assertEqual('(-20, -10] | [10, 20)', str(b))
        self.assertEqual('(-100, -20] | (-10, 10) | [20, 100)', str(a))


if __name__ == '__main__':
    unittest.main()
