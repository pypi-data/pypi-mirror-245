import datetime as dt

import plotly.graph_objects as go
import plotly.io as pio
import polars as pl
from pandas import DataFrame as pd_DataFrame
from plotly.subplots import make_subplots

from humbldata.core.constants import IV_COLUMNS, IV_ENDPOINTS, RV_COLUMNS
from humbldata.core.helpers import DataFrameHelpers as dfh
from humbldata.core.helpers import OpenBBHelpers as obbh
from humbldata.core.models.abstract.errors import HumblDataError
from humbldata.plotting import plotly_theme  # noqa: F401


def format_date(
    date: str | None = None, datetime: bool = False
) -> str | dt.datetime:
    """Set the default date to today's date if no date is provided, or validate
    and format the provided date. If datetime is True, return a datetime object
    with 'us' and UTC time zone info.

    Parameters
    ----------
    date : str, optional
        The date string in the format "YYYY-MM-DD". If not provided, today's
        date will be used (default is None).
    datetime : bool, optional
        If True, return a datetime object with 'us' and UTC time zone info
        (default is False).

    Returns
    -------
    str | dt.datetime
        The validated and formatted date string in the format "YYYY-MM-DD", or
        a datetime object with 'us' and UTC time zone info if datetime is True.

    Raises
    ------
    ValueError
        If the date is not in the correct format.

    Examples
    --------
    >>> format_date()
    '2022-01-01'  # This would return the current date

    >>> format_date('2022-01-01')
    '2022-01-01'

    >>> format_date('2022-01-01', datetime=True)
    datetime.datetime(2022, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)

    >>> format_date('01-01-2022')
    ValueError: time data '01-01-2022' does not match format '%Y-%m-%d'
    """
    if date is None:
        date_obj = dt.datetime.now(dt.timezone.utc)
    else:
        try:
            date_obj = dt.datetime.strptime(date, "%Y-%m-%d")
        except ValueError as e:
            raise HumblDataError(
                "The date must be in the format 'YYYY-MM-DD'"
            ) from e

    if datetime:
        return date_obj.replace(tzinfo=dt.timezone.utc)
    else:
        return date_obj.strftime("%Y-%m-%d")


def check_iv_endpoint(iv_endpoint: str):
    """
    Checks if the provided 'iv_endpoint' is valid or not.

    Parameters
    ----------
    iv_endpoint : str
        The endpoint to be checked.

    Raises
    ------
    HumblDataError
        If the 'iv_endpoint' is not in the list of valid endpoints (IV_ENDPOINTS).

    Returns
    -------
    None

    Examples
    --------
    >>> check_iv_endpoint('strikesHistory')
    None

    >>> check_iv_endpoint('invalid_endpoint')
    HumblDataError: Invalid 'iv_endpoint'. Available options are
    ["strikesHistory", "ivRankHistory", "summariesHistory", "coreDataHistory",]
    """
    if iv_endpoint not in IV_ENDPOINTS:
        raise HumblDataError(
            f"Invalid 'iv_endpoint'. Available options are {IV_ENDPOINTS}."
        )


def data_alignment(
    ivol_df: pl.LazyFrame | pl.DataFrame,
    rvol_df: pl.LazyFrame | pl.DataFrame,
    on="date",
):
    """
    Aligns the implied volatility (ivol) and realized volatility (rvol)
    dataframes based on the 'date' column.

    Parameters
    ----------
    ivol_df : DataFrame or LazyFrame
        The implied volatility dataframe to be aligned.
    rvol_df : DataFrame or LazyFrame
        The realized volatility dataframe to be aligned.
    on : str, optional
        The column name to align the dataframes on (default is "date").

    Returns
    -------
    tuple of DataFrame or LazyFrame
        A tuple containing the aligned implied volatility and realized
        volatility dataframes.

    Raises
    ------
    ValueError
        If the 'date' column is not in the correct datetime format.

    Examples
    --------
    >>> data_alignment(ivol_df, rvol_df)
    (DataFrame with aligned 'date', DataFrame with aligned 'date')

    >>> data_alignment(ivol_df, rvol_df, on='invalid_column')
    ValueError: 'invalid_column' is not in list
    """
    # Convert date columns to Datetime if a string
    rvol_df = dfh.convert_to_datetime(rvol_df, "date", datetime=True)
    ivol_df = dfh.convert_to_datetime(ivol_df, "date", datetime=True)

    ivol_df, rvol_df = pl.align_frames(ivol_df, rvol_df, on=on)
    return ivol_df.interpolate(), rvol_df.interpolate()


def _validate_columns(
    iv_endpoint: str,
    iv_calc_column: str,
    rv_calc_column: str,
    rvol_method: str,
    rv_mean: bool,
) -> None:
    """
    An internal function used in vap_engine(). Validates the columns based on
    the provided parameters. This function does not need to catch invalid
    `iv_endpoints` because it is called after `check_iv_endpoint()` in `calc_vap()`

    Parameters
    ----------
    iv_endpoint : str
        The endpoint to be checked.
    iv_calc_column : str
        The column to be calculated for implied volatility.
    rv_calc_column : str
        The column to be calculated for realized volatility.
    rvol_method : str
        The method to be used for calculating realized volatility.
    rv_mean : bool
        A flag used to determine if the mean of realized volatility should be
        calculated.

    Raises
    ------
    ValueError
        If the 'iv_calc_column' is not in the list of valid columns for the
        'iv_endpoint',
        or if 'rv_mean' is True but 'rv_calc_column' is not 'Volatility_mean',
        or if 'rv_calc_column' is not in the list of valid columns for the
        rvol_method'.

    Returns
    -------
    None

    Examples
    --------
    >>> validate_columns('strikesHistory', 'iv_calc_column', 'rv_calc_column',
    'rvol_method', True)
    None

    >>> validate_columns('invalid_endpoint', 'iv_calc_column', 'rv_calc_column'
    'rvol_method', True)
    ValueError: Invalid iv_calc_column for iv_endpoint 'invalid_endpoint'.
    Expected one of ['valid_columns'], but got `iv_calc_column`
    """
    iv_valid_columns = IV_COLUMNS.get(iv_endpoint)

    if iv_valid_columns is None:
        raise HumblDataError(
            f"""Invalid iv_endpoint. Available options: (iv_endpoint: [iv_calc_column])
            {IV_COLUMNS}."""
        )
    if iv_valid_columns and iv_calc_column not in iv_valid_columns:
        raise HumblDataError(
            f"Invalid iv_calc_column for iv_endpoint '{iv_endpoint}'."
            f" Expected one of {iv_valid_columns}, but got `{iv_calc_column}`"
        )

    if rv_mean and rv_calc_column != "Volatility_mean":
        raise HumblDataError(
            "rv_mean is True, but rv_calc_column is not 'Volatility_mean'."
            f"Make rv_mean = False if you want to use one of {RV_COLUMNS.values()}."
        )

    if not rv_mean:
        rv_valid_columns = RV_COLUMNS.get(rvol_method)
        if rv_valid_columns and rv_calc_column not in rv_valid_columns:
            raise HumblDataError(
                f"Invalid rv_calc_column for rvol_method '{rvol_method}'."
                f" Expected one of {rv_valid_columns}, but got `{rv_calc_column}`"
            )


def vap_engine(
    rvol_method: str,
    iv_endpoint: str,
    ivol_df: pl.DataFrame,
    rvol_df: pl.DataFrame,
    iv_calc_column: str,
    rv_calc_column: str,
    rv_mean: bool,
    clean: bool = True,
) -> pl.DataFrame:
    """
    Calculates the volatility premium. If the <mean> argument is True,
    it will calculate the mean of 10,20,30D volatility.

    Parameters
    ----------
    rvol_method : str
        The method to be used for calculating realized volatility.
    iv_endpoint : str
        The endpoint to be checked.
    ivol_df : pl.DataFrame
        The dataframe containing the implied volatility data.
    rvol_df : pl.DataFrame
        The dataframe containing the realized volatility data.
    iv_calc_column : str
        The column in the implied volatility dataframe to be used for
        calculations.
    rv_calc_column : str
        The column in the realized volatility dataframe to be used for
        calculations.
    rv_mean : bool
        A flag indicating whether the mean of realized volatility should be
        calculated.
    clean : bool, optional
        A flag indicating whether the result should be cleaned
        (default is True).

    Returns
    -------
    pl.DataFrame
        The dataframe containing the calculated volatility premium.

    Raises
    ------
    ValueError
        If the 'iv_calc_column' is not in the list of valid columns for the
        'iv_endpoint', or if 'rv_mean' is True but 'rv_calc_column' is not
        'Volatility_mean',
        or if 'rv_calc_column' is not in the list of valid columns for the
        'rvol_method'.

    Examples
    --------
    >>> vap_engine('rvol_method', 'iv_endpoint', ivol_df, rvol_df,
    'iv_calc_column', 'rv_calc_column', True, True)
    DataFrame with calculated volatility premium.
    """
    # Step 1: Validate Column Selection ------------------------------------
    _validate_columns(
        iv_endpoint=iv_endpoint,
        iv_calc_column=iv_calc_column,
        rv_calc_column=rv_calc_column,
        rvol_method=rvol_method,
        rv_mean=rv_mean,
    )

    # Step 2: Choose Column ------------------------------------------------
    if iv_endpoint == "summariesHistory":
        iv_calc = ivol_df.select(pl.col(iv_calc_column) * 100)
    else:
        iv_calc = ivol_df.select(pl.col(iv_calc_column))

    rv_calc = rvol_df.select(pl.col(rv_calc_column))

    # Step 3: Calculate the volatility premium -----------------------------
    result = pl.DataFrame(
        {
            "date": ivol_df.select("date").collect().to_series(),
            "ticker": ivol_df.select("ticker").collect().to_series(),
            "premia_pct": (
                ((iv_calc.collect() / rv_calc.collect()) - 1).to_series()
            )
            * 100,
        }
    ).lazy()

    # DONE ---------------------------------------------------------------------
    if clean:
        return result.drop_nulls()
    else:
        return result


def merge_data(
    self,
    price_data: pl.DataFrame | pd_DataFrame | pl.LazyFrame | None = None,
    premia_data: pl.DataFrame | pd_DataFrame | None = None,
) -> pl.LazyFrame:
    """
    Merges the price data and premia data based on the 'date'.

    Parameters
    ----------
    self : object
        Used to extract the data from self object to fetch price data if
        price_df is None.
    price_data : DataFrame, optional
        The price data to be merged. If None, the function will fetch the data.
    premia_data : DataFrame, optional
        The premia data to be merged. If None, an exception will be raised.

    Returns
    -------
    DataFrame
        The merged data.

    Raises
    ------
    Exception
        If no premia_data is available.

    Examples
    --------
    >>> merge_data(price_data=df1, premia_data=df2)
    DataFrame with merged data.
    """
    if price_data is None:
        price_data = obbh.get_stock_prices(
            symbol=self.ticker,
            fromdate=self.fromdate,
            todate=self.todate,
            silent=self.silent,
            lazy=False,
        )

    if premia_data is None:
        raise HumblDataError(
            "No premia_data available. Please run calc_vap() before running performance()."  # noqa: E501
        )

    merged_data = price_data.join(
        premia_data,
        on="date",
        how="inner",  # only where date exists in both
    ).select(
        [
            "date",
            "ticker",  # moved to front of df
            "open",
            "high",
            "low",
            "close",
            "adj_close",
            "volume",
            "premia_pct",
        ]
    )

    return merged_data


def vap_signal_engine(
    data: pl.LazyFrame,
    roc_column: str = "premia_pct",
    roc_period: int = 1,
    roc_order: int = 1,
    roc_pct: bool = True,
    **kwargs,
) -> pl.LazyFrame:
    """
    This function is the main engine for generating VAP signals.

    Parameters
    ----------
    data : pl.LazyFrame
        The DataFrame on which to calculate the ROC. (merged_data)
    roc_column : str, optional
        The column to calculate the ROC for.
    roc_period : int, optional
        The number of periods to use for the ROC calculation.
    roc_order : int, optional
        The order of the ROC calculation.
    roc_pct : bool, optional
        Whether to return the ROC as a percentage.
    **kwargs : dict
        Additional parameters. Used for:
            - `signal_method`: used to determine the calculation method.
            Default is 'rolling'.
            - When `signal_method=rolling`:
                If you use rolling, you must pass a window argument.
                Default is 10.
                `window = 10`

    Returns
    -------
    pl.LazyFrame
        The DataFrame with the new column.

    """
    data = _roc(
        data=data,
        column=roc_column,
        periods=roc_period,
        order=roc_order,
        pct=roc_pct,
    )
    data = _percentile(data=data, new_column="premia_pctile", **kwargs)
    data = _quantiles(data=data, **kwargs)
    data = _generate_gross_signals(data, period=roc_period, order=roc_order)
    # Convert column to date
    data = dfh.convert_to_datetime(data, "date", datetime=True)

    return data


def _percentile(
    data: pl.LazyFrame, new_column="premia_percentile", **kwargs
) -> pl.LazyFrame:
    """
    Calculate a growing percentile of a column in a DataFrame.

    Parameters
    ----------
    data : pl.LazyFrame
        The DataFrame to calculate the percentile on. (merged_data)
    new_column : str, optional
        The name of the column to be created (default is "premia_percentile").
    **kwargs : dict
        Additional parameters. Used for:
            - `signal_method`: used to determine the calculation method.
            Default is 'rolling'.
            - When `signal_method=rolling`:
                If you use rolling, you must pass a window argument.
                Default is 10.
                `window = 10`

    Returns
    -------
    pl.DataFrame
        The DataFrame with the new column.

    Examples
    --------
    >>> calculate_growing_percentile(data, merged_data, "premia_percentile", signal_method="rolling", window=10)
    DataFrame with new column 'premia_percentile'.

    >>> calculate_growing_percentile(data, merged_data, "premia_percentile", signal_method="growing")
    DataFrame with new column 'premia_percentile'.
    """
    signal_method = kwargs.get("signal_method", "rolling")

    if signal_method == "growing":
        # Calculate the growing percentile
        rank_calc = (pl.element().rank() / pl.element().len()).last()
        out = data.with_columns(
            pl.col("premia_pct")
            .cumulative_eval(rank_calc, min_periods=1)
            .alias(new_column)
        )
    elif signal_method == "rolling":
        window = kwargs.get("window", 10)
        data_p = data.collect().to_pandas()
        data_p[new_column] = (
            data_p["premia_pct"].rolling(window, min_periods=1).rank(pct=True)
        )
        out = pl.from_pandas(data_p).lazy()
    return out


def _quantiles(
    data: pl.LazyFrame,
    **kwargs,
) -> pl.LazyFrame:
    """
    Calculate growing quantiles of a column in a DataFrame.

    Parameters
    ----------
    data : pl.DataFrame
        The DataFrame on which to calculate the growing quantiles. (merged_data)
    **kwargs : dict
        - `signal_method` : Determines the calculation method.
        Default is rolling.
        - `window` : int, optional.
        The window size for the rolling calculation. Only used when
        signal_method=rolling. Default is 10.
        - `quantiles` : Used to generate gross/degross signals at the top/bottom
        of values. Default is (0.10, 0.90).

    Details
    -------
    When `signal_method='rolling'`, you can pass:
        - `window=<int>`

    Returns
    -------
    pl.DataFrame
        The DataFrame with the new columns for the calculated quantiles
        ("degross_quantile", "gross_quantile")
    """
    signal_method = kwargs.get("signal_method", "rolling")
    quantile_names = ["degross_quantile", "gross_quantile"]
    quantiles = kwargs.get("quantiles", (0.1, 0.9))

    # Calculate the growing quantiles
    if signal_method == "growing":
        for quantile, name in zip(quantiles, quantile_names, strict=True):
            quantile_calc = pl.element().quantile(quantile)
            data = data.with_columns(
                pl.col("premia_pct")
                .cumulative_eval(quantile_calc, min_periods=1)
                .alias(name)
            )
    # Calculate the rolling quantiles
    elif signal_method == "rolling":
        window = kwargs.get("window", 10)
        for quantile, name in zip(quantiles, quantile_names, strict=True):
            data = data.with_columns(
                pl.col("premia_pct")
                .rolling_quantile(quantile, window_size=window, min_periods=1)
                .alias(name)
            )
    return data


def _roc(
    data: pl.LazyFrame,
    column: str = "premia_pct",
    periods: int = 1,
    order: int = 1,
    pct: bool = True,
) -> pl.LazyFrame:
    """
    Calculate the Rate of Change (ROC) for a specified column in a DataFrame.

    Parameters
    ----------
    data : pl.DataFrame
        The DataFrame on which to calculate the ROC. (merged_data)
    column : str
        The column to calculate the ROC for.
    periods : int, optional
        The number of periods to use for the ROC calculation. Default is 1.
    order : int, optional
        The order of the difference for the ROC calculation. Default is 1.
    pct : bool, optional
        Whether to return the ROC as a percentage. If False, return as a ratio.
        Default is True.

    Returns
    -------
    pl.DataFrame
        The DataFrame with the new column for the calculated ROC.

    """
    for i in range(order):
        roc = (pl.col(column) - pl.col(column).shift(periods)) / pl.col(
            column
        ).shift(periods).abs()
        if pct:
            roc *= 100
        column = f"ROC_{periods}D_{i+1}"
        data = data.with_columns(roc.alias(column))
    return data


def _generate_gross_signals(
    data: pl.LazyFrame, period: int = 1, order: int = 1
) -> pl.LazyFrame:
    """
    Generates two new columns 'gross_fired' and 'degross_fired' in the DataFrame
    based on certain conditions.

    A 'gross_fired' signal is generated when the 'premia_pct' is greater than
    the 'gross_quantile' and the ROC is less than 0.
    A 'degross_fired' signal is generated when the 'premia_pct' is less than
    the 'degross_quantile' and the ROC is greater than 0.

    Parameters
    ----------
    data : pl.DataFrame
        The DataFrame in which to generate the signals.
    period : int, optional
        The period used to create column name. Default is 1.
    order : int, optional
        The order used to create column name. Default is 1.

    Returns
    -------
    pl.DataFrame
        The DataFrame with the new 'gross_fired' and 'degross_fired' columns.

    Examples
    --------
    >>> _generate_gross_signals(data, period=1, order=1)
    """
    roc_column = f"ROC_{period}D_{order}"
    data = data.with_columns(
        [
            (
                (pl.col("premia_pct") > pl.col("gross_quantile"))
                & (pl.col(roc_column) < 0)
            ).alias("gross_fired"),
            (
                (pl.col("premia_pct") < pl.col("degross_quantile"))
                & (pl.col(roc_column) > 0)
            ).alias("degross_fired"),
        ]
    )
    return data


def vap_performance_engine(self, **kwargs):
    # Setup --------------------------------------------------------------------
    import numpy as np
    from quantstats.stats import to_drawdown_series as dd_series

    from humbldata.performance.stats import performance_stats as p_stats

    if self.signal_degross is None and self.signal_gross is None:
        raise Exception(
            "No buy/sell data available. Please check VolatilityPremium.signal()"  # noqa: E501
        )
    # Initialize an empty list to store the trade data
    trade_data = []
    sell_date = None
    init_investment = kwargs.get("init_investment", 100)
    reinvest = kwargs.get("reinvest", 1)
    capital = init_investment

    # Collect LazyFrames
    self.signal_gross = self.signal_gross.collect()
    self.signal_degross = self.signal_degross.collect()

    # Step 1: Loop through each row in the buy orders dataframe ----------------
    for row in self.signal_gross.select(["date", "adj_close"]).iter_rows(
        named=False
    ):
        # With named = F, row[0] = date, row[1] = adj close
        buy_date = row[0]
        # Skip buy orders that are before the latest sale
        if sell_date is not None:
            if buy_date < sell_date:
                continue
        buy_price = row[1]
        # Find the next sell order that occurs after the buy order
        next_sell_order = self.signal_degross.filter(
            pl.col("date") > buy_date
        ).head(1)
        # If no next sell order, use the most recent available close price
        if next_sell_order.shape[0] == 0:
            sell_date = self.merged_data["date"].max()
            sell_price = self.merged_data.filter(pl.col("date") == sell_date)[
                "adj_close"
            ].item()
        else:
            sell_date = next_sell_order["date"].item()
            sell_price = next_sell_order["adj_close"].item()
        # Skip first iteration to keep inital investmnet before
        # multiplying by the reinvest coefficient
        if capital != init_investment:
            investment = capital * reinvest
        else:
            investment = capital
        # Update the capital for the next trade
        trade_return = np.log(sell_price / buy_price)
        capital = capital + (investment * trade_return)
        # Append the trade data to the list
        trade_data.append(
            {
                "buy_date": buy_date,
                "buy_price": buy_price,
                "sell_date": sell_date,
                "sell_price": sell_price,
                "investment": investment,
                "trade_return": trade_return,
                "capital": capital,
            }
        )
    # Convert the list of trade data into a dataframe
    trade_data = pl.DataFrame(trade_data)
    trade_data = dfh.convert_to_datetime(trade_data, "buy_date", datetime=True)
    trade_data = dfh.convert_to_datetime(
        trade_data, "sell_date", datetime=True
    ).collect()
    # Add drawdown column
    drawdown = (dd_series(trade_data["capital"].to_pandas()) * 100).__round__(6)
    trade_data = trade_data.with_columns(drawdown=pl.from_pandas(drawdown))
    # Step 2: Calculate Performance stats ----------------------------------
    performance_stats = p_stats(df=trade_data, **kwargs)

    # DONE: Compile Stats --------------------------------------------------
    self.trade_data = trade_data.lazy()
    self.trade_stats = performance_stats
    return self


def plot_engine(self, plot_method, show: bool = False):
    """
    This method plots data based on the provided plot method.

    Parameters
    ----------
    plot_method : str
        The method to use for plotting. Options are "simple", "signal", and "performance".
    show : bool
        This is used to control the fig.show() code. You do not want to show
        plot in a webapp, they will open new tabs. Default is False.

    Returns
    -------
    self
        Returns the instance of the class.
        .perf_plot: performance plot
        .plot: premia vs price plot

    Raises
    ------
    ValueError
        If an invalid plot_method is provided.
    """
    # Step 1: Plot Data based on self.plot_method ------------------------------
    pio.templates.default = "humbl_dark"

    if plot_method == "simple":
        fig = _plot_simple(self.merged_data.collect(), ticker=self.ticker)
    elif plot_method == "signal":
        fig = _plot_signal(
            self.merged_data.collect(),
            signal_gross=self.signal_gross.collect(),
            signal_degross=self.signal_degross.collect(),
            ticker=self.ticker,
        )
    elif plot_method == "performance":
        fig, perf_fig = _plot_performance(
            data=self.merged_data.collect(),
            trade_data=self.trade_data.collect(),
            signal_gross=self.signal_gross,  # DataFrame has been .collect()'ed in vap_performance_engine() # noqa: E501
            signal_degross=self.signal_degross,  # DataFrame has been .collect()'ed in vap_performance_engine() # noqa: E501
            ticker=self.ticker,
        )
    else:
        raise ValueError(f"Invalid plot_method: {plot_method}")

    # Linking Spike Lines Across Both Plots
    fig.update_traces(xaxis="x2")

    # Set Config
    config = {
        "displaylogo": False,
        "modeBarButtonsToRemove": ["lasso", "select", "zoomin", "zoomout"],
        "modeBarButtonsToAdd": ["v1hovermode"],
    }

    perf_config = {
        "displaylogo": False,
        "modeBarButtonsToRemove": [
            "lasso",
            "select",
            "zoomin",
            "zoomout",
            "hoverClosestCartesian",
            "hoverCompareCartesian",
            # "toggleSpikelines",
        ],
        "modeBarButtonsToAdd": ["v1hovermode", "togglespikelines"],
    }

    if plot_method == "performance":
        if show:
            fig.show(config=config)
            perf_fig.show(config=perf_config)
        self.plot = fig
        self.perf_plot = perf_fig

    else:
        if show:
            fig.show(config=config)
        self.plot = fig
    return self


def _plot_simple(data, ticker):
    """Plotting Method to show a simple Price vs Premia Plot, no signals"""

    # Step 1: Create subplots --------------------------------------------------
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
    )

    # Step 2: Add Price Trace --------------------------------------------------
    fig.add_trace(
        go.Scatter(
            x=data["date"],
            y=data["adj_close"],
            mode="lines",
            name="Price",
            # line=dict(color="#fbba21"),
        ),
        row=1,
        col=1,
    )

    # Step 3: Add Premia Trace -------------------------------------------------
    fig.add_trace(
        go.Scatter(
            x=data["date"],
            y=data["premia_pct"],
            mode="lines",
            name="Premia",
            # line=dict(color="red"),
        ),
        row=2,
        col=1,
    )

    # Step 4: Create Layout and Axes -------------------------------------------
    fig = _plot_simple_layout(fig, ticker)

    return fig


def _plot_simple_layout(fig, ticker, zero_line_color: str = "rgb(63,70,139)"):
    fig.update_layout(
        # template="humbl_dark",
        height=600,
        autosize=True,
        hovermode="x",
        spikedistance=50,  # Distance from the cursor (in pixels) at which a spike is shown # noqa: E501
        # plot_bgcolor="rgb(25,25,25)",
        # title=f"{ticker}",
        legend=dict(
            #     xanchor="center",
            #     x=0.5,
            #     y=-0.15,
            #     orientation="h",
            #     traceorder="normal",
            #     font=dict(family="open-sans", size=12, color="white"),
            bgcolor="rgba(0,0,0,0)",
            #     bordercolor="rgb(63,70,139)",
            #     borderwidth=0.5,
        ),
        modebar=dict(add=["v1hovermode"]),
    )

    fig.update_xaxes(
        title="Date",
        showgrid=True,
        showspikes=True,
        spikemode="across",
        spikethickness=-2,
        spikecolor="purple",
        showline=False,
        row=2,
        col=1,
    )
    fig.update_yaxes(
        title="Price ($)",
        showgrid=False,
        showspikes=True,
        spikemode="across",
        spikethickness=-2,
        spikecolor="purple",
        fixedrange=False,
        showline=False,
        row=1,
        col=1,
    )
    fig.update_yaxes(
        title="Premia (%)",
        showgrid=False,
        showspikes=True,
        spikemode="across",
        spikethickness=-2,
        spikecolor="purple",
        fixedrange=False,
        zeroline=True,
        zerolinecolor=zero_line_color,
        showline=False,
        row=2,
        col=1,
    )
    # Add Lines Around the Plot
    fig = _plot_simple_layout_trace(fig)
    return fig


def _plot_simple_layout_trace(fig, line_color: str = "rgb(63,70,139)"):
    # Top Line
    fig.add_shape(
        type="line",
        xref="paper",
        yref="paper",
        x0=0,
        y0=1.0,
        x1=1.0,
        y1=1.0,
        line=dict(
            color=line_color,
            width=1.2,
        ),
    )
    # Bottom Line
    fig.add_shape(
        type="line",
        xref="paper",
        yref="paper",
        x0=0,
        y0=0.0,
        x1=1.0,
        y1=0.0,
        line=dict(
            color=line_color,
            width=1.2,
        ),
    )
    # Right Line
    fig.add_shape(
        type="line",
        xref="paper",
        yref="paper",
        x0=1.0,
        y0=1.0,
        x1=1.0,
        y1=0,
        line=dict(
            color=line_color,
            width=1.2,
        ),
    )
    # Left Line
    fig.add_shape(
        type="line",
        xref="paper",
        yref="paper",
        x0=0.0,
        y0=1.0,
        x1=0.0,
        y1=0,
        line=dict(
            color=line_color,
            width=1.2,
        ),
    )
    # Middle line
    fig.add_shape(
        type="line",
        xref="paper",
        yref="paper",
        x0=0.0,
        y0=0.5,
        x1=1.0,
        y1=0.5,
        line=dict(
            color=line_color,
            width=0.8,
        ),
    )
    return fig


def _plot_signal(data, signal_gross, signal_degross, ticker):
    """Plotting Method to show  Price vs Premia Plot, with signals"""
    # Setup: Create Simple Plot ------------------------------------------------
    fig = _plot_simple(data, ticker)

    # Step 1: Add Signal Markers to Price plot (row 1) -------------------------
    fig.add_trace(
        go.Scatter(
            x=signal_degross["date"],
            y=signal_degross["adj_close"],
            mode="markers",
            name="De-Gross",
            marker=dict(color="red"),
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=signal_gross["date"],
            y=signal_gross["adj_close"],
            mode="markers",
            name="Gross",
            marker=dict(color="green"),
        ),
        row=1,
        col=1,
    )
    return fig


def _plot_performance(data, trade_data, signal_gross, signal_degross, ticker):
    # Setup: Create Signal Plot ------------------------------------------------
    fig = _plot_signal(data, signal_gross, signal_degross, ticker)

    mean_return = trade_data["trade_return"].mean() * 100

    # Step 1: Create Trade Stat Plots ------------------------------------------
    # Histogram of returns
    hist_plot = go.Histogram(
        x=trade_data["trade_return"] * 100,
        nbinsx=50,
        marker=dict(
            color="rgba(0, 200, 100, 0.6)",
            line=dict(color="rgba(255, 255, 255, 1)", width=0.5),
        ),
        name="Freq.",
    )
    # Drawdown graph
    drawdown_plot = go.Scatter(
        x=trade_data["sell_date"],
        y=trade_data["drawdown"],
        mode="lines",
        fill="tozeroy",
        line=dict(color="red"),
        fillcolor="rgba(255, 0, 0, 0.3)",
        hoverinfo="x+y",
    )
    # Growth of $1 graph
    growth_plot = go.Scatter(
        x=trade_data["sell_date"],
        y=trade_data["capital"],
        mode="lines",
        fill="tozeroy",
        line=dict(color="green"),
        fillcolor="rgba(0, 255, 0, 0.3)",
        hoverinfo="x+y",
    )
    # Create subplot
    perf_fig = make_subplots(
        rows=2,
        cols=2,
        column_widths=[0.35, 0.65],
        specs=[[{"rowspan": 2}, {}], [None, {}]],
        vertical_spacing=0.2,
    )
    perf_fig.add_trace(hist_plot, row=1, col=1)
    perf_fig.add_trace(growth_plot, row=1, col=2)
    perf_fig.add_trace(drawdown_plot, row=2, col=2)

    perf_fig.update_layout(
        showlegend=False,
        title=f"{ticker} | Volatility Premium Strategy Performance",
        shapes=[
            dict(
                type="line",
                x0=mean_return,
                x1=mean_return,
                y0=0,
                y1=1,
                yref="paper",
                line=dict(color="orange", dash="solid", width=3),
            ),
        ],
        annotations=[
            dict(
                x=mean_return,
                y=1.1,
                yref="paper",
                text=f"<b>Mean: {round(mean_return, 2)}</b>",
                showarrow=False,
                font=dict(color="orange"),
            ),
        ],
    )
    # Format Histogram
    perf_fig.update_xaxes(
        title_text="Returns (%)", showgrid=False, row=1, col=1
    )
    perf_fig.update_yaxes(title_text="Frequency", row=1, col=1)
    # Format Growth
    perf_fig.update_yaxes(title_text="Gains ($)", row=1, col=2)
    perf_fig.update_xaxes(showticklabels=False, row=1, col=2)
    # Format Drawdown
    perf_fig.update_yaxes(title_text="Drawdowns (%)", row=2, col=2)

    return fig, perf_fig
