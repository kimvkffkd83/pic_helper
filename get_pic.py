import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
from io import BytesIO
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import json


def fetch_images(url, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Selenium으로 웹페이지 열기
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    # 페이지 소스 가져오기
    html = driver.page_source
    driver.quit()

    # BeautifulSoup으로 이미지 태그 찾기
    soup = BeautifulSoup(html, 'html.parser')
    img_tags = soup.find_all('img')

    # 이미지 다운로드 및 저장
    for idx, img in enumerate(img_tags):
        img_url = img.get('src')
        if not img_url:
            continue

        try:
            img_data = requests.get(img_url).content
            img_name = os.path.join(folder, f'image_{idx + 1}.jpg')

            with open(img_name, 'wb') as img_file:
                img_file.write(img_data)

            # 이미지 검증 및 열기
            img = Image.open(BytesIO(img_data))
            img.verify()
            print(f"Saved {img_name}")

        except Exception as e:
            print(f"Failed to save {img_url}: {e}")


def start_scraping():
    url = url_entry.get()
    folder = folder_path.get()
    fetch_images(url, folder)


def browse_folder():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)

# GUI를 만들어보자!
root = tk.Tk()
root.title("겸댕이 파이팅!♥️")
root.geometry("500x600")
root.resizable(False, False)
root.attributes('-topmost', True) # 창이 항상 맨 위에

tab = ttk.Notebook(root)
tab.pack()

# tab1 = tk.Frame(tab)
# tab2 = tk.Frame(tab)
tab3 = tk.Frame(tab)

# tab.add(tab1, text="표 이미지 변환")
# tab.add(tab2, text="이미지 다운로드")
tab.add(tab3, text="부가기능")

# 탭3 - 부가기능
tk.Label(tab3, text="대/소문자 변환", font=("맑은 고딕", 14)).pack(pady=10)

frame1 = tk.Frame(tab3)
frame1.pack(pady=5)

tk.Label(frame1, text="변환 전 : ").grid(row=0, column=0, padx=5, pady=5)
etc_cvt_input_before = tk.Entry(frame1, width=50)
etc_cvt_input_before.grid(row=0, column=1, padx=5, pady=5)
btn_convert = tk.Button(frame1, text="변환", command=lambda: convert_text(etc_cvt_input_before, etc_cvt_input_after))
btn_convert.grid(row=0, column=2, padx=5, pady=5)

tk.Label(frame1, text="변환 후 : ").grid(row=1, column=0, padx=5, pady=5)
etc_cvt_input_after = tk.Entry(frame1, width=50)
etc_cvt_input_after.grid(row=1, column=1, padx=5, pady=5)
btn_copy = tk.Button(frame1, text="복사", command=lambda: copy_text(etc_cvt_input_after))
btn_copy.grid(row=1, column=2, padx=5, pady=5)

btn_copy = tk.Button(frame1, text="모두 지우기", command=lambda: remove_text(etc_cvt_input_before, etc_cvt_input_after))
btn_copy.grid(row=2, column=1, padx=5, pady=5)


# 텍스트 변환 함수
def convert_text(input_before, input_after):
    text = input_before.get()
    converted_text = text.swapcase()  # 대/소문자 변환
    input_after.delete(0, tk.END)
    input_after.insert(0, converted_text)


# 텍스트 복사 함수
def copy_text(entry):
    root.clipboard_clear()
    root.clipboard_append(entry.get())


# 인풋 초기화 함수
def remove_text(input_before, input_after):
    input_before.delete(0, tk.END)
    input_after.delete(0, tk.END)


# 구분선
separator = ttk.Separator(tab3, orient='horizontal')
separator.pack(fill='x', pady=10)


root.mainloop()
