def my_function(*args, **kwargs):
    print("Positional arguments:", args)
    print("Keyword arguments:", kwargs)

if __name__ == "__main__":
    my_function(1, 2, name="John", age=30)