# dromSearchingBot
Бот обновляет дром и отсылает сообщение в Telegram, если появился новый автомобиль.
Автомобили для трекинга хранятся в папке cars в формате json. Как заполнять JSON файлы написано в json_files.txt.
Так же необходимо заполнить config.json

# Install

Execute command "pip install -r requirements.txt" in terminal

# First start
Автомобили для трекинга хранятся в папке cars в формате json.  
Так же необходимо заполнить config.json  
Как заполнять JSON файлы написано в json_files.txt.  

Необходимо создать файл .env и заполнить его следующими полями:  
API_TOKEN=YOUR_TELEGRAM_TOKEN
CHANNEL_ID=YOUR_TELEGRAM_ID

# Create .exe

Execute command "python setup.py build" in terminal

