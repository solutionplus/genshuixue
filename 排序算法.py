为什么快速排序大多数情况下比堆排序、归并排序快？
    堆排序      归并排序        快速排序
最坏时间   O(nlogn)     O(nlogn)        O(n^2)
最好时间   O(nlogn)     O(nlogn)        O(nlogn)
平均时间   O(nlogn)     O(nlogn)        O(nlogn)
因为快排的最坏时间虽然复杂度高，但是在统计意义上，这种数据出现的概率极小，
而堆排序过程里的交换跟快排过程里的交换虽然都是常量时间，但是常量时间差很多。
实验证明：
数据规模    快速排序    归并排序    希尔排序    堆排序
1000万       0.75           1.22          1.77          3.57
5000万       3.78           6.29          9.48         26.54  
1亿          7.65           13.06         18.79        61.31