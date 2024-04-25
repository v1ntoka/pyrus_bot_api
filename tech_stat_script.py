from modules.parser import Parser
from bot.bot import Bot


def send_message_to_teams(channels=("petrenkoka@sovcombank.ru", "galimovir@sovcombank.ru", "zinnatullinan1@sovcombank.ru")):
    token = "001.0039273119.0945063047:1000000460"
    url = "https://api.teams.sovcombank.ru/bot/v1/"
    name = "opvk_stat_bot"
    client = Bot(token=token, api_url_base=url, name=name)
    file = open("output/tech_problems_result.csv", 'r', encoding="utf-8")
    for channel_id in channels:
        client.send_file(chat_id=channel_id,
                         file=file, caption="Статистика технических проблем за неделю")
        file.seek(0)
    file.close()


def main():
    prs = Parser(env_path="modules/.env")
    result = prs.tech_problems_stat()
    # result_group = result[result["Problem"].isin(["Не сработала петля Б", "Не сработала петля А"])].groupby(
    #     ["Object", "Problem", "Entrance"])
    result_group = result.groupby(
        ["Object", "Problem", "Entrance"])
    with open("output/tech_problems_result.csv", 'w', encoding="utf-8") as output:
        result_group.count().to_csv(output, encoding="utf-8")
    send_message_to_teams()


if __name__ == "__main__":
    main()
