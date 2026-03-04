numbers = [5, 7, 6, 7, 8, 8, 6, 6, 6]

print("Sum:", sum(numbers))

mean = sum(numbers) / len(numbers)
print("Mean:", mean)

numbers_sorted = sorted(numbers)
median = numbers_sorted[len(numbers)//2]
print("Median:", median)

from collections import Counter
mode = Counter(numbers).most_common(1)[0][0]
print("Mode:", mode)