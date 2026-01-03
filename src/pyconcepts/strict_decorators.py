from typing import Callable, TypeVar, ParamSpec, TypedDict

P = ParamSpec("P")
R = TypeVar("R")

def log(fn: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {fn.__name__}")
        return fn(*args, **kwargs)
    return wrapper

class User(TypedDict):
    id: int

@log
def get_user(user_id: int) -> User:
    return {"id": user_id}

if __name__ == "__main__":
    user = get_user(1)
    print(user)

