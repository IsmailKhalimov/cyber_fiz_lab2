# Лабораторная работа 2: NLP

Студент: Халимов И. И.

Группа: М8О-408Б-22

Локальный инференс LLM **Qwen2.5:0.5B** на сервере **Ollama** с отправкой
запросов по HTTP из Python-скрипта.

## Стек

- [Ollama](https://ollama.com/) — сервер инференса.
- Qwen2.5:0.5B — языковая модель (~397 МБ).
- Python 3.10+ (используется только стандартная библиотека, `pip install` не требуется).

## Структура

- `main.py` — скрипт, отправляющий 10 запросов на Ollama через HTTP API и
  сохраняющий отчёт.
- `report.md` — отчёт инференса (генерируется скриптом).
- `README.md` — этот файл.

## Установка и запуск

### 1. Установить Ollama

- **Windows** (PowerShell):
  ```powershell
  winget install --id Ollama.Ollama -e
  ```
  либо скачать инсталлятор с <https://ollama.com/download>.
- **Linux**:
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```
- **macOS**: скачать `.dmg` с <https://ollama.com/download>.

Проверка установки:
```bash
ollama --version
```

### 2. Поднять сервер и скачать модель

На Windows после установки Ollama запускается автоматически (иконка в трее).
На Linux/macOS сервер запускается командой:
```bash
ollama serve
```

Сервер слушает HTTP на `http://localhost:11434`. Проверка:
```bash
curl http://localhost:11434/api/version
```

Скачать модель:
```bash
ollama pull qwen2.5:0.5b
```

### 3. Запустить скрипт и получить отчёт

```bash
python main.py
```

Скрипт последовательно отправит 10 запросов на `POST /api/generate`,
выведет ответы в консоль и сохранит итоговую таблицу в `report.md`.

## Пример ручного запроса через curl

```bash
curl http://localhost:11434/api/generate -d "{\"model\":\"qwen2.5:0.5b\",\"prompt\":\"Привет!\",\"stream\":false}"
```
