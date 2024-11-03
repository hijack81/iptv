import requests

# URLs для исходного и целевого файлов
source_url = "https://gitlab.com/iptv135435/iptvshared/-/raw/main/IPTV_SHARED.m3u"
user_repo_file = "premier_test.m3u"  # локальное имя файла, в который будут добавляться ссылки

# Ключевые слова для поиска нужных каналов
target_channels = [
    "Матч! Премьер", "Матч Премьер", "Матч! Пpемьер HD",
    "Матч! Футбол 1", "Матч! Футбол 1 HD", "Матч! Футбол 2",
    "Матч! Футбол 2 HD", "Матч! Футбол 3", "Матч! Футбол 3 HD"
]

def download_m3u(url):
    """Скачивает содержимое .m3u файла по URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def filter_target_channels(m3u_content, channel_names):
    """Возвращает строки, содержащие названия нужных каналов из списка channel_names."""
    filtered_lines = []
    lines = m3u_content.splitlines()
    
    for i in range(len(lines)):
        # Проверяем, содержит ли строка одно из названий каналов из channel_names
        if any(channel in lines[i] for channel in channel_names):
            filtered_lines.append(lines[i])      # Добавляем строку с названием канала
            if i + 1 < len(lines):
                filtered_lines.append(lines[i + 1])  # Добавляем следующую строку с URL трансляции
    
    return "\n".join(filtered_lines)

def update_repo(source_content, user_content):
    """Добавляет новые строки из source_content в user_content, если их еще нет."""
    updated_content = user_content
    new_lines = source_content.splitlines()
    
    for line in new_lines:
        if line not in user_content:
            updated_content += f"\n{line}"
    
    return updated_content

def main():
    # Скачиваем содержимое исходного и целевого .m3u файлов
    source_content = download_m3u(source_url)
    
    # Фильтруем каналы по нужным названиям
    target_content = filter_target_channels(source_content, target_channels)
    
    # Загружаем текущий контент `premier_test.m3u` из локального репозитория
    try:
        with open(user_repo_file, "r", encoding="utf-8") as f:
            user_content = f.read()
    except FileNotFoundError:
        user_content = ""  # Если файл еще не существует, создаем новый контент
    
    # Обновляем целевой файл новыми ссылками
    updated_content = update_repo(target_content, user_content)
    
    # Сохраняем обновленный контент
    with open(user_repo_file, "w", encoding="utf-8") as f:
        f.write(updated_content)
    print(f"Обновление завершено и сохранено в {user_repo_file}")

if __name__ == "__main__":
    main()
