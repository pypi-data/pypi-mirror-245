import numpy as np

_T_COL = "__treated"


def experiment(assigner_inst, base_df, col_to_treat, treat_rate=0.2, seed=742):
    treat_arr = np.random.RandomState(seed).rand(base_df.shape[0]) < treat_rate
    orig_fun = getattr(assigner_inst, col_to_treat)

    def f(df, *args, **kwargs):
        out = orig_fun(df, *args, **kwargs)
        return out + df[_T_COL].astype(int)

    f.__name__ = col_to_treat
    _reset_atts(assigner_inst, col_to_treat, f)
    out = base_df.assign(**{_T_COL: treat_arr}).pipe(assigner_inst)
    _reset_atts(assigner_inst, col_to_treat, orig_fun)
    return out


def measure_effect(assigner, base_df, cause_col, effect_col, treat_rate=0.2, seed=742):
    exp_df = experiment(assigner, base_df, cause_col, treat_rate, seed)
    return exp_df.groupby(_T_COL)[effect_col].mean().pipe(lambda s: s[True] - s[False])


def _reset_atts(assigner_inst, reset_att, reset_val):
    # needed to preserve order
    for c in assigner_inst.__dir__():
        if c.startswith("_"):
            continue
        v = reset_val if c == reset_att else getattr(assigner_inst, c)
        setattr(assigner_inst, c, v)
