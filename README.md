# BsubTaskExecutor Class Documentation
## Overview
`BsubTaskExecutor` is a Python class designed for managing and executing parallel tasks, particularly useful in environments where batch job submissions are handled via commands like bsub. This class automates the process of loading tasks, submitting them, monitoring their status, and handling timeouts or failures.

## Features
1. Task Management: Load and manage execution tasks from a JSON file.
1. Parallel Execution: Control the number of tasks executed in parallel, respecting a defined upper limit.
1. Logging Support: Integration with a logging system to record important actions and errors.
1. Dynamic Task Handling: Monitor and update the status of each task dynamically.
1. Error and Timeout Handling: Manage task failures and timeouts proactively.

## Installation
No special installation steps are required beyond the basic Python setup. Ensure that the Python environment is configured with necessary permissions to execute system commands like bsub and bkill.

## Dependencies
1. Python 3.x
1. subprocess module for executing system commands
1. json module for loading tasks from a file
1. time module for handling sleep intervals
1. re module for regular expression operations

## Usage
Initialization
To use the BsubTaskExecutor, you must initialize it with a path to a JSON file containing the tasks to be executed. Optionally, you can specify the maximum number of parallel tasks and a logger for error logging.

```python
    from BsubTaskExecutor import BsubTaskExecutor
    # Initialize with task file and optional parallel limit and logger
    executor = BsubTaskExecutor(case_list='path/to/your/tasks.json', max_parallel=5, logger=my_logger)
```


## JSON File Format
The JSON file should contain a list of tasks, where each task is represented as a dictionary with at least the following keys:

1. command: The system command to be executed.
1. log: Path or identifier for logging output of the task.
1. tc: Timeout count for the task.
Example of tasks.json:
```json
  [
    {
        "command": "bsub -q my_queue make run seed=112233",
        "log": "./112233.log",
        "tc": 10
    },
    {
        "command": "bsub -q my_queue make run seed=223344",
        "log": "223344.log",
        "tc": 5
    }
]
```

### Running the Executor
Once initialized, you can start the task execution by calling the run method. This method will handle task submissions, monitoring, and other lifecycle events until all tasks are processed.

```python
# Run the executor to process all tasks
task_statuses = executor.run()
print(task_statuses)
```

## Monitoring and Logs
The executor will manage task statuses internally and can use the provided logger to output error messages or important information. Ensure your logger is configured to capture or display these messages as needed.

## Troubleshooting
* Task Fails to Submit: Check the command syntax and permissions.
* Tasks Not Completing: Verify the tc values are sufficient for tasks to complete.
* Logging Issues: Ensure the logger is correctly initialized and configured.
For any other issues or detailed usage questions, refer to the source code or contact the support team.
