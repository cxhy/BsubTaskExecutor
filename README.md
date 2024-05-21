# BsubTaskExecutor Class Documentation
## Overview

`BsubTaskExecutor` is a powerful and flexible Python module designed for developers and system administrators who need to manage and schedule tasks in LSF (Load Sharing Facility) environments. By leveraging the LSF system's bsub and bkill commands, this class provides a robust framework for automating task submissions, monitoring, and management with an emphasis on handling parallel executions efficiently.

This module simplifies the complexities associated with direct LSF job handling by providing a high-level interface that automates:

Task Submission: Automatically submits jobs to the LSF queue using the provided command specifications.
Concurrency Control: Manages the concurrency level of job execution according to user-defined limits, ensuring optimal resource utilization without overloading the system.
Real-Time Monitoring: Continuously monitors the status of submitted jobs, capturing updates and dynamically adjusting the task handling as needed.
Error and Timeout Handling: Proactively manages jobs that fail or exceed their runtime thresholds, with capabilities to retry or terminate tasks as configured.
Ideal for applications ranging from simple batch processing to complex data processing workflows, `BsubTaskExecutor` enhances productivity and reliability in job scheduling on LSF platforms. Whether integrating into data science pipelines, automation scripts, or backend services, this module provides a scalable solution to meet the demands of modern computational tasks.



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
To use the `BsubTaskExecutor`, you must initialize it with a path to a JSON file containing the tasks to be executed. Optionally, you can specify the maximum number of parallel tasks and a logger for error logging.

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

## License
`BsubTaskExecutor` is licensed under the GNU General Public License v3.0 (GPL-3.0), which ensures that the software remains free for all its users. This license permits users to run, study, share, and modify the software while ensuring that all copies and derivatives remain free as well.

For more details on the GPL-3.0 license, please visit [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html).

By integrating `BsubTaskExecutor` in your projects, you agree to comply with the terms and conditions of GPL-3.0.

