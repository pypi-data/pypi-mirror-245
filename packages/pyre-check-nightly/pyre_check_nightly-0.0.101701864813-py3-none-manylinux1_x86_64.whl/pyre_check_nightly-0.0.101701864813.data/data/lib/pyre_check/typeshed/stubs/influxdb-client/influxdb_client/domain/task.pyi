from _typeshed import Incomplete

class Task:
    openapi_types: Incomplete
    attribute_map: Incomplete
    discriminator: Incomplete
    def __init__(
        self,
        id: Incomplete | None = None,
        org_id: Incomplete | None = None,
        org: Incomplete | None = None,
        name: Incomplete | None = None,
        owner_id: Incomplete | None = None,
        description: Incomplete | None = None,
        status: Incomplete | None = None,
        labels: Incomplete | None = None,
        authorization_id: Incomplete | None = None,
        flux: Incomplete | None = None,
        every: Incomplete | None = None,
        cron: Incomplete | None = None,
        offset: Incomplete | None = None,
        latest_completed: Incomplete | None = None,
        last_run_status: Incomplete | None = None,
        last_run_error: Incomplete | None = None,
        created_at: Incomplete | None = None,
        updated_at: Incomplete | None = None,
        links: Incomplete | None = None,
    ) -> None: ...
    @property
    def id(self): ...
    @id.setter
    def id(self, id) -> None: ...
    @property
    def org_id(self): ...
    @org_id.setter
    def org_id(self, org_id) -> None: ...
    @property
    def org(self): ...
    @org.setter
    def org(self, org) -> None: ...
    @property
    def name(self): ...
    @name.setter
    def name(self, name) -> None: ...
    @property
    def owner_id(self): ...
    @owner_id.setter
    def owner_id(self, owner_id) -> None: ...
    @property
    def description(self): ...
    @description.setter
    def description(self, description) -> None: ...
    @property
    def status(self): ...
    @status.setter
    def status(self, status) -> None: ...
    @property
    def labels(self): ...
    @labels.setter
    def labels(self, labels) -> None: ...
    @property
    def authorization_id(self): ...
    @authorization_id.setter
    def authorization_id(self, authorization_id) -> None: ...
    @property
    def flux(self): ...
    @flux.setter
    def flux(self, flux) -> None: ...
    @property
    def every(self): ...
    @every.setter
    def every(self, every) -> None: ...
    @property
    def cron(self): ...
    @cron.setter
    def cron(self, cron) -> None: ...
    @property
    def offset(self): ...
    @offset.setter
    def offset(self, offset) -> None: ...
    @property
    def latest_completed(self): ...
    @latest_completed.setter
    def latest_completed(self, latest_completed) -> None: ...
    @property
    def last_run_status(self): ...
    @last_run_status.setter
    def last_run_status(self, last_run_status) -> None: ...
    @property
    def last_run_error(self): ...
    @last_run_error.setter
    def last_run_error(self, last_run_error) -> None: ...
    @property
    def created_at(self): ...
    @created_at.setter
    def created_at(self, created_at) -> None: ...
    @property
    def updated_at(self): ...
    @updated_at.setter
    def updated_at(self, updated_at) -> None: ...
    @property
    def links(self): ...
    @links.setter
    def links(self, links) -> None: ...
    def to_dict(self): ...
    def to_str(self): ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
