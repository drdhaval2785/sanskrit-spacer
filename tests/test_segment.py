from src.segment import segment, clean


def test_segment():
    assert segment("tau rājaputrau kārtsnyena dharmyamākhyānamuttamam .\nvācovidheyaṃ tatsarvaṃ kṛtvā kāvyamaninditau ..1-4-12..") == [
        "tau rājaputrau kārtsnyena dharmyamākhyānamuttamam", "vācovidheyaṃ tatsarvaṃ kṛtvā kāvyamaninditau"]
    assert segment("kṛto 'tra bhinnaliṅgānām || 8 ||") == ["kṛto'tra bhinnaliṅgānām"]
    assert segment("`caraṇaśabda' ityādinā sūtrasya viṣayaṃ darśayati.") == [
        "caraṇaśabda", "ityādinā sūtrasya viṣayaṃ darśayati"]
    assert segment("kṣudir sampevaṇe (dhā.pā.1443) kṣudyata iti kṣudraḥ") == ["kṣudir sampevaṇe", "kṣudyata iti kṣudraḥ"]
    assert segment("Dharmakṣetre Kurukṣetre") == ["dharmakṣetre kurukṣetre"]


def test_clean():
    assert clean("ahaṃ vijaā kiṃ karīadu") == ([], "hiatus")
    assert clean("iti") == ([], "too_short")
    assert clean("dharmakṣetre kurukṣetre") == (["Darmakzetre kurukzetre"], None)
