numbers = [1, 2, 3, 4, 2, 5, 2, 6, 7, 2]

print("The list of numbers:", numbers)
target = int(input("Enter the number you want to count: "))

count = numbers.count(target)

print(f"The number {target} appears {count} times in the list.")