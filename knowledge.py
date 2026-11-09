from pathlib import Path


KNOWLEDGE_DIR = Path(__file__).resolve().parent / "knowledge_base"


def load_knowledge(filename: str) -> str:
    file_path = KNOWLEDGE_DIR / filename

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    return content


def search_knowledge(keyword: str) -> list[str]:
    text = load_knowledge("return_policy.txt")

    lines = text.splitlines()

    results = []

    for line in lines:
        if keyword.lower() in line.lower():
            results.append(line)

    return results

if __name__ == "__main__":
    results = search_knowledge("refund")

    for result in results:
        print(result)
