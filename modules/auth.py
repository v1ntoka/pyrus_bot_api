import requests
from dotenv import load_dotenv
import os
import json


class AuthorisationError(Exception):
    ...


class Authorisation:
    def __init__(self) -> None:
        load_dotenv()
        self.__email = os.getenv("EMAIL_AUTH")
        self.__security_key = os.getenv("SECURITY_KEY")
        self.headers = {
            "Content-Type": "application/json"
        }
        self.access_token = self.__get_token()
        if self.access_token:
            self.headers.update(
                {"Authorization": f"Bearer {self.access_token}"})
        else:
            raise AuthorisationError("Не удалось получить access token")

    def __get_token(self):
        url = "https://pyrus.sovcombank.ru/api/v4/auth"
        data = {
            "login": self.__email,
            "security_key": self.__security_key,
        }
        access_token = requests.post(url, json=data, headers=self.headers)
        return json.loads(access_token.text)["access_token"]


def main():
    auth = Authorisation()
    print(auth.headers)


if __name__ == "__main__":
    main()
