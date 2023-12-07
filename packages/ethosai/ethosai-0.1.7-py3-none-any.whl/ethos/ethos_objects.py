from typing import BinaryIO

import os
import ethos as ethos
from ethos import ethos_client
from ethos.ethos_client.rest import ApiException
import urllib3

__all__ = [
    "Config",
    "Model",
    "ModelVersion",
    "ModelVersionConfig",
    "ModelVersion",
    "Resource",
]


class Config:
    def __init__(self, *, api_key=None, api_host=None, org_id=None):
        self.api_key = api_key or os.environ.get("ETHOS_API_KEY")
        self.api_host = api_host or os.environ.get("ETHOS_API", "https://api.ethosai.com")
        self.org_id = org_id or os.environ.get("ETHOS_ORG")

    def validate(self):
        if not self.api_key:
            raise ValueError(
                "ETHOS_API_KEY must be set in the environment or passed to ethos.config.api_key"
            )
        if not self.org_id:
            raise ValueError(
                "ETHOS_ORG must be set in the environment or passed to ethos.config.org_id"
            )


class EthosObject:
    def __init__(self):
        self._loaded = False
        self._object = None
        self._config = ethos.config
        self._client_config = None

    @property
    def _client(self):
        self._config.validate()
        client_config = ethos_client.Configuration(
            host=self._config.api_host,
            access_token=self._config.api_key,
        )
        return ethos_client.ApiClient(client_config)


class Model(EthosObject):
    def __init__(self, *, workspace_id, name):
        self.workspace_id = workspace_id
        self.name = name
        self.__model = None
        super().__init__()

    def __repr__(self):
        return f"<Model {self.name}>"

    @property
    def _model(self):
        if self.__model:
            return self.__model

        with self._client as api_client:
            models_api = ethos_client.ModelsApi(api_client)
            models_data = models_api.get_models(workspace_id=self.workspace_id, name=self.name)
            if models_data.data:
                model = models_data.data[0]
            else:
                raise ApiException(
                    f"Model name not found - must be registered in Ethos first. "
                    f"Got name: {self.name}"
                )
        self.__model = model
        return self.__model

    def new_version(self):
        return ModelVersion(_loaded_model=self._model)


class ModelVersionConfig:
    decision_threshold = None


class ModelVersion(EthosObject):
    def __init__(self, id=None, _loaded_model=None):
        super().__init__()

        self.model = _loaded_model
        self._model_version_config = ModelVersionConfig()

        if id:
            self.id = id  # TODO: load if ID is provided, and set self.model.
            raise NotImplementedError
        else:
            self._create()

    def __repr__(self):
        return f"<ModelVersion {self.id}>"

    def _create(self):
        with self._client as api_client:
            models_api = ethos_client.ModelsApi(api_client)
            model_version_create = ethos_client.ModelVersionCreate(model_id=self.model["id"])
            model_version = models_api.create_model_version(model_version_create)

        self.id = model_version.id
        self._model_version = model_version

    @property
    def config(self):
        return self._model_version_config

    def track_training_data(
        self,
        name,
        *,
        df,
        id_column,
        target,
        version_tags=None,
        tags=None,
    ):
        Resource(related=self).track_dataset(
            name=name,
            version_tags=version_tags,
            tags=["train"] + (tags or []),
            df=df,
            id_column=id_column,
            target=target,
        )

    def track_inference_data(
        self,
        name,
        *,
        df,
        id_column,
        actual_values,
        predict=None,
        predict_proba=None,
        version_tags=None,
        tags=None,
    ):
        Resource(related=self).track_dataset(
            name=name,
            df=df,
            version_tags=version_tags,
            tags=["inference"] + (tags or []),
            id_column=id_column,
            actual_values=actual_values,
            predict=predict,
            predict_proba=predict_proba,
        )

    def track_protected_data(
        self,
        name,
        *,
        df,
        id_column,
        version_tags=None,
        tags=None,
    ):
        Resource(related=self).track_dataset(
            name=name,
            version_tags=version_tags,
            tags=["protected"] + (tags or []),
            df=df,
            id_column=id_column,
        )

    def track_dataset(self, name, *, df, id_column=None, version_tags=None, tags=None):
        Resource(related=self).track_dataset(
            name=name,
            df=df,
            id_column=id_column,
            version_tags=version_tags,
            tags=tags or [],
        )

    def track_file(self, name, *, file, mimetype, version_tags=None, tags=None):
        Resource(related=self).track_file(
            name=name,
            file=file,
            mimetype=mimetype,
            version_tags=version_tags,
            tags=tags or [],
        )

    def finalize(self):
        with self._client as api_client:
            models_api = ethos_client.ModelsApi(api_client)
            model_version_update = ethos_client.ModelVersionUpdate(action="finalize")
            models_api.update_model_version(
                model_version_id=self.id,
                model_version_update=model_version_update,
            )


class Resource(EthosObject):
    def __init__(self, *, related, defer=True):
        self._default_datasource = None
        self.related = related
        super().__init__()

    @property
    def default_datasource(self):
        if self._default_datasource:
            return self._default_datasource
        with self._client as api_client:
            datasources_api = ethos_client.DatasourcesApi(api_client)
            datasources = datasources_api.get_datasources(org_id=self._config.org_id)

            if len(datasources.data) == 1:
                self._default_datasource = datasources.data[0]
            else:
                raise NotImplementedError(
                    f"Multi-datasource support has not been implemented. "
                    f"Expected exactly one, got: {len(datasources.data)}"
                )
        return self._default_datasource

    def _upload_blob(self, *, signed_upload_url, content):
        http = urllib3.PoolManager()
        headers = {"Content-Type": "application/octet-stream"}
        response = http.request("PUT", signed_upload_url, body=content, headers=headers)

        if response.status not in (200, 201):
            raise ApiException(f"Failed to upload blob. Got status code: {response.status}")
        return response

    def track_file(
        self,
        name,
        *,
        file: BinaryIO,
        mimetype,
        version_tags=None,
        tags=None,
    ):
        version_tags = version_tags or []
        tags = tags or []
        with self._client as api_client:
            blobs_api = ethos_client.BlobsApi(api_client)
            resources_api = ethos_client.ResourcesApi(api_client)

            try:
                # 1) Create blob:
                datasource = self.default_datasource
                blob_create = ethos_client.BlobCreate(
                    datasource_id=datasource["id"],
                    filename=name,
                    mimetype=mimetype,
                )
                blob = blobs_api.create_blob(blob_create)

                # 2) Upload the blob:
                self._upload_blob(
                    signed_upload_url=blob.signed_upload_url,
                    content=file.read(),
                )

                # 3) Create the resource:
                resource_blob_link_creates = [ethos_client.ResourceBlobLinkCreate(blob_id=blob.id)]
                resource_create = ethos_client.ResourceCreate(
                    type="file",
                    name=name,
                    related_id=self.related.id,
                    version_tags=version_tags,
                    tags=tags,
                    resource_blob_links=resource_blob_link_creates,
                )
                resources_api.create_resource(resource_create)
            except ApiException as e:
                print("Exception when calling API: %s\n" % e)

    def track_dataset(
        self,
        name,
        *,
        df,
        version_tags=None,
        tags=None,
        id_column=None,
        actual_values=None,
        target=None,
        predict=None,
        predict_proba=None,
    ):
        version_tags = version_tags or []
        tags = tags or []
        with self._client as api_client:
            blobs_api = ethos_client.BlobsApi(api_client)
            resources_api = ethos_client.ResourcesApi(api_client)

            try:
                # 1) Create blob:
                datasource = self.default_datasource
                blob_create = ethos_client.BlobCreate(
                    datasource_id=datasource["id"],
                    filename=f"{name}.csv",
                    mimetype="text/csv",
                )
                blob = blobs_api.create_blob(blob_create)

                # 2) Upload the CSV to the blob:
                self._upload_blob(
                    signed_upload_url=blob.signed_upload_url,
                    content=df.to_csv(index=False).encode("utf-8"),
                )

                # 3) Create the dataset schema:
                column_creates = []
                if id_column:
                    column_create = {
                        "name": id_column,
                        "type": "id",
                        "dtype": df[id_column].dtype.name,
                    }
                    column_creates.append(column_create)
                if target:
                    column_create = {
                        "name": target,
                        "type": "target",
                        "dtype": df[target].dtype.name,
                    }
                    column_creates.append(column_create)
                if actual_values:
                    column_create = {
                        "name": actual_values,
                        "type": "actual_values",
                        "dtype": df[actual_values].dtype.name,
                    }
                    column_creates.append(column_create)
                if predict:
                    column_create = {
                        "name": predict,
                        "type": "predict",
                        "dtype": df[predict].dtype.name,
                    }
                    column_creates.append(column_create)
                if predict_proba:
                    column_create = {
                        "name": predict_proba,
                        "type": "predict_proba",
                        "dtype": df[predict_proba].dtype.name,
                    }
                    column_creates.append(column_create)
                if "protected" in tags:
                    for column in set(df.columns):
                        if column == id_column:
                            continue
                        column_create = {
                            "name": column,
                            "type": "protected",
                            "dtype": df[column].dtype.name,
                        }
                        column_creates.append(column_create)

                dataset_schema_create = {
                    "columns": column_creates,
                }

                # Add any columns that are not already in the schema.
                # TODO: we will likely remove this in preference for server-side detection later.
                column_create_names = [column["name"] for column in column_creates]
                for column in [
                    column for column in df.columns if column not in column_create_names
                ]:
                    column_create = {
                        "name": column,
                        "type": "default",
                        "dtype": df[column].dtype.name,
                    }
                    column_creates.append(column_create)

                # 4) Create the resource:
                resource_blob_link_creates = [ethos_client.ResourceBlobLinkCreate(blob_id=blob.id)]
                resource_create = ethos_client.ResourceCreate(
                    type="dataset",
                    name=name,
                    related_id=self.related.id,
                    version_tags=version_tags,
                    tags=tags,
                    resource_blob_links=resource_blob_link_creates,
                    dataset_schema=dataset_schema_create,
                )
                resources_api.create_resource(resource_create)
            except ApiException as e:
                print("Exception when calling API: %s\n" % e)
