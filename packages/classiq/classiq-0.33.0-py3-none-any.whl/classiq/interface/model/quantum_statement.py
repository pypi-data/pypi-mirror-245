from typing import Mapping, Union

from pydantic import BaseModel

from classiq.interface.model.handle_binding import (
    HandleBinding,
    SlicedHandleBinding,
    SubscriptHandleBinding,
)


class QuantumStatement(BaseModel):
    pass


class QuantumOperation(QuantumStatement):
    @property
    def wiring_inputs(self) -> Mapping[str, HandleBinding]:
        return dict()

    @property
    def wiring_inouts(
        self,
    ) -> Mapping[
        str, Union[SlicedHandleBinding, SubscriptHandleBinding, HandleBinding]
    ]:
        return dict()

    @property
    def wiring_outputs(self) -> Mapping[str, HandleBinding]:
        return dict()
