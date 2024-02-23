from letsrolld import film


def test_get_services_empty():
    assert film.get_services([]) == set()


def test_get_services_single():
    assert film.get_services([film.AMAZONPRIME]) == {film.AMAZONPRIME}


def test_get_services_multiple():
    expected = {film.AMAZONPRIME, film.CRITERION}
    assert film.get_services([film.AMAZONPRIME, film.CRITERION]) == expected


def test_get_services_alias_FREE_kanopy():
    assert film.KANOPY in film.get_services([film.FREE_ALIAS])


def test_get_services_alias_FREE_amazon():
    assert film.AMAZON not in film.get_services([film.FREE_ALIAS])


def test_get_services_alias_FREE_plus_explicit_entry():
    expected = set(film.FREE_SERVICES) | {film.AMAZON}
    assert film.get_services([film.FREE_ALIAS, film.AMAZON]) == expected
