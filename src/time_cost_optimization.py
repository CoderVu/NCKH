import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Hàm tính đường găng và thời gian
def critical_path_method(tasks):
    ids = [task["task"] for task in tasks]
    idx = {id: i for i, id in enumerate(ids)}
    n = len(tasks)

    e_m = np.zeros((n, n))  # Ma trận quan hệ trước (predecessors)
    l_m = np.zeros((n, n))

    # Xây dựng ma trận quan hệ
    for i, task in enumerate(tasks):
        for predecessor in task["predecessors"]:
            e_m[idx[predecessor], i] = 1
            l_m[idx[predecessor], i] = 1

    dates = np.zeros((n, 5))  # ES, EF, LS, LF, Slack
    dates[:, -2:] = float('inf')
    early = np.sum(e_m, axis=0)

    # Tính ES và EF
    while np.sum(early) != -len(early):
        for i in np.where(early == 0)[0]:
            early[i] = -1
            dates[i, 0] = max([dates[j, 1] for j in range(n) if e_m[j, i] == 1], default=0)
            dates[i, 1] = dates[i, 0] + tasks[i]["duration"]
            for j in range(n):
                if e_m[i, j] == 1:
                    early[j] -= 1

    finish_time = max(dates[:, 1])
    late = np.sum(l_m, axis=1)

    # Tính LS và LF
    while np.sum(late) != -len(late):
        for i in np.where(late == 0)[0]:
            late[i] = -1
            dates[i, 3] = min([dates[j, 2] for j in range(n) if l_m[i, j] == 1], default=finish_time)
            dates[i, 2] = dates[i, 3] - tasks[i]["duration"]
            dates[i, -1] = dates[i, 3] - dates[i, 1]
            for j in range(n):
                if l_m[j, i] == 1:
                    late[j] -= 1

    critical_path = [ids[i] for i in range(n) if dates[i, -1] == 0]
    dates_df = pd.DataFrame(dates, index=ids, columns=['ES', 'EF', 'LS', 'LF', 'Slack'])
    return dates_df, critical_path, finish_time
def optimize_cost_and_time(tasks, deadline):
    total_cost = 0  # Tổng chi phí tăng thêm
    task_updates = {}  # Sử dụng từ điển để lưu các công việc đã được cập nhật

    while True:
        # Xác định đường găng và tổng thời gian hiện tại
        dates_df, critical_path, total_time = critical_path_method(tasks)

        # Kiểm tra nếu đã đạt thời gian yêu cầu (deadline)
        if total_time <= deadline:
            break

        # Lọc ra các công việc trên đường găng có thể giảm thời gian
        reducible_tasks = [
            task for task in tasks
            if task["duration"] > task["duration_min"] and task["task"] in critical_path
        ]
        if not reducible_tasks:  # Không còn công việc nào có thể giảm
            break

        # Tính chi phí giảm thời gian trên mỗi đơn vị
        for task in reducible_tasks:
            task["crash_cost_per_time"] = round(
                (task["cost_min"] - task["cost"]) / (task["duration"] - task["duration_min"]),
                5  # Làm tròn đến 5 chữ số thập phân
            )

        # Sắp xếp các công việc có thể giảm thời gian theo chi phí tăng thêm tăng dần
        reducible_tasks.sort(key=lambda x: x["crash_cost_per_time"])

        # Chọn công việc có chi phí giảm thấp nhất để thực hiện giảm thời gian
        task_to_reduce = reducible_tasks[0]
        task_to_reduce["duration"] -= 1
        task_to_reduce["cost"] += task_to_reduce["crash_cost_per_time"]
        total_cost += task_to_reduce["crash_cost_per_time"]

        # Lưu thông tin cập nhật của công việc
        task_updates[task_to_reduce["task"]] = {
            "initial_duration": task_to_reduce["duration"] + 1,
            "updated_duration": task_to_reduce["duration"],
            "initial_cost": task_to_reduce["cost"] - task_to_reduce["crash_cost_per_time"],
            "updated_cost": task_to_reduce["cost"],
            "suggested_time": task_to_reduce["duration"],
            "additional_cost": task_to_reduce["crash_cost_per_time"]
        }

        # Cập nhật lại đường găng và thời gian hoàn thành
        dates_df, critical_path, total_time = critical_path_method(tasks)

    # Chuyển đổi từ điển task_updates thành danh sách
    task_updates_list = [{"task": task, **updates} for task, updates in task_updates.items()]

    return total_cost, total_time, task_updates_list


def gantt_chart(tasks, dates, size_x=15, size_y=10, show_slack=True, return_fig=False):
    finish_time = dates.iloc[:, 1].max()
    task_names = list(dates.index.values)
    fig, ax = plt.subplots(figsize=(size_x, size_y))
    yticks = np.arange(len(task_names)) * 2  # Space for task names
    xticks = np.arange(0, finish_time + 2)  # Time ticks
    height = 0.5  # Height of the bars

    # Định nghĩa màu sắc cho công việc
    colors = ['#007acc' if dates.iloc[i, -1] > 0 else '#00cc66' for i in range(len(dates))]

    ax.set_ylabel('Công việc')
    ax.set_xlabel('Thời gian (ngày)')
    ax.set_xlim(0, finish_time + 1)
    ax.set_xticks(xticks)
    plt.gca().invert_yaxis()  # Invert the y-axis to have the first task on top
    ax.grid(True)

    for i in range(len(dates)):
        start_time = dates.iloc[i, 0]
        end_time = dates.iloc[i, 1]
        duration = end_time - start_time
        ax.broken_barh([(start_time, duration)],
                       (yticks[i] - height / 2, height),
                       facecolors=colors[i])
        ax.text(start_time + duration / 2, yticks[i],
                task_names[i], ha='center', va='center', color='w')

        # Hiển thị thời gian dư nếu có
        if dates.iloc[i, -1] > 0 and show_slack:
            ax.hlines(y=yticks[i], xmin=dates.iloc[i, 1], xmax=dates.iloc[i, -2],
                      linewidth=1, color='red', linestyle='--')
            ax.plot(dates.iloc[i, -2], yticks[i], 'o', markersize=5, color='red')

            # Xử lý các mối liên kết
        if len(tasks[i]["predecessors"]) > 0:
            dependencies = tasks[i]["predecessors"]
            for item in dependencies:
                predecessor_index = task_names.index(item)
                pred_start = dates.iloc[predecessor_index, 0]
                conn_x = pred_start + (dates.iloc[predecessor_index, 1] - pred_start) / 2
                conn_y = yticks[predecessor_index] + 0.5 if yticks[predecessor_index] > yticks[i] else yticks[predecessor_index] - 0.5
                ax.hlines(y=yticks[i], xmin=dates.iloc[i, 0], xmax=conn_x, linewidth=1, color='black')
                ax.vlines(x=conn_x, ymin=yticks[i] - height / 2, ymax=conn_y, linewidth=1, color='black')

    # Thêm chú thích cho các loại đường
    ax.plot([], [], color='black', label='Mối quan hệ phụ thuộc', linestyle='-')
    ax.plot([], [], color='red', label='Thời gian dự trữ', linestyle='--')
    ax.plot([], [], color='#00cc66', label='Công việc găng', linestyle='-')
    ax.plot([], [], color='#007acc', label='Công việc không găng', linestyle='-')

    plt.legend()
    
    if return_fig:
        return fig
    else:
        plt.show()

def plot_diagonal_chart(tasks, dates_df, size_x=15, size_y=10, return_fig=False):
    task_times = {}

    for task in tasks:
        task_name = task["task"]
        start_week = dates_df.loc[task_name, 'ES']
        end_week = dates_df.loc[task_name, 'EF']
        task_times[task_name] = (start_week, end_week)

    fig, ax = plt.subplots(figsize=(size_x, size_y))

    for i, task in enumerate(tasks):
        task_name = task["task"]
        start_week, end_week = task_times[task_name]

        ax.plot([start_week, end_week], [i, i + 1], marker='o', label=task_name, lw=2, color='skyblue')
        ax.text((start_week + end_week) / 2, i + 0.5, task_name, ha='center', va='bottom', fontsize=10)

        for pred in task["predecessors"]:
            pred_start_week, pred_end_week = task_times[pred]
            pred_index = next(idx for idx, t in enumerate(tasks) if t["task"] == pred)

            ax.plot([pred_end_week, start_week], [pred_index + 1, i], linestyle='--', color='gray')

    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels([task["task"] for task in tasks])
    ax.set_title('Sơ đồ Xiên (Tiến trình công việc)')
    ax.grid(True)

    ax.set_xlim(0, max(task_times[task["task"]][1] for task in tasks) + 1)
    ax.set_ylim(-1, len(tasks))

    ax.axhline(0, color='black', lw=2)

    if return_fig:
        return fig
    else:
        plt.show()