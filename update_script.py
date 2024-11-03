import requests

# URLs для исходного и целевого репозиториев
source_url = "https://raw.githubusercontent.com/smolnp/IPTVru/gh-pages/IPTVru.m3u"
user_repo_url = "https://raw.githubusercontent.com/hijack81/iptv/main/All.m3u"

def download_m3u(url):
    """Скачивает содержимое .m3u файла по URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def filter_sports_channels(m3u_content):
    """Возвращает строки с `group-title="Спортивные"` из содержимого .m3u файла."""
    sports_lines = []
    lines = m3u_content.splitlines()
    
    for i in range(len(lines)):
        if 'group-title="Спортивные"' in lines[i]:
            sports_lines.append(lines[i])      # Добавляем строку с названием канала
            if i + 1 < len(lines):
                sports_lines.append(lines[i + 1])  # Добавляем следующую строку с URL трансляции
    
    return "\n".join(sports_lines)

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
    user_content = download_m3u(user_repo_url)
    
    # Фильтруем спортивные каналы и обновляем целевой файл
    sports_content = filter_sports_channels(source_content)
    updated_content = update_repo(sports_content, user_content)
    
    # Сохраняем обновленный контент
    with open("All.m3u", "w", encoding="utf-8") as f:
        f.write(updated_content)
    print("Обновление завершено и сохранено в All.m3u")

if __name__ == "__main__":
    main()
