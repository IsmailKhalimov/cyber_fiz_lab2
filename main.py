"""Отправка запросов на локальный сервер Ollama и формирование отчёта инференса."""

import json
import sys
import urllib.request
from pathlib import Path

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:0.5b"
REPORT_PATH = Path(__file__).with_name("report.md")

PROMPTS = [
    "Что такое киберфизическая система? Ответь одним предложением.",
    "Назови три закона Ньютона.",
    "Переведи на английский: 'Привет, как дела?'",
    "Напиши функцию на Python, которая возвращает факториал числа n.",
    "Сколько будет 17 * 24?",
    "Кто написал роман 'Война и мир'?",
    "Объясни простыми словами, что такое HTTP-протокол.",
    "Составь список из 5 планет Солнечной системы.",
    "Какое сейчас самое большое простое число, известное человечеству?",
    "Напиши короткое хокку про осень.",
]


def ask(prompt: str) -> str:
    """Отправить запрос модели через HTTP API Ollama и вернуть ответ.

    Параметры:
        prompt: текст запроса к LLM.

    Возвращает:
        Строку с ответом модели.
    """
    payload = json.dumps(
        {"model": MODEL, "prompt": prompt, "stream": False}
    ).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("response", "").strip()


def escape_cell(text: str) -> str:
    """Подготовить текст к вставке в ячейку Markdown-таблицы.

    Экранирует символ '|' и заменяет переводы строк на '<br>',
    чтобы многострочные ответы корректно отображались в таблице.
    """
    return text.replace("|", "\\|").replace("\r\n", "\n").replace("\n", "<br>")


def build_report(pairs: list[tuple[str, str]]) -> str:
    """Сформировать текст отчёта в формате Markdown-таблицы.

    Параметры:
        pairs: список пар (запрос, ответ).

    Возвращает:
        Строку с содержимым отчёта.
    """
    lines = [
        f"# Отчёт инференса LLM ({MODEL})",
        "",
        "| № | Запрос к LLM | Ответ LLM |",
        "|---|--------------|-----------|",
    ]
    for i, (q, a) in enumerate(pairs, 1):
        lines.append(f"| {i} | {escape_cell(q)} | {escape_cell(a)} |")
    return "\n".join(lines) + "\n"


def main() -> None:
    """Прогнать список запросов через LLM и сохранить отчёт."""
    pairs: list[tuple[str, str]] = []
    for i, prompt in enumerate(PROMPTS, 1):
        print(f"[{i}/{len(PROMPTS)}] {prompt}")
        answer = ask(prompt)
        print(f"-> {answer}\n")
        pairs.append((prompt, answer))
    REPORT_PATH.write_text(build_report(pairs), encoding="utf-8")
    print(f"Отчёт сохранён: {REPORT_PATH}")


if __name__ == "__main__":
    try:
        main()
    except urllib.error.URLError as e:
        print(f"Ошибка подключения к Ollama ({OLLAMA_URL}): {e}", file=sys.stderr)
        sys.exit(1)
