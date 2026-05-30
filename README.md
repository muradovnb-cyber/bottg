# Claude Telegram Bot

Бот для общения с Claude прямо из Telegram.

## Быстрый старт

### 1. Получи токены

- **Telegram токен**: напиши [@BotFather](https://t.me/BotFather) → `/newbot`
- **Anthropic API ключ**: зайди на [console.anthropic.com](https://console.anthropic.com)

### 2. Установи зависимости

```bash
pip install -r requirements.txt
```

### 3. Задай переменные окружения

**Linux/Mac:**
```bash
export TELEGRAM_TOKEN="твой_токен"
export ANTHROPIC_API_KEY="твой_ключ"
```

**Windows:**
```cmd
set TELEGRAM_TOKEN=твой_токен
set ANTHROPIC_API_KEY=твой_ключ
```

Или просто замени строки в `bot.py`:
```python
TELEGRAM_TOKEN = "твой_токен_здесь"
ANTHROPIC_API_KEY = "твой_ключ_здесь"
```

### 4. Запусти бота

```bash
python bot.py
```

---

## Деплой на сервер (чтобы бот работал 24/7)

### Railway (бесплатно)
1. Зарегистрируйся на [railway.app](https://railway.app)
2. Создай новый проект → Deploy from GitHub
3. Добавь переменные окружения в настройках
4. Готово!

### Render (бесплатно)
1. Зарегистрируйся на [render.com](https://render.com)
2. New → Web Service → подключи репозиторий
3. Build command: `pip install -r requirements.txt`
4. Start command: `python bot.py`
5. Добавь переменные окружения

---

## Команды бота

| Команда | Описание |
|---------|----------|
| `/start` | Приветствие |
| `/clear` | Очистить историю диалога |
| `/help` | Справка |

## Ограничение доступа (опционально)

Чтобы бот отвечал только тебе, раскомментируй в `bot.py`:
```python
ALLOWED_USER_IDS = {123456789}  # твой Telegram ID
```

Свой ID можно узнать у [@userinfobot](https://t.me/userinfobot).
