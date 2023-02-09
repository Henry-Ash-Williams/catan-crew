#!/usr/bin/env python3
from Resources import Resources, ResourceKind, RESOURCE_REQUIREMENTS


class Bank:
    def __init__(self, available: int = 19):
        self.available_resources = Resources(
            available, available, available, available, available
        )

    def distribute(self, amount: int, resource_kind: ResourceKind) -> Resources:
        self.available_resources[resource_kind.name] -= amount
        r = Resources()
        r[resource_kind.name] = amount
        return r

    def return_to_bank(self, returned_resources: Resources):
        self.available_resources += returned_resources
