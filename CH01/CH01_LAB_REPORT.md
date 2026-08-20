# Lab Report — Chapter 1: Binary Search

*Complete both sections and commit this file with your code.*

## Test Results

*Paste your printed step counts and describe what your growth chart shows.*

```text
Linear search index: 9
Linear search steps: 10
Binary search index: 9
Binary search steps: 2

n: 128
Actual steps: 7
Naive formula: 8

n: 256
Actual steps: 8
Naive formula: 9

n: 1024
Actual steps: 10
Naive formula: 11

n: 2048
Actual steps: 11
Naive formula: 12

10 10 3
100 100 6
1000 1000 9
10000 10000 13
100000 100000 16
1000000 1000000 19

Steps for 1024: 10
Steps for 2048: 11
```

## Reflection Questions


1. **Explain binary search to someone who has never programmed.**

   Binary search is like looking for a name in a phone book. Instead of checking every name from the beginning, you open near the middle and decide whether the name you want comes before or after that point. You keep cutting the remaining section in half until you find the correct name.

2. **Doubling the list adds only one step to binary search. Why does that happen?**

   Binary search removes half of the remaining list after every guess. When the list becomes twice as large, it only takes one extra halving step to reduce it back to about the previous size. That is why the number of steps increases very slowly even when the list gets much larger.

3. **Where does binary search show up in real software?**

   Binary search can be used when software needs to quickly find information in sorted data. For example, it can be used to search sorted records, locate values in databases, or find an item in a large ordered list more efficiently than checking every item one at a time.
