# pip install selenium==4.15.2
import time
import os
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

search_keyword = "여자 강아지상 연예인"
max_scroll_count = 5  # 원하는 스크롤 횟수 지정

# Chrome 드라이버 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

# 구글 이미지 검색
driver.get("https://www.google.com/imghp")
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys(search_keyword)
search_box.send_keys(Keys.RETURN)
time.sleep(2)

# 페이지 스크롤하여 이미지 로드
print("페이지 스크롤 시작...")
current_scroll_count = 0

while current_scroll_count < max_scroll_count:
    # 끝까지 스크롤
    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);"
    )
    time.sleep(1.5)

    current_scroll_count += 1
    print(f"스크롤 {current_scroll_count}/{max_scroll_count} 완료")

print("스크롤 완료!")

# 이미지 다운로드 폴더 생성
download_folder = "dog_downloaded_images"
os.makedirs(download_folder, exist_ok=True)

# 썸네일 이미지 찾기 및 다운로드
print("\n이미지 다운로드 시작...")

# 구글 이미지 검색 결과 컨테이너 안의 썸네일만 선택
thumbnail_containers = driver.find_elements(By.CSS_SELECTOR, "div.eA0Zlc div img")

print(f"찾은 이미지 개수: {len(thumbnail_containers)}")

downloaded_count = 0
for image in thumbnail_containers:
    image_url = image.get_attribute("src")
    
    # 이미지 크기 확인 (아이콘 제외)
    width = image.get_attribute("width")
    height = image.get_attribute("height")
    
    # 크기가 100px 이상인 이미지만 다운로드
    if width and height:
        if int(width) < 100 or int(height) < 100:
            continue
    
    # 유효한 URL인지 확인 (data: URL 제외)
    if image_url and image_url.startswith("http"):
        response = requests.get(image_url)
        file_path = os.path.join(download_folder, f"image_{downloaded_count + 1}.jpg")
        
        with open(file_path, "wb") as file:
            file.write(response.content)
        
        downloaded_count += 1
        print(f"다운로드 완료: {downloaded_count}")

print(f"\n총 {downloaded_count}개의 이미지 다운로드 완료!")
print(f"저장 위치: {download_folder}")

# 드라이버 종료
driver.quit()
