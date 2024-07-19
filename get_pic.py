import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import json
from PIL import Image, ImageTk
import pytesseract
import datetime

# Tesseract OCR 경로 설정 (Windows의 경우)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# GUI를 만들어보자!
root = tk.Tk()
root.title("겸댕이 파이팅!♥️")
root.geometry("500x650")
root.resizable(False, False)
root.attributes('-topmost', True)  # 창이 항상 맨 위에

tab = ttk.Notebook(root)
tab.pack()

tab1 = tk.Frame(tab)
tab2 = tk.Frame(tab)
tab3 = tk.Frame(tab)
tab4 = tk.Frame(tab)

tab.add(tab1, text="이미지 변환")
tab.add(tab2, text="이미지 다운로드")
tab.add(tab3, text="부가기능")
tab.add(tab4, text="설정")

# 전역 리스트 변수
converted_list = []

# 탭1 - 이미지 변환 영역
def process_image(image_path):
    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(Image.open(image_path), lang='eng')
    print(text)
    # Split the text by lines and process it
    lines = text.splitlines()
    processed_data = []
    for line in lines:
        if line.strip():
            parts = line.split()
            if len(parts) == 2:
                no, serial = parts
                processed_data.append({
                    "no": no,
                    "serial": serial,
                    "processed": "false"
                })
    return processed_data


def load_image():
    # Open a file dialog to select an image file
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return

    # Display the image in the Tkinter window
    img = Image.open(file_path)
    img.thumbnail((400, 400))
    img = ImageTk.PhotoImage(img)
    imgLabel.config(image=img)
    imgLabel.image = img

    # Process the image and print the result
    global converted_list
    converted_list = process_image(file_path)
    # for item in data_list:
    #     print(item)
    update_table(converted_list)
    save_to_file(converted_list)

def update_table(data):
    for i in tree.get_children():
        tree.delete(i)
    for item in data:
        tree.insert("", "end", values=(item["no"], item["serial"], item["processed"]))

def save_to_file(data):
    today_date = datetime.datetime.now().strftime("%Y%m%d")
    file_name = f"{today_date}_converted.txt"
    with open(file_name, "w", encoding="utf-8") as file:
        for item in data:
            file.write(f'{item["no"]}\t{item["serial"]}\t{item["processed"]}\n')

def edit_cell(event):
    selected_item = tree.selection()[0]
    column = tree.identify_column(event.x)
    if column == '#2':  # Only allow editing for the 'serial' column
        x, y, width, height = tree.bbox(selected_item, column)
        modi_entry.delete(0, tk.END)
        modi_entry.insert(0, tree.item(selected_item, 'values')[1])
        modi_entry.focus()
        modi_entry.bind("<Return>", lambda e: save_edit(modi_entry, selected_item, 1))
        modi_entry.bind("<FocusOut>", lambda e: save_edit(modi_entry, selected_item, 1))

def save_edit(entry, item, column_index):
    new_value = entry.get()
    tree.set(item, column=column_index, value=new_value)
    # Update the global data_list with the new value
    item_index = tree.index(item)
    global converted_list
    converted_list[item_index]["serial"] = new_value

# Set up the main Tkinter window
tab1_frame1 = tk.Frame(tab1)
tab1_frame1.pack(pady=5)

load_img_btn = tk.Button(tab1_frame1, text="Load Image", command=load_image)
load_img_btn.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

imgLabel = tk.Label(tab1_frame1)
imgLabel.grid(row=1, column=0, padx=10, pady=10)

# 구분선
separator = ttk.Separator(tab1_frame1, orient='vertical')
separator.grid(row=1, column=1, sticky='ns', padx=2)

# Treeview for displaying data
columns = ("no", "serial", "processed")
tree = ttk.Treeview(tab1_frame1, columns=columns, show="headings", height=20)

tree.heading("no", text="No")
tree.heading("serial", text="Serial")
tree.heading("processed", text="Processed")

tree.column("no", width=50, anchor="center")
tree.column("serial", width=150, anchor="center")
tree.column("processed", width=100, anchor="center")

tree.grid(row=1, column=3, padx=10, pady=10)

tree.bind("<Double-1>", edit_cell)

modi_entry = tk.Entry(tab1_frame1)
modi_entry.grid(row=2, column=0, columnspan=4, padx=10, pady=10)


# // 탭1 - 이미지 변환

# 탭2 - 이미지 다운로드
tab2_frame1 = tk.Frame(tab2)
tab2_frame1.pack(pady=5)

tempLabel = tk.Label(tab2_frame1,height=10, width=30)
tempLabel.grid(row=0, column=0, padx=10, pady=10)
tab2_button = tk.Button(tab2_frame1, text="Print Data", command=lambda: print(converted_list))
tab2_button.grid(row=0, column=1, padx=10, pady=10)

# // 탭2 - 이미지 다운로드

# 탭3 - 부가기능 영역
# 부가기능 - 대소문자 변환
tk.Label(tab3, text="대/소문자 변환", font=("맑은 고딕", 14)).pack(pady=10)

tab3_frame1 = tk.Frame(tab3)
tab3_frame1.pack(pady=5)

tk.Label(tab3_frame1, text="변환 전 : ").grid(row=0, column=0, padx=5, pady=5)
etc_cvt_input_before = tk.Entry(tab3_frame1, width=50)
etc_cvt_input_before.grid(row=0, column=1, padx=5, pady=5)
btn_convert = tk.Button(tab3_frame1, text="변환", command=lambda: convert_text(etc_cvt_input_before, etc_cvt_input_after))
btn_convert.grid(row=0, column=2, padx=5, pady=5)

tk.Label(tab3_frame1, text="변환 후 : ").grid(row=1, column=0, padx=5, pady=5)
etc_cvt_input_after = tk.Entry(tab3_frame1, width=50)
etc_cvt_input_after.grid(row=1, column=1, padx=5, pady=5)

btn_cvt_copy = tk.Button(tab3_frame1, text="복사", command=lambda: copy_entry_text(etc_cvt_input_after))
btn_cvt_copy.grid(row=1, column=2, padx=5, pady=5)

btn_delete = tk.Button(tab3_frame1, text="모두 지우기",
                       command=lambda: remove_text(etc_cvt_input_before, etc_cvt_input_after))
btn_delete.grid(row=2, column=1, padx=5, pady=5)


# 텍스트 변환 함수
def convert_text(input_before, input_after):
    text = input_before.get()
    converted_text = text.swapcase()  # 대/소문자 변환
    input_after.delete(0, tk.END)
    input_after.insert(0, converted_text)


# 엔트리 텍스트 복사 함수
def copy_entry_text(entry):
    root.clipboard_clear()
    root.clipboard_append(entry.get())


# 인풋 초기화 함수
def remove_text(input_before, input_after):
    input_before.delete(0, tk.END)
    input_after.delete(0, tk.END)


# // 부가기능 - 대소문자 변환

# 구분선
separator = ttk.Separator(tab3, orient='horizontal')
separator.pack(fill='x', pady=10)

# 부가기능 - 품목별 키워드 저장
tk.Label(tab3, text="품목별 키워드 저장", font=("맑은 고딕", 14)).pack(pady=10)

tab3_frame2 = tk.Frame(tab3)
tab3_frame2.pack(pady=5)

# 품목 리스트
tk.Label(tab3_frame2, text="품목", font=("맑은 고딕", 12)).grid(row=0, column=0, columnspan=2, padx=5, pady=5)

listbox = tk.Listbox(tab3_frame2, height=15, width=15)
listbox.grid(row=1, column=0, rowspan=4, columnspan=2, padx=5, pady=5)

btn_up = tk.Button(tab3_frame2, text="▲", command=lambda: move_up(listbox))
btn_up.grid(row=5, column=0, padx=5, pady=5)

btn_down = tk.Button(tab3_frame2, text="▼", command=lambda: move_down(listbox))
btn_down.grid(row=5, column=1, padx=5, pady=5)

# 구분선
separator = ttk.Separator(tab3_frame2, orient='vertical')
separator.grid(row=1, column=2, rowspan=4, sticky='ns', padx=10)

# 품목
tk.Label(tab3_frame2, text="품목명: ").grid(row=1, column=3, padx=5, pady=5)
etc_input_item = tk.Entry(tab3_frame2, width=30)
etc_input_item.grid(row=1, column=4, columnspan=4, padx=5, pady=5)

tk.Label(tab3_frame2, text="키워드: ").grid(row=2, column=3, padx=5, pady=5)
etc_input_kwd = tk.Text(tab3_frame2, height=10, width=30)
etc_input_kwd.grid(row=2, column=4, columnspan=4, padx=5, pady=5)

btn_kwd_copy = tk.Button(tab3_frame2, text="복사", command=lambda: copy_text(etc_input_kwd))
btn_kwd_copy.grid(row=3, column=4, padx=5, pady=5)

btn_kwd_modi = tk.Button(tab3_frame2, text="수정", command=lambda: mody_text(etc_input_kwd))
btn_kwd_modi.grid(row=3, column=5, padx=5, pady=5)

btn_kwd_reg = tk.Button(tab3_frame2, text="등록", command=lambda: reg_item(etc_input_item, etc_input_kwd))
btn_kwd_reg.grid(row=3, column=6, padx=5, pady=5)

btn_kwd_del = tk.Button(tab3_frame2, text="삭제", command=lambda: del_item(etc_input_item))
btn_kwd_del.grid(row=3, column=7, padx=5, pady=5)

# 복사
# 수정
# 새로 등록
# 삭제


# 데이터 파일 경로
ECT_KEYWORD_FILE = 'keyword.json'

# 초기 데이터
initial_data = {
    "상의1": "캐주얼자켓, 캐주얼아우터, 여름아우터, 여름자켓, 청자켓",
    "상의2": "반팔티, 캐주얼반팔, 반팔티셔츠, 쿨티셔츠",
    "바지": "키워드1, 키워드2",
    "신발": "키워드3, 키워드4",
    "가방": "키워드5, 키워드6"
}


# 데이터 로드 함수
def load_data():
    if not os.path.exists(ECT_KEYWORD_FILE):
        save_data(initial_data)
    with open(ECT_KEYWORD_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)


# 데이터 저장 함수
def save_data(data):
    with open(ECT_KEYWORD_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# 데이터 초기화
keyword_data = load_data()

# 초기 리스트박스 데이터 추가
for item in keyword_data.keys():
    listbox.insert(tk.END, item)


# 리스트박스 선택 시 키워드 출력
def on_select(event):
    selected = listbox.get(listbox.curselection())
    keywords = keyword_data.get(selected)
    etc_input_item.delete(0, tk.END)
    etc_input_item.insert(0, selected)
    etc_input_kwd.delete('1.0', tk.END)
    etc_input_kwd.insert("2.0", keywords)


listbox.bind('<<ListboxSelect>>', on_select)


# 순서 변경, 위로
def move_up(listbox):
    try:
        index = listbox.curselection()[0]
        if index > 0:
            item = listbox.get(index)
            listbox.delete(index)
            listbox.insert(index - 1, item)
            listbox.select_set(index - 1)
            update_data_from_listbox()
    except (IndexError, tk.TclError):
        pass


# 순서 변경, 아래로
def move_down(listbox):
    try:
        index = listbox.curselection()[0]
        if index < listbox.size() - 1:
            item = listbox.get(index)
            listbox.delete(index)
            listbox.insert(index + 1, item)
            listbox.select_set(index + 1)
            update_data_from_listbox()
    except (IndexError, tk.TclError):
        pass


# 품목 수정된 상태 그대로 저장하기
def update_data_from_listbox():
    items = listbox.get(0, tk.END)
    global keyword_data
    data = {item: keyword_data.get(item, "") for item in items}
    save_data(data)


# 텍스트 복사 함수
def copy_text(text):
    root.clipboard_clear()
    root.clipboard_append(text.get("1.0", tk.END))


# 텍스트 수정 함수
def mody_text(text):
    item_name = etc_input_item.get()
    keywords = text.get("1.0", tk.END).strip()
    if item_name in keyword_data:
        keyword_data[item_name] = keywords
        update_listbox()
        save_data(keyword_data)


def update_listbox():
    listbox.delete(0, tk.END)
    for item in keyword_data.keys():
        listbox.insert(tk.END, item)


# 품목 등록 함수
def reg_item(item_entry, text_widget):
    item = item_entry.get().strip()
    text = text_widget.get("1.0", tk.END).strip()

    if item and text:
        keyword_data[item] = text
        save_data(keyword_data)
        update_listbox()
        item_entry.delete(0, tk.END)
        text_widget.delete("1.0", tk.END)
        messagebox.showinfo("등록 완료", f"'{item}' 항목이 등록되었습니다.")
    else:
        messagebox.showwarning("입력 오류", "품목명과 키워드를 입력하세요.")


# 품목 삭제 함수
def del_item(item_entry):
    item = item_entry.get().strip()

    if item in keyword_data:
        if messagebox.askyesno("삭제 확인", f"'{item}' 항목을 삭제하시겠습니까?"):
            del keyword_data[item]
            save_data(keyword_data)
            update_listbox()
            item_entry.delete(0, tk.END)
            etc_input_kwd.delete("1.0", tk.END)
            messagebox.showinfo("삭제 완료", f"'{item}' 항목이 삭제되었습니다.")
    else:
        messagebox.showwarning("삭제 오류", "존재하지 않는 품목명입니다.")


# // 탭3 - 부가기능 영역

# 탭4 - 설정 영역
tk.Label(tab4, text="설정", font=("맑은 고딕", 14)).pack(pady=10)

tab4_frame1 = tk.Frame(tab4)
tab4_frame1.pack(pady=5)

tk.Label(tab4_frame1, text="전체 투명도 조절", font=("맑은 고딕", 14)).grid(row=0, column=0)

scaleVar = tk.IntVar()


def scaleSelect(self):
    value = "값 : " + str(scale.get())
    scaleLabel.config(text=value)
    root.attributes('-alpha', scale.get() / 100)  # 투명도 설정


scaleVar.set(100)  # 초기값 100 설정
scale = tk.Scale(tab4_frame1,
                 variable=scaleVar,
                 command=scaleSelect,
                 orient="horizontal",
                 showvalue=False,
                 tickinterval=10,
                 from_=10,
                 to=100,
                 resolution=10,
                 width=15,
                 length=300)
scale.grid(row=1, column=0, padx=10, pady=10)

scaleLabel = tk.Label(tab4_frame1, text="값 : 0")
scaleLabel.grid(row=2, column=0)

# 구분선
separator = ttk.Separator(tab4, orient='horizontal')
separator.pack(fill='x', pady=10)

tab4_frame2 = tk.Frame(tab4)
tab4_frame2.pack(pady=5)

tk.Label(tab4_frame2, text="항상 맨 위로", font=("맑은 고딕", 14)).grid(row=0, column=0)
btn_toggle_always_up = tk.Button(tab4_frame2, text="변경", command=lambda: onToggleAlwaysUp())
btn_toggle_always_up.grid(row=1, column=0, padx=5, pady=5)
toggleLabel = tk.Label(tab4_frame2, text="현재 상태 : 항상 맨 위로")
toggleLabel.grid(row=2, column=0)


def onToggleAlwaysUp():
    if root.attributes('-topmost'):
        root.attributes('-topmost', False)
        toggleLabel.config(text="현재 상태 : 순서대로")
    else:
        root.attributes('-topmost', True)
        toggleLabel.config(text="현재 상태 : 항상 맨 위로")

        # 구분선


separator = ttk.Separator(tab4, orient='horizontal')
separator.pack(fill='x', pady=10)

tab4_frame3 = tk.Frame(tab4)
tab4_frame3.pack(pady=5)
tk.Label(tab4_frame3, text="버그가 발생하거나,", font=("맑은 고딕", 14)).grid(row=0, column=0)
tk.Label(tab4_frame3, text="추가하고 싶은 기능이 생기면 언제든 연락주세요!!", font=("맑은 고딕", 14)).grid(row=1, column=0)
tk.Label(tab4_frame3, text="당신을 응원하는 김팔랑 드림♥️", font=("맑은 고딕", 14)).grid(row=3, column=0)

# // 탭4 - 설정 영역

root.mainloop()
