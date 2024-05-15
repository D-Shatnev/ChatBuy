# AIBazaar

## Установка

```bash
git clone https://github.com/D-Shatnev/AIBazaar.git
python3.10 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .

# install dev dependencies (optional)
python -m pip install -e .[dev]
```

## Парсер

Для работы парсера используется selenium. Он требует, чтобы был скачан драйвер для браузера. Для Google Chrome и Firefox они разные.

### установка драйвера

Chrome:
```bash
sh ./scripts/download_driver.sh chrome
```

Firefox:
```bash
sh ./scripts/download_driver.sh firefox
```

### Аккаунт firefox

Для того, чтобы работать с Firefox, возможно постребуется указать путь к папке аккаунта. Чтобы узнать расположение папки аккаунта, заходим в настройки Firefox и в адресную строку вводим
```
about:profiles
```

Там будет путь к папке с аккаунтом.