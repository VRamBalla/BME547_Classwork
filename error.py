def function_name():
    a = 0
    b = 2
    c = b/a
    return c


def main():
    try:
        function_name()
    except ZeroDivisionError:
        print("zero in denominator, not valid")


if __name__ == "__main__":
    main()