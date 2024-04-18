from auth import Client
import json


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
        self.objects_set = self.__get_objects_set()

    def __get_objects_set(self) -> set:
        result = set()
        for task in self.form_tasks:
            result.add(self.__get_object_name(task))
        return result

    def __get_object_name(self, task: dict) -> str | None:
        for field in task["fields"]:
            if field.get("id") == 35:
                try:
                    return field["value"]["values"][3] + ' / ' + field["value"]["values"][4]
                except KeyError:
                    return None

    def __get_first_line_problem(self, task: dict) -> str | None:
        ...


def to_json(task: dict) -> None:
    with open("output.json", 'w', encoding="utf-8") as output:
        json.dump(task, output, ensure_ascii=False)


def main():
    prs = Parser()
    # for task in prs.form_tasks:
    #     for field in task["fields"]:
    #         if field["id"] == 40:
    #             to_json(field)
    #             break
    to_json(prs.get_catalog()["items"])


if __name__ == "__main__":
    main()
