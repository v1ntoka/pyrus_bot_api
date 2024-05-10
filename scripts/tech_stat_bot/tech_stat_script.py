from scripts.tech_stat_bot.parser import Parser
from bot.bot import Bot
import datetime as dt
from pathlib import Path


def send_message_to_teams(conf: dict, file_path: Path | str, message: str = ""):
    token = conf["bot_token"]
    url = conf["api_url"]
    name = conf["bot_name"]
    channels = conf["channels"]
    client = Bot(token=token, api_url_base=url, name=name)
    file = open("output/tech_problems_result.xlsx", 'rb')
    for channel_id in channels:
        client.send_file(chat_id=channel_id,
                         file=file, caption=message)
        file.seek(0)
    file.close()


def get_tech_problems(conf_pyrus: dict, conf_teams: dict, default_tasks_fields: dict, result_path: Path | str):
    prs = Parser(config=conf_pyrus, catalogs=conf_pyrus["catalogs_ids"],
                 default_form_id=conf_pyrus["form_ids"]["support_hp"],
                 default_task_fields=default_tasks_fields)
    result = prs.tech_problems_stat()
    result_group = result.groupby(
        ["Object", "Problem", "Entrance"])
    result_group.count().to_excel(result_path)
    send_message_to_teams(conf_teams, result_path, message="Статистика технических проблем за неделю")


def main():
    config = Parser.get_config()
    conf_pyrus = config["pyrus"]
    conf_teams = config["vk_teams"]
    default_tasks_fields = {
        "fld43": f"gt{(dt.datetime.now() - dt.timedelta(days=7)).date()}",
        "include_archived": "y",  # закрытые
    }
    tech_problems_path = Path("output/tech_problems_result.xlsx")
    get_tech_problems(conf_pyrus, conf_teams, default_tasks_fields, tech_problems_path)
    # send_message_to_teams(conf_teams)


if __name__ == "__main__":
    main()
