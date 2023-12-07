# stdlib
from typing import List

# third party
from result import Result

# relative
from ...node.credentials import SyftVerifyKey
from ...serde.serializable import serializable
from ...store.document_store import BaseUIDStoreStash
from ...store.document_store import DocumentStore
from ...store.document_store import PartitionKey
from ...store.document_store import PartitionSettings
from ...types.uid import UID
from ...util.telemetry import instrument
from .settings import NodeSettingsV2

NamePartitionKey = PartitionKey(key="name", type_=str)
ActionIDsPartitionKey = PartitionKey(key="action_ids", type_=List[UID])


@instrument
@serializable()
class SettingsStash(BaseUIDStoreStash):
    object_type = NodeSettingsV2
    settings: PartitionSettings = PartitionSettings(
        name=NodeSettingsV2.__canonical_name__, object_type=NodeSettingsV2
    )

    def __init__(self, store: DocumentStore) -> None:
        super().__init__(store=store)

    def set(
        self, credentials: SyftVerifyKey, settings: NodeSettingsV2
    ) -> Result[NodeSettingsV2, str]:
        res = self.check_type(settings, self.object_type)
        # we dont use and_then logic here as it is hard because of the order of the arguments
        if res.is_err():
            return res
        return super().set(credentials=credentials, obj=res.ok())

    def update(
        self, credentials: SyftVerifyKey, settings: NodeSettingsV2
    ) -> Result[NodeSettingsV2, str]:
        res = self.check_type(settings, self.object_type)
        # we dont use and_then logic here as it is hard because of the order of the arguments
        if res.is_err():
            return res
        return super().update(credentials=credentials, obj=res.ok())
