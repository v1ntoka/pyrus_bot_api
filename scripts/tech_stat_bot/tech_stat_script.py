from scripts.tech_stat_bot.parser import Parser
from bot.bot import Bot
import datetime as dt


def send_message_to_teams(conf: dict):
    token = conf["bot_token"]
    url = conf["api_url"]
    name = conf["bot_name"]
    # channels = conf["channels"]
    channels = ["galimovir@sovcombank.ru", ]
    client = Bot(token=token, api_url_base=url, name=name)
    file = open("output/tech_problems_result.xlsx", 'rb')
    for channel_id in channels:
        client.send_file(chat_id=channel_id,
                         file=file, caption="Статистика технических проблем за неделю")
        file.seek(0)
    file.close()


def main():
    config = Parser.get_config()
    conf_pyrus = config["pyrus"]
    conf_teams = config["vk_teams"]
    default_tasks_fields = {
        "fld43": f"gt{(dt.datetime.now() - dt.timedelta(days=7)).date()}",
        "include_archived": "y",  # закрытые
    }
    prs = Parser(config=conf_pyrus, catalogs=conf_pyrus["catalogs_ids"],
                 default_form_id=conf_pyrus["form_ids"]["support_hp"],
                 default_task_fields=default_tasks_fields)
    result = prs.tech_problems_stat()
    result_group = result.groupby(
        ["Object", "Problem", "Entrance"])
    result_group.count().to_excel("output/tech_problems_result.xlsx")
    send_message_to_teams(conf_teams)


if __name__ == "__main__":
    main()
