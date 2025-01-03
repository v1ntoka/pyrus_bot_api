import pandas as pd

from scripts.tech_stat_bot.parser import Parser

import datetime as dt
from pathlib import Path
from copy import copy


def get_tech_problems(conf_pyrus: dict, default_tasks_fields: dict, result_path: Path | str):
    prs = Parser(config=conf_pyrus, catalogs=conf_pyrus["catalogs_ids"],
                 default_form_id=conf_pyrus["form_ids"]["support_hp"],
                 default_task_fields=default_tasks_fields)
    result = prs.tech_problems_stat()
    # result = result_raw.sort_values(["Object", "Problem"])
    # result_group = result.groupby(
    #     ["Object", "Problem"])
    # result_count = result_group.count()#.to_excel(result_path)
    # result_count_sorted = result_count.sort_values(["Object", "Task_id"], ascending=False)#.to_excel(result_path)
    #
    # tasks_obj = result.groupby(
    #     ["Object"]
    # ).count()
    #
    # tasks_obj_sorted = tasks_obj.sort_values(["Task_id"], ascending=False)
    #
    # for index, row in tasks_obj_sorted.iterrows():
    #     print(row.name)

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
        objects_problems_sorted[obj].extend(problems)
        # for p in problems:
            # objects_problems_sorted[obj][p[0]] = p[1]
    pd.DataFrame.from_dict(objects_problems_sorted, orient='index').to_excel(result_path)

def main():
    config = Parser.get_config()
    conf_pyrus = config["pyrus"]
    default_tasks_fields = {
        "fld43": f"gt{(dt.datetime.now() - dt.timedelta(days=7)).date()}",
        "include_archived": "y",  # закрытые
    }
    tech_problems_path = Path("output/tech_problems_result.xlsx")
    get_tech_problems(conf_pyrus, default_tasks_fields, tech_problems_path)


if __name__ == "__main__":
    main()
