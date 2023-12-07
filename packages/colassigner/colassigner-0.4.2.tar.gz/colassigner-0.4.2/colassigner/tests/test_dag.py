from colassigner import ColAssigner, get_dag


class Cols(ColAssigner):  # pragma: no cover
    # TODO: nested

    def __init__(self):
        self._a = 4

    def col_a(self, df):
        return range(self._a, df.shape[0] + self._a)

    def col_b(self, df):
        return df.loc[:, Cols.col_a] - 1

    def col_c(self, df):
        return self._helper(df, 3)

    def col_d(self, df):
        return self._helper2(df, Cols.col_c)

    def col_e(self, df):
        return self._helper2(df, col=Cols.col_a) + self._helper3(df)

    def _helper(self, df, n):
        if n > 100:
            return self._helper(df, n / 2)
        return df.loc[:, Cols.col_b].pipe(lambda s: s * 3)

    def _helper2(self, df, col):
        for _ in range(3):
            pass
        return df[col] ** 2

    def _helper3(self, df):
        try:
            "boo"
        except ValueError:
            raise IndexError()
        return self._helper2(df, Cols.col_d) - self._helper(df, 3)


true_dag = [
    ("col_a", "col_b"),
    ("col_b", "col_c"),
    ("col_c", "col_d"),
    ("col_a", "col_e"),
    ("col_b", "col_e"),
    ("col_d", "col_e"),
]


def test_graph_detection():
    assert sorted(true_dag) == sorted(get_dag(Cols))
