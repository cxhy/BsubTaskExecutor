#! /usr/bin/python3
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# Author: guodz
# Email: cxhy1981@gmail.com
# Date: 2024
# Description: BsubTaskExecutor is a Python module designed to 
# streamline task scheduling and management in LSF environments, 
# offering automated job submission, real-time monitoring, and 
# robust error handling.

import json,re
import subprocess
import time

class BsubTaskExecutor:
    __MAX_PARALLEL_LIMIT = 50

    def __init__(self,case_list,max_parallel=3,logger=None):
        self.case_list = case_list
        self.__set_and_calculate_max_parallel_limit()
        self.max_parallel = max(1,min(max_parallel,self.__MAX_PARALLEL_LIMIT))
        self.logger = logger
        self.tasks = []
        self.task_status = {}
        self.task_timeouts = {}
        self.task_cnt = {}
        self.load_case()

    def __set_and_calculate_max_parallel_limit(self):
        new_limit = 50 
        self.__MAX_PARALLEL_LIMIT = new_limit

    def load_case(self):
        with open(self.case_list,'r') as file:
            data = json.load(file)
            for case in data:
                task = case['command']
                log  = case['log']
                tc   = case['tc']
                self.tasks.append((task,log,tc))
                self.task_status[task] = 'PEND'
                self.task_cnt[task] = 0
                self.task_timeouts[task] = tc

    def submit_task(self,task):
        command = task[0]
        try:
            result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            jobid = result.stdout.read().decode().strip()
            jobid_match = re.search(r"Job <(\d+)>", jobid)
            if jobid_match:
                jobid = jobid_match.group(1)
                return jobid
        except subprocess.CalledProcessError as e:
            if self.logger:
                self.logger.error(f"Error submitting task : {task}, Error : {e}")
                return None

    def update_tasks_status(self,running_task):
        command = "bjobs"
        try:
            result = subprocess.run(command,shell=True,capture_output=True,text=True)
            output_lines = result.stdout.strip().split('\n')[1:]
            status_map = {line.split()[0]: line.split()[2] for line in output_lines}

            for task, jobid in running_task.items():
                if jobid in status_map:
                    status = status_map[jobid]
                    self.task_status[task] = status
                else:
                    self.task_status[task] = 'DONE'
        except subprocess.CalledProcessError as e:
            if self.logger:
                self.logger.error(f"Error checking status for jobid: {list(running_task.values())}, Error: {e}")


    def kill_task(self,jobid):
        command = f"bkill {jobid}"
        try:
            subprocess.run(command, shell=True)
        except subprocess.CalledProcessError as e:
            if self.logger:
                self.logger.error(f"Error killing jobid: {jobid}, Error: {e}")

    def get_task_timeout(self, task):
        return self.task_timeouts.get(task)

    def monitor_tasks(self):
        running_task = {}
        while self.tasks or running_task:
            self.update_tasks_status(running_task)
            for task, jobid in list(running_task.items()):
                status = self.task_status[task]
                if status == 'RUN':
                    self.task_cnt[task] += 1
                    if self.task_cnt[task] > self.get_task_timeout(task):
                        self.task_status[task] = 'TIMEOUT'
                elif status == 'DONE':
                    del running_task[task]
                elif status == 'TIMEOUT':
                    self.kill_task(jobid)
                    del running_task[task]
            available_slots = self.max_parallel - len(running_task)
            while available_slots > 0 and self.tasks:
                task = self.tasks.pop(0)
                jobid = self.submit_task(task)
                if jobid:
                    running_task[task[0]] = jobid
                    self.task_status[task[0]] = 'RUN'
                    available_slots -= 1
            if running_task or self.tasks:
                time.sleep(60)
        return self.task_status

    def run(self):
        return self.monitor_tasks()




def main():
    pass


if __name__ == "__main__":
    main()
