"""Tests for the ``phoenix`` star keyword, provided by phoenix4all."""

import pytest
from phoenix4all.taurex import Phoenix4AllStar

from taurex.parameter import factory
from taurex.parameter.classfactory import KEYWORD_ALIASES
from taurex.parameter.classfactory import ClassFactory
from taurex.stellar import Star


@pytest.mark.parametrize("keyword", ["phoenix", "PHOENIX", "phoenix4all"])
def test_phoenix_keyword_maps_to_phoenix4all(keyword):
    """Both ``phoenix`` and ``phoenix4all`` resolve to Phoenix4AllStar."""
    cf = ClassFactory()

    assert cf.find_klass_from_keyword(keyword, Star) is Phoenix4AllStar
    assert cf.find_klass_from_keyword(keyword) is Phoenix4AllStar


def test_aliases_are_lower_case():
    """Lookup lowercases the keyword, so alias keys must be lower case."""
    assert all(k == k.lower() for k in KEYWORD_ALIASES)


def test_create_star_phoenix_type():
    """``star_type = phoenix`` builds a Phoenix4AllStar with its kwargs."""
    star = factory.create_star(
        {"star_type": "phoenix", "temperature": 5800, "source": "synphot"}
    )

    assert isinstance(star, Phoenix4AllStar)
    assert star.temperature == pytest.approx(5800)
    assert star.get_spectrum_params["source"] == "synphot"


def test_create_star_phoenix_rejects_phoenix_path():
    """The removed ``phoenix_path`` option fails loudly instead of silently."""
    with pytest.raises(KeyError, match="phoenix_path"):
        factory.create_star({"star_type": "phoenix", "phoenix_path": "spectra"})
