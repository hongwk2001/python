def add_numbers(a, b):
    return a + b

def multiply_numbers(a, b):
    return a * b

def perform_operations(operation, a, b):
    if operation == "add":
        result = add_numbers(a, b)
        print(f"The result of adding {a} and {b} is: {result}")
    elif operation == "multiply":
        result = multiply_numbers(a, b)
        print(f"The result of multiplying {a} and {b} is: {result}")
    else:
        print("Invalid operation")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-operation", help="The operation to perform (add/multiply)")
    parser.add_argument("-a", type=int, help="The first operand")
    parser.add_argument("-b", type=int, help="The second operand")
    args = parser.parse_args()

    perform_operations(args.operation, args.a, args.b)
