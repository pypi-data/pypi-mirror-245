#! -*- coding:utf-8 -*

import bisect

try:
    from typing import List, Tuple, Union, Protocol
except ImportError:
    from typing import Union, Protocol

    List, Tuple = list, tuple


class Comparable(Protocol):
    def __lt__(self, other) -> bool:
        ...

    def __le__(self, other) -> bool:
        ...

    def __eq__(self, other) -> bool:
        ...

    def __gt__(self, other) -> bool:
        ...

    def __ge__(self, other) -> bool:
        ...


class Interval(object):
    """type of interval object.

    """

    def __init__(self, arr: list, /):
        """

        :param arr: a list which length is 5, elements from 0 to 4 respectively are
            [left, right, include_left, include_right].

            examples:
            case: [2, 5, True, False], represent an interval [2, 5)
                arr[2] is True, so 2 is close, likely 5 is open
            case: [3, 3, True, True], represent an interval [3, 3], or can said is a discrete point 3
                note: in this case, arr[2] and arr[3] must be True
            case: [NEG_INF, 3, False, True], represent an interval (-inf, 3]
                note: for NEG_INF and INF, its include must be False
            case: [NEG_INF, INF, False, False], represent an interval (-inf, inf)
        """
        self.arr = arr

    @property
    def left(self) -> Comparable:
        """left of interval.

        :return:
        """
        return self.arr[0]

    @property
    def include_left(self) -> bool:
        """whether left itself be included.

        :return:
        """
        return self.arr[2]

    @property
    def right(self) -> Comparable:
        """right of interval.

        :return:
        """
        return self.arr[1]

    @property
    def include_right(self) -> bool:
        """whether right itself be included.

        :return:
        """
        return self.arr[3]

    def __repr__(self):
        """Return repr(self).

        :return:
        """
        if self.left == self.right:
            return str(self.left)
        val = str(self.left) + ', ' + str(self.right)
        if self.include_left:
            val = '[' + val
        else:
            val = '(' + val
        if self.include_right:
            val += ']'
        else:
            val += ')'
        return val


class NegativeInf(object):
    """Type of negative infinite.

    """

    def __repr__(self):
        return '-inf'

    def __eq__(self, other):
        return other is self or isinstance(other, NegativeInf)

    def __lt__(self, other):
        """Return self < other.

        :param other:
        :return:
        """
        return self != other

    def __le__(self, other):
        """Return self <= other.

        :param other:
        :return:
        """
        return True

    def __gt__(self, other):
        """Return self > other.

        :param other:
        :return:
        """
        return False

    def __ge__(self, other):
        """Return self >= other.

        :param other:
        :return:
        """
        return self == other


class PositiveInf(object):
    """Type of positive infinite.

    """

    def __repr__(self):
        return 'inf'

    def __eq__(self, other):
        return self is other or isinstance(other, PositiveInf)

    def __lt__(self, other):
        """Return self < other.

        :param other:
        :return:
        """
        return False

    def __le__(self, other):
        """Return self <= other.

        :param other:
        :return:
        """
        return self == other

    def __gt__(self, other):
        """Return self > other.

        :param other:
        :return:
        """
        return self != other

    def __ge__(self, other):
        """Return self >= other.

        :param other:
        :return:
        """
        return True


NEG_INF = NegativeInf()
POS_INF = PositiveInf()


class IntervalHandler(object):
    """Type of interval handler.

    """

    def __init__(self, ):
        # 存在中间区域 (a, b)  其中，a 和 b 都不是无穷
        self._mid_interval_arrays: List[list] = []
        # 标记该区间集是个无限集 (-inf, inf)
        self.inf_flag: bool = False
        # 存在负无穷区间 (-inf, neg_inf_value)
        self._neg_inf_values: list = []
        # 存在正无穷区间 (inf_value, inf)
        self._inf_values: list = []

    def add_interval(self, left: Comparable, right: Comparable,
                     /, *,
                     include_left: bool = False,
                     include_right: bool = False):
        """Add an interval.

        :param left:
        :param right:
        :param include_left:
        :param include_right:
        :return:
        """
        if self.inf_flag:
            return
        if left is not NEG_INF:
            if right is not POS_INF:
                if left <= right:
                    # (3, 5) (3, 3)
                    if left == right:
                        include_left, include_right = True, True
                    self._mid_interval_arrays.append([left, right, include_left, include_right])
                    return
                    # (3, 2)
                raise ValueError("Interval '%s' error, must left <= right."
                                 % (Interval([left, right, include_left, include_right]),))
            # (3, inf)
            self._inf_values.append((left, include_left))
            return

        if right is not POS_INF:
            # (-inf, -3)
            self._neg_inf_values.append((right, include_right))
            return

        # (-inf, inf)
        self.inf_flag = True

    def join_neg_inf_mid_inf(self, ) -> List[list]:
        """Join the negative infinity region, the middle region, and the positive infinity region.

        :return:
        """
        if self.inf_flag:
            return [[NEG_INF, POS_INF, False, False]]

        mid_intervals = sorted(self._mid_interval_arrays)
        if self._neg_inf_values:
            neg_inf_value, neg_inf_value_included = sorted(self._neg_inf_values)[-1]
            # 存在负无穷区间 (-inf, -3) (-inf, -3]
            # 注意，此处不能和 right 进行比较，考虑 mid_intervals: [(2, 7), (3, 4)], 遇到 (-inf, 5)
            pos = bisect.bisect_left([e[0] for e in mid_intervals], neg_inf_value, )
            """
            a. [-10, -5, -3, 2, 5]  pos = 2
            b. [-10, -5, 2, 5]  pos = 2
            c. [-10, -5,]  pos = 2
            d. [2, 5]  pos = 0
            e. []  pos = 0
            a. value[:pos] < neg_inf_value <= value[pos:]
            """
            del mid_intervals[:pos]
            mid_intervals.insert(0, [NEG_INF, neg_inf_value, False, neg_inf_value_included])
        if self._inf_values:
            inf_value, inf_value_included = sorted(self._inf_values)[0]
            # 存在正无穷区间 (5, inf) [5, inf)
            # 注意，此处不能和 right 进行比较，考虑 mid_intervals: [(-inf, 3) ], 遇到 (-3, inf)
            pos = bisect.bisect_right([e[0] for e in mid_intervals], inf_value, )
            """
            a. [-3, 2, 5, 10, 12]  pos = 3  
            b. [-3, 2, 10, 12]  pos = 2
            c. [10, 12]  pos = 0
            d. [-3, 2]  pos = 2
            e. []  pos = 0
            a. value[:pos] <= inf_value < value[pos:]
            """
            del mid_intervals[pos:]
            mid_intervals.append([inf_value, POS_INF, inf_value_included, False])
        return mid_intervals


class IntervalSet(object):
    """Type of Interval set.
    """

    def __init__(self, interval_arrays: List[Union[list, Comparable]] = None, /, *, merge: bool = True):
        """

        :param interval_arrays: list of interval, every interval can be one of follows:
            1.a list which length is 4, elements from 0 to 3 respectively are
                [left, right, include_left, include_right].
                left and right must be Comparable object.

            examples:
            case: [2, 5, True, False], represent an interval [2, 5)
                arr[2] is True, so 2 is close, likely 5 is open
            case: [3, 3, True, True], represent an interval [3, 3], or can said is a discrete point 3
                note: in this case, arr[2] and arr[3] must be True
            case: [NEG_INF, 3, False, True], represent an interval (-inf, 3]
                note: for NEG_INF and INF, its include must be False
            case: [NEG_INF, INF, False, False], represent an interval (-inf, inf)

            2.a single value, like 3, equivalent to [3, 3, True, True].

        :param merge: default True, unless you sure the interval_arrays you passed in is ordered, simplest, and
            all interval is list form (as show following), you can set it to False.
            - ordered: like [[3, 5, False, False], [2, 4, False, False]] is not ordered,
                because in iterm of comparison, first interval > second interval
            - simplest: like [3, 5, False, False], [4, 6, False, False]] is not simplest,
                because first and second can be joined as [3, 6, False, False]
            - all interval is list form: like [3, 5, False, False], 7] is not satisfied,
                because the second interval is not list form
        """
        self.interval_arrays: List[list] = interval_arrays
        self.inf_flag = False
        self.interval_handler: IntervalHandler = IntervalHandler()
        self.reset_interval_arrays(interval_arrays or [], merge=merge)

    @property
    def intervals(self) -> List[Interval]:
        """Return all intervals of self.

        :return:
        """
        return [Interval(e) for e in self.interval_arrays]

    @classmethod
    def inf_tvs(cls) -> 'IntervalSet':
        """Return a new infinite interval set.

        :return:
        """
        return cls([[NEG_INF, POS_INF, False, False]], merge=False)

    @classmethod
    def empty_tvs(cls) -> 'IntervalSet':
        """Return a new empty interval set.

        :return:
        """
        return cls([], merge=False)

    def copy(self, ) -> 'IntervalSet':
        """Return a copy of self.
        Note: later, modify to new will not affect self, versa.

        :return:
        """
        return IntervalSet([e.copy() for e in self.interval_arrays], merge=False)

    def reset_interval_arrays(self, interval_arrays: List[list], /, *, merge: bool = True):
        """Reset self with new interval_arrays.

        :param interval_arrays: new interval_arrays
        :param merge: whether merge or not
        :return:
        """
        if interval_arrays and merge:
            interval_arrays.sort()
            self._merge(interval_arrays)
        self.interval_arrays = interval_arrays
        # 标记该区间集是个无限集 (-inf, inf)
        if self._is_inf(interval_arrays):
            self.inf_flag = True

    def __len__(self):
        return len(self.intervals)

    def is_empty(self) -> bool:
        """Return True if self is empty, otherwise False.

        :return:
        """
        return len(self.intervals) == 0

    @classmethod
    def _is_inf(cls, interval_arrays: List[list], /) -> bool:
        return len(interval_arrays) == 1 and interval_arrays[0][0] == NEG_INF and interval_arrays[0][1] == POS_INF

    @classmethod
    def parse_from_str(cls, tvs_str: str, /) -> 'IntervalSet':
        """Return an interval set parsed from a string, which element only can be int.

        :param tvs_str:
        :return:
        """
        interval_handler = IntervalHandler()
        for i, group in enumerate(tvs_str.split('|')):
            group = group.strip()
            if not group:
                continue
            if group.startswith(('(', '[')):
                tmp = group[1:-1].split(',')
                if len(tmp) != 2:
                    raise ValueError(
                        "Interval '%s' error, not match like (left, right) or discrete_point." % (group,))
                left, right = [e.strip() for e in tmp]
                left = int(left) if left != '-inf' else NEG_INF
                right = int(right) if right != 'inf' else POS_INF
                interval_handler.add_interval(
                    left, right, include_left=group[0] == '[', include_right=group[-1] == ']')
                continue
            value = int(group)
            interval_handler.add_interval(value, value, include_left=True, include_right=True)
        interval_arrays = interval_handler.join_neg_inf_mid_inf()
        return cls(interval_arrays)

    @classmethod
    def _merge(cls, interval_arrays: List[list], /, *, start: int = 0, end: int = None):
        """合并，合并能够合并的区间
        1.前提：intervals 是排序过的，且：
            -.(left, right) 严格升序
            -.当相邻的两个区间的 (left, right) 相等时，按 (include_left, include_right) 排序，即
                (f, f), (f, t), (t, f), (t, t)
        2.部分排序时，必须保证 [:start] 和 [end:] 两部分已合并过

        :param interval_arrays: intervals[start: end]之间的需要合并
        :param start: 起始下标
        :param end: start + N，N≥1
        :return:
        """
        if not interval_arrays:
            return []
        start = max(min(start, len(interval_arrays) - 1) - 2, 0)
        merged_interval_arrays: List[list] = [interval_arrays[start]]
        if end is None:
            end = len(interval_arrays)
        else:
            end = min(max(end, start + 1) + 2, len(interval_arrays))
        for i in range(start + 1, end):
            cls._merge_new(merged_interval_arrays, interval_arrays[i])

        interval_arrays[start: end] = merged_interval_arrays

    @classmethod
    def _merge_new(cls, new_arrays: List[list], new: list, /):
        """
        总计如下情况：
        cu: (2, 8)
        一、不相交或者外切
        1. cu.left, cu.right < new.left, new.right  (10, y) 右侧远离
        2. cu.left, cu.right == new.left, new.right (8, y)  右侧外切
        3. new.left, new.right < cu.left, cu.right  (x, 0)  左侧远离
        4. new.left, new.right == cu.left, cu.right (x, 2)  左侧外切
        二、左端
        1. new.left < cu.left  (-3, y)
        2. cu.left == new.left (2, y)  左侧内切
        3. cu.left < new.left  (4, y)
        三、右端
        1. new.right < cu.right  (x, 6)
        2. cu.right == new.right (x, 8)  右侧内切
        3. cu.right < new.right  (x, 10)

        :param new_arrays:
        :param new:
        :return: 下一轮的 cu
        """
        if new_arrays[-1][1] < new[0]:
            # new: (10, y) 右侧远离
            new_arrays.append(new.copy())
            return
        cu = new_arrays[-1]
        if cu[1] == new[0]:
            # 右侧外切
            # new: (8, y) 8<=y
            if cu[3] or new[2]:
                # 两个区间连接
                cu[1] = new[1]
                cu[3] = new[3]
                return
            new_arrays.append(new.copy())
            return

        if cu[0] == new[0]:
            # 左侧内切
            # cu: (2, x) 2<=x new: (2, y) 2<=y
            cu[2] = cu[2] or new[2]
            if cu[2] and len(new_arrays) > 1 and new_arrays[-2][1] == cu[0]:
                # 触发连接
                cu[0] = new_arrays[-2][0]
                cu[2] = new_arrays[-2][2]
                del new_arrays[-2]

        if cu[1] < new[1]:
            # 右侧外包含  new: (x, 10)
            cu[1] = new[1]
            cu[3] = new[3]
        elif new[1] == cu[1]:
            # 右侧内切
            cu[3] = cu[3] or new[3]

    def __getitem__(self, item: int, /) -> Interval:
        try:
            return self.intervals[item]
        except IndexError:
            raise IndexError("IntervalSet index out of range.")

    def __repr__(self):
        lis = []
        for interval in self:
            lis.append(str(interval))

        return ' | '.join(lis)

    def add(self, left: Comparable, right: Comparable, include_left: bool = False, include_right: bool = False, /):
        """Add an interval into self, will be merged automatically.

        :param left:
        :param right:
        :param include_left:
        :param include_right:
        :return:

        examples:
        >>> tvs1 = IntervalSet.parse_from_str('(0, 3] | (100, inf)')
        >>> tvs1.add(3, 4)
        >>> tvs1
        (0, 4) | (100, inf)
        >>> tvs1.add(4, 4)
        >>> tvs1
        (0, 4] | (100, inf)
        """
        if left > right:
            raise ValueError("Interval '%s' error, must left <= right."
                             % (Interval([left, right, include_left, include_right]),))
        elif left == right:
            include_left = include_right = True
        self._join_many_sorted_arr_into_longest(self.interval_arrays, [[left, right, include_left, include_right]])
        self.__dict__ = self.__class__(self.interval_arrays, merge=False).__dict__

    @classmethod
    def _join_many_sorted_arr_into_longest(cls, longest_arr: List[list], /, *other_arrays: List[list],
                                           merge: bool = True):
        """合并多个有序数组到 longest_arr 中
        内部会视情况选择相对较高效的方法进行合并。

        :param longest_arr: 必须有序
        :param other_arrays: 必须有序
        :param merge:
        :return:
        """
        if not other_arrays:
            return longest_arr
        if len(longest_arr) >= 100:
            interval_min = min(arr[0] for arr in other_arrays)
            interval_max = max(arr[-1] for arr in other_arrays)
            lo, hi = bisect.bisect_left(longest_arr, interval_min), bisect.bisect_right(longest_arr, interval_max)
            if hi - lo <= len(longest_arr) * 0.618:
                """总宽度 ≤ longest_tvs_arr 的长度 * 0.618
                此时，只需要对 longest_arr 中部分做处理即可
                """
                mid = longest_arr[lo: hi]
                for arr in other_arrays:
                    mid += arr
                mid.sort()
                longest_arr[lo:hi] = mid
                if merge:
                    cls._merge(longest_arr, start=lo, end=lo + len(mid) + 1)
                return longest_arr
            if sum(len(arr) for arr in other_arrays) <= min(100, int(len(longest_arr) / 10)):
                # 其他 arr 总长度 ≤ longest_tvs_arr 的长度 / 10，且 ≤ 100
                cls._merge_arr_into_other_by_bisect(longest_arr, other_arrays, merge=merge)
                return longest_arr

        for arr in other_arrays:
            longest_arr += arr
        longest_arr.sort()
        if merge:
            cls._merge(longest_arr)
        return longest_arr

    @classmethod
    def _merge_arr_into_other_by_bisect(cls, longest_arr: List[list], other_arrays: Tuple[List[list]],
                                        /, *,
                                        merge: bool = True):
        for arr in other_arrays:
            for v in arr:
                pos = bisect.bisect_left(longest_arr, v)
                longest_arr.insert(pos, v)
                if merge:
                    cls._merge(longest_arr, start=pos, end=pos + 1)

    def union(self, *tvs_lis: 'IntervalSet', ) -> 'IntervalSet':
        """Return union of several interval sets as a new interval set.

        :param tvs_lis: list of interval set
        :return:

        examples:
        >>> tvs1 = IntervalSet.parse_from_str('(0, 3] | (100, inf)')
        >>> tvs2 = IntervalSet.parse_from_str('(2, 5) | (-inf, -100)')
        >>> tvs3 = IntervalSet.parse_from_str('[4, 9) | 0')
        >>> tvs1.union(tvs2, tvs3)
        (-inf, -100) | [0, 9) | (100, inf)
        >>> tvs1.union()  # also can passed in zero other interval sets
        (0, 3] | (100, inf)
        """
        if not tvs_lis:
            return self.copy()
        if self.inf_flag or any(tvs.inf_flag for tvs in tvs_lis):
            # 如果有任一区间为无限集
            return self.inf_tvs()

        new_intervals = self.interval_arrays
        for other in tvs_lis:
            new_intervals = self._calc_union(new_intervals, other.interval_arrays)
            if self._is_inf(new_intervals):
                return self.inf_tvs()

        return self.__class__(new_intervals, merge=False)

    @classmethod
    def _calc_union(cls, interval_arrays_1: List[list], interval_arrays_2: List[list], ) \
            -> List[list]:
        """

        :param interval_arrays_1:
        :param interval_arrays_2:
        :return:
        """
        i, j = 0, 0
        arrays_unionised: List[list] = [[NEG_INF, NEG_INF, False, False]]
        new1, new2 = None, None
        while True:
            if new1 is None and i < len(interval_arrays_1):
                new1 = interval_arrays_1[i]
                i += 1
            if new2 is None and j < len(interval_arrays_2):
                new2 = interval_arrays_2[j]
                j += 1
            if new1 is not None:
                if new2 is not None:
                    if new1 < new2:
                        new, new1 = new1, None
                    elif new2 < new1:
                        new, new2 = new2, None
                    else:
                        new, new1, new2 = new1, None, None
                else:
                    new, new1 = new1, None
            elif new2 is not None:
                new, new2 = new2, None
            else:
                break
            # 接下来将 cu 和 new 合并
            # 在如上逻辑前提下，必定有：cu.left <= new.left
            cls._merge_new(arrays_unionised, new)

        if arrays_unionised[0][1] == NEG_INF:
            del arrays_unionised[0]
        remain = interval_arrays_1[i:] + interval_arrays_2[j:]
        last = arrays_unionised[-1]
        if remain and last[3] and last[1] == remain[0]:
            # cu 和 remain[0] 合并
            last[1] = remain[1]
            last[3] = remain[3]
            del remain[0]
        arrays_unionised.extend(remain)
        return arrays_unionised

    def __or__(self, other: 'IntervalSet', ) -> 'IntervalSet':
        """Return self | other.

        :param other:
        :return:
        """
        return self.union(other)

    def __ior__(self, other: 'IntervalSet', ) -> 'IntervalSet':
        """Return self |= other.

        :param other:
        :return:
        """
        self.__dict__ = self.union(other).__dict__
        return self

    def update(self, *tvs_lis: 'IntervalSet'):
        """Update self with the union of self and all interval sets in tvs_lis.

        :param tvs_lis: list of interval set.
        :return:
        """
        self.__dict__ = self.union(*tvs_lis).__dict__

    def intersection(self, *tvs_lis: 'IntervalSet') -> 'IntervalSet':
        """Return intersection between self and other interval set in tvs_lis.

        :param tvs_lis: list of interval set
        :return:

        examples:
        >>> tvs1 = IntervalSet.parse_from_str('(0, 5] | (100, inf)')
        >>> tvs2 = IntervalSet.parse_from_str('(2, 7) | (200, inf)')
        >>> tvs3 = IntervalSet.parse_from_str('[4, 9) | (300, inf)')
        >>> tvs1.intersection(tvs2, tvs3)
        [4, 5] | (300, inf)
        >>> tvs1.intersection()  # also can passed in zero other interval sets
        (0, 5] | (100, inf)
        """
        tvs_lis = [self] + list(tvs_lis)
        if not tvs_lis or any(tvs.is_empty() for tvs in tvs_lis):
            # 如果有任一个是空集
            return self.__class__()
        if len(tvs_lis) == 1:
            # 如果只有一个 tvs
            return tvs_lis[0].copy()
        """剪枝，将＜最大左端的区间移除掉，避免无效运算，右端同样
        先找出最大的左端点，最小的右端点
        假设 left_max: -5  right_min: 7
        (f, f), (f, t), (t, f), (t, t)

        对于左端，任意 arr[1] ＜ left_max 的区间都是无效的，例如 (l, r)，只要 r < -5，注意 r == -5 的有可能产生交点
        可以按 (-5, -5, f, f) 进行靠左二分查找，pos < lo 的都是无效区间？
        但是有可能：..., (-8, -3), (-2, 2), ...
        所以：有可能 pos = lo - 1 也有效。

        同样，对于右端，任何 right_min ＜ arr[0] 的区间都是无效的，按 (7, 7, True, True) 进行靠右二分查找
        但是有可能：..., (3, 6), [7, 10), ... 此时 l == 7 的有可能产生交点
        所以调整为 按 (7, INF, True, True) 进行靠右二分查找，则 pos >= hi 的必定是无效区间.

        有可能 hi - lo == 0, 此时意味着：
        区间集 A：(-5, 7)
        区间集 B：(-20, -10), (10, 20)
        即：对于B来说，与 [left_max, right_min] 无交集，此时求交集结果必定为空。


        :param tvs_lis:
        :return:
        """
        left_max = max(tvs.interval_arrays[0][0] for tvs in tvs_lis)
        interval_left_max = [left_max, left_max, False, False, 0]
        right_min = min(tvs.interval_arrays[-1][1] for tvs in tvs_lis)
        interval_right_min = [right_min, POS_INF, True, True, 0]
        valid_interval_arrays_lis: List[Tuple[List[list], int, int]] = []

        for tvs in tvs_lis:
            lo = bisect.bisect_left(tvs.interval_arrays, interval_left_max)
            if lo > 0 and left_max <= tvs.interval_arrays[lo - 1][1]:
                lo -= 1
            hi = bisect.bisect_right(tvs.interval_arrays, interval_right_min)
            if lo == hi:
                return self.__class__()
            valid_interval_arrays_lis.append((tvs.interval_arrays, lo, hi))

        valid_interval_arrays_lis.sort(key=lambda e: len(e[0]))
        first = valid_interval_arrays_lis[0]
        new_intervals = first[0][first[1]:first[2]]
        for other in valid_interval_arrays_lis[1:]:
            new_intervals = self._calc_intersection(new_intervals, other[0], other[1], other[2])
            if not new_intervals:
                return self.__class__()

        return self.__class__(new_intervals, merge=False)

    @classmethod
    def _calc_intersection(cls, interval_arrays_1: List[list], interval_arrays_2: List[list], start: int, end: int, ) \
            -> List[list]:
        """

        :param interval_arrays_1:
        :param interval_arrays_2:
        :param start:
        :param end:
        :return:
        """
        intersect_arrays = []
        i, j = 0, start
        end = end or len(interval_arrays_2)
        while i < len(interval_arrays_1):
            cu = interval_arrays_1[i]
            # 该变量标记，cu[0] < new[0]
            while j < end and interval_arrays_2[j][0] <= cu[1]:
                new = interval_arrays_2[j]
                """总计如下情况：
                cu: (2, 5) 
                一、不相交或者外切
                1. cu.left, cu.right < new.left, new.right  (7, y)
                2. cu.left, cu.right == new.left, new.right (5, y)
                3. new.left, new.right < cu.left, cu.right  (x, 0) 
                4. new.left, new.right == cu.left, cu.right (x, 2) 
                二、左端
                1. new.left < cu.left  (-3, y)
                2. cu.left == new.left (2, y)
                3. cu.left < new.left  (4, y)
                三、右端
                1. new.right < cu.right  (x, 3)  
                2. cu.right == new.right (x, 5)
                3. cu.right < new.right  (x, 7)
                """
                if new[1] < cu[0]:
                    # new: (x, 1)  new 下一个
                    j += 1
                    continue
                if new[1] == cu[0]:
                    if cu[2] and new[3]:
                        # new: (x, 2]  孤立点 2 被析出，且与后续必不相交
                        intersect_arrays.append([new[1], new[1], True, True])
                    j += 1
                    continue
                if cu[1] == new[0]:
                    if new[2] and cu[3]:
                        # new: [5, y)  孤立点 5 被析出，且与后续必不相交
                        intersect_arrays.append([new[0], new[0], True, True])
                    break

                if cu[0] < new[0]:
                    # new: (3, y)
                    left = new[0]
                    include_left = new[2]
                elif new[0] < cu[0]:
                    # new: (0, y)
                    left = cu[0]
                    include_left = cu[2]
                else:
                    # new: (2, y)
                    left = cu[0]
                    include_left = cu[2] and new[2]

                if new[1] < cu[1]:
                    # new: (x, 3)
                    right = new[1]
                    include_right = new[3]
                elif new[1] > cu[1]:
                    # new: (x, 6)
                    right = cu[1]
                    include_right = cu[3]
                else:
                    # new: (x, 5)
                    right = new[1]
                    include_right = new[3] and cu[3]

                if left <= right:
                    intersect_arrays.append([left, right, include_left, include_right])

                if cu[1] < new[1]:
                    break

                j += 1

            i += 1

        return intersect_arrays

    def __and__(self, other: 'IntervalSet', ) -> 'IntervalSet':
        """Return self & other.

        :param other:
        :return:
        """
        return self.intersection(other)

    def __iand__(self, other: 'IntervalSet', ) -> 'IntervalSet':
        """Return self &= other.

        :param other:
        :return:
        """
        self.__dict__ = self.intersection(other).__dict__
        return self

    def intersection_update(self, *tvs_lis: 'IntervalSet'):
        """Update self with the intersection between self and other interval set in tvs_lis.

        :param tvs_lis: list of interval set
        :return:

        examples:
        >>> tvs1 = IntervalSet.parse_from_str('(0, 5] | (100, inf)')
        >>> tvs2 = IntervalSet.parse_from_str('(2, 7) | (200, inf)')
        >>> tvs3 = IntervalSet.parse_from_str('[4, 9) | (300, inf)')
        >>> tvs1.intersection_update(tvs2, tvs3)
        >>> tvs1
        [4, 5] | (300, inf)
        >>> tvs1.intersection_update()  # also can passed in zero other interval sets
        >>> tvs1
        [4, 5] | (300, inf)
        """
        self.__dict__ = self.intersection(*tvs_lis).__dict__

    def difference(self, *other_tvs_lis: 'IntervalSet', ) -> 'IntervalSet':
        """Return the difference of self from other interval sets as a new set.

        For any interval in the return interval set, satisfy: belongs to self, but
        does not belong to any interval set in tvs_lis.


        :param other_tvs_lis: list of interval set
        :return:

        examples:
        >>> tvs1 = IntervalSet.parse_from_str('(0, 10) | (100, inf)')
        >>> tvs2 = IntervalSet.parse_from_str('(2, 7) | (200, inf)')
        >>> tvs3 = IntervalSet.parse_from_str('[4, 9) | (300, inf)')
        >>> tvs1.difference(tvs2, tvs3)
        (0, 2] | [9, 10) | (100, 200]
        >>> tvs1.intersection()  # also can passed in zero other interval sets
        (0, 10) | (100, inf)
        """
        if not other_tvs_lis:
            return self.copy()
        if not self or any(tvs.inf_flag for tvs in other_tvs_lis):
            return self.__class__()

        new_tvs = self.copy()
        for tvs in other_tvs_lis:
            new_tvs._difference_update_one(tvs, )
            if not new_tvs:
                break

        return new_tvs

    def _difference_update_one(self, other: 'IntervalSet', /, ):
        """

        :param other:
        :return:
        """
        """将与 tvs 无交集的区间 从 tvs_lis 中移除，避免无效运算
        先找出 tvs[0][0] tvs[-1][1]
        假设 left_min: -5  right_max: 7
        (f, f), (f, t), (t, f), (t, t)

        对于 左端，任意 arr[1] ＜ left_min 的区间都是无效的，例如 (l, r)，只要 r < -5，注意 r == -5 的有可能产生影响
        可以按 (-5, -5, f, f) 进行靠左二分查找，pos < lo 的都是无效区间？
        但是有可能：..., (-8, -3), (-2, 2), ...
        所以：有可能 pos = lo - 1 也有效。

        同样，对于右端，任何 right_max ＜ arr[0] 的区间都是无效的，按 (7, 7, True, True) 进行靠右二分查找
        但是有可能：..., (3, 6), [7, 10), ... 此时 l == 7 的有可能产生影响
        所以调整为 按 (7, INF, True, True) 进行靠右二分查找，则 pos >= hi 的必定是无效区间.

        有可能 hi - lo == 0, 此时意味着：
        tvs：(-5, 7)
        区间集 B：(-20, -10), (10, 20)
        即：对于B来说，与 [left_max, right_min] 无交集，此时 B 对对求差集无影响，忽略即可。
        """
        left_min = self.interval_arrays[0][0]
        interval_left_min = [left_min, left_min, False, False, 0]
        interval_right_max = [self.interval_arrays[-1][1], POS_INF, True, True, 0]
        lo = bisect.bisect_left(other.interval_arrays, interval_left_min)
        if lo > 0 and left_min <= other.interval_arrays[lo - 1][1]:
            lo -= 1
        hi = bisect.bisect_right(other.interval_arrays, interval_right_max)
        if lo == hi:
            return
        interval_arrays_1, interval_arrays_2 = self.interval_arrays, other.interval_arrays
        j = lo
        new_arrays = []
        cu = []
        while interval_arrays_1:
            cu = cu or interval_arrays_1.pop(0)
            # cu: (2, 8)  cu 的左端会随着迭代而变化
            if cu[1] < interval_arrays_2[j][0]:
                # new: (10, 16)
                new_arrays.append(cu)
                cu = []
                continue

            while j < hi:
                # new.left <= cu.right 一旦出现 new: (6, y) 则中止对 other 的迭代
                new = interval_arrays_2[j]
                """总计如下情况：
                cu: (2, 8) 
                一、不相交或者外切
                1. cu.left, cu.right < new.left, new.right  (10, y) 右侧远离
                2. cu.left, cu.right == new.left, new.right (8, y)  右侧外切
                3. new.left, new.right < cu.left, cu.right  (x, 0)  左侧远离
                4. new.left, new.right == cu.left, cu.right (x, 2)  左侧外切
                二、左端
                1. new.left < cu.left  (-3, y)
                2. cu.left == new.left (2, y)  左侧内切
                3. cu.left < new.left  (4, y)
                三、右端
                1. new.right < cu.right  (x, 6)  
                2. cu.right == new.right (x, 8)  右侧内切
                3. cu.right < new.right  (x, 10)
                """
                if cu[1] < new[0]:
                    # new: (10, y) 右侧远离
                    new_arrays.append(cu)
                    cu = []
                    break

                if new[1] < cu[0]:
                    # new: (x, 1)  左侧远离
                    j += 1
                    continue

                if new[1] == cu[0]:
                    # 左侧外切
                    # new (x, 2)  x<=2
                    if cu[2] and new[3]:
                        # cu[0] 变为不闭合
                        if cu[0] == cu[1]:
                            # cu: 2
                            cu = []
                            j += 1
                            break
                        cu[2] = False
                    j += 1
                    continue

                if cu[1] == new[0]:
                    # 右侧外切
                    # new: (8, y) 8<=y
                    if cu[3] and new[2]:
                        # cu[1] 变得不闭合
                        if cu[0] == cu[1]:
                            # cu: 8
                            cu = []
                            break
                        cu[3] = False
                    new_arrays.append(cu)
                    cu = []
                    break

                if cu[0] < new[0]:
                    # 左侧内包含 new: (3, y2)  3<y1
                    new_arrays.append([cu[0], new[0], cu[2], not new[2]])
                elif cu[0] == new[0]:
                    # 左侧内切
                    # cu: (2, x) 2<=x new: (2, y) 2<=y
                    if cu[2] and not new[2]:
                        new_arrays.append([cu[0], cu[0], True, True])

                if new[1] < cu[1]:
                    # 右侧内包含  new: (x, 6)
                    cu[0] = new[1]
                    cu[2] = not new[3]
                    j += 1
                elif new[1] == cu[1]:
                    # 右侧内切
                    if cu[3] and not new[3]:
                        # cu: (x1, 8]  new: (x2, 8)
                        new_arrays.append([cu[1], cu[1], True, True])
                    j += 1
                    cu = []
                    break
                else:
                    # new: (x, 10)
                    cu = []
                    break

            if j == hi:
                if cu:
                    new_arrays.append(cu)
                break
        new_arrays.extend(interval_arrays_1)
        self.reset_interval_arrays(new_arrays, merge=False)

    def __sub__(self, other: 'IntervalSet', ) -> 'IntervalSet':
        """Return self - other.

        :param other:
        :return:
        """
        return self.difference(other)

    def __isub__(self, other: 'IntervalSet', ) -> 'IntervalSet':
        """Return self -= other.

        :param other:
        :return:
        """
        self._difference_update_one(other)
        return self

    def difference_update(self, *other_tvs_lis: 'IntervalSet', ):
        """Update self with the difference of self and other interval sets.

        For any interval in updated self, satisfy: belongs to self, but
        does not belong to any interval set in tvs_lis.

        :param other_tvs_lis: list of interval set
        :return:

        examples:
        >>> tvs1 = IntervalSet.parse_from_str('(0, 10) | (100, inf)')
        >>> tvs2 = IntervalSet.parse_from_str('(2, 7) | (200, inf)')
        >>> tvs3 = IntervalSet.parse_from_str('[4, 9) | (300, inf)')
        >>> tvs1.difference_update(tvs2, tvs3)
        >>> tvs1
        (0, 2] | [9, 10) | (100, 200]
        >>> tvs1.difference_update()  # also can passed in zero other interval sets
        >>> tvs1
        (0, 2] | [9, 10) | (100, 200]
        """
        self.__dict__ = self.difference(*other_tvs_lis).__dict__

    def symmetric_difference(self, *tvs_lis: 'IntervalSet', ) -> 'IntervalSet':
        """Return the symmetric difference of self and interval set in tvs_lis as a new set.

        For any interval in the return interval set, satisfy: only belongs to self or one of interval set in tvs_lis..

        Special note: When three or more interval sets, t1.symmetric_difference(t2, t3),
        its result is often different to using the operation ^ , like t1 ^ t2 ^ t3,
        the latter is equivalent to symmetric_difference(symmetric_difference(t1, t2), t3).

        :param tvs_lis: list of interval set
        :return:

        examples:
        >>> tvs1 = IntervalSet.parse_from_str('(0, 3] | (100, inf)')
        >>> tvs2 = IntervalSet.parse_from_str('(2, 5) | (200, inf)')
        >>> tvs3 = IntervalSet.parse_from_str('[4, 9) | (300, inf)')
        >>> tvs1.symmetric_difference(tvs2, tvs3)
        (0, 2] | (3, 4) | [5, 9) | (100, 200]
        >>> tvs1.symmetric_difference()  # also can passed in zero other interval sets
        (0, 3] | (100, inf)
        """
        # 过滤出非空区间集
        tvs_lis = [self] + list(tvs_lis)
        tvs_lis = [e for e in tvs_lis if e]
        if not tvs_lis or sum(tvs.inf_flag for tvs in tvs_lis) > 1:
            return self.__class__()
        if len(tvs_lis) == 1:
            return tvs_lis[0].copy()
        valid_arrays: List[list] = []
        sn_max = 0
        for tvs in tvs_lis:
            for arr in tvs.interval_arrays:
                arr.append(sn_max)
            valid_arrays.append(tvs.interval_arrays)
            sn_max += 1

        arrays_sorted = sorted(valid_arrays, key=len, reverse=True)
        longest_arr: List[list] = arrays_sorted[0].copy()

        self._join_many_sorted_arr_into_longest(longest_arr, *arrays_sorted[1:], merge=False)

        new_intervals, value_close, checked_value = [], False, NEG_INF
        cu = longest_arr[0].copy()
        i = 1
        while i < len(longest_arr):
            """总计如下情况：
            cu: (2, 5) 
            一、不相交或者外切
            1. cu.left, cu.right < new.left, new.right  (7, y)
            2. cu.left, cu.right == new.left, new.right (5, y)
            3. new.left, new.right < cu.left, cu.right  (x, 0)  忽略
            4. new.left, new.right == cu.left, cu.right (x, 2)  忽略
            二、左端
            1. new.left < cu.left  (-3, y)
            2. cu.left == new.left (2, y)
            3. cu.left < new.left  (4, y)
            三、右端
            1. new.right < cu.right  (x, 3)  
            2. cu.right == new.right (x, 5)
            3. cu.right < new.right  (x, 7)
            """
            new = longest_arr[i]
            if new[4] == cu[4] or cu[1] < new[0]:
                """
                case: 同一 sn 的两个区间必定不相交，所以下一个出现时，上一个必定属于对称差集结果
                case: cu.right < new.left, 如 cu: (2, 5) new: (6, 10)  new 完全处于 cu 的右侧
                """
                # 或者不相交 cu: (2, 5) new: (6, 10)  new 完全处于 cu 的右侧
                del cu[4]
                new_intervals.append(cu)
                cu = new.copy()
                i += 1
                continue
            if cu[1] == new[0]:
                # 在 cu 右侧外切  cu: (2, 5) (5, 5) new: (5, y) (5, 5)
                # 需要检查 cu.right 的闭合性
                value_close, checked_value = self._check_close(longest_arr, cu[1], cu[3] + new[2], i + 1, value_close,
                                                               checked_value)
                if value_close:
                    # 5 是闭合的, cu 变为 (2, y)
                    cu[1] = new[1]
                    cu[3] = new[3]
                    cu[4] = new[4]
                    """下一个区间的可能性：
                    case: (5, z) 此时，(2, 5) 析出，且不需要重复检查 5 的闭合度
                    case: (6, z) 此时，(2, 6) 析出，但需要检查 6 的闭合度
                    case: (y, z) 此时，(2, y) 析出，但需要检查 y 的闭合度
                    case: (y+1, z) 此时，(2, y) 析出，也不需要检查 y 的闭合度
                    """
                else:
                    # 5 不闭合
                    if cu[0] < cu[1]:
                        # (2, 5) 被析出
                        cu[3] = False
                        del cu[4]
                        new_intervals.append(cu)
                    if cu[1] < new[1]:
                        # cu 变为 (5, y) y>5
                        cu = new.copy()
                        cu[2] = False
                        """下一个区间的可能性：
                        case: (5, z) 此时，cu -> (y, z)，不需要重复检查 5 的闭合度
                        case: (6, z) 此时，(5, 6) 析出，不需要重复检查 5 的闭合度, 但需要检查 6 的闭合度
                        case: (y, z) 此时，(y, y) 析出，cu -> (y, z)，需要检查 y 的闭合度
                        case: (y+1, z) 此时，(5, y) 析出，也不需要检查 y 的闭合度
                        """
                    else:
                        # 此时 new 是 (5, 5)，需要重新定位 cu
                        cu, i = self._lookup_next_cu(longest_arr, i + 1, new[1])
                i += 1
                continue

            # 走到此处时，必定 new.left < cu.right
            if cu[0] < new[0]:
                """cu.left < new.left < cu.right  如 cu: (2, 5) new: (3, y)
                """
                value_close, checked_value = self._check_close(longest_arr, new[0], 1 + new[2], i + 1, value_close,
                                                               checked_value)
                new_intervals.append([cu[0], new[0], cu[2], value_close])
            elif cu[0] == new[0]:
                """cu.left=new.left  如 cu: (2, 5) new: (2, y)           
                """
                value_close, checked_value = self._check_close(longest_arr, new[0], cu[2] + new[2], i + 1, value_close,
                                                               checked_value)
                if value_close:
                    # 析出孤立点 2
                    new_intervals.append([cu[0], cu[0], True, True])
            if cu[1] < new[1]:
                """new.left < cu.right < new.right, 如 cu: (2, 5) new: (3, 7)                
                next 有可能是 (3, 8) (4, 7) (5, 7) (6, 9)
                """
                value_close, checked_value = self._check_close(longest_arr, cu[1], 1 + cu[3], i + 1, value_close,
                                                               checked_value)
                cu = [cu[1], new[1], value_close, new[3], new[4]]
            elif cu[1] == new[1]:
                """new.left < cu.right == new.right, 如 cu: (2, 7) new: (3, 7)  
                """
                value_close, checked_value = self._check_close(longest_arr, new[1], cu[3] + new[3], i + 1, value_close,
                                                               checked_value)
                if value_close:
                    # cu 变成孤立点，且 sn 设置为 -1，因为相当于改变了 new.right 的闭合性，导致 new 与 下一个区间变的相交
                    cu = [cu[1], cu[1], True, True, -1]
                else:
                    """此时 cu 被耗尽，怎么办？
                    next 有可能是 (3, 8) (4, 5) (4, 12) (5, 6) (5, 9) (7, 7) (7, 11) (8, 12)
                    """
                    cu, i = self._lookup_next_cu(longest_arr, i + 1, new[1])
            else:
                """new.left < new.right < cu.right, 如 cu: (2, 5) new: (3, 4)                
                next 有可能是 (3, 8) (4, 7) (5, 7) (6, 9)
                """
                value_close, checked_value = self._check_close(longest_arr, new[1], 1 + new[3], i + 1, value_close,
                                                               checked_value)
                cu = [new[1], cu[1], value_close, cu[3], cu[4]]
            i += 1
        if cu:
            del cu[4]
            new_intervals.append(cu)
        for arr in longest_arr:
            del arr[4]
        return self.__class__(new_intervals, merge=False)

    @classmethod
    def _lookup_next_cu(cls, interval_arrays: List[list], start: int, lg_value: Comparable, ) -> Tuple[list, int]:
        """找出 right > lg_value 的第一个区间

        :param interval_arrays:
        :param start:
        :param lg_value:
        :return: 区间，区间的下标
        """
        cu = []
        while start < len(interval_arrays):
            if lg_value < interval_arrays[start][1]:
                cu = interval_arrays[start].copy()
                if cu[0] <= lg_value:
                    cu[0] = lg_value
                    cu[2] = False
                break
            start += 1
        return cu, start

    @classmethod
    def _check_close(cls, interval_arrays: List[list], to_check_value: Comparable, close_degree: int, start: int,
                     latest_checked_close: bool, latest_checked_value, ) -> Tuple[bool, Comparable]:
        """检查左端的闭合度
        左端相同时，(2, 5) (2, 5] [2, 5) [2, 5] (2, 6), (2, 6], [2, 6), [2, 6], ...

        case: [2, 2] [2, 2] (2, 5) (2, 8) 合并后 返回 1[5, 8), i+4, 2
        case: (2, 5) [2, 5] (2, 7) (2, 12) 合并后 返回 1[7, 8), i+4, 1
        case: (2, 5) [2, 5]  合并后 返回 [5, 5], i+2, 1
        case: (2, 5] [2, 5]  合并后 返回 (5, 5), i+2, 1
        case: (2, 2) [2, 5] [2, 5]  合并后 返回 (5, 5), i+3, 1

        :param interval_arrays:
        :param start:
        :return: 合并至极限的单一覆盖区间, 后续待处理的下标, left_close_num
            区间的闭合性不是简单的 boo 值，而是总计闭合度
        """
        if to_check_value == latest_checked_value:
            return latest_checked_close, latest_checked_value
        if close_degree > 1:
            return False, to_check_value
        for j in range(start, len(interval_arrays)):
            # 假定 to_check_value = 5
            new = interval_arrays[j]
            if to_check_value < new[0]:
                # (6, y)
                break
            # (x, y) 且 x<=to_check_value
            if new[0] == to_check_value:
                # (5, y)
                close_degree += new[2]
            elif new[1] == to_check_value:
                # (x, 5)
                close_degree += new[3]
            elif to_check_value < new[1]:
                # (4, 6)
                close_degree += 1
            if close_degree > 1:
                return False, to_check_value
        return close_degree == 1, to_check_value

    def __xor__(self, other: 'IntervalSet', ) -> 'IntervalSet':
        """Return self ^ other.

        :param other:
        :return:
        """
        return self.symmetric_difference(other)

    def __ixor__(self, other: 'IntervalSet', ) -> 'IntervalSet':
        """return self ^= other.

        :param other:
        :return:
        """
        self.__dict__ = self.symmetric_difference(other).__dict__
        return self

    def symmetric_difference_update(self, *tvs_lis: 'IntervalSet', ):
        """Update self with the symmetric difference of self and interval set in tvs_lis.

        For any interval in updated self, satisfy: only belongs to self or one of interval set in tvs_lis.

        Special note: When three or more interval sets, t1.symmetric_difference_update(t2, t3),
        its result is often different to using the operation ^= , like t1 ^= t2, and then t1 ^= t3,
        the latter is equivalent to t1.symmetric_difference_update(t2), and then t1.symmetric_difference_update(t3).

        :param tvs_lis: list of interval set
        :return:

        examples:
        >>> tvs1 = IntervalSet.parse_from_str('(0, 3] | (100, inf)')
        >>> tvs2 = IntervalSet.parse_from_str('(2, 5) | (200, inf)')
        >>> tvs3 = IntervalSet.parse_from_str('[4, 9) | (300, inf)')
        >>> tvs1.symmetric_difference_update(tvs2, tvs3)
        >>> tvs1
        (0, 2] | (3, 4) | [5, 9) | (100, 200]
        >>> tvs1.symmetric_difference_update()  # also can passed in zero other interval sets
        >>> tvs1
        (0, 2] | (3, 4) | [5, 9) | (100, 200]
        """
        self.__dict__ = self.symmetric_difference(*tvs_lis).__dict__

    @classmethod
    def complementary_many(cls, *tvs_lis: 'IntervalSet', ) -> 'IntervalSet':
        """Return complementary of union of tvs_lis relative to (-inf, inf).

        :param tvs_lis:
        :return:

        examples:
        >>> tvs1 = IntervalSet.parse_from_str('-3 | (0, 2]')
        >>> tvs2 = IntervalSet.parse_from_str('(3, 5)')
        >>> tvs3 = IntervalSet.parse_from_str('[7, 9) | (300, inf)')
        >>> IntervalSet.complementary_many(tvs1, tvs2, tvs3)
        (-inf, -3) | (-3, 0] | (2, 3] | [5, 7) | [9, 300]
        """
        if not tvs_lis:
            return cls()
        return cls.difference(cls.inf_tvs(), *tvs_lis)

    def complementary(self, ) -> 'IntervalSet':
        """Return complementary of self relative to (-inf, inf).

        :return:

        examples:
        >>> tvs1 = IntervalSet.parse_from_str('(0, 3] | (100, inf)')
        >>> tvs1.complementary()
        (-inf, 0] | (3, 100]
        """
        self.__dict__ = self.complementary_many(self).__dict__
        return self

    def __invert__(self, ) -> 'IntervalSet':
        """Return ~self.

        :return:
        """
        return self.complementary()

    def __eq__(self, other: 'IntervalSet'):
        if not isinstance(other, IntervalSet):
            return False
        if len(self) != len(other):
            return False
        for i1, i2 in zip(self.interval_arrays, other.interval_arrays):
            if i1 != i2:
                return False
        return True

    def issuperset(self, other: 'IntervalSet', /) -> bool:
        """Return True self is super set on other.

        :param other:
        :return:
        """
        return other.difference(self).is_empty()

    def issubset(self, other: 'IntervalSet', /) -> bool:
        """Return True if self is sub set under other.

        :param other:
        :return:
        """
        return self.difference(other).is_empty()

    def is_disjoint(self, other: 'IntervalSet', /) -> bool:
        """Return True if self does not overlap on other.

        :param other:
        :return:
        """
        return self.intersection(other).is_empty()

    def __contains__(self, item: Union[Interval, list, Comparable], /) -> bool:
        """Return whether interval in self or not.

        :param item: an Interval, or a list represent an interval, or a Comparable value represent a discrete point
        :return:
        """
        if isinstance(item, Interval):
            item = item.arr
        elif not isinstance(item, list):
            item = [item, item, True, True]

        # 假定 item: (2, 8)
        pos = bisect.bisect_left(self.interval_arrays, item)
        # 有可能 (1, 9) (2, 8)
        # 或者 (2, 7) (2, 8)
        # 也有可能  (2, 8) (2, 8] [2, 8) [2, 8]
        if pos > 0 and self.interval_arrays[pos - 1][0] < item[0]:
            pos -= 1
        while pos < len(self.interval_arrays):
            arr: list = self.interval_arrays[pos]
            if item[0] < arr[0]:
                break
            if (arr[0] < item[0] or (arr[0] == item[0] and (arr[2] - item[2] >= 0))) \
                    and (item[1] < arr[1] or (item[1] == arr[1] and (arr[3] - item[3] >= 0))):
                return True
            pos += 1

        return False
