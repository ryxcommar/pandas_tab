# Pandas Tab

[![](https://github.com/ryxcommar/pandas_tab/actions/workflows/tests.yml/badge.svg)](../../actions)
[![](https://github.com/ryxcommar/pandas_tab/actions/workflows/style.yml/badge.svg)](../../actions)

Implementation of Stata's `tabulate` command in Pandas for extremely easy to type one-way and two-way tabulations.

Support:

- **Python 3.7 and 3.8:** Pandas >=0.23.x
- **Python 3.9:** Pandas >=1.0.x

## Background & Purpose

As someone who made the move from Stata to Python, one thing I noticed is that I end up doing fewer tabulations of my data when working in Pandas. I believe that the reason for this has a lot to do with API differences that make it slightly less convenient to run tabulations extremely quickly.

For example, if you want to look at values counts in column "foo", in Stata it's merely `tab foo`. In Pandas, it's `df["foo"].value_counts()`. This is over twice the amount of typing.

It's not just a brevity issue. If you want to add one more column and to go from one-way to two-way tabulation (e.g. look at "foo" and "bar" together), this isn't as simple as adding one more column:

- `df[["foo", "bar"]].value_counts().unstack()` requires one additional transformation to move away from a multi-indexed series.
- `pd.crosstab(df["foo"], df["bar"])` is a totally different interface from the one-way tabulation.

Pandas Tab attempts to solve these issues by creating an interface more similar to Stata: `df.tab("foo")` and `df.tab("foo", "bar")` give you, respectively, your one-way and two-way tabulations.

## Example

```python
# using IPython integration:
# ! pip install pandas-tab[full]
# ! pandas_tab init

import pandas as pd

df = pd.DataFrame({
    "foo":  ["a", "a", "b", "a", "b", "c", "a"],
    "bar":  [4,   5,   7,   6,   7,   7,   5],
    "fizz": [12,  63,  23,  36,  21,  28,  42]
})

# One-way tabulation
df.tab("foo")

# Two-way tabulation
df.tab("foo", "bar")

# One-way with aggregation
df.tab("foo", values="fizz", aggfunc=pd.Series.mean)

# Two-way with aggregation
df.tab("foo", "bar", values="fizz", aggfunc=pd.Series.mean)
```

Outputs:

```
>>> # One-way tabulation
>>> df.tab("foo")

     size  percent
foo               
a       4    57.14
b       2    28.57
c       1    14.29

>>> # Two-way tabulation
>>> df.tab("foo", "bar")

bar  4  5  6  7
foo            
a    1  2  1  0
b    0  0  0  2
c    0  0  0  1

>>> # One-way with aggregation
>>> df.tab("foo", values="fizz", aggfunc=pd.Series.mean)

      mean
foo       
a    38.25
b    22.00
c    28.00

>>> # Two-way with aggregation
>>> df.tab("foo", "bar", values="fizz", aggfunc=pd.Series.mean)

bar     4     5     6     7
foo                        
a    12.0  52.5  36.0   NaN
b     NaN   NaN   NaN  22.0
c     NaN   NaN   NaN  28.0
```

## Setup

### Full Installation (IPython / Jupyter Integration)

The full installation includes a CLI that adds a startup script to IPython:

```shell
pip install pandas-tab[full]
```

Then, to enable the IPython / Jupyter startup script:

```shell
pandas_tab init
```

You can quickly remove the startup script as well:

```shell
pandas_tab delete
```

More on the startup script in the section **IPython / Jupyter Integration**.

### Simple installation:

If you don't want the startup script, you don't need the extra dependencies. Simply install with:

```shell
pip install pandas-tab
```

## IPython / Jupyter Integration

The startup script auto-loads `pandas_tab` each time you load up a new IPython kernel (i.e. each time you fire up or restart your Jupyter Notebook).

You can run the startup script in your terminal with `pandas_tab init`.

Without the startup script:

```python
# WITHOUT STARTUP SCRIPT
import pandas as pd
import pandas_tab

df = pd.read_csv("foo.csv")
df.tab("x", "y")
```

Once you install the startup script, you don't need to do `import pandas_tab`:

```python
# WITH PANDAS_TAB STARTUP SCRIPT INSTALLED
import pandas as pd

df = pd.read_csv("foo.csv")
df.tab("x", "y")

```

The IPython startup script is convenient, but there are some downsides to using and relying on it:

- It needs to load Pandas in the background each time the kernel starts up. For typical data science workflows, this should not be a problem, but you may not want this if your workflows ever avoid Pandas.
- The IPython integration relies on hidden state that is environment-dependent. People collaborating with you may be unable to replicate your Jupyter notebooks if there are any `df.tab()`'s in there and you don't `import pandas_tab` manually.

For that reason, I recommend the IPython integration for solo exploratory analysis, but for collaboration you should still `import pandas_tab` in your notebook.

## Limitations / Known Issues

- No tests or guarantees for 3+ way cross tabulations. Both `pd.crosstab` and `pd.Series.value_counts` support multi-indexing, however this behavior is not yet tested for `pandas_tab`.
- Behavior for `dropna` kwarg mimics `pd.crosstab` (drops blank columns), not `pd.value_counts` (include `NaN`/`None` in the index), even for one-way tabulations.
- No automatic hook into Pandas; you must import `pandas_tab` in your code to register the extensions. Pandas does not currently search entry points for extensions, other than for plotting backends, so it's not clear that there's a clean way around this.
- Does not mimic Stata's behavior of taking unambiguous abbreviations of column names, and there is no option to turn this on/off.
- Pandas 0.x is incompatible with Numpy 1.20.x. If using Pandas 0.x, you need Numpy 1.19.x.
- (Add more stuff here?)
