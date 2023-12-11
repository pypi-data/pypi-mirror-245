import numpy as np
import pandas as pd
import os
from datetime import timedelta, datetime, time
from volstreet.config import logger
from volstreet.vectorized_blackscholes import add_greeks_to_dataframe
from volstreet.backtests.underlying_info import UnderlyingInfo
from volstreet.backtests.framework import IntradayBackTest
from volstreet.parallelization import execute_in_parallel
from volstreet.utils.data_io import make_directory_if_needed

# %%


class DeltaBackTest(IntradayBackTest):
    RESULTS_FOLDER = "data\\delta_backtests\\"

    def __init__(self, underlying: UnderlyingInfo):
        super().__init__(underlying)
        self.rolling_atm_info = None

    def get_strike_columns(self):
        return ["call_strike", "put_strike"]

    def merge_with_option_prices(
        self,
        data_frame_to_merge: pd.DataFrame,
    ) -> pd.DataFrame:
        option_prices = self.option_prices.reset_index()

        merged_with_call_prices = data_frame_to_merge.merge(
            option_prices[["timestamp", "expiry", "call_price", "strike"]],
            left_on=["timestamp", "expiry", "call_strike"],
            right_on=["timestamp", "expiry", "strike"],
            how="left",
        )
        merged_with_put_prices = merged_with_call_prices.merge(
            option_prices[["timestamp", "expiry", "put_price", "strike"]],
            left_on=["timestamp", "expiry", "put_strike"],
            right_on=["timestamp", "expiry", "strike"],
            how="left",
        )
        merged_with_put_prices.drop(columns=["strike_x", "strike_y"], inplace=True)

        return merged_with_put_prices

    def store_atm_info(self, intraday_prices: pd.DataFrame):
        intraday_prices = self._build_option_chain_skeleton(
            self.underlying.name,
            intraday_prices,
            num_strikes=1,
            num_exp=1,
            threshold_days_expiry=0,
        )
        with_option_prices = self.merge_with_option_prices(intraday_prices)
        rolling_atm_info = with_option_prices[
            [
                "timestamp",
                "open",
                "time_to_expiry",
                "call_strike",
                "put_strike",
                "call_price",
                "put_price",
            ]
        ]

        rolling_atm_info.columns = [
            "atm_" + col if (("call" in col) or ("put" in col)) else col
            for col in rolling_atm_info.columns
        ]
        self.rolling_atm_info = rolling_atm_info

    def add_greeks_to_rolling_atm_info(self):
        temp_df = self.rolling_atm_info.copy()
        temp_df.columns = [col.replace("atm_", "") for col in temp_df.columns]
        temp_df = temp_df.astype({"open": float, "call_strike": int, "put_strike": int})
        self.rolling_atm_info = add_greeks_to_dataframe(
            temp_df, r_col="r", use_one_iv=False
        )

    def calculate_moving_interest_rate(self) -> pd.DataFrame:
        with_option_prices = self.rolling_atm_info.copy()
        with_option_prices["synthetic_rate"] = (
            with_option_prices["atm_call_strike"]
            + with_option_prices["atm_call_price"]
            - with_option_prices["atm_put_price"]
        )
        with_option_prices["r"] = (
            (with_option_prices["synthetic_rate"] / with_option_prices["open"]) - 1
        ) * (1 / with_option_prices["time_to_expiry"])

        # Removing infinities
        with_option_prices["r"] = np.where(
            with_option_prices["r"] == np.inf,
            50,
            np.where(with_option_prices["r"] == -np.inf, -50, with_option_prices["r"]),
        )
        self.rolling_atm_info["r"] = with_option_prices["r"]
        return with_option_prices[["timestamp", "r"]]

    @staticmethod
    def find_closest_deltas(
        strikes: pd.DataFrame,
        target: float,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        delta_col = "call_delta" if "call_delta" in strikes.columns else "put_delta"
        lower_strike = strikes[strikes[delta_col] <= target].nlargest(1, delta_col)
        upper_strike = strikes[strikes[delta_col] >= target].nsmallest(1, delta_col)
        if lower_strike.empty:
            lower_strike = (
                upper_strike.copy()
            )  # Crucial to copy the dataframe here because we assign a new column later
            # And want to avoid overwriting the original dataframe
        if upper_strike.empty:
            upper_strike = (
                lower_strike.copy()
            )  # Crucial to copy the dataframe here because we assign a new column later
            # And want to avoid overwriting the original dataframe
        return lower_strike, upper_strike

    @staticmethod
    def calculate_ratios(
        lower: pd.DataFrame,
        upper: pd.DataFrame,
        target: float,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        col = "call_delta" if "call_delta" in lower.columns else "put_delta"
        lower_delta = lower[col].iloc[0]
        upper_delta = upper[col].iloc[0]
        lower_strike = lower["strike"].iloc[0]
        upper_strike = upper["strike"].iloc[0]

        if lower_strike == upper_strike:
            ratio_lower = 1
            ratio_upper = 0
        else:
            ratio_lower = (upper_delta - target) / (upper_delta - lower_delta)
            ratio_upper = (target - lower_delta) / (upper_delta - lower_delta)

        lower["ratio"] = ratio_lower
        upper["ratio"] = ratio_upper

        return lower, upper

    def calculate_strikes_and_ratios(
        self,
        option_chain: pd.DataFrame,
        delta_range: tuple,
        target_delta: float,
    ) -> dict[str, list[tuple]]:
        if not (delta_range[0] <= target_delta <= delta_range[1]):
            raise ValueError("Target delta must be within the specified delta range.")

        option_chain["put_delta"] = np.abs(option_chain["put_delta"])

        def filter_and_sort_options(options, delta_col):
            filtered_options = options[options[delta_col] >= delta_range[0]]
            filtered_options = filtered_options[
                filtered_options[delta_col] <= delta_range[1]
            ]
            return filtered_options[["strike", delta_col]].sort_values(by=delta_col)

        calls = filter_and_sort_options(option_chain, "call_delta")
        puts = filter_and_sort_options(option_chain, "put_delta")

        def find_best_strike(options, target_delta):
            col = "call_delta" if "call_delta" in options.columns else "put_delta"
            close_strikes = options[np.abs(options[col] - target_delta) <= 0.01]
            if not close_strikes.empty:
                return close_strikes.iloc[0]
            return None

        trade_dict = {}
        best_call = find_best_strike(calls, target_delta)
        best_put = find_best_strike(puts, target_delta)

        if best_call is not None:
            trade_dict["calls"] = [*zip([[best_call["strike"], 1]])]

        if best_put is not None:
            trade_dict["puts"] = [*zip([[best_put["strike"], 1]])]

        if best_call is not None and best_put is not None:
            return trade_dict

        if best_call is None:
            lower_call_delta, upper_call_delta = self.find_closest_deltas(
                calls, target_delta
            )
            call_ratios = self.calculate_ratios(
                lower_call_delta, upper_call_delta, target_delta
            )
            trade_calls = [
                strike_df[["strike", "ratio"]].values.tolist()[0]
                for strike_df in call_ratios
            ]
            trade_dict["calls"] = [*zip(*[*filter(lambda x: x[1] != 0, trade_calls)])]

        if best_put is None:
            lower_put_delta, upper_put_delta = self.find_closest_deltas(
                puts, target_delta
            )
            put_ratios = self.calculate_ratios(
                lower_put_delta, upper_put_delta, target_delta
            )
            trade_puts = [
                strike_df[["strike", "ratio"]].values.tolist()[0]
                for strike_df in put_ratios
            ]
            trade_dict["puts"] = [*zip(*[*filter(lambda x: x[1] != 0, trade_puts)])]
        return trade_dict

    def select_equal_strikes(
        self,
        snapshot: pd.DataFrame,
        trade_deltas_between: tuple[float, float],
    ) -> tuple[int, int]:
        def filter_and_process(
            df_with_greeks: pd.DataFrame, deltas_range: tuple[float, float]
        ) -> pd.DataFrame:
            df = df_with_greeks.copy()
            # Filtering for strikes with deltas within the given range
            filtered_df = df[
                (df["call_delta"] > deltas_range[0])
                & (df["call_delta"] < deltas_range[1])
                & (df["put_delta"] > deltas_range[0])
                & (df["put_delta"] < deltas_range[1])
            ]
            return filtered_df

        with_option_prices = self.merge_with_option_prices(snapshot)
        with_option_prices = with_option_prices.astype(
            {"open": float, "call_strike": int, "put_strike": int}
        )
        with_greeks = add_greeks_to_dataframe(with_option_prices, r_col="r")
        with_greeks["put_delta"] = np.abs(with_greeks["put_delta"])

        filtered = filter_and_process(with_greeks, trade_deltas_between)

        if filtered.empty:
            logger.info(
                f"No strikes found in the given delta range {trade_deltas_between}. "
                f"Trying to find strikes in the range (0.22, 0.78)"
            )
            filtered = filter_and_process(
                with_greeks, (0.22, 0.78)
            )  # Hardcoded fallback

        if filtered.empty:
            raise ValueError(
                "No strikes found in the given delta range. Handle this error by shifting the range or "
                "by advancing in time."
            )

        # Creating a DataFrame with all combinations of Call and Put strikes
        call_strikes = filtered["call_strike"].repeat(len(filtered))
        put_strikes = np.tile(filtered["put_strike"], len(filtered))
        call_deltas = filtered["call_delta"].repeat(len(filtered)).values
        put_deltas = np.tile(filtered["put_delta"], len(filtered))

        # Calculate disparities using vectorized operations
        disparities = np.maximum(call_deltas, put_deltas) / np.minimum(
            call_deltas, put_deltas
        )
        # Creating the final DataFrame
        combined_df = pd.DataFrame(
            {
                "call_strike": call_strikes,
                "put_strike": put_strikes,
                "disparity": disparities,
            },
        )
        combined_df = combined_df.reset_index(drop=True)
        if combined_df.empty:
            return self.select_equal_strikes(snapshot, (0.25, 0.75))
        most_equal_strike = combined_df.loc[combined_df["disparity"].idxmin()]
        return most_equal_strike["call_strike"], most_equal_strike["put_strike"]

    def prepare_segment_for_processing(
        self,
        segment_prices: pd.DataFrame,
        trade_deltas_between: tuple[float, float],
    ):
        """Prepares the segment for processing by adding the call and put strikes and
        merging with option prices and adding greeks"""

        entry_snapshot = self.snapshot_at_entry(segment_prices.iloc[0], num_strikes=8)
        logger.info(f"{self.underlying.name} delta backtest: built snapshot at entry")
        potential_strikes = np.unique(
            entry_snapshot[["call_strike", "put_strike"]].values
        ).tolist()
        if not all(self.strike_available(potential_strikes)):
            logger.info(
                f"Fetching missed strikes {potential_strikes} and some additional strikes for {segment_prices.iloc[0].name}"
            )
            additional_strikes = np.arange(
                min(potential_strikes) - 10 * self.underlying.base,
                max(potential_strikes)
                + 10 * self.underlying.base
                + self.underlying.base,
                self.underlying.base,
            ).tolist()
            self.fetch_missed_strikes(additional_strikes, segment_prices.iloc[0].name)
        self.check_option_prices_availability(entry_snapshot)
        call_strike, put_strike = self.select_equal_strikes(
            entry_snapshot, trade_deltas_between
        )
        logger.info(f"{self.underlying.name} delta backtest: selected strikes")
        segment_prices["call_strike"] = call_strike
        segment_prices["put_strike"] = put_strike
        self.check_option_prices_availability(segment_prices)
        segment_prices_with_option_prices = self.merge_with_option_prices(
            segment_prices
        )
        segment_prices_with_option_prices = add_greeks_to_dataframe(
            segment_prices_with_option_prices, r_col="r", use_one_iv=False
        )
        logger.info(f"{self.underlying.name} delta backtest: added greeks")
        segment_prices_with_option_prices.set_index("timestamp", inplace=True)
        return segment_prices_with_option_prices

    @staticmethod
    def process_result(
        segment: pd.DataFrame, segment_result: pd.DataFrame
    ) -> pd.DataFrame:
        columns = segment_result.columns.tolist()
        additional_cols = [
            "open",
            "call_strike",
            "put_strike",
            "call_price",
            "put_price",
            "call_iv",
            "put_iv",
            "call_delta",
            "put_delta",
            "call_gamma",
            "put_gamma",
        ]
        processed_result = segment_result.merge(
            segment[additional_cols], left_index=True, right_index=True
        )
        processed_result = processed_result[additional_cols + columns]
        return processed_result

    def reset_state(self):
        self.expiry = None
        self._option_prices = pd.DataFrame()
        self.unique_strikes = []
        return self

    def fetch_and_prepare_index_prices(self, from_date, to_date, only_expiry):
        index_prices = self.fetch_index_prices(self.underlying.name, from_date, to_date)
        index_prices.set_index("timestamp", inplace=True)
        if only_expiry:
            index_prices = index_prices[
                [
                    _date in self.underlying.expiry_dates.date
                    for _date in index_prices.index.date
                ]
            ]
        return index_prices

    def run_day(
        self,
        intraday_prices: pd.DataFrame,
        start_after: tuple[int, int] = (9, 15),
        scan_exit_time: tuple[int, int] = (14, 40),
        starting_exposure: int = 10000000,
        max_multiple_of_exposure: float = 2,
        trade_deltas_between: tuple[float, float] = (0.35, 0.65),
        delta_threshold_pct: float = 0.02,
    ) -> pd.DataFrame:
        intraday_prices = intraday_prices[
            (intraday_prices.index.time > time(*start_after))
        ].copy()

        # Determine the starting quantity
        starting_qty = int(starting_exposure / intraday_prices.iloc[0]["open"])
        exit_delta_disparity = (
            trade_deltas_between[1] / trade_deltas_between[0]
        ) * 1.05  # Hard coded 5% buffer

        if intraday_prices.index[-1].time() < time(*scan_exit_time):
            logger.info(
                f"{self.underlying.name} delta backtest: "
                f"Skipping {intraday_prices.index[-1].date} as the last timestamp is before scan exit time"
            )
            return pd.DataFrame()
        logger.info(
            f"{self.underlying.name} delta backtest: Running backtest for day {intraday_prices.index[0].date()}"
        )
        expiry = self.determine_expiry(intraday_prices.iloc[0])
        if self.expiry is None or self.expiry != expiry:
            self.reset_state()
            self.expiry = expiry
            self.fetch_and_store_option_prices(
                intraday_prices.iloc[0], 10
            )  # Fetching 10 strikes each side

        # Adding helper columns to the intraday prices
        intraday_prices["expiry"] = self.expiry.strftime("%d%b%y").upper()
        intraday_prices["time_to_expiry"] = (
            self.expiry - intraday_prices.index
        ).total_seconds() / (60 * 60 * 24 * 365)
        self.store_atm_info(intraday_prices)
        moving_interest_rates = self.calculate_moving_interest_rate()
        self.add_greeks_to_rolling_atm_info()
        intraday_prices = intraday_prices.merge(
            moving_interest_rates, on="timestamp", how="left"
        )
        intraday_prices = intraday_prices.astype({"r": "float64"})
        intraday_prices.set_index("timestamp", inplace=True)

        current_segment = intraday_prices.copy()
        segment_results = []
        while not current_segment.empty and current_segment.index[0].time() < time(
            *scan_exit_time
        ):
            logger.info(
                f"{self.underlying.name} delta backtest: Running backtest for segment {current_segment.index[0]}"
            )
            # Strikes/prices/greeks are added here
            current_segment = self.prepare_segment_for_processing(
                current_segment, trade_deltas_between
            )
            logger.info(
                f"{self.underlying.name} delta backtest: Prepared segment for {current_segment.index[0]}"
            )
            # The main processing function
            segment_result = process_segment(
                current_segment,
                starting_qty=starting_qty,
                max_multiple_of_exposure=max_multiple_of_exposure,
                exit_delta_disparity=exit_delta_disparity,
                delta_threshold_pct=delta_threshold_pct,
            )

            logger.info(
                f"{self.underlying.name} delta backtest: Processed segment for {current_segment.index[0]}"
            )
            segment_result = self.process_result(current_segment, segment_result)
            logger.info(
                f"{self.underlying.name} delta backtest: Processed result for {current_segment.index[0]}"
            )
            segment_results.append(segment_result)
            current_segment = intraday_prices[
                intraday_prices.index >= segment_result.index[-1]
            ].copy()
        return pd.concat(segment_results)

    def make_result_folder(self, folder_name: str = None):
        # Deciding the folder to store the results in
        directory = os.path.join(DeltaBackTest.RESULTS_FOLDER, self.underlying.name)
        if folder_name is None:
            if os.path.exists(directory):
                folder_number = len(os.listdir(directory)) + 1
            else:
                folder_number = 1
            folder_name = f"backtest_{folder_number}\\"
        else:
            folder_name = f"{folder_name}\\"
        directory = os.path.join(directory, folder_name)
        make_directory_if_needed(directory)
        return directory

    def run_backtest_subset(
        self,
        underlying: UnderlyingInfo,
        index_prices: pd.DataFrame,
        date_subset: list[datetime],
        result_folder: str,
        *args,
        **kwargs,
    ) -> None:
        """
        Runs the backtest for a subset of dates.
        """

        self.underlying = underlying
        self.expiry = None
        self._option_prices = pd.DataFrame()
        self.unique_strikes = []

        logger.info(f"Running backtest for {date_subset}")

        for date in date_subset:
            try:
                # Filter prices for the specific date
                prices = index_prices[index_prices.index.date == date]
                result = self.run_day(prices, *args, **kwargs)
                if not result.empty:
                    backtest_date = result.index[0].date()
                    filename = os.path.join(result_folder, f"{backtest_date}.csv")
                    result.to_csv(filename)
            except Exception as e:
                logger.error(f"Error while running backtest for {date}: {e}")

    def run_backtest_in_parallel(
        self,
        from_date: str | datetime,
        to_date: str | datetime = None,
        only_expiry: bool = False,
        folder_name: str = None,
        n_jobs: int = 5,
        *args,
        **kwargs,
    ):
        """
        Runs the backtest in parallel by splitting the index prices based on unique dates.
        """
        index_prices = self.fetch_and_prepare_index_prices(
            from_date, to_date, only_expiry
        )
        result_folder = self.make_result_folder(folder_name)

        # Split the unique dates into chunks for parallel processing
        split_dates = np.array_split(np.unique(index_prices.index.date), 5)

        underlying = self.underlying

        # Prepare tasks for parallel execution
        tasks = [
            (
                lambda dc=date_chunk: self.run_backtest_subset(
                    underlying,
                    index_prices[pd.DatetimeIndex(index_prices.index.date).isin(dc)],
                    dc.tolist(),
                    result_folder,
                    *args,
                    **kwargs,
                )
            )
            for date_chunk in split_dates
        ]

        logger.info(f"Running backtest for {len(tasks)} chunks")
        # Execute tasks in parallel
        results = execute_in_parallel(tasks, n_jobs=n_jobs)

        return results

    def run_backtest(
        self,
        from_date: str | datetime,
        to_date: str | datetime = None,
        only_expiry: bool = False,
        folder_name: str = None,
        *args,
        **kwargs,
    ):
        index_prices = self.fetch_and_prepare_index_prices(
            from_date, to_date, only_expiry
        )
        result_folder = self.make_result_folder(folder_name)
        for date, prices in index_prices.groupby(index_prices.index.date):
            try:
                result = self.run_day(prices, *args, **kwargs)
                if not result.empty:
                    backtest_date = result.index[0].date()
                    filename = os.path.join(result_folder, f"{backtest_date}.csv")
                    result.to_csv(filename)
            except Exception as e:
                logger.error(f"Error while running backtest for {date}: {e}")
                continue

    def consolidate_backtest(self, folder_name):
        path = os.path.join(
            DeltaBackTest.RESULTS_FOLDER, self.underlying.name, folder_name
        )
        full_df = pd.DataFrame()
        for day in os.listdir(path):
            day_df = pd.read_csv(os.path.join(path, day))
            full_df = pd.concat([full_df, day_df], ignore_index=True)
        full_df.set_index("timestamp", inplace=True)
        full_df.index = pd.to_datetime(full_df.index, dayfirst=True, format="mixed")
        return full_df


def update_positions_and_premium(
    row: pd.Series,
    net_delta: float,
    call_positions: int,
    put_positions: int,
    premium_received: float,
    delta_threshold: float,
) -> tuple[int, int, float]:
    if (
        net_delta > delta_threshold
    ):  # Net delta is positive, sell the required call amount to neutralize
        qty_call_to_sell = int((abs(net_delta) - 0) / row["call_delta"])
        call_positions -= qty_call_to_sell
        premium_received += qty_call_to_sell * row["call_price"]
    elif (
        net_delta < -delta_threshold
    ):  # Net delta is negative, sell another put to neutralize
        qty_put_to_sell = int((abs(net_delta) - 0) / abs(row["put_delta"]))
        put_positions -= qty_put_to_sell
        premium_received += qty_put_to_sell * row["put_price"]

    return call_positions, put_positions, premium_received


def process_segment(
    prepared_segment: pd.DataFrame,
    starting_qty: int,
    max_multiple_of_exposure: float,
    exit_delta_disparity: float,
    delta_threshold_pct: float,
) -> pd.DataFrame:
    entry_data = prepared_segment.iloc[0]
    breach_qty = int(starting_qty * max_multiple_of_exposure)

    call_positions = -starting_qty  # Sell call
    put_positions = -starting_qty  # Sell put
    premium_received = (
        entry_data["call_price"] * starting_qty + entry_data["put_price"] * starting_qty
    )  # Update PnL
    delta_threshold = delta_threshold_pct * starting_qty
    delta_check_interval = entry_data.name + timedelta(minutes=1)

    # Lists to store PnL and net delta for each minute
    premium_received_history = []
    net_delta_history = []
    call_position_history = []
    put_position_history = []
    mtm_history = []

    # Iterate through the data minute by minute
    for i, row in prepared_segment.iterrows():
        net_delta = (
            call_positions * row["call_delta"] + put_positions * row["put_delta"]
        )

        if abs(net_delta) > delta_threshold and i >= delta_check_interval:
            (
                call_positions,
                put_positions,
                premium_received,
            ) = update_positions_and_premium(
                row,
                net_delta,
                call_positions,
                put_positions,
                premium_received,
                delta_threshold,
            )

            # Update the net delta
            net_delta = (
                call_positions * row["call_delta"] + put_positions * row["put_delta"]
            )
            delta_check_interval = i + timedelta(minutes=1)

            # Exit the position if the deltas are too different or if the position is too large
            if (
                max(abs(row["call_delta"]), abs(row["put_delta"]))
                / min(abs(row["call_delta"]), abs(row["put_delta"]))
                > exit_delta_disparity
            ) or (
                np.logical_or(call_positions < -breach_qty, put_positions < -breach_qty)
            ):
                # Make the final appends before breaking
                premium_received_history.append(premium_received)
                net_delta_history.append(net_delta)
                call_position_history.append(call_positions)
                put_position_history.append(put_positions)
                mtm_history.append(
                    call_positions * row["call_price"]
                    + put_positions * row["put_price"]
                )
                break

        # Append histories
        premium_received_history.append(premium_received)
        net_delta_history.append(net_delta)
        call_position_history.append(call_positions)
        put_position_history.append(put_positions)
        mtm_history.append(
            call_positions * row["call_price"] + put_positions * row["put_price"]
        )

    segment_result = pd.DataFrame(
        {
            "call_positions": call_position_history,
            "put_positions": put_position_history,
            "net_delta": net_delta_history,
            "premium": premium_received_history,
            "mtm": mtm_history,
        },
        index=prepared_segment[(prepared_segment.index <= i)].index,
    )

    return segment_result


def summarize_results(df: pd.DataFrame) -> pd.DataFrame:
    # Identify duplicate timestamps, which signify exit points
    duplicate_times = df[df.index.duplicated(keep="last")]

    # Finding the last row of each day
    final_exits = df.loc[
        df.groupby(df.index.date).apply(lambda x: x.iloc[-1].name).tolist()
    ]

    exit_times = pd.concat([duplicate_times, final_exits])

    # For each duplicate date, sum the 'premium' and 'mtm' to calculate profit
    exit_times["profit"] = exit_times["premium"] + exit_times["mtm"]

    return exit_times.sort_index()


def extreme_summary(summary: pd.DataFrame) -> pd.DataFrame:
    summary = summary.copy()
    exposure_in_shares = abs(
        np.minimum(summary.call_positions, summary.put_positions).median()
    )  # Taking the median of the higher of the two positions.
    # Median to avoid outliers from depressing the percentage return.
    summary["exposure"] = exposure_in_shares * summary.open
    summary["profit_percentage"] = (summary.profit / summary.exposure) * 100
    return summary.groupby(summary.index.date).profit_percentage.sum()
