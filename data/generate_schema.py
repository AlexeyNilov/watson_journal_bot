from data.fastlite_db import DB


def write_schema(file_path: str, tables: list[str]) -> None:
    with open(file_path, "w") as f:
        f.write("\n\n".join(DB.t[table].schema for table in tables))


write_schema("data/schema.sql", ["event"])
