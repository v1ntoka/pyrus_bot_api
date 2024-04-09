import requests
from auth import Authorisation


class Forms:
    def __init__(self) -> None:
        self.access_token = Authorisation().access_token


def main():
    f = Forms()
    print(f.access_token)


if __name__ == "__main__":
    main()
