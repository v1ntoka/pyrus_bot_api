import json

from parser import Parser

def main():
    catalog_id = int(input("Input catalog id:\t"))
    config = Parser.get_config()["pyrus"]
    client = Parser(
        config,
        config["catalogs_ids"],
        config["form_ids"]["support_hp"],
    )
    catalog = client.get_catalog(catalog_id)
    with open(f"catalog-{catalog_id}.json", 'w', encoding='utf-8') as file:
        json.dump(catalog, file, ensure_ascii=False)


if __name__ == "__main__":
    main()