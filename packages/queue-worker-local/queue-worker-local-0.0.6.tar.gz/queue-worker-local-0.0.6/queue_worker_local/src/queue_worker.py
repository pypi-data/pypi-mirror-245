import argparse
import json
import multiprocessing
import random
import subprocess
import sys
import time

from circles_local_database_python.generic_crud import Connector, GenericCRUD
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from queue_local.database_queue import DatabaseQueue

QUEUE_WORKER_COMPONENT_ID = 159
QUEUE_WORKER_COMPONENT_NAME = 'queue_worker_local_python_package/src/queue_worker.py'
DEVELOPER_EMAIL = 'akiva.s@circ.zone'

installed = []  # to avoid installing the same package multiple times


class QueueWorker(DatabaseQueue):
    def __init__(self, schema_name: str = "queue", table_name: str = "queue_item_table",
                 view_name: str = "queue_item_view", id_column_name: str = "queue_item_id",
                 connection: Connector = None) -> None:
        super().__init__(schema_name=schema_name, table_name=table_name, view_name=view_name,
                         id_column_name=id_column_name, connection=connection)
        self.logger = Logger(object={'component_id': QUEUE_WORKER_COMPONENT_ID,
                                     'component_name': QUEUE_WORKER_COMPONENT_NAME,
                                     'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
                                     'developer_email': DEVELOPER_EMAIL})
        self.all_actions = self.get_all_actions()

    def execute(self, action_ids: tuple, min_delay_after_execution_ms: float, max_delay_after_execution_ms: float,
                total_missions: int = sys.maxsize) -> None:
        """Execute tasks from the queue."""
        self.install_packages(action_ids)
        max_delay_after_execution_ms = max(max_delay_after_execution_ms, min_delay_after_execution_ms)
        try:
            self.logger.start("START execute", object={
                "action_ids": action_ids,
                "min_delay_after_execution_ms": min_delay_after_execution_ms,
                "max_delay_after_execution_ms": max_delay_after_execution_ms,
                "total_missions": total_missions})

            for mission in range(total_missions):
                queue_item = self.get(action_ids=action_ids)
                if not queue_item:
                    self.logger.info(f'The queue does not have more items of action_ids {action_ids}')
                    break

                try:
                    function_parameters = json.loads(queue_item["function_parameters_json"] or "{}")
                    class_parameters = json.loads(queue_item["class_parameters_json"] or "{}")
                    formatted_function_params = ', '.join(
                        [f'{key}={repr(value)}' for key, value in function_parameters.items()])
                except json.decoder.JSONDecodeError as e:
                    self.logger.exception('Wrong json format', object=e)
                    raise

                action = self.get_action(queue_item)
                filename = action["filename"]
                function_name = action["function_name"]

                if filename.endswith('.py'):
                    args = self._get_python_args(action, class_parameters, function_parameters)
                # elif...
                else:
                    self.logger.exception("Unsupported file extension " + filename +
                                          " for action " + str(queue_item['action_id']))
                    break

                self.logger.info(f'Executing the following shell script: {" ".join(args)}')
                result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if "returned_value: " in result.stdout:
                    # TODO: the delimiter should be defined once
                    stdout, returned_value = result.stdout.split("returned_value: ")
                else:
                    stdout = result.stdout
                    returned_value = None
                stderr = result.stderr
                return_code = result.returncode
                return_message = "Success" if return_code == 0 else "Error"

                data_json = {
                    "stdout": stdout,
                    "stderr": stderr,
                    "return_code": return_code,
                    "return_message": return_message,
                    "returned_value": returned_value
                }

                self.update_by_id(id_column_value=queue_item[self.id_column_name], data_json=data_json)
                if not stderr:
                    self.logger.info(f'Successfully executed {function_name}({formatted_function_params})')
                else:
                    self.logger.error(f'Error while executing {function_name}({formatted_function_params}):\n{stderr}')
                    self.push_back(queue_item)
                    # TODO: should we break or continue?

                # TODO: change to non-blocking sleep (async function)?
                time.sleep(random.uniform(min_delay_after_execution_ms / 1000, max_delay_after_execution_ms / 1000))
            self.logger.end("END execute_until_stopped")
        except Exception as e:
            self.logger.exception("An error occurred during execution:", object=e)

    @staticmethod
    def _get_python_args(action: dict, class_parameters: dict, function_parameters: dict) -> list:
        """Get the arguments for the python command line."""
        function_name = action["function_name"]
        filename = action["filename"].replace(".py", "")
        folder = (action["folder_name"] + ".") if action["folder_name"] else ""

        function_module = action["function_module"]

        if function_module:
            function_call = f"{function_module}(**{class_parameters}).{function_name}(**{function_parameters})"
        else:
            function_call = f"{function_name}(**{function_parameters})"
        command = f'from {folder}{filename} import {function_module or function_name}\n' + \
                  f'result = {function_call}\n' + \
                  'print("returned_value: " + str(result), end="")'
        return [sys.executable, '-c', command]

    def get_action(self, queue_item: dict) -> dict:
        """Get the action from the database."""
        try:
            return next(action for action in self.all_actions if action['action_id'] == queue_item['action_id'])
        except StopIteration:
            raise ValueError(f"No such action_id {queue_item['action_id']}")

    @staticmethod
    def get_all_actions() -> list:
        """Get all actions from the database."""
        all_actions = GenericCRUD("action").select_multi_dict_by_id(
            "action_view", id_column_name="is_queue_action", id_column_value=1)
        return all_actions

    def install_packages(self, action_ids: tuple) -> None:
        for action in self.all_actions:
            if action["action_id"] not in action_ids or action["package_name"] in installed:
                continue
            filename = action["filename"]
            package_name = action["package_name"]

            if not filename or not package_name:
                continue
            if filename.endswith('.py'):
                try:
                    subprocess.check_call(["pip", "install", "-U", package_name])
                except subprocess.CalledProcessError as e:
                    self.logger.exception(f"Failed to install {package_name}", object=e)
                    continue
            elif filename.endswith(".ts"):
                subprocess.check_call(["npm", "install", package_name])
                subprocess.check_call(["npm", "update", package_name])
            # elif...
            installed.append(action["package_name"])


def execute_queue_worker(action_ids: tuple, min_delay_after_execution_ms: float, max_delay_after_execution_ms: float,
                         total_missions: int):
    queue_worker = QueueWorker()  # cannot share it between processes
    queue_worker.execute(action_ids, min_delay_after_execution_ms, max_delay_after_execution_ms, total_missions)


def main():
    """See README.md"""
    parser = argparse.ArgumentParser(description='Queue Worker')

    parser.add_argument('-min_delay_after_execution_ms', type=float, default=0.0)
    parser.add_argument('-max_delay_after_execution_ms', type=float, default=0.0)
    parser.add_argument('-action_ids', type=int, nargs='+', help='List of action IDs')
    parser.add_argument('-total_missions', type=int, default=sys.maxsize, help='Number of missions to execute')
    parser.add_argument('-processes', type=int, default=1, help='Number of processes to start')

    args = parser.parse_args()

    if any(x is None for x in vars(args).values()):
        print(f"Usage: python {__file__} -min_delay_after_execution_ms 0 -max_delay_after_execution_ms 1 "
              f"-action_ids 1 2 4 -total_missions 100 -processes 1")
        return

    processes = []
    try:
        for _ in range(args.processes):
            args = (tuple(args.action_ids), args.min_delay_after_execution_ms,
                    args.max_delay_after_execution_ms, args.total_missions // args.processes)
            process = multiprocessing.Process(target=execute_queue_worker, args=args)
            processes.append(process)

        # Start the processes
        for process in processes:
            process.start()

        # Wait for all processes to complete
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()


if __name__ == "__main__":
    main()
