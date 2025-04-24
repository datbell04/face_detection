import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Listbox, simpledialog
import requests
import subprocess
from tkinter import font as tkfont

API_UPLOAD = "http://localhost:5000/upload"
API_LIST = "http://localhost:5000/images"
API_DELETE = "http://localhost:5000/delete"


def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        name = simpledialog.askstring("Đặt tên ảnh", "Nhập tên cho ảnh này:")
        if not name:
            messagebox.showwarning("Thiếu tên", "Bạn chưa nhập tên ảnh.")
            return
        with open(file_path, 'rb') as f:
            files = {'image': f}
            data = {'name': name}
            try:
                response = requests.post(API_UPLOAD, files=files, data=data)
                if response.status_code == 200:
                    messagebox.showinfo("Thành công", "Ảnh đã được upload lên server.")
                    status_var.set("✅ Ảnh đã upload thành công!")
                else:
                    messagebox.showerror("Lỗi", f"Không thể upload ảnh. Mã lỗi: {response.status_code}")
                    status_var.set("❌ Upload thất bại!")
            except Exception as e:
                messagebox.showerror("Lỗi kết nối", str(e))
                status_var.set("❌ Lỗi kết nối khi upload ảnh.")

def run_face_recognition():
    try:
        subprocess.run(["python", "face_detection.py"])
        status_var.set("🔍 Đã chạy nhận diện khuôn mặt.")
    except Exception as e:
        messagebox.showerror("Lỗi khi chạy nhận diện", str(e))
        status_var.set("❌ Lỗi khi chạy nhận diện.")

def load_images_to_listbox(listbox):
    try:
        response = requests.get(API_LIST)
        if response.status_code == 200:
            images = response.json()
            listbox.delete(0, tk.END)
            for img in images:
                listbox.insert(tk.END, img)
        else:
            messagebox.showerror("Lỗi", "Không thể lấy danh sách ảnh.")
    except Exception as e:
        messagebox.showerror("Lỗi kết nối", str(e))

def delete_image(listbox):
    try:
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Chưa chọn ảnh", "Vui lòng chọn một ảnh để xoá.")
            return
        selected_image = listbox.get(selection[0])
        parts = selected_image.split(':')
        if len(parts) < 2:
            messagebox.showerror("Lỗi", "Không thể trích xuất ID ảnh.")
            return
        image_id = parts[1].split(',')[0].strip().strip("'")
        response = requests.delete(f"{API_DELETE}/{image_id}")
        if response.status_code == 200:
            messagebox.showinfo("Thành công", "Ảnh đã được xoá khỏi server.")
            listbox.delete(selection[0])
            status_var.set("🗑️ Ảnh đã được xoá.")
        else:
            messagebox.showerror("Lỗi", f"Không thể xoá ảnh. Mã lỗi: {response.status_code}")
            status_var.set("❌ Lỗi khi xoá ảnh.")
    except requests.exceptions.RequestException as req_err:
        messagebox.showerror("Lỗi kết nối", f"Lỗi khi gọi API: {str(req_err)}")
    except Exception as e:
        messagebox.showerror("Lỗi không xác định", str(e))

def show_image_list():
    try:
        response = requests.get(API_LIST)
        if response.status_code == 200:
            win = Toplevel(root)
            win.title("📂 Danh sách ảnh")
            win.geometry("400x400")
            win.configure(bg="#fdfdfd")

            label = tk.Label(win, text="🖼️ Danh sách ảnh đã lưu", font=("Helvetica", 14, "bold"), bg="#fdfdfd")
            label.pack(pady=10)

            listbox = Listbox(win)
            listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

            images = response.json()
            for img in images:
                listbox.insert(tk.END, img)

            btn_frame = tk.Frame(win, bg="#fdfdfd")
            btn_frame.pack(pady=10)

            btn_delete = tk.Button(btn_frame, text="🗑️ Xoá ảnh", command=lambda: delete_image(listbox), width=15)
            btn_delete.grid(row=0, column=0, padx=5)

            btn_reset = tk.Button(btn_frame, text="🔄 Tải lại", command=lambda: load_images_to_listbox(listbox), width=15)
            btn_reset.grid(row=0, column=1, padx=5)
        else:
            messagebox.showerror("Lỗi", "Không thể lấy danh sách ảnh.")
    except Exception as e:
        messagebox.showerror("Lỗi kết nối", str(e))


# === GUI CHÍNH ===
root = tk.Tk()
root.title("🧠 Face Recognition App")
root.geometry("500x350")
root.configure(bg="#f5faff")

title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")

# Tiêu đề
title_label = tk.Label(root, text="🧠 Ứng dụng Nhận diện Khuôn mặt", font=title_font, bg="#f5faff", fg="#2b2b2b")
title_label.pack(pady=20)

# Nút trong một khung riêng
btn_frame = tk.Frame(root, bg="#f5faff")
btn_frame.pack()

def create_hover_button(text, command, bg, row):
    btn = tk.Button(btn_frame, text=text, command=command, height=2, bg=bg, relief=tk.RAISED)
    btn.grid(row=row, column=0, pady=5, sticky="ew", padx=20)  # sticky="ew" giúp nút mở rộng ngang
    # Hiệu ứng hover
    btn.bind("<Enter>", lambda e: btn.config(bg="#d9f1ff"))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn


create_hover_button("📤 Upload ảnh", upload_image, "#e6f7ff", 0)
create_hover_button("🔍 Nhận diện khuôn mặt", run_face_recognition, "#e6ffe6", 1)
create_hover_button("🖼️ Danh sách ảnh trong CSDL", show_image_list, "#fff0e6", 2)

# Thanh trạng thái
status_var = tk.StringVar()
status_var.set("⚡ Sẵn sàng")

status_bar = tk.Label(root, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#e6e6e6")
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()
