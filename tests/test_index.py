import pytest
import pandas.testing as pdt

from pyam.index import get_index_levels, replace_index_values
from pyam import IAMC_IDX


def test_get_index_levels(test_df_index):
    """Assert that get_index_levels returns the correct values"""
    assert get_index_levels(test_df_index, "scenario") == ["scen_a", "scen_b"]


def test_get_index_levels_raises(test_df_index):
    """Assert that get_index_levels raises with non-existing level"""
    with pytest.raises(KeyError):
        get_index_levels(test_df_index, "foo")


@pytest.mark.parametrize(
    "exp_scen, mapping",
    [
        (["scen_c", "scen_c", "scen_b"], {"scen_a": "scen_c"}),
        (["scen_c", "scen_c", "scen_c"], {"scen_a": "scen_c", "scen_b": "scen_c"}),
        (["scen_b", "scen_b", "scen_c"], {"scen_a": "scen_b", "scen_b": "scen_c"})
        # this test ensures that no transitive replacing occurs
    ],
)
def test_replace_index_level(test_pd_df, test_df_index, exp_scen, mapping):
    """Assert that replace_index_value works as expected"""
    pd_df = test_pd_df.copy()
    pd_df["scenario"] = exp_scen
    exp = pd_df.set_index(IAMC_IDX)

    obs = test_df_index.copy()
    obs.index = replace_index_values(obs, "scenario", mapping)

    pdt.assert_frame_equal(exp, obs)


def test_replace_index_level_raises(test_df_index):
    """Assert that replace_index_value raises with non-existing level"""
    with pytest.raises(KeyError):
        replace_index_values(test_df_index, "foo", {"scen_a": "scen_c"})
