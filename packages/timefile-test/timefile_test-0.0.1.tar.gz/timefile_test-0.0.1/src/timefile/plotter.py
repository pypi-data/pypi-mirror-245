import re
from . import config
import ast
import matplotlib.pyplot as plt


def _plot_and_save(f_name: str, y: list, y_name: str, t: list, t_name: str = "time_delta"):
    plt.scatter(y, t)
    plt.xlabel(y_name)
    plt.ylabel(t_name)
    plt.title(f'Scatter Plot: {y_name} vs. {t_name}')
    plt.savefig(f"{config.PLOT_DIR}/{f_name}_{y_name}.png")

def _plot_function(func_name: str, func_logs: list[dict]):
    flat_func_logs = {"time_delta": []}
    for log in func_logs:
        log = ast.literal_eval(log)
        flat_func_logs["time_delta"].append(log.pop("time_delta"))
        for k, v in log["kwargs"].items():
            if k not in flat_func_logs:
                flat_func_logs[k] = []
            flat_func_logs[k].append(v)
    
    time_delta_logs = flat_func_logs.pop("time_delta")
    for k, v in flat_func_logs.items():
        _plot_and_save(f_name=func_name, y=v, y_name=k, t=time_delta_logs)

    
def _plot_functions(functions: dict[list[dict]]):
     for k, v in functions.items():
        _plot_function(k, v)

def timeplot():
    functions = {}
    log_pattern = re.compile(r'(?P<timestamp>.*?) \[(?P<level>.*?)\] \[(?P<function_name>.*?)\]: (?P<message>.*)')
    with open(config.LOG_FILEPATH, 'r') as log_file:
        for line in log_file:
            match = log_pattern.match(line)
            if match:
                # timestamp_str = match.group('timestamp')
                # timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                # level = match.group('level')
                function_name = match.group('function_name')

                # TODO: Find a better way
                if function_name in config.BAD_FUNCTIONS:
                    continue

                if function_name not in functions:
                    functions[function_name] = []

                message = match.group('message')
                functions[function_name].append(message)
    _plot_functions(functions)