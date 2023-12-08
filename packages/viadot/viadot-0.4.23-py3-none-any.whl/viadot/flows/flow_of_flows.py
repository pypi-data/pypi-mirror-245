from typing import Any, Dict, List

from prefect import Flow, Task, apply_map
from prefect.tasks.prefect import StartFlowRun


class Pipeline(Flow):
    def __init__(
        self,
        name: str,
        project_name: str,
        extract_flows_names: List[str],
        transform_flow_name: str,
        timeout: int = 3600,
        *args: List[any],
        **kwargs: Dict[str, Any]
    ):
        self.extract_flows_names = extract_flows_names
        self.transform_flow_name = transform_flow_name
        self.project_name = project_name
        self.timeout = timeout
        super().__init__(*args, name=name, **kwargs)
        self.gen_flow()

    def gen_start_flow_run_task(self, flow_name: str, flow: Flow = None) -> Task:
        start_flow_run_task = StartFlowRun(wait=True, timeout=self.timeout)
        t = start_flow_run_task.bind(
            flow_name=flow_name, project_name=self.project_name, flow=flow
        )
        return t

    def gen_flow(self):
        extract_flow_runs = apply_map(
            self.gen_start_flow_run_task, self.extract_flows_names, flow=self
        )
        start_flow_run_task_2 = StartFlowRun(wait=True, timeout=self.timeout)
        transform_flow_run = start_flow_run_task_2.bind(
            flow_name=self.transform_flow_name,
            project_name=self.project_name,
            flow=self,
        )
        transform_flow_run.set_upstream(extract_flow_runs, flow=self)
