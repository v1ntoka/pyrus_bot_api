from modules.parser import Parser


def main():
    prs = Parser(env_path="modules/.env")
    result = prs.tech_problems_stat()
    result_group = result[result["Problem"].isin(["Не сработала петля Б", "Не сработала петля А"])].groupby(
        ["Object", "Problem", "Entrance"])
    with open("output/tech_problems_result.csv", 'w', encoding="utf-8") as output:
        result_group.count().to_csv(output)


if __name__ == "__main__":
    main()
