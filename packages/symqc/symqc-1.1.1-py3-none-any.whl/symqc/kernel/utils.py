from multiprocessing.sharedctypes import Value
from sympy import Matrix, pprint, latex, Abs, im, re


def get_bit(val, n):
    """Get the n-th bit of val.

    No check is performed.
    """
    return val >> n & 1


def set_bit(val, n, bit):
    if bit == 1:
        return val | (1 << n)
    if bit == 0:
        return val & ~(1 << n)
    raise ValueError("bit to set should be 0 or 1")


def remap_bits(val, bit_pos_list):
    """Remap the bits of val according to bit_pos_list, i.e.,
    $$
    \sum_{i=0}^{l - 1}{val\langle i\rangle \times 2^{bit_pos_list[i]}}
    $$
    where, $val\langle i\rangle$ is the i-th bit of val.
    """
    sum = 0
    for i in range(len(bit_pos_list)):
        sum += get_bit(val, i) << bit_pos_list[i]
    return sum


def gamma(t_val, t_qubits, o_val, o_qubits, c_val=0, c_qubits=[]):
    """This function calculates the following value:
        $$
        \Gamma(k,x)|_{\{o_0, o_1, \cdots, o_{l-1}\}, \{t_0, t_1, \cdots, t_{n-1}\}} = \sum_{i=0}^{l -1}{k\langle i\rangle \times 2^{o_i}} + \sum_{i=0}^{n-1}{x\langle i\rangle \times 2^{t_i}}
        $$
    i.e., $\overline{o_{l-1}\cdots b_{n-1}o_{l-2}\cdots b_{n-2}\cdots b_{0}o_{0}}$.
    This value is used in expanding a matrix when applying a gate on qubits.

    Parameters
    ----------
    t_qubits : list of integers
        a list of target qubits
    o_qubits : list of integers
        a list of other qubits
    t_val : an integer value
        it should have the same length as t_qubits
    o_val : an integer value
        it should have the same length as o_qubits

    Returns
    -------
    integer
        the value of $\Gamma(k,x)$
    """
    if c_qubits == []:
        return remap_bits(o_val, o_qubits) + remap_bits(t_val, t_qubits)
    else:
        return (
            remap_bits(o_val, o_qubits)
            + remap_bits(t_val, t_qubits)
            + remap_bits(c_val, c_qubits)
        )


def find_main(state, qubit):
    p0 = 0
    p1 = 0
    for i in range(len(state)):
        num = re(Abs(state[i], evaluate=True).evalf())
        # num = Abs(state[i], evaluate=True).evalf()
        cal = num * num
        if (i >> qubit) & 0x1:
            p1 += cal
        else:
            p0 += cal
    # print(p0, p1)
    return p0, p1


def kron(A, B):
    """Return the Kronecker product of matrix A and matrix B"""
    return Matrix(
        [
            [
                A.row(i // B.rows)[j // B.cols] * B.row(i % B.rows)[j % B.cols]
                for j in range(A.cols * B.cols)
            ]
            for i in range(A.rows * B.rows)
        ]
    )


def extract_qubit_res(target_qubits, basis):
    """Get the measurement result of each qubit, and return them as a list of tuples,
    with each tuple being `(qubit, bit)`.
    """
    qubit_result = []
    for qubit in target_qubits:
        bit = (basis >> qubit) & 1
        qubit_result.append((qubit, bit))
    return qubit_result


def gen_subset(s):
    """Given a mask such as '010110', assume 1s locate at ${p_0, p_1, ..., p_{k-1}}$, this function returns the set ${S_j}$, j = 0, 1, ..., 2^{k}-1, with
    $$
    S_j = \sum_{i=0}^{k-1} j<i> * 2^{p_i}
    $$
    where $j<i>$ is the i-th bit of $j$.
    """
    res = []
    now = s
    while now:
        res.append(now)
        now = (now - 1) & s
    res.append(now)
    return res


def map_bit(x, s, mapp):
    for i in range(len(mapp)):
        s |= ((x >> i) & 1) << mapp[i]
    return s


def get_inverse_mask(set_bits, length):
    """Return an `length`-bit integer with the `k`-th bit set to 0 and
    otherwise 1 for `k` in `set_bits`.
    """
    mask = 0
    for i in set_bits:
        mask |= 1 << i
    return (~mask) & ((1 << length) - 1)


def get_mask(set_bits):
    """Return an integer with the `k`-th bit set to 1 and otherwise 0
    for `k` in `set_bits`.
    """
    mask = 0
    for i in set_bits:
        mask |= 1 << i
    return mask


def get_discrete(x):
    rx = sorted([(i, j) for i, j in zip(x, range(len(x)))])
    res = [0] * len(x)
    for i in range(len(rx)):
        res[rx[i][1]] = i
    return res


def str_bin(x, n):
    s = bin(x)[2:]
    return "0" * (n - len(s)) + s


def make_bin(x, n, keys):
    s = str_bin(x, n)
    return "".join(["%s_{%s}" % (i, j) for i, j in zip(s, keys)])


def make_ket(keys: list):
    keys.reverse()
    n = len(keys)
    return [make_bin(i, n, keys) for i in range(1 << n)]
