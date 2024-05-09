import requests
import json
from pathlib import Path


class AuthorisationError(Exception):
    ...


class FormIdError(Exception):
    ...


class Client:

    def __init__(self, config: dict, default_form_id: int | str = '',
                 default_task_fields: dict | None = None) -> None:
        self.default_form_id = default_form_id
        self.default_tasks_fields = default_task_fields if default_task_fields is not None else {}
        self.__api_url = config["api_url"]
        self.__email = config["email_auth"]
        self.__security_key = config["security_key"]
        self.headers = {
            "Content-Type": "application/json"
        }
        self.access_token = self.__get_token()
        if self.access_token:
            self.headers.update(
                {"Authorization": f"Bearer {self.access_token}"})
        else:
            raise AuthorisationError("Cannot get the access token")

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

        if not form_id:
            if self.default_form_id:
                form_id = self.default_form_id
            else:
                raise FormIdError("Empty form_id and default_form_id")

        form_url = self.__api_url + "forms/" + str(form_id)
        response = requests.get(url=form_url, headers=self.headers)
        return json.loads(response.text)

    def get_tasks_by_form(self, form_id: int | str = '', fields: dict | None = None) -> dict:
        """Метод возвращает список задач, созданных по форме.
        В ответе возвращаются только общая информация о задаче,
        список заполненных полей формы и маршрутизация.
        """

        if not form_id:
            if self.default_form_id:
                form_id = self.default_form_id
            else:
                raise FormIdError("Empty form_id and default_form_id")

        if fields is None:
            fields = self.default_tasks_fields

        form_url = self.__api_url + f"forms/{form_id}/register"
        response = requests.post(
            url=form_url, headers=self.headers, json=fields)
        return json.loads(response.text)

    def get_catalog(self, cat_id: int | str = 6655) -> dict:
        cat_url = self.__api_url + "catalogs/" + str(cat_id)
        response = requests.get(url=cat_url, headers=self.headers)
        return json.loads(response.text)

    @staticmethod
    def get_config(config_path: str | Path = '') -> dict:
        if not config_path:
            config_path = Path.cwd() / "conf.json"
        with open(config_path, 'r', encoding='utf-8') as conf:
            return json.load(conf)
