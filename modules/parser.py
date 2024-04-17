import requests
from auth import Authorisation
import json


class Forms:
    def __init__(self, ) -> None:
        self.headers = Authorisation().headers
        url = "https://pyrus.sovcombank.ru/api/v4/forms/{form_id}/"


def main():
    f = Forms()
    headers = f.headers
    url = "https://pyrus.sovcombank.ru/api/v4/forms/{form_id}/register".format(
        form_id=307143)
    # url = "https://pyrus.sovcombank.ru/api/v4/forms"
    response = json.loads(requests.get(
        url=url, headers=headers, params={"include_archived": "y", "": ""}).text)
    with open("output.json", 'w', encoding="utf-8") as output:
        json.dump(response["tasks"], output, ensure_ascii=False)

    print(len(response["tasks"]))


if __name__ == "__main__":
    main()
