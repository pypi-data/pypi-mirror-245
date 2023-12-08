from dataclasses import dataclass
from pollination_dsl.dag import Inputs, GroupedDAG, task, Outputs
from pollination.honeybee_radiance_postprocess.post_process import AnnualIrradianceMetrics


@dataclass
class AnnualIrradiancePostprocess(GroupedDAG):
    """Post-process for annual irradiance."""

    # inputs
    input_folder = Inputs.folder(
        description='Folder with initial results before redistributing the '
        'results to the original grids.'
    )

    @task(
        template=AnnualIrradianceMetrics,
    )
    def calculate_metrics(
        self, folder=input_folder
    ):
        return [
            {
                'from': AnnualIrradianceMetrics()._outputs.annual_metrics,
                'to': 'metrics'
            }
        ]

    metrics = Outputs.folder(
        source='metrics', description='metrics folder.'
    )
