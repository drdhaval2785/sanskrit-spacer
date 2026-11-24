from src.metrics import encode, positions, Meter


def test_encode():
    letters, labels = encode("tam uvAca")
    assert letters == "tamuvAca"
    assert labels == [0, 0, 1, 0, 0, 0, 0, 0]


def test_example():
    gold = positions("tam uvAca tataH")
    pred = positions("tamuvAca ta taH")
    assert gold == {2, 7} and pred == {7, 9}
    m = Meter()
    m.add(gold, pred, 13)
    r = m.result()
    assert (r["tp"], r["fp"], r["fn"]) == (1, 1, 1)
    assert r["boundary_p"] == r["boundary_r"] == r["boundary_f1"] == 0.5
    assert r["word_p"] == r["word_r"] == r["word_f1"] == 0
    assert r["sentence_acc"] == 0
