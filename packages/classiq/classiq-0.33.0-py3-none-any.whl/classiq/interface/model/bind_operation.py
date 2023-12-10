from typing import Mapping

from classiq.interface.model.handle_binding import HandleBinding
from classiq.interface.model.quantum_statement import QuantumOperation

BIND_INPUT_NAME = "bind_input"
BIND_OUTPUT_NAME = "bind_output"


class BindOperation(QuantumOperation):
    in_handle: HandleBinding
    out_handle: HandleBinding

    @property
    def wiring_inputs(self) -> Mapping[str, HandleBinding]:
        return {BIND_INPUT_NAME: self.in_handle}

    @property
    def wiring_outputs(self) -> Mapping[str, HandleBinding]:
        return {BIND_OUTPUT_NAME: self.out_handle}
