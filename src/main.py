import tkinter as tk
from home import TimeCostOptimizationApp

class IntroductionWindow:
    def __init__(self, master):
        self.master = master
        master.title("Giới thiệu")
        master.geometry("600x400")

        label_title = tk.Label(master, text="Đại học Bách Khoa Đà Nẵng", font=("Arial", 20, "bold"))
        label_title.pack(pady=20)

        label_student = tk.Label(master, text="Sinh viên: Nguyễn Văn A", font=("Arial", 14))
        label_student.pack(pady=10)

        label_topic = tk.Label(master, text="CHƯƠNG TRÌNH TỐI ƯU HÓA SƠ ĐỒ MẠNG THEO TIÊU CHÍ THỜI GIAN VÀ CHI PHÍ", font=("Arial", 14))
        label_topic.pack(pady=10)

        start_button = tk.Button(master, text="Bắt đầu", command=self.start_app, font=("Arial", 14, "bold"), bg="gray", fg="white")
        start_button.pack(pady=20)

    def start_app(self):
        self.master.destroy()
        root = tk.Tk()
        app = TimeCostOptimizationApp(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    intro = IntroductionWindow(root)
    root.mainloop()