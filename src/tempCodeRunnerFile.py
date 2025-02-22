import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from home import TimeCostOptimizationApp 

class ProjectOptimizationApp:
    def __init__(self, master):
        self.master = master
        master.title("Tối ưu hóa sơ đồ mạng")
        master.geometry("880x500")
        master.config(bg="#E3F2FD")

        title_label = tk.Label(
            master,
            text="CHƯƠNG TRÌNH TỐI ƯU HÓA SƠ ĐỒ MẠNG\nTHEO TIÊU CHÍ THỜI GIAN VÀ CHI PHÍ",
            font=("Helvetica", 17, "bold"),
            fg="#00796B",
            bg="#E3F2FD",
            justify="center",
            padx=20,
            pady=12
        )
        title_label.pack(pady=10)

        main_frame = tk.Frame(master, bg="white", bd=3, relief="ridge")
        main_frame.pack(pady=10, padx=20, fill="both", expand=True)

        logo_frame = tk.Frame(main_frame, bg="white")
        logo_frame.pack(side="left", padx=20, pady=20)

        try:
            logo = Image.open("e:/Python/nghiencuu/GIT/NCKH/src/image/logo.png")
            logo = logo.resize((220, 220), Image.LANCZOS)
            logo_image = ImageTk.PhotoImage(logo)

            logo_label = tk.Label(logo_frame, image=logo_image, bg="white")
            logo_label.image = logo_image
            logo_label.pack()
        except Exception as e:
            print("Lỗi khi tải ảnh:", e)

        input_frame = tk.Frame(main_frame, bg="white", bd=2, relief="ridge")
        input_frame.pack(side="right", padx=30, pady=30, fill="both", expand=True)
        

        input_title = tk.Label(
            input_frame,
            text="Nhập các thông số của dự án",
            font=("Arial", 15, "bold"),
            fg="#00796B",
            bg="white"
        )
        input_title.grid(row=0, column=0, columnspan=2, pady=12)

        # Cấu hình khung nhập liệu đẹp hơn
        def create_labeled_entry(parent, label_text, row):
            label = tk.Label(parent, text=label_text, font=("Arial", 13, "bold"), bg="white")
            label.grid(row=row, column=0, padx=10, pady=10, sticky="w")

            entry = tk.Entry(parent, width=30, font=("Arial", 13), bg="#F1F8E9", bd=2, relief="solid")
            entry.grid(row=row, column=1, padx=10, pady=10, sticky="w")
            return entry

        self.entry_name = create_labeled_entry(input_frame, "Tên dự án", 1)
        self.entry_time_unit = create_labeled_entry(input_frame, "Đơn vị thời gian", 2)

        button_frame = tk.Frame(input_frame, bg="white")
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        execute_button = tk.Button(
            button_frame, text="Thực hiện", font=("Arial", 13, "bold"),
            bg="#4CAF50", fg="white", width=10, height=1, command=self.validate_and_proceed
        )
        execute_button.pack(side="left", padx=(30, 10))

        cancel_button = tk.Button(
            button_frame, text="Hủy bỏ", font=("Arial", 13, "bold"),
            bg="#D32F2F", fg="white", width=10, height=1, command=master.quit
        )
        cancel_button.pack(side="left", padx=(10, 30))
        cancel_button.pack(side="left", padx=10)

    def validate_and_proceed(self):
        name = self.entry_name.get().strip()
        time_unit = self.entry_time_unit.get().strip()

        if not name or not time_unit:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return 

        self.master.destroy()
        root = tk.Tk()
        app = TimeCostOptimizationApp(root, name, time_unit)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectOptimizationApp(root)
    root.mainloop()
