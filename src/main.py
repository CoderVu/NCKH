import tkinter as tk
from home import TimeCostOptimizationApp

class IntroductionWindow:
    def __init__(self, master):
        self.master = master
        master.title("Giới thiệu")
        master.geometry("700x500")
        master.config(bg="#f0f8ff")  

        # Khung chứa nội dung chính
        main_frame = tk.Frame(master, bg="white", bd=3, relief="ridge")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)

        # Tiêu đề
        label_title = tk.Label(main_frame, text="Đại học Bách Khoa Đà Nẵng", 
                               font=("Arial", 24, "bold"), fg="#4b0082", bg="white")
        label_title.pack(pady=20)

        # Thông tin sinh viên
        label_student = tk.Label(main_frame, text="Sinh viên: Nguyễn Văn A", 
                                 font=("Arial", 16), fg="#2f4f4f", bg="white")
        label_student.pack(pady=5)

        # Chủ đề đồ án
        label_topic = tk.Label(main_frame, 
                               text="CHƯƠNG TRÌNH TỐI ƯU HÓA SƠ ĐỒ MẠNG\nTHEO TIÊU CHÍ THỜI GIAN VÀ CHI PHÍ", 
                               font=("Arial", 14), fg="#483d8b", bg="white", justify="center")
        label_topic.pack(pady=10)

        # Nút bắt đầu
        start_button = tk.Button(main_frame, text="Bắt đầu", 
                                 font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", 
                                 activebackground="#4CAF50", activeforeground="white",
                                 cursor="hand2", relief="raised", bd=2, 
                                 command=self.start_app)
        start_button.pack(pady=20)

      
        start_button.bind("<Enter>", lambda e: start_button.config(bg="#4CAF50"))
        start_button.bind("<Leave>", lambda e: start_button.config(bg="#4CAF50"))

    def start_app(self):
        self.master.destroy()
        root = tk.Tk()
        app = TimeCostOptimizationApp(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    intro = IntroductionWindow(root)
    root.mainloop()
