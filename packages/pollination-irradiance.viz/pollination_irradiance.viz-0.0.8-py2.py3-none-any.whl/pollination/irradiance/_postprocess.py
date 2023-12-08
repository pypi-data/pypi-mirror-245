from dataclasses import dataclass
from pollination_dsl.dag import Inputs, GroupedDAG, task, Outputs
from pollination.honeybee_radiance_postprocess.post_process import AnnualIrradianceMetrics
from pollination.honeybee_display.translate import ModelToVis


@dataclass
class AnnualIrradiancePostprocess(GroupedDAG):
    """Post-process for annual irradiance."""

    # inputs
    model = Inputs.file(
        description='Input Honeybee model.',
        extensions=['json', 'hbjson', 'pkl', 'hbpkl', 'zip']
    )

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

    @task(template=ModelToVis, needs=[calculate_metrics])
    def create_vsf(
        self, model=model, grid_data='metrics', output_format='vsf'
    ):
        return [
            {
                'from': ModelToVis()._outputs.output_file,
                'to': 'visualization.vsf'
            }
        ]

    metrics = Outputs.folder(
        source='metrics', description='metrics folder.'
    )

    visualization = Outputs.file(
        source='visualization.vsf',
        description='Annual Irradiance result visualization in VisualizationSet format.'
    )
