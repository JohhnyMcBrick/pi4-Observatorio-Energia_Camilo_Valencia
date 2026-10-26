from datetime import date, timedelta

import pytest

from src.common.fechas import ventanas


def test_ventanas_parte_el_rango_en_bloques_de_30_dias():
    bloques = list(ventanas(date(2026, 1, 1), date(2026, 3, 1), 30))
    assert bloques[0] == (date(2026, 1, 1), date(2026, 1, 30))
    assert bloques[1] == (date(2026, 1, 31), date(2026, 3, 1))
    assert len(bloques) == 2


def test_ventanas_cubren_todo_el_rango_sin_huecos_ni_solapes():
    inicio, fin = date(2024, 1, 1), date(2026, 9, 30)
    bloques = list(ventanas(inicio, fin, 30))
    assert bloques[0][0] == inicio and bloques[-1][1] == fin
    for (_, fin_a), (ini_b, _) in zip(bloques, bloques[1:]):
        assert ini_b == fin_a + timedelta(days=1)
    assert all((b - a).days + 1 <= 30 for a, b in bloques)
    assert sum((b - a).days + 1 for a, b in bloques) == (fin - inicio).days + 1


def test_ventanas_un_solo_dia():
    assert list(ventanas(date(2026, 5, 5), date(2026, 5, 5), 7)) == [(date(2026, 5, 5), date(2026, 5, 5))]


def test_ventanas_con_inicio_posterior_al_fin_no_entrega_nada():
    assert list(ventanas(date(2026, 5, 6), date(2026, 5, 5), 7)) == []


def test_ventanas_rechaza_tamano_invalido():
    with pytest.raises(ValueError):
        list(ventanas(date(2026, 1, 1), date(2026, 1, 2), 0))
