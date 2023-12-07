from _typeshed import Incomplete

import pika.compat

class AMQPConnectorException(Exception): ...
class AMQPConnectorStackTimeout(AMQPConnectorException): ...
class AMQPConnectorAborted(AMQPConnectorException): ...
class AMQPConnectorWrongState(AMQPConnectorException): ...

class AMQPConnectorPhaseErrorBase(AMQPConnectorException):
    exception: Incomplete
    def __init__(self, exception, *args) -> None: ...

class AMQPConnectorSocketConnectError(AMQPConnectorPhaseErrorBase): ...
class AMQPConnectorTransportSetupError(AMQPConnectorPhaseErrorBase): ...
class AMQPConnectorAMQPHandshakeError(AMQPConnectorPhaseErrorBase): ...
class AMQPConnectionWorkflowAborted(AMQPConnectorException): ...
class AMQPConnectionWorkflowWrongState(AMQPConnectorException): ...

class AMQPConnectionWorkflowFailed(AMQPConnectorException):
    exceptions: Incomplete
    def __init__(self, exceptions, *args) -> None: ...

class AMQPConnector:
    def __init__(self, conn_factory, nbio) -> None: ...
    def start(self, addr_record, conn_params, on_done) -> None: ...
    def abort(self) -> None: ...

class AbstractAMQPConnectionWorkflow(pika.compat.AbstractBase):
    def start(self, connection_configs, connector_factory, native_loop, on_done) -> None: ...
    def abort(self) -> None: ...

class AMQPConnectionWorkflow(AbstractAMQPConnectionWorkflow):
    def __init__(self, _until_first_amqp_attempt: bool = False) -> None: ...
    def set_io_services(self, nbio) -> None: ...
    def start(self, connection_configs, connector_factory, native_loop, on_done) -> None: ...
    def abort(self) -> None: ...
