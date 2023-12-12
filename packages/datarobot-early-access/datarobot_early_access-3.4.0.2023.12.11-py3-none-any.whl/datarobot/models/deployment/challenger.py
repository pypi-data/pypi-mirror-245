#
# Copyright 2023 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from datarobot.enums import DEFAULT_MAX_WAIT
from datarobot.models.api_object import APIObject
from datarobot.utils.waiters import wait_for_async_resolution


class Challenger(APIObject):
    """A challenger is an alternative model being compared to the model currently deployed"""

    _path = "deployments/{}/challengers/"

    @classmethod
    def create(
        cls,
        deployment_id: str,
        model_package_id: str,
        prediction_environment_id: str,
        name: str,
        max_wait: int = DEFAULT_MAX_WAIT,
    ) -> None:
        """Create a challenger for a deployment

        Parameters
        ----------
        deployment_id : str
            The id of the deployment
        model_package_id : str
            The model package id of the challenger model
        prediction_environment_id : str
            The prediction environment id of the challenger model
        name : str
            The name of the challenger model
        max_wait : int, optional
            The amount of seconds to wait for successful resolution of a challenger creation job.

        Examples
        --------
        .. code-block:: python

        from datarobot import Challenger
        challenger = Challenger.create(
            deployment_id="5c939e08962d741e34f609f0",
            name="Elastic-Net Classifier",
            model_package_id="5c0a969859b00004ba52e41b",
            prediction_environment_id="60b012436635fc00909df555"
        )
        """
        payload = {
            "modelPackageId": model_package_id,
            "name": name,
            "predictionEnvironmentId": prediction_environment_id,
        }
        path = cls._path.format(deployment_id)
        response = cls._client.post(path, json=payload)
        wait_for_async_resolution(cls._client, response.headers["Location"], max_wait)
