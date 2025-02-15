import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import pandas as pd
from result import open_result_window 
from time_cost_optimization import optimize_cost_and_time, critical_path_method

class TimeCostOptimizationApp:
    def __init__(self, master):
        self.master = master
        style = ttk.Style()
        master.title("CHƯƠNG TRÌNH TỐI ƯU HÓA SƠ ĐỒ MẠNG THEO CHỈ TIÊU THỜI GIAN - CHI PHÍ")
        master.state('zoomed')
        style.configure("Treeview", rowheight=30, borderwidth=1)
        style.configure("Treeview", rowheight=30, borderwidth=1, relief="solid")
        style.configure("Treeview", fieldbackground="white", background="white")
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        style.map("Treeview", background=[("selected", "#347083")])
        
        self.create_widgets()
        self.initialize_tasks()
        self.selected_item = None
    
    def create_widgets(self):
        # Định nghĩa phông chữ in đậm
        bold_font = ("Arial", 10, "bold")

        # Tiêu đề chính
        title_label = tk.Label(
            self.master, text="CHƯƠNG TRÌNH TỐI ƯU HÓA SƠ ĐỒ MẠNG", 
            font=("Arial", 14, "bold"), fg="blue", bg="#f4f4f4"
        )
        title_label.grid(row=0, column=0, columnspan=6, pady=10)
        
        # Định nghĩa các cột
        columns = ("Tên công việc", "T.gian b.thường", "T.gian khẩn", "Cp.bình thường", "Cp.khẩn trương", "Trước")
        
        self.tree = ttk.Treeview(self.master, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        self.tree.grid(row=1, column=0, columnspan=6, padx=10, pady=10, sticky='nsew')

        # Thêm thanh cuộn dọc
        scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=1, column=6, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Khung chứa các ô nhập liệu
        entry_frame = tk.Frame(self.master, bg="#f4f4f4")
        entry_frame.grid(row=2, column=0, columnspan=6, pady=10)

        self.entries = {}
        for i, col in enumerate(columns):
            label = tk.Label(entry_frame, text=col, bg="#f4f4f4")
            label.grid(row=0, column=i, padx=5)
            entry = tk.Entry(entry_frame)
            entry.grid(row=1, column=i, padx=5)
            self.entries[col] = entry

        # Khung chứa các nút bấm
        btn_frame = tk.Frame(self.master, bg="#f4f4f4")
        btn_frame.grid(row=3, column=0, columnspan=6, pady=10)

        tk.Button(btn_frame, text="Thêm hàng", command=self.add_row, bg="gray", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Xóa hàng", command=self.delete_row, bg="gray", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Lưu", command=self.save_data, bg="gray", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Trở lại", command=self.reset_data, bg="gray", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Chỉnh sửa", command=self.edit_row, bg="gray", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=4, padx=5)
        tk.Button(btn_frame, text="Tệp", command=self.import_csv, bg="gray", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=5, padx=5)
        tk.Button(btn_frame, text="Xóa toàn bộ", command=self.clear_data, bg="gray", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=6, padx=5)

        # Thêm ô nhập liệu cho deadline
        deadline_label = tk.Label(btn_frame, text="Deadline", bg="#f4f4f4")
        deadline_label.grid(row=0, column=7, padx=5)
        self.deadline_entry = tk.Entry(btn_frame)
        self.deadline_entry.grid(row=0, column=8, padx=5)

        tk.Button(btn_frame, text="Tối ưu", command=self.optimize, bg="gray", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=9, padx=5)
        
    def initialize_tasks(self):
        # Danh sách công việc có sẵn
        predefined_tasks = [
            {"task": "1-2", "duration": 5, "duration_min": 3, "cost": 2, "cost_min": 2.5, "predecessors": []},
            {"task": "1-3", "duration": 4, "duration_min": 4, "cost": 3, "cost_min": 3, "predecessors": []},
            {"task": "1-4", "duration": 8, "duration_min": 7, "cost": 4, "cost_min": 5, "predecessors": []},
            {"task": "2-3", "duration": 3, "duration_min": 2, "cost": 1.2, "cost_min": 1.5, "predecessors": ["1-2"]},
            {"task": "2-6", "duration": 7, "duration_min": 5, "cost": 2, "cost_min": 3, "predecessors": ["1-2"]},
            {"task": "3-5", "duration": 3, "duration_min": 3, "cost": 8, "cost_min": 8, "predecessors": ["1-3", "2-3"]},
            {"task": "4-5", "duration": 5, "duration_min": 5, "cost": 3, "cost_min": 3, "predecessors": ["1-4"]},
            {"task": "4-7", "duration": 4, "duration_min": 3, "cost": 3, "cost_min": 3.7, "predecessors": ["1-4"]},
            {"task": "5-6", "duration": 9, "duration_min": 6, "cost": 0.7, "cost_min": 1.6, "predecessors": ["3-5"]},
            {"task": "5-7", "duration": 11, "duration_min": 7, "cost": 1.5, "cost_min": 2, "predecessors": ["3-5"]},
            {"task": "6-8", "duration": 8, "duration_min": 6, "cost": 0.6, "cost_min": 1.5, "predecessors": ["2-6", "5-6"]},
            {"task": "7-8", "duration": 10, "duration_min": 9, "cost": 1, "cost_min": 1.05, "predecessors": ["4-7", "5-7"]}
        ]
        self.tasks = predefined_tasks

        # Thêm dữ liệu vào bảng
        for task in predefined_tasks:
            self.tree.insert("", "end", values=(task["task"], task["duration"], task["duration_min"], task["cost"], task["cost_min"], ", ".join(task["predecessors"])))

    def add_row(self):
        """Thêm một dòng mới vào bảng từ các ô nhập liệu"""
        values = [self.entries[col].get() for col in self.entries]
        self.tree.insert("", "end", values=values)
        self.save_data()  # Lưu dữ liệu sau khi thêm hàng
        for entry in self.entries.values():
            entry.delete(0, tk.END)
    
    def delete_row(self):
        """Xóa dòng được chọn"""
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
            self.save_data(is_delete=True)  # Lưu dữ liệu sau khi xóa hàng
    
    def edit_row(self):
        """Chỉnh sửa dòng được chọn"""
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_item = selected_item
            values = self.tree.item(selected_item)["values"]
            for i, col in enumerate(self.entries):
                self.entries[col].delete(0, tk.END)
                self.entries[col].insert(0, values[i])
    
    def save_data(self, is_delete=False, is_import=False):
        """Lưu dữ liệu từ bảng vào danh sách"""
        task = self.entries["Tên công việc"].get().strip()
        if task or is_delete:
            if self.selected_item and not is_delete:
                # Cập nhật hàng đã chọn
                values = [self.entries[col].get() for col in self.entries]
                self.tree.item(self.selected_item, values=values)
                self.selected_item = None
            elif not is_delete:
                # Thêm hàng mới
                values = [self.entries[col].get() for col in self.entries]
                self.tree.insert("", "end", values=values)
            
            self.tasks = []
            for row in self.tree.get_children():
                values = self.tree.item(row)["values"]
                if values[0]:  # Chỉ lưu nếu có công việc
                    task_data = {
                        "task": values[0],
                        "duration": int(values[1]) if values[1] else 0,
                        "duration_min": int(values[2]) if values[2] else 0,
                        "cost": float(values[3]) if values[3] else 0.0,
                        "cost_min": float(values[4]) if values[4] else 0.0,
                        "predecessors": [p.strip() for p in values[5].split(',') if p.strip()]
                    }
                    self.tasks.append(task_data)
            if not is_delete and not is_import:
                messagebox.showinfo("Lưu dữ liệu", "Dữ liệu đã được lưu thành công!")
            # Xóa các ô nhập liệu sau khi lưu
            for entry in self.entries.values():
                entry.delete(0, tk.END)
        elif not is_delete and not is_import:
            messagebox.showerror("Lỗi", "Tên công việc không được để trống!")   
           
            
    
    def reset_data(self):
        """Xóa dữ liệu trong bảng và khởi tạo lại"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.initialize_tasks()
    def clear_data(self, is_import=False):
        """Xóa dữ liệu trong Treeview"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        if not is_import:
            messagebox.showinfo("Clear Data", "Dữ liệu đã được xóa thành công!")
    
   
    def import_csv(self):
        """Nhập dữ liệu từ file CSV"""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                df = pd.read_csv(file_path)
                df = df.fillna('')  # Thay thế NaN bằng chuỗi rỗng
                self.clear_data(is_import=True)
                for _, row in df.iterrows():
                    self.tree.insert("", "end", values=(row["Tên công việc"], row["T.gian b.thường"], row["T.gian khẩn"], row["Cp.bình thường"], row["Cp.khẩn trương"], row["Trước"]))
                self.save_data(is_import=True)
                messagebox.showinfo("Nhập dữ liệu", "Dữ liệu đã được nhập thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể nhập dữ liệu từ file CSV: {e}")

    def get_tasks_from_treeview(self):
        """Lấy dữ liệu từ Treeview"""
        tasks = []
        for row in self.tree.get_children():
            values = self.tree.item(row)["values"]
            if values[0]:  # Chỉ lưu nếu có công việc
                task_data = {
                    "task": values[0],
                    "duration": int(values[1]) if values[1] else 0,
                    "duration_min": int(values[2]) if values[2] else 0,
                    "cost": float(values[3]) if values[3] else 0.0,
                    "cost_min": float(values[4]) if values[4] else 0.0,
                    "predecessors": [p.strip() for p in values[5].split(',') if p.strip()]
                }
                tasks.append(task_data)
        return tasks
    def optimize(self):
        try:
            deadline = int(self.deadline_entry.get().strip())
            # Lấy dữ liệu từ Treeview
            self.tasks = self.get_tasks_from_treeview()
            # Store original durations and costs
            original_tasks = [{**task} for task in self.tasks]
            
            # Calculate initial total duration and cost
            dates_df, critical_path, initial_finish_time = critical_path_method(self.tasks)
            initial_total_cost = sum(task["cost"] for task in self.tasks)

            # Perform optimization
            total_cost, total_time, task_updates = optimize_cost_and_time(self.tasks, deadline)

            results = []
            for original_task in original_tasks:
                task = next(task for task in self.tasks if task["task"] == original_task["task"])
                is_critical = "Yes" if task["task"] in critical_path else "No"
                task_update = next((update for update in task_updates if update["task"] == task["task"]), {})
                suggested_time = task_update.get("suggested_time", original_task["duration"])
                additional_cost = task_update.get("additional_cost", "N/A")
                es = dates_df.loc[task['task'], 'ES']
                ef = dates_df.loc[task['task'], 'EF']
                ls = dates_df.loc[task['task'], 'LS']
                lf = dates_df.loc[task['task'], 'LF']
                slack = dates_df.loc[task['task'], 'Slack']
                results.append((
                    task['task'], 
                    is_critical,
                    original_task['duration'], 
                    original_task['duration_min'], 
                    suggested_time, 
                    original_task['cost'], 
                    original_task['cost_min'], 
                    additional_cost, 
                    ", ".join(original_task['predecessors']),
                    es, ef, ls, lf, slack
                ))

            # Create summary
            summary = f"Đường găng: {', '.join(critical_path)}\n"
            summary += f"Thời gian hoàn thành ban đầu: {initial_finish_time}\n"
            summary += f"Thời gian hoàn thành sau tối ưu: {total_time}\n"
            summary += f"Chi phí ban đầu: {initial_total_cost}\n"
            summary += f"Chi phí sau tối ưu: {initial_total_cost + total_cost}\n"
           
            open_result_window(results, summary, self.tasks, dates_df)
        except Exception as e:
            messagebox.showerror("Error", str(e))
# Chạy chương trình
if __name__ == "__main__":
    root = tk.Tk()
    app = TimeCostOptimizationApp(root)
    root.mainloop()