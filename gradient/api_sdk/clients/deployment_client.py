from gradient import config
from gradient.api_sdk.utils import MessageExtractor
from .base_client import BaseClient
from .. import models, repositories, serializers
from ..exceptions import GradientSdkError


class DeploymentsClient(BaseClient):
    HOST_URL = config.config.CONFIG_HOST

    def create(self, deployment_type, model_id, name, machine_type, image_url, instance_count):
        """
        Method to create deployment instance

        :param deployment_type:
        :param model_id:
        :param name:
        :param machine_type:
        :param image_url:
        :param instance_count:
        :return: Created deployment id
        """
        deployment = models.Deployment(
            deployment_type=deployment_type,
            model_id=model_id,
            name=name,
            machine_type=machine_type,
            image_url=image_url,
            instance_count=instance_count
        )

        id_ = self._create(deployment, serializers.DeploymentSchema)
        return id_

    def start(self, deployment_id):
        """
        Start deployment

        :param deployment_id:
        """
        return self._get_post_response(deployment_id)

    def stop(self, deployment_id):
        """
        Stop deployment

        :param deployment_id:
        """
        return self._get_post_response(deployment_id, is_running=False)

    def list(self, filters):
        """
        List deployments with optional filtering

        Options:
          --state [BUILDING|PROVISIONING|STARTING|RUNNING|STOPPING|STOPPED|ERROR] Filter by deployment state
          --projectId TEXT Use to filter by project ID
          --model_id TEXT Use to filter by model ID

        :param state|projectId|model_id filters:
        """
        return repositories.ListDeployments(self.client).list(filters=filters)

    @staticmethod
    def _get_deployment_dict(deployment, schema_cls):
        deployment_schema = schema_cls()
        deployment_dict = deployment_schema.dump(deployment).data

        return deployment_dict

    @staticmethod
    def _get_error_message(response):
        try:
            response_data = response.json()
        except ValueError:
            return "Unknown error"

        msg = MessageExtractor().get_message_from_response_data(response_data)
        return msg

    def _get_create_response(self, deployment_dict):
        return self.client.post("/deployments/createDeployment/", json=deployment_dict)

    def _process_response(self, response):
        if response.ok:
            return response.json()["deployment"]["id"]

        msg = self._get_error_message(response)
        # TODO prepare more detailed error type message
        raise GradientSdkError(msg)

    def _create(self, deployment, schema_cls):
        deployment_dict = self._get_deployment_dict(deployment, schema_cls)
        response = self._get_create_response(deployment_dict)
        handle = self._process_response(response)
        return handle

    def _get_post_response(self, deployment_id, is_running=True):
        data = {
            "id": deployment_id,
            "isRunning": is_running
        }
        return self.client.post("/deployments/updateDeployment/", json=data)
