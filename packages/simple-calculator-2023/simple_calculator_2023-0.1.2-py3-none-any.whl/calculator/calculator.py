# calculator/calculator.py
import argparse

class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

def main():
    parser = argparse.ArgumentParser(description="Command-line calculator")
    parser.add_argument("operation", choices=["add", "subtract", "multiply", "divide"], nargs="?",
                        help="The operation to perform. If not provided, show this help message and exit.")
    parser.add_argument("operand1", type=float, nargs="?", help="The first operand")
    parser.add_argument("operand2", type=float, nargs="?", help="The second operand")

    args = parser.parse_args()

    if not args.operation:
        parser.print_help()
        return

    calculator = Calculator()

    if args.operation == "add":
        result = calculator.add(args.operand1, args.operand2)
    elif args.operation == "subtract":
        result = calculator.subtract(args.operand1, args.operand2)
    elif args.operation == "multiply":
        result = calculator.multiply(args.operand1, args.operand2)
    elif args.operation == "divide":
        result = calculator.divide(args.operand1, args.operand2)

    print(f"Result of {args.operation} {args.operand1} and {args.operand2}: {result}")

if __name__ == "__main__":
    main()
