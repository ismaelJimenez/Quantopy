import numpy as np
import pandas._testing as tm
import quantopy as qp
from numpy.testing import assert_allclose


class TestReturnDataFrame:
    def test_manipulations(self):
        rdf = qp.ReturnDataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})
        assert type(rdf) is qp.ReturnDataFrame

        sliced1 = rdf[["A", "B"]]
        assert type(sliced1) is qp.ReturnDataFrame

        to_series = rdf["A"]
        assert type(to_series) is qp.ReturnSeries

    def test_gmean(self):
        rs = qp.ReturnDataFrame(
            {"x": [0.9, 0.1, 0.2, 0.3, -0.9], "y": [0.05, 0.1, 0.2, -0.5, 0.2]}
        )
        expected = qp.ReturnSeries([-0.200802, -0.036209], index=["x", "y"])
        tm.assert_series_equal(rs.gmean(), expected, rtol=1e-5)
        assert type(rs.gmean()) is qp.ReturnSeries

    def test_sharpe_ratio(self) -> None:
        # Data from https://en.wikipedia.org/wiki/Sharpe_ratio
        mu = [0.25, 0.12]
        sigma = [0.1, 0.1]  # mean and standard deviation
        riskfree_rate = 0.1
        rdf = qp.random.generator.returns(mu, sigma, 10000)
        rs_sharpe_ratio = rdf.sharpe_ratio(riskfree_rate)

        expected = (np.array(mu) - riskfree_rate) / sigma
        assert_allclose(rs_sharpe_ratio, expected, rtol=1e-1)
        assert type(rs_sharpe_ratio) is qp.ReturnSeries

    def test_effect(self):
        mu_list = [0.03, 0.015, 0.04, 0.005, 0.01]  # mean
        sigma_list = [0.01, 0.01, 0.01, 0.01, 0.01]  # standard deviation
        rdf = qp.random.generator.returns(mu_list, sigma_list, 1000)

        expected = (qp.ReturnSeries(mu_list) + 1) ** 12 - 1  # type: ignore

        effect = rdf.effect(qp.stats.period.MONTHLY)
        assert type(effect) is qp.ReturnSeries

        tm.assert_almost_equal(
            effect,
            expected,
            rtol=1e-1,
        )
