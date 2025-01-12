import pandas as pd
from bot.bot import Bot
from scripts.tech_stat_bot.parser import Parser

import datetime as dt
from pathlib import Path


def send_message_to_teams(conf: dict, file_path: Path | str, message: str = ""):
    token = conf["bot_token"]
    url = conf["api_url"]
    name = conf["bot_name"]
    channels = conf["channels"]
    client = Bot(token=token, api_url_base=url, name=name)
    response = client.self_get()
    print(response)
    # file = open(file_path, 'rb')
    # print("Начинаю рассылать статистику")
    # for channel_id in channels:
    #     print(f"Отправка {channel_id}")
    #     response = client.send_file(chat_id=channel_id,
    #                      file=file, caption=message)
    #     print(f"Status: {response.status_code}: {response.reason}")
    #     print(response.url)
    #     file.seek(0)
    # file.close()


def get_tech_problems(conf_pyrus: dict, default_tasks_fields: dict, result_path: Path | str):
    prs = Parser(config=conf_pyrus, catalogs=conf_pyrus["catalogs_ids"],
                 default_form_id=conf_pyrus["form_ids"]["support_hp"],
                 default_task_fields=default_tasks_fields)
    result = prs.tech_problems_stat()
    if result and len(result) > 0:
        print(f"Получены задачи по форме Поддержка Hippoparking. Всего получено задач: {len(result)}")
    else:
        print(f"Не удалось получить задачи по форме Поддержка Hippoparking")
        exit(1)
    objects_count_dict = {}
    for obj in result:
        if obj["Object"] and obj["Object"] != "Нет":
            objects_count_dict[obj["Object"]] = objects_count_dict.setdefault(obj["Object"], 0) + 1
    objects_count = [(k, v) for k, v in objects_count_dict.items()]
    objects_count.sort(key=lambda x: x[1], reverse = True)

    objects_problems = {obj[0]: {} for obj in objects_count}
    objects_problems_sorted = {obj[0]: [] for obj in objects_count}

    for task in result:
        if task["Object"] and task["Object"] != "Нет":
            name = task["Object"]
            problem = task["Problem"]
            objects_problems[name][problem] = objects_problems[name].setdefault(problem, 0) + 1

    for obj, stat in objects_problems.items():
        problems = [(k, v) for k, v in stat.items()]
        problems.sort(key=lambda x: x[1], reverse=True)
        for i in problems:
            objects_problems_sorted[obj].append(f"{i[0]}: {i[1]}")
    pd.DataFrame.from_dict(objects_problems_sorted, orient='index').to_excel(result_path)

def main():
    config = Parser.get_config()
    conf_pyrus = config["pyrus"]
    default_tasks_fields = {
        # "fld40": "14256095,14256096,14256106,14256098",
        "fld43": f"gt{(dt.datetime.now() - dt.timedelta(days=31)).date()}",
        "include_archived": "y",  # закрытые
    }
    tech_problems_path = Path("output/tech_problems_result.xlsx")
    folder = Path("output/")
    if not folder.exists():
        folder.mkdir()
    message = "Статистика обращений за неделю."
    get_tech_problems(conf_pyrus, default_tasks_fields, tech_problems_path)
    # send_message_to_teams(config['vk_teams'], tech_problems_path, message)


if __name__ == "__main__":
    main()
