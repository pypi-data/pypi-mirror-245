from argparse import ArgumentParser
from pathlib import Path

from sympy import init_printing
from symqc.simulator import SymQC

# 1. Argument parsing
cl_opt = ArgumentParser(description="A symbolic simulator for QCIS programs")
cl_opt.add_argument("prog_fn", type=str, help="name of the QCIS file to simulate")
cl_opt.add_argument(
    "-l",
    "--output_list",
    required=False,
    nargs="+",
    type=int,
    default=[],
    help="the index of the instructions we need the answer.",
)
cl_opt.add_argument(
    "-o",
    "--out_fn",
    required=False,
    type=str,
    default="result.md",
    help="name of markdown file to store the simulate result.",
)
# cl_opt.add_argument("-N", required=False, type=int, help="num of qubits in simulation")
# cl_opt.add_argument("-s", "--symbol", help="use the symbol args", action="store_true")
# cl_opt.add_argument("-k", "--ket", help="Use the ket present", action="store_true")

args = cl_opt.parse_args()
# state_repr = "ket" if args.ket else "full_amp"
state_repr = "full_amp"
qcis_fn = Path(args.prog_fn).resolve()

if qcis_fn.suffix != ".qcis":
    print("Warning: given file does not end with '.qcis' suffix.")

if not qcis_fn.exists():
    print("Error: cannot find the given file: {}. Simulation aborts.".format(qcis_fn))
    exit(-1)

symqc = SymQC()
symqc.compile_file(qcis_fn)
symqc.simulate(state_repr=state_repr)
symqc.dump_result(args.prog_fn, args.out_fn)
