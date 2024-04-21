import requests
from dotenv import load_dotenv
import os
import json
import datetime as dt


class AuthorisationError(Exception):
    ...


class Client:

    def __init__(self, env_path: str | None = None, default_form_id: int | str = 307143) -> None:
        load_dotenv(env_path)
        self.default_form_id = default_form_id
        self.default_tasks_fields = {
            # "field_ids": [43, 44, ],
            # "fld35": "2287714",
            "fld43": f"gt{(dt.datetime.now() - dt.timedelta(days=7)).date()}",
            "include_archived": "y",  # закрытые
        }
        self.__api_url = os.getenv("API_URL")
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

    def get_form_info(self, form_id: int | str = '') -> dict:
        """Метод возвращает описание формы с указанным id.
        """

        if form_id == '':
            form_id = self.default_form_id

        form_url = self.__api_url + "forms/" + str(form_id)
        response = requests.get(url=form_url, headers=self.headers)
        return json.loads(response.text)

    def get_tasks_by_form(self, form_id: int | str = '', fields: dict | None = None) -> dict:
        """Метод возвращает список задач, созданных по форме.
        В ответе возвращаются только общая информация о задаче,
        список заполненных полей формы и маршрутизация.
        """

        if form_id == '':
            form_id = self.default_form_id

        if fields == None:
            fields = self.default_tasks_fields

        form_url = self.__api_url + f"forms/{form_id}/register"
        response = requests.post(
            url=form_url, headers=self.headers, json=fields)
        return json.loads(response.text)

    def get_catalog(self, cat_id: int | str = 6655) -> dict:
        cat_url = self.__api_url + "catalogs/" + str(cat_id)
        response = requests.get(url=cat_url, headers=self.headers)
        return json.loads(response.text)


def main():
    client = Client()
    print(client.headers)


if __name__ == "__main__":
    main()
