import time

PROGRESS_BAR_SIZE = 15


class Task:
    def __init__(self, task_name):
        self.name = task_name
        self.start_time = time.time()
        self.is_progressive_task = False
        self.is_done = False

    def get_execution_time(self):
        return round(time.time() - self.start_time, 2)


current_task = Task('')
current_subtask = Task('')


def start_task(task_name):
    global current_task
    if not current_task.is_done and current_task.name != '':
        end_current_task()
    current_task = Task(task_name)
    print(task_name)


def end_current_task():
    global current_task, current_subtask
    current_task.is_done = True
    if not current_subtask.is_done and current_subtask.name != '':
        end_current_subtask()
    print(f'└► Done in {current_task.get_execution_time()}s\n')


def start_subtask(task_name):
    global current_subtask
    if not current_subtask.is_done and current_subtask.name != '':
        end_current_subtask()
    current_subtask = Task(task_name)
    print(f'├► {current_subtask.name}', end='')


def set_subtask_progression(index, length):
    global current_subtask
    current_subtask.is_progressive_task = True
    progression = int(round(index * 100 / (length - 1)))
    if progression % 1 == 0:
        int_progression = int(round(progression * PROGRESS_BAR_SIZE / 100))

        bar = '█' * int_progression + '░' * (PROGRESS_BAR_SIZE - int_progression)
        time_remaining = round((length - index) * (time.time() - current_subtask.start_time) / (index + 1), 1)

        print(f'\r├► {current_subtask.name} {bar} {time_remaining}s    ', end='')

        if index == length - 1:
            end_current_subtask()


def end_current_subtask():
    global current_subtask
    current_subtask.is_done = True
    bar = '█' * PROGRESS_BAR_SIZE + ' done in ' if current_subtask.is_progressive_task else ''
    execution_time = str(current_subtask.get_execution_time()) + 's'
    print(f'\r├► {current_subtask.name} {bar}{execution_time}')
