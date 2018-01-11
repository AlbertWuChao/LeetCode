# -*- encoding=utf8 -*-

'''
There are two sorted arrays nums1 and nums2 of size m and n respectively.

Find the median of the two sorted arrays. The overall run time complexity should be O(log (m+n)).

Example 1:
nums1 = [1, 3]
nums2 = [2]

The median is 2.0
Example 2:
nums1 = [1, 2]
nums2 = [3, 4]

The median is (2 + 3)/2 = 2.5

思路：
    在2个有序数组间做一次二分查找, 找到中位数下标
    
'''

class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        if len(nums1) == 0:
            return self.mid(nums2)
        elif len(nums2) == 0:
            return self.mid(nums1)
        elif len(nums1) == 1 and len(nums2) == 1:
            return (float(nums1[0]) + nums2[0]) / 2
        elif nums1[-1] <= nums2[0]:
            return self.sorted(nums1, nums2)
        elif nums2[-1] <= nums1[0]:
            return self.sorted(nums2, nums1)
        remain = (len(nums1) + len(nums2)) / 2
        return self.binaryExclude(nums1, 0, nums2, 0, remain) 

    def sorted(self, arr1, arr2):
        all_len = len(arr1) + len(arr2)
        mid = all_len / 2
        type_len = all_len % 2
        if type_len == 1:
            return self.sorted_value(arr1, arr2, mid)
        v1 = self.sorted_value(arr1, arr2, mid - 1)
        v2 = self.sorted_value(arr1, arr2, mid)
        return (float(v1) + v2) / 2

    def sorted_value(self, arr1, arr2, index):
        if len(arr1) > index:
            return arr1[index]
        else:
            return arr2[index - len(arr1)]

    def mid(self, arr):
        lg = len(arr)
        if lg % 2 == 0:
            return (float(arr[lg/2-1]) + arr[lg/2]) / 2
        else:
            return arr[lg/2]

    def remain_end(self, arr1, left1, arr2, left2):
        type_len = (len(arr1) + len(arr2)) % 2

        l11 = left1 + 1
        l22 = left2 + 1
        # 奇数长度
        if type_len == 1:
            if l11 >= len(arr1):
                v2 = arr2[l22]
            elif l22 >= len(arr2):
                v2 = arr1[l11]
            else:
                v2 = arr1[l11] if arr1[l11] < arr2[l22] else arr2[l22]
            v1 = arr1[left1] if arr1[left1] > arr2[left2] else arr2[left2]
            return v1 if v1 < v2 else v2
        # 偶数长度
        v1 = arr1[left1]
        v2 = arr2[left2]
        if l11 >= len(arr1):
            if arr2[l22] < v1: v1 = arr2[l22]
        elif l22 >= len(arr2):
            if arr1[l11] < v2: v2 = arr1[l11]
        else:
            if arr2[l22] < v1: v1 = arr2[l22]
            if arr1[l11] < v2: v2 = arr1[l11]

        return (float(v1) + v2) / 2

    def in_one_end(self, arr, left, remain, type_len, max1):
        '''
        确定值在一个列表内
        len(all)奇数 ==> arr[left + remain]
        len(all)偶数 ==> (arr[left + remain] + arr[left + remain - 1]) / 2
        '''
        if type_len == 1:
            return arr[left + remain]
        else:
            v1 = max1
            v2 = arr[left + remain]
            if arr[left + remain - 1] > v1: v1 = arr[left + remain - 1]
            return (float(v1) + v2) / 2

    def binaryExclude(self, arr1, left1, arr2, left2, remain):
        '''
        中值的remian的初始值为 len(arr1) + len(arr2) / 2 ==> 初始值命名为K
        left1 & left2 从0开始，每次去除一部分比中指小的数组部分，直到去掉K-1个
        min(arr1[remain / 2 + left1], arr2[remain / 2 + left2]) 必定比中值小，为可去除部分
        如果 remain / 2 + left1 > len(arr1) && max(arr1) < arr2[remain / 2 + left2], 则确定中值在arr2中 
        如果 remain < 2, 则递归结束(remain最终会等于1):
            len(all)奇数 ==> min(a1[l1 + 1], a2[l2 + 1])
            len(all)偶数 ==> avg(max(a1[l1], a2[l2]), min(a1[l1+1], a2[l2+1]))
        '''
        # 剩余长度较短的数组放前面
        if len(arr1) - left1 > len(arr2) - left2:
            return self.binaryExclude(arr2, left2, arr1, left1, remain)
        if remain < 2:
            assert remain == 1
            return self.remain_end(arr1, left1, arr2, left2)
        mid1 = left1 + (remain / 2)
        mid2 = left2 + (remain / 2)

        # 如果arr1长度不够
        if mid1 >= len(arr1):
            max1 = arr1[-1]
            if max1 <= arr2[mid2]:
                # 确定中值在arr2中
                return self.in_one_end(arr2, left2, remain - len(arr1), (len(arr1) + len(arr2)) % 2, max1)
            else:
                return self.binaryExclude(arr1, left1, arr2, mid2, remain + left2 - mid2)
        # 如果arr1长度足够
        if arr1[mid1] < arr2[mid2]:
            return self.binaryExclude(arr1, mid1, arr2, left2, remain + left1 - mid1)
        else:
            return self.binaryExclude(arr1, left1, arr2, mid2, remain + left2 - mid2)
        
if __name__ == '__main__':
    solu = Solution()
    nums1 = [2, 6]
    nums2 = [1, 3, 4, 5]
    import time
    t1 = long(time.time() * 1000)
    print solu.findMedianSortedArrays(nums1, nums2)
    t2 = long(time.time() * 1000)
    print t2 - t1
