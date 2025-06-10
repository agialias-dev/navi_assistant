from functions.run_python import run_python_file

def tests():
    test1 = run_python_file("calculator", "main.py")
    print(test1)
    test2 = run_python_file("calculator", "tests.py")
    print(test2)
    test3 = run_python_file("calculator", "../main.py")
    print(test3)
    test4 = run_python_file("calculator", "nonexistent.py")
    print(test4)

if __name__ == "__main__":
    tests()