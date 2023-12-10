from typing import List


class QubitNameManager:
    def __init__(self, qubit_names: List[str] = []) -> None:
        """Create a qubit name manager. Note, since the qubit names are
        used to determine the qubit index in the circuit, all qubits should
        have unique names to avoid ambiguity.

        Raises:
            ValueError: If there are duplicate qubit names.
        """
        if len(qubit_names) != len(list(set(qubit_names))):
            raise ValueError("qubit names are not unique")

        self.idx_to_name = qubit_names
        self.name_to_idx = {}
        for idx, name in enumerate(self.idx_to_name):
            self.name_to_idx[name] = idx

    def get_qubit_names(self):
        return self.idx_to_name

    def dump_name_idx_map(self):
        print(self.name_to_idx)

    def get_name_idx_map(self):
        return self.name_to_idx

    def to_idx(self, qubit_name: str):
        """Return the corresponding index of the qubit in the simulator.

        Every qubit has a unique index in the simulator. Operations
        applied on the qubit should take the unique index as parameter
        during simulation.
        This function returns the index of the given qubit.
        """
        return self.name_to_idx[qubit_name]

    def to_name(self, qubit_idx):
        """Return the name of the qubit corresponding to the given index."""
        return self.idx_to_name[qubit_idx]
