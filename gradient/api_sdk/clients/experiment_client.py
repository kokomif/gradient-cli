from gradient import constants, config
from . import http_client
from .base_client import BaseClient
from .. import repositories, models


class ExperimentsClient(BaseClient):
    HOST_URL = config.config.CONFIG_EXPERIMENTS_HOST
    LOG_HOST_URL = config.config.CONFIG_LOG_HOST

    def __init__(self, api_key, *args, **kwargs):
        super(ExperimentsClient, self).__init__(api_key, *args, **kwargs)
        self.logs_client = http_client.API(api_url=self.LOG_HOST_URL,
                                           api_key=api_key,
                                           logger=self.logger)

    def create_single_node(
            self,
            name,
            project_id,
            machine_type,
            command,
            ports=None,
            workspace_url=None,
            working_directory=None,
            artifact_directory=None,
            cluster_id=None,
            experiment_env=None,
            model_type=None,
            model_path=None,
            container=None,
            container_user=None,
            registry_username=None,
            registry_password=None,
            registry_url=None,
    ):
        """
        Create single node experiment

        .. code-block:: python
            :linenos:
            :emphasize-lines: 3,5

            gradient experiments create singlenode
            --projectId <your-project-id>
            --name singleEx
            --experimentEnv "{"EPOCHS_EVAL":5,"TRAIN_EPOCHS":10,"MAX_STEPS":1000,"EVAL_SECS":10}"
            --container tensorflow/tensorflow:1.13.1-gpu-py3
            --machineType K80
            --command "python mnist.py"
            --workspaceUrl https://github.com/Paperspace/mnist-sample.git
            --modelType Tensorflow
            --modelPath /artifacts

        Note: ``--modelType Tensorflow`` is currently required if you wish you create a Deployment from your model,
        since Deployments currently only use Tensorflow Serving to serve models. Also, ``--modelPath /artifacts``
        is currently required for singlenode experiments if you need your model to appear in your Model Repository so
        that you can deploy it using Deployments.

        :param str name: Name of new experiment  [required]
        :param str project_id: Project ID  [required]
        :param str machine_type: Machine type [required]
        :param str command: Container entrypoint command  [required]
        :param str ports: Port to use in new experiment
        :param str workspace_url: Project git repository url
        :param str working_directory: Working directory for the experiment
        :param str artifact_directory: Artifacts directory
        :param str cluster_id: Cluster ID
        :param dict experiment_env: Environment variables in a JSON
        :param str model_type: defines the type of model that is being generated by the experiment. Model type must be one of Tensorflow, ONNX, or Custom
        :param str model_path: Model path
        :param str container: Container (dockerfile) [required]
        :param str container_user: Container user for running the specified command in the container. If no containerUser is specified, the user will default to 'root' in the container.
        :param str registry_username: Registry username for accessing private docker registry container if nessesary
        :param str registry_password: Registry password for accessing private docker registry container if nessesary
        :param str registry_url: Registry server URL for accessing private docker registry container if nessesary

        :returns: experiment handle
        :rtype: str
        """

        experiment = models.SingleNodeExperiment(
            experiment_type_id=constants.ExperimentType.SINGLE_NODE,
            name=name,
            project_id=project_id,
            machine_type=machine_type,
            ports=ports,
            workspace_url=workspace_url,
            working_directory=working_directory,
            artifact_directory=artifact_directory,
            cluster_id=cluster_id,
            experiment_env=experiment_env,
            model_type=model_type,
            model_path=model_path,
            container=container,
            command=command,
            container_user=container_user,
            registry_username=registry_username,
            registry_password=registry_password,
            registry_url=registry_url,
        )

        handle = repositories.CreateSingleNodeExperiment(self.client).create(experiment)
        return handle

    def create_multi_node(
            self,
            name,
            project_id,
            experiment_type_id,
            worker_container,
            worker_machine_type,
            worker_command,
            worker_count,
            parameter_server_container,
            parameter_server_machine_type,
            parameter_server_command,
            parameter_server_count,
            ports=None,
            workspace_url=None,
            working_directory=None,
            artifact_directory=None,
            cluster_id=None,
            experiment_env=None,
            model_type=None,
            model_path=None,
            worker_container_user=None,
            worker_registry_username=None,
            worker_registry_password=None,
            worker_registry_url=None,
            parameter_server_container_user=None,
            parameter_server_registry_username=None,
            parameter_server_registry_password=None,
            parameter_server_registry_url=None,
    ):
        """
        Create multinode experiment

        *EXAMPLE*::

            gradient experiments create multinode
            --name multiEx
            --projectId <your-project-id>
            --experimentType GRPC
            --workerContainer tensorflow/tensorflow:1.13.1-gpu-py3
            --workerMachineType K80
            --workerCommand "python mnist.py"
            --workerCount 2
            --parameterServerContainer tensorflow/tensorflow:1.13.1-gpu-py3
            --parameterServerMachineType K80
            --parameterServerCommand "python mnist.py"
            --parameterServerCount 1
            --workspaceUrl https://github.com/Paperspace/mnist-sample.git
            --modelType Tensorflow

        Note: ``--modelType Tensorflow`` is currently required if you wish you create a Deployment from your model,
        since Deployments currently only use Tensorflow Serving to serve models. Also, ``--modelPath /artifacts``
        is currently required for singlenode experiments if you need your model to appear in your Model Repository so
        that you can deploy it using Deployments.


        :param str name: Name of new experiment  [required]
        :param str project_id: Project ID  [required]
        :param str experiment_type_id: Experiment Type ID [GRPC|MPI] [required]
        :param str worker_container: Worker container (dockerfile) [required]
        :param str worker_machine_type: Worker machine type  [required]
        :param str worker_command: Worker command  [required]
        :param int worker_count: Worker count  [required]
        :param str parameter_server_container: Parameter server container  [required]
        :param str parameter_server_machine_type: Parameter server machine type  [required]
        :param str parameter_server_command: Parameter server command  [required]
        :param int parameter_server_count: Parameter server count  [required]
        :param str ports: Port to use in new experiment
        :param str workspace_url: Project git repository url
        :param str working_directory: Working directory for the experiment
        :param str artifact_directory: Artifacts directory
        :param str cluster_id: Cluster ID
        :param dict experiment_env: Environment variables in a JSON
        :param str model_type: defines the type of model that is being generated by the experiment. Model type must be one of Tensorflow, ONNX, or Custom
        :param str model_path: Model path
        :param str worker_container_user: Worker container user
        :param str worker_registry_username: Registry username for accessing private docker registry container if nessesary
        :param str worker_registry_password: Registry password for accessing private docker registry container if nessesary
        :param str worker_registry_url: Registry server URL for accessing private docker registry container if nessesary
        :param str parameter_server_container_user: Parameter server container user
        :param str parameter_server_registry_username: Registry username for accessing private docker registry container if nessesary
        :param str parameter_server_registry_password: Registry password for accessing private docker registry container if nessesary
        :param str parameter_server_registry_url: Registry server URL for accessing private docker registry container if nessesary

        :returns: experiment handle
        :rtype: str
        """
        experiment = models.MultiNodeExperiment(
            name=name,
            project_id=project_id,
            experiment_type_id=experiment_type_id,
            worker_container=worker_container,
            worker_machine_type=worker_machine_type,
            worker_command=worker_command,
            worker_count=worker_count,
            parameter_server_container=parameter_server_container,
            parameter_server_machine_type=parameter_server_machine_type,
            parameter_server_command=parameter_server_command,
            parameter_server_count=parameter_server_count,
            ports=ports,
            workspace_url=workspace_url,
            working_directory=working_directory,
            artifact_directory=artifact_directory,
            cluster_id=cluster_id,
            experiment_env=experiment_env,
            model_type=model_type,
            model_path=model_path,
            worker_container_user=worker_container_user,
            worker_registry_username=worker_registry_username,
            worker_registry_password=worker_registry_password,
            worker_registry_url=worker_registry_url,
            parameter_server_container_user=parameter_server_container_user,
            parameter_server_registry_username=parameter_server_registry_username,
            parameter_server_registry_password=parameter_server_registry_password,
            parameter_server_registry_url=parameter_server_registry_url,
        )

        handle = repositories.CreateMultiNodeExperiment(self.client).create(experiment)
        return handle

    def run_single_node(
            self,
            name,
            project_id,
            machine_type,
            command,
            ports=None,
            workspace_url=None,
            working_directory=None,
            artifact_directory=None,
            cluster_id=None,
            experiment_env=None,
            model_type=None,
            model_path=None,
            container=None,
            container_user=None,
            registry_username=None,
            registry_password=None,
            registry_url=None,
    ):
        """Create and start single node experiment

        *EXAMPLE*::

            gradient experiments run singlenode
            --projectId <your-project-id>
            --name singleEx
            --experimentEnv "{"EPOCHS_EVAL":5,"TRAIN_EPOCHS":10,"MAX_STEPS":1000,"EVAL_SECS":10}"
            --container tensorflow/tensorflow:1.13.1-gpu-py3
            --machineType K80
            --command "python mnist.py"
            --workspaceUrl https://github.com/Paperspace/mnist-sample.git
            --modelType Tensorflow
            --modelPath /artifacts

        Note: ``--modelType Tensorflow`` is currently required if you wish you create a Deployment from your model,
        since Deployments currently only use Tensorflow Serving to serve models. Also, ``--modelPath /artifacts``
        is currently required for singlenode experiments if you need your model to appear in your Model Repository so
        that you can deploy it using Deployments.

        :param str name: Name of new experiment  [required]
        :param str project_id: Project ID  [required]
        :param str machine_type: Machine type [required]
        :param str command: Container entrypoint command  [required]
        :param str ports: Port to use in new experiment
        :param str workspace_url: Project git repository url
        :param str working_directory: Working directory for the experiment
        :param str artifact_directory: Artifacts directory
        :param str cluster_id: Cluster ID
        :param dict experiment_env: Environment variables in a JSON
        :param str model_type: defines the type of model that is being generated by the experiment. Model type must be one of Tensorflow, ONNX, or Custom
        :param str model_path: Model path
        :param str container: Container (dockerfile) [required]
        :param str container_user: Container user for running the specified command in the container. If no containerUser is specified, the user will default to 'root' in the container.
        :param str registry_username: Registry username for accessing private docker registry container if nessesary
        :param str registry_password: Registry password for accessing private docker registry container if nessesary
        :param str registry_url: Registry server URL for accessing private docker registry container if nessesary

        :returns: experiment handle
        :rtype: str
        """

        experiment = models.SingleNodeExperiment(
            experiment_type_id=constants.ExperimentType.SINGLE_NODE,
            name=name,
            project_id=project_id,
            machine_type=machine_type,
            ports=ports,
            workspace_url=workspace_url,
            working_directory=working_directory,
            artifact_directory=artifact_directory,
            cluster_id=cluster_id,
            experiment_env=experiment_env,
            model_type=model_type,
            model_path=model_path,
            container=container,
            command=command,
            container_user=container_user,
            registry_username=registry_username,
            registry_password=registry_password,
            registry_url=registry_url,
        )

        handle = repositories.RunSingleNodeExperiment(self.client).create(experiment)
        return handle

    def run_multi_node(
            self,
            name,
            project_id,
            experiment_type_id,
            worker_container,
            worker_machine_type,
            worker_command,
            worker_count,
            parameter_server_container,
            parameter_server_machine_type,
            parameter_server_command,
            parameter_server_count,
            ports=None,
            workspace_url=None,
            working_directory=None,
            artifact_directory=None,
            cluster_id=None,
            experiment_env=None,
            model_type=None,
            model_path=None,
            worker_container_user=None,
            worker_registry_username=None,
            worker_registry_password=None,
            worker_registry_url=None,
            parameter_server_container_user=None,
            parameter_server_registry_username=None,
            parameter_server_registry_password=None,
            parameter_server_registry_url=None,
    ):
        """Create and start multinode experiment

        The following command creates and starts a multinode experiment called multiEx and places it within the Gradient
        Project identified by the --projectId option. (Note: in some early versions of the CLI this option was called
        --projectHandle.)

        *EXAMPLE*::

            gradient experiments run multinode
            --name multiEx
            --projectId <your-project-id>
            --experimentType GRPC
            --workerContainer tensorflow/tensorflow:1.13.1-gpu-py3
            --workerMachineType K80
            --workerCommand "python mnist.py"
            --workerCount 2
            --parameterServerContainer tensorflow/tensorflow:1.13.1-gpu-py3
            --parameterServerMachineType K80
            --parameterServerCommand "python mnist.py"
            --parameterServerCount 1
            --workspaceUrl https://github.com/Paperspace/mnist-sample.git
            --modelType Tensorflow

        Note: ``--modelType Tensorflow`` is currently required if you wish you create a Deployment from your model, since
        Deployments currently only use Tensorflow Serving to serve models.

        :param str name: Name of new experiment  [required]
        :param str project_id: Project ID  [required]
        :param str experiment_type_id: Experiment Type ID [GRPC|MPI] [required]
        :param str worker_container: Worker container (dockerfile) [required]
        :param str worker_machine_type: Worker machine type  [required]
        :param str worker_command: Worker command  [required]
        :param int worker_count: Worker count  [required]
        :param str parameter_server_container: Parameter server container  [required]
        :param str parameter_server_machine_type: Parameter server machine type  [required]
        :param str parameter_server_command: Parameter server command  [required]
        :param int parameter_server_count: Parameter server count  [required]
        :param str ports: Port to use in new experiment
        :param str workspace_url: Project git repository url
        :param str working_directory: Working directory for the experiment
        :param str artifact_directory: Artifacts directory
        :param str cluster_id: Cluster ID
        :param dict experiment_env: Environment variables in a JSON
        :param str model_type: defines the type of model that is being generated by the experiment. Model type must be one of Tensorflow, ONNX, or Custom
        :param str model_path: Model path
        :param str worker_container_user: Worker container user
        :param str worker_registry_username: Registry username for accessing private docker registry container if nessesary
        :param str worker_registry_password: Registry password for accessing private docker registry container if nessesary
        :param str worker_registry_url: Registry server URL for accessing private docker registry container if nessesary
        :param str parameter_server_container_user: Parameter server container user
        :param str parameter_server_registry_username: Registry username for accessing private docker registry container if nessesary
        :param str parameter_server_registry_password: Registry password for accessing private docker registry container if nessesary
        :param str parameter_server_registry_url: Registry server URL for accessing private docker registry container if nessesary

        :returns: experiment handle
        :rtype: str

        """
        experiment = models.MultiNodeExperiment(
            name=name,
            project_id=project_id,
            experiment_type_id=experiment_type_id,
            worker_container=worker_container,
            worker_machine_type=worker_machine_type,
            worker_command=worker_command,
            worker_count=worker_count,
            parameter_server_container=parameter_server_container,
            parameter_server_machine_type=parameter_server_machine_type,
            parameter_server_command=parameter_server_command,
            parameter_server_count=parameter_server_count,
            ports=ports,
            workspace_url=workspace_url,
            working_directory=working_directory,
            artifact_directory=artifact_directory,
            cluster_id=cluster_id,
            experiment_env=experiment_env,
            model_type=model_type,
            model_path=model_path,
            worker_container_user=worker_container_user,
            worker_registry_username=worker_registry_username,
            worker_registry_password=worker_registry_password,
            worker_registry_url=worker_registry_url,
            parameter_server_container_user=parameter_server_container_user,
            parameter_server_registry_username=parameter_server_registry_username,
            parameter_server_registry_password=parameter_server_registry_password,
            parameter_server_registry_url=parameter_server_registry_url,
        )

        handle = repositories.RunMultiNodeExperiment(self.client).create(experiment)
        return handle

    def start(self, experiment_id):
        """Start existing experiment that has not run

        *EXAMPLE*::

            gradient experiments start <experiment_id>

        :param str experiment_id: Experiment ID
        :raises: exceptions.GradientSdkError
        """
        repositories.StartExperiment(self.client).start(experiment_id)

    def stop(self, experiment_id):
        """Stop running experiment

        *EXAMPLE*::

            gradient experiments stop <experiment_id>

        :param str experiment_id: Experiment ID
        :raises: exceptions.GradientSdkError
        """
        repositories.StopExperiment(self.client).stop(experiment_id)

    def list(self, project_id=None):
        """Get a list of experiments. Optionally filter by project ID

        *EXAMPLE*::

            gradient experiments list

        *EXAMPLE RETURN*::

            +-----------------------------+----------------+----------+
            | Name                        | ID             | Status   |
            +-----------------------------+----------------+----------+
            | mnist-multinode             | experiment-id  | canceled |
            | mnist-multinode             | experiment-id  | failed   |
            | mnist-multinode             | experiment-id  | created  |
            | mnist-multinode             | experiment-id  | canceled |
            | mnist-multinode             | experiment-id  | canceled |
            | mnist-multinode             | experiment-id  | canceled |
            | mnist-multinode             | experiment-id  | canceled |
            | mnist                       | experiment-id  | stopped  |
            +-----------------------------+----------------+----------+


        :param str|list|None project_id:
        :return: experiments
        :rtype: list[models.SingleNodeExperiment|models.MultiNodeExperiment]
        """
        experiments = repositories.ListExperiments(self.client).list(project_id=project_id)
        return experiments

    def get(self, experiment_id):
        """Get experiment instance

        :param str experiment_id: Experiment ID
        :rtype: models.SingleNodeExperiment|models.MultiNodeExperiment
        """
        experiment = repositories.GetExperiment(self.client).get(experiment_id=experiment_id)
        return experiment

    def logs(self, experiment_id, line=0, limit=10000):
        """Show list of latest logs from the specified experiment.

        *EXAMPLE*::

            gradient experiments logs --experimentId

        :param str experiment_id: Experiment ID
        :param int line: line number at which logs starts to display on screen
        :param int limit: maximum lines displayed on screen, default set to 10 000

        :returns: list of LogRows
        :rtype: list[models.LogRow]
        """
        logs = repositories.ListExperimentLogs(self.logs_client).list(experiment_id, line, limit)
        return logs

    def yield_logs(self, experiment_id, line=0, limit=10000):
        """Get log generator. Polls the API for new logs

        :param str experiment_id:
        :param int line: line number at which logs starts to display on screen
        :param int limit: maximum lines displayed on screen, default set to 10 000

        :returns: generator yielding LogRow instances
        :rtype: Iterator[models.LogRow]
        """
        logs_generator = repositories.ListExperimentLogs(self.logs_client).yield_logs(experiment_id, line, limit)
        return logs_generator
