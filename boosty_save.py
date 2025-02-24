#boosty_save от hinaichigo-fox! 
#https://github.com/hinaichigo-fox
import requests
from bs4 import BeautifulSoup
import os
import re
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore

# Инициализация colorama для корректной работы с цветами в терминале
init(autoreset=True)

def get_page_content(url, cookies, block):
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
	}

	# Отправляем GET-запрос с куками
	response = requests.get(url, headers=headers, cookies=cookies)

	# Проверяем успешность запроса
	if response.status_code == 200:
		# Получаем заголовок страницы с помощью регулярного выражения
		match = re.search(r'COMMON_POST_POSTCONTENT:TITLE">([^<]+)', response.text)
		title = match.group(1) if match else "Заголовок не найден"

		# Парсим HTML с помощью BeautifulSoup для извлечения ссылок на изображения
		soup = BeautifulSoup(response.text, "html.parser")
		links = set()

		# Ищем ссылки как в <a href="...">, так и в <img src="...">
		for tag in soup.find_all(['a', 'img']):
			attr = 'href' if tag.name == 'a' else 'src'
			if tag.has_attr(attr):
				link = tag[attr]
				if link.startswith("https://images.boosty.to/image"):
					clean_link = link.split("?")[0]  # Обрезаем всё после знака вопроса
					# Проверяем, есть ли изображение в блок-листе
					img_name = clean_link.split('/')[-1]
					if img_name not in block:
						links.add(clean_link)

		# Вывод заголовка и количества найденных изображений
		print(f"Заголовок страницы: {title}")
		print(f"Найдено изображений: {len(links)}")

		return list(links), title
	else:
		print(f"{Fore.RED}Ошибка: {response.status_code}")
		return [], f"Ошибка: {response.status_code}"

def download_image(link, page_folder, title):
	try:
		img_name = link.split('/')[-1]
		img_path = os.path.join(page_folder, img_name + ".jpg")

		# Проверяем, существует ли уже файл
		if os.path.exists(img_path):
			print(f"{Fore.CYAN}Изображение {img_name} уже скачано.")
			return

		# Отправляем GET-запрос для скачивания изображения
		img_response = requests.get(link)
		if img_response.status_code == 200:
			with open(img_path, 'wb') as file:
				file.write(img_response.content)
			print(f"{Fore.GREEN}Изображение {img_name} сохранено в папку {title}")
		else:
			print(f"{Fore.RED}Не удалось скачать изображение: {link}")
	except Exception as e:
		print(f"{Fore.RED}Ошибка при скачивании изображения {link}: {e}")

def save_images(links, folder_path, title):
	# Создаем папку с названием страницы
	page_folder = os.path.join(folder_path, title)
	if not os.path.exists(page_folder):
		os.makedirs(page_folder)

	# Используем ThreadPoolExecutor для многопоточной загрузки (до 5 потоков)
	with ThreadPoolExecutor(max_workers=5) as executor:
		executor.map(lambda link: download_image(link, page_folder, title), links)

if __name__ == "__main__":
	while True:
		url = input('Введите ссылку на страницу (или введите "exit" для выхода): ')
		if url.lower() == 'exit':
			print("Конец")
			break
		cookies = {
			"session": "123"
		}
		headers = {
			"Authorization": "213"
		}

		#Список блокируемых файлов
		block = ["123", "456", "789"]

		image_links, page_title = get_page_content(url, cookies, block)

		#Путь к папке скачивания
		folder_path = "/boosty_save/"#ставим нужный путь
		#функа для сохранения
		save_images(image_links, folder_path, page_title)
