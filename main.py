import functions

operation = input("Enter the operation to perform (add/multiply): ")
a = int(input("Enter the first operand: "))
b = int(input("Enter the second operand: "))

functions.perform_operations(operation=operation, a=a, b=b)