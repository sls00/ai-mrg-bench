# Illustrative BISG proxy sample (P4)

`home_credit_bisg_proxy_sample.csv` is a **synthetic US surname + ZCTA panel** for the P4 architecture notebook.

It is **not** a subset of Kaggle Home Credit Default Risk. Home Credit application files lack US ZCTA fields required by BISG; this sample demonstrates the *column contract* and `surgeo` wiring that a future Home Credit scale run would use after geography mapping / US-population substitution.

See `notebooks/02_home_credit_bias_proxy.ipynb` and research findings R-03 / R-07.
