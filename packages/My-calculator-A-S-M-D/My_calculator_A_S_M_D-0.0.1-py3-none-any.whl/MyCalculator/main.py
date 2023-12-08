def add(x, y):
    return x + y

def sub(x, y):
    return x - y

def mult(x, y):
    return x * y

def div(x, y):
    if y != 0:
        return x / y
    else:
        return "Cannot divide by zero."

while True:
    print("\nCalculator:")
    print("1. Addition")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Quit")

    choix = input("Enter choice (1/2/3/4/5): ")

    if choix == '5':
        print("Calculator exit.")
        break

    if choix in ('1', '2', '3', '4'):
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))

        if choix == '1':
            print(num1,"+",num2,"=",add(num1,num2))
        elif choix == '2':
            print(num1,"-",num2,"=",sub(num1,num2))
        elif choix == '3':
            print(num1,"*",num2,"=",mult(num1,num2))
        elif choix == '4':
            print(num1,"/",num2,"=",div(num1,num2))
    else:
        print("Invalid valeur. Enter a valid choice.")
