from stripe import api_requestor as api_requestor
from stripe.api_resources.abstract import (
    CreateableAPIResource as CreateableAPIResource,
    ListableAPIResource as ListableAPIResource,
    SearchableAPIResource as SearchableAPIResource,
    UpdateableAPIResource as UpdateableAPIResource,
    custom_method as custom_method,
)

class Charge(CreateableAPIResource, ListableAPIResource, SearchableAPIResource, UpdateableAPIResource):
    OBJECT_NAME: str
    def capture(self, idempotency_key: str | None = None, **params): ...
    def refund(self, idempotency_key: str | None = None, **params): ...
    def update_dispute(self, idempotency_key: str | None = None, **params): ...
    def close_dispute(self, idempotency_key: str | None = None, **params): ...
    def mark_as_fraudulent(self, idempotency_key: str | None = None): ...
    def mark_as_safe(self, idempotency_key: str | None = None): ...
