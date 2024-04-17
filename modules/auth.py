import requests
from dotenv import load_dotenv
import os
import json
import datetime as dt


class AuthorisationError(Exception):
    ...


class Client:
    WEEKLY_TASKS_FIELDS: dict = {
        # "field_ids": [9, ],
        # за неделю
        # "fld2": "4",
        "fld9": f"gt{dt.datetime.now().date() - dt.timedelta(days=7)}",
        "include_archived": "y",  # закрытые
    }

    def __init__(self) -> None:
        load_dotenv()
        self.__api_url = "https://pyrus.sovcombank.ru/api/v4/"
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
        url = self.__api_url + "auth"
        data = {
            "login": self.__email,
            "security_key": self.__security_key,
        }
        access_token = requests.post(url, json=data, headers=self.headers)
        return json.loads(access_token.text)["access_token"]

    def get_form_info(self, form_id: int | str) -> json.loads:
        form_url = self.__api_url + "forms/" + str(form_id)
        response = requests.get(url=form_url, headers=self.headers)
        return json.loads(response.text)

    def get_tasks_by_form(self, form_id: int | str, fields: dict = {}) -> json.loads:
        form_url = self.__api_url + f"forms/{form_id}/register"
        response = requests.post(
            url=form_url, headers=self.headers, json=fields)
        return json.loads(response.text)


def main():
    auth = Client()
    response = auth.get_tasks_by_form(307143, fields=auth.WEEKLY_TASKS_FIELDS)
    print(len(response["tasks"][0]))
    with open("output.json", 'w', encoding="utf-8") as output:
        json.dump(response["tasks"][0], output, ensure_ascii=False)


if __name__ == "__main__":
    main()
