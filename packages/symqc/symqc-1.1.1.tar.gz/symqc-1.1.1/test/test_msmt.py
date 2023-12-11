from symqc.simulator import SymQC


def test_one_shot():
    """Test the one-shot measurement result."""
    symqc = SymQC()
    bell_prog = """
        H    Q1
        Y2M  Q2
        CZ   Q1 Q2
        Y2P  Q2
        M    Q1
        M    Q2
    """
    symqc.compile(bell_prog)
    res = symqc.simulate(work_mode="one_shot", num_shots=10)
    assert all(v in [[0, 0], [1, 1]] for v in res[1])

def test_state_vector():
    """Test the one-shot measurement result."""
    symqc = SymQC()
    bell_prog = """
        H    Q1
        Y2M  Q2
        CZ   Q1 Q2
        Y2P  Q2
        M    Q1
        M    Q2
    """
    symqc.compile(bell_prog)
    res = symqc.simulate(work_mode="final_state")
    a = res["quantum"][1][0]
    b = res["quantum"][1][3]
    assert a==b


if __name__ == "__main__":
    test_one_shot()
    test_state_vector()
