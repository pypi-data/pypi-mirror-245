from enum import Enum
from typing import List, Optional, Any
import os
import json

import requests
from pydantic import BaseModel as PydanticBaseModel


class FlorenceException(Exception):
    """Florence Exception class"""
    pass


class BaseModel(PydanticBaseModel):
    """Base class for all models."""
    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True
        use_enum_values = True
        allow_population_by_field_name = True
        validate_assignment = True


class S3Configuration(BaseModel):
    """S3 Configuration model"""
    preSignedUrl: str


class TextBasedConfiguration(BaseModel):
    """Text Based Configuration model"""
    text: str


class ProviderType(Enum):
    """Provider Type enum"""
    S3 = "S3"
    TEXT = "Text"


class SchemaProvider(BaseModel):
    """Schema Provider model"""
    type: ProviderType
    s3Configuration: Optional[S3Configuration]
    textBasedConfiguration: Optional[TextBasedConfiguration]


class GlossaryProvider(BaseModel):
    """Glossary Provider model"""
    type: ProviderType
    s3Configuration: Optional[S3Configuration]
    textBasedConfiguration: Optional[TextBasedConfiguration]


class DataSource(BaseModel):
    """Data Source model"""
    id: Optional[str]
    name: str
    type: str
    tenantId: str
    schemaProvider: SchemaProvider
    glossaryProvider: Optional[GlossaryProvider]


class DataSources(BaseModel):
    """Data Sources model"""
    dataSources: List[DataSource]


class DataSourceCreationResponse(BaseModel):
    """Data Source Creation Response model"""
    id: str


class APIKey(BaseModel):
    """API Key model"""
    id: str
    name: str
    value: str


class UsagePlanName(Enum):
    """Usage Plan Name enum"""
    FLORENCE_FREE = "florence-free"
    FLORENCE_ELITE = "florence-elite"
    FLORENCE_PREMIUM = "florence-premium"
    FLORENCE_ENTERPRISE = "florence-enterprise"


class SubscriptionType(Enum):
    """Subscription Type enum"""
    STRIPE = "stripe"
    AWS = "aws"


class StripeSubscriptionDetails(BaseModel):
    """Stripe Subscription Details"""
    customerId: str


class Subscription(BaseModel):
    """Subscription model"""
    planName: UsagePlanName
    type: Optional[SubscriptionType] = None
    stripeSubscriptionDetails: Optional[StripeSubscriptionDetails] = None


class Tenant(BaseModel):
    """Tenant model"""
    id: Optional[str]
    name: Optional[str]
    email: str
    isActive: Optional[bool] = True
    apiKeys: Optional[List[APIKey]] = []
    subscription: Optional[Subscription] = None


class InternalResponse(BaseModel):
    """Response model"""
    body: str
    statusCode: int
    headers: dict


class SQLGenerationContext(BaseModel):
    """Represents the context for the SQL generation"""

    database_schema: Optional[str]
    database_type: Optional[str]
    query: str


class SQLQueryContext(BaseModel):
    """Represents the context for the SQL generation"""
    query: str
    tenantId: str
    datasourceId: str


class GeneratedSQL(BaseModel):
    """Represents the generated SQL"""

    sql: str
    contexts: List[str] = None


class Florence:
    """Client for interacting with the Florence API."""

    DEFAULT_API_URL = "https://e6hojy8yq1.execute-api.ap-southeast-1.amazonaws.com/dev"
    DEFAULT_REQUEST_TIMEOUT_IN_SECS = 100
    FLORENCE_API_KEY_ENV_VAR = "FLORENCE_API_KEY"
    FLORENCE_TENANT_ID_KEY_ENV_VAR = "FLORENCE_TENANT_ID"
    ALLOWED_CONTEXTS_SIZE = 5

    def __init__(self, api_key: str = None, api_url: str = None, tenant_id: str = None):
        """Initialise the client."""
        self._api_url = api_url if api_url else Florence.DEFAULT_API_URL
        api_key_env = os.environ.get(Florence.FLORENCE_API_KEY_ENV_VAR)
        self._api_key = api_key_env if api_key_env else api_key
        tenant_id_env = os.environ.get(Florence.FLORENCE_TENANT_ID_KEY_ENV_VAR)
        self._tenant_id = tenant_id_env if tenant_id_env else tenant_id
        if self._tenant_id is None:
            self._tenant_id = self._tenant_by_api_key().id
        self._validate_client()

    def ask(self, datasource_id: str, query: str, contexts: List[str] = None) -> GeneratedSQL:
        """Ask a question"""
        if contexts and len(contexts) > Florence.ALLOWED_CONTEXTS_SIZE:
            raise FlorenceException(
                f"Maximum of {Florence.ALLOWED_CONTEXTS_SIZE} contexts are allowed.")
        sql_query_context = SQLQueryContext(
            query=query, tenantId=self._tenant_id, datasourceId=datasource_id)
        return self._get_sql(sql_query_context)

    def add_datasource(self, datasource_name: str, datasource_type: str, ddl: str, glossary: str) -> DataSource:
        """Add a new datasource"""
        datasource = DataSource(
            name=datasource_name,
            type=datasource_type,
            tenantId=self._tenant_id,
            schemaProvider=SchemaProvider(
                type=ProviderType.TEXT,
                textBasedConfiguration=TextBasedConfiguration(
                    text=ddl
                )
            ),
            glossaryProvider=GlossaryProvider(
                type=ProviderType.TEXT,
                textBasedConfiguration=TextBasedConfiguration(
                    text=glossary
                )
            )
        )
        return self._add_tenant_datasource(datasource)

    def datasources(self) -> DataSources:
        """Get tenant datasources."""
        headers = self._request_headers_with_api_key()
        response = requests.get(
            f"{self._api_url}/datasource/{self._tenant_id}", headers=headers,
            timeout=Florence.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return self._handle_response(response, DataSources)

    def datasource(self, datasource_id: str) -> DataSource:
        """Get a tenant datasource."""
        headers = self._request_headers_with_api_key()
        response = requests.get(
            f"{self._api_url}/datasource/{self._tenant_id}/{datasource_id}", headers=headers,
            timeout=Florence.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return self._handle_response(response, DataSource)

    def tenant(self) -> Tenant:
        """Get a tenant."""
        headers = self._request_headers_with_api_key()
        response = requests.get(
            f"{self._api_url}/tenant/{self._tenant_id}", headers=headers,
            timeout=Florence.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return self._handle_response(response, Tenant)

    def update_datasource(self, datasource: DataSource) -> DataSource:
        """Update a tenant datasource."""
        response = self._update_tenant_datasource(datasource)
        assert response.id == datasource.id, "Datasource ID must match after updation"
        return datasource

    def _add_tenant_datasource(self, datasource: DataSource) -> DataSource:
        """Add a new tenant datasource."""
        headers = self._request_headers_with_api_key()
        response = requests.post(
            f"{self._api_url}/datasource", headers=headers, json=datasource.dict(),
            timeout=Florence.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return self._handle_response(response, DataSource)

    def _get_sql(self, context: SQLQueryContext) -> GeneratedSQL:
        """Get SQL."""
        headers = self._request_headers_with_api_key()
        tenant_id = context.tenantId
        datasource_id = context.datasourceId
        sql_generation_context = SQLGenerationContext(query=context.query)
        response = requests.post(
            f"{self._api_url}/sql/{tenant_id}/{datasource_id}", headers=headers,
            json=sql_generation_context.dict(),
            timeout=Florence.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return self._handle_response(response, GeneratedSQL)

    def _handle_response(self, response: requests.Response, response_model: Any = None) -> [BaseModel, None]:
        """Handle the response from the API."""
        if response.status_code != 200:
            raise FlorenceException(
                f"Error: {response.status_code} - {response.text}")
        response_as_json = response.json()
        internal_response = InternalResponse(**response_as_json)
        if internal_response.statusCode != 200:
            raise FlorenceException(internal_response.body)
        if not response_model:
            return
        reponse_body_as_dict = json.loads(internal_response.body)
        return response_model(**reponse_body_as_dict)

    def _request_headers_with_api_key(self, use_api_key=True) -> dict:
        """Get the request headers with the API key."""
        headers = {"Content-Type": "application/json"}
        if self._api_key and use_api_key:
            headers["x-api-key"] = self._api_key
        return headers

    def _tenant_by_api_key(self) -> Tenant:
        """Get a tenant by API key."""
        headers = self._request_headers_with_api_key(use_api_key=True)
        response = requests.get(
            f"{self._api_url}/tenant", headers=headers, timeout=Florence.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return self._handle_response(response, Tenant)

    def _update_tenant_datasource(self, datasource: DataSource) -> DataSourceCreationResponse:
        """Update a tenant datasource."""
        headers = self._request_headers_with_api_key()
        response = requests.put(
            f"{self._api_url}/datasource", headers=headers, json=datasource.dict(),
            timeout=Florence.DEFAULT_REQUEST_TIMEOUT_IN_SECS)
        return self._handle_response(response, DataSourceCreationResponse)

    def _validate_client(self) -> None:
        """Validate the client."""
        if not self._api_key:
            raise FlorenceException(
                "API Key is missing. Please set the FLORENCE_API_KEY environment variable or pass it to the constructor.")
        if self._tenant_id:
            return
        raise FlorenceException(
            "Tenant ID is missing. Please set the FLORENCE_TENANT_ID environment variable or pass it to the constructor."
        )
