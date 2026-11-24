from src.translit import iast_to_slp1, slp1_to_deva, deva_to_slp1, deva_bytes


def test_iast():
    assert iast_to_slp1("tau rājaputrau kārtsnyena dharmyamākhyānamuttamam") == "tO rAjaputrO kArtsnyena DarmyamAKyAnamuttamam"
    assert iast_to_slp1("oṃ namaḥ śivāya") == "oM namaH SivAya"
    assert iast_to_slp1("so'pi kṛto'tra") == "so'pi kfto'tra"
    assert iast_to_slp1("the quick fox") is None


def test_deva():
    assert slp1_to_deva("tam uvAca") == "तम् उवाच"
    assert slp1_to_deva("tamuvAca") == "तमुवाच"
    assert deva_to_slp1("तमुवाच धर्मक्षेत्रे") == "tamuvAca Darmakzetre"
    assert deva_bytes("tam uvAca") == 23
