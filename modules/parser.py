from modules.auth import Client
import json
import pandas as pd


class GetTasksError(Exception):
    ...


class Parser(Client):
    def __init__(self, env_path: str | None = None, default_form_id: int | str = 307143) -> None:
        super().__init__(env_path=env_path, default_form_id=default_form_id)
        try:
            self.form_tasks = self.get_tasks_by_form()["tasks"]
        except KeyError:
            raise GetTasksError(
                f"Не удалось получить задачи с id {self.default_form_id}")
        self.objects_dict = self.__get_catalog_dict(5831)
        self.tech_problems_dict = self.__get_catalog_dict(7171)
        self.entrance_dict = self.__get_catalog_dict(7184)
        # self.all_problems_dict = self.__get_catalog_dict(6655)

    def __get_catalog_dict(self, cat_id: int) -> dict:
        result = dict()
        response = self.get_catalog(cat_id)["items"]
        index = 0
        match cat_id:
            case 6655:
                index = 3
            case 5831:
                index = 3
            case _:
                index = 0
        for obj in response:
            result[obj["item_id"]] = obj["values"][index]
        return result

    def __get_tech_line(self, task: dict) -> dict | None:
        result = {"Task_id": task["id"]}
        for field in task["fields"]:
            match field["id"]:
                case 35:
                    result["Object"] = self.objects_dict[
                        field["value"]["item_id"]]
                case 44:
                    result["Problem"] = self.tech_problems_dict[
                        field["value"]["item_id"]]
                case 45:
                    result["Entrance"] = self.entrance_dict[
                        field["value"]["item_id"]]
                case _:
                    continue
        return result

    def tech_problems_stat(self) -> pd.DataFrame:
        data = {"Task_id": [], "Object": [], "Problem": [], "Entrance": []}
        for task in self.form_tasks:
            try:
                for key in (tmp := self.__get_tech_line(task)):
                    data[key].append(tmp[key])
            except KeyError:
                continue
        return pd.DataFrame(data)


def to_json(task: dict, filename: str = "output") -> None:
    with open("output/" + filename + ".json", 'w', encoding="utf-8") as output:
        json.dump(task, output, ensure_ascii=False)
