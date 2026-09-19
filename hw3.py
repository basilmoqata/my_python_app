numbers = []

for i in range(5):
    num = float(input(f"Enter number {i+1}: "))
    numbers.append(num)

total = sum(numbers)
average = total / len(numbers)
largest = max(numbers)

print("\n--- Results ---")
print(f"Total: {total}")
print(f"Average: {average}")
print(f"Largest number: {largest}")