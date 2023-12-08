# data_functions.py
# -*- coding: utf-8 -*-

"""
Functions which serve for data transformation purposes
"""

from typing import (
    Literal,
)

import itertools

from tqdm import tqdm

import pandas as pd


# ______________________________________________________________________________________________________________________


def stack_temporal_dataframe(
        df: pd.DataFrame,
        start_col: str,
        end_col: str,
        freq: str,
        silent: bool = True,
) -> pd.DataFrame:
    """
    Transforms a dataframe along a date range,
    from columns [start_col, end_col] to one column [temporal_range].

    Args:
        df:         Input dataframe. Must be unique in rows!
        start_col:  Name of the start date column
        end_col:    Name of the end date column
        freq:       Interval frequency. Use a pandas DateOffset object from ->
                    https://pandas.pydata.org/docs/user_guide/timeseries.html#dateoffset-objects
        silent:     If False, a tqdm progres bar will be shown

    Returns:
        transformed dataframe with new column 'temporal_range'
    """

    records = []
    iterator = df.to_dict(orient='records')
    iterator = iterator if silent else tqdm(iterator)

    for row in iterator:
        temporal_range = pd.date_range(row[start_col], row[end_col], freq=freq)

        l_tmp = list(
            itertools.product(
                [[el] for el in temporal_range],
                [list(row.values())],
            )
        )

        records.extend(list(map(lambda x: sum(x, []), l_tmp)))

    df_output = pd.DataFrame(records, columns=['temporal_records'] + list(df.columns))
    df_output.drop(columns=[start_col, end_col], inplace=True)
    df_output.reset_index(drop=True, inplace=True)
    # recast to original dtypes from input df
    for col, dtype in df.dtypes.items():
        if col in df_output.columns and col != 'temporal_column' and df_output[col].dtype != dtype:
            df_output[col] = df_output[col].astype(dtype)

    return df_output


# ______________________________________________________________________________________________________________________


def unstack_temporal_dataframe(
        df: pd.DataFrame,
        temporal_column: str,
        group_by: list,
        silent: bool = True,
) -> pd.DataFrame:
    """
    Transforms a dataframe along a date range,
    from one column [temporal_range] to columns [start_col, end_col].

    Args:
        df:                 Input dataframe
        temporal_column:    Name of temporal column
        group_by:           Name of columns for which to group by
        silent:             If False, a tqdm progres bar will be shown

    Returns:
        transformed dataframe with new columns 'valid_from' and 'valid_to'
    """
    if isinstance(group_by, str):
        group_by = [group_by]

    iterator = df.groupby(by=group_by)
    iterator = iterator if silent else tqdm(iterator)

    rows_output = []
    for _, group in iterator:
        temporal_index = group[temporal_column].to_list()
        group.set_index(keys=[temporal_column] + group_by, inplace=True)

        comparison = group.compare(group.shift())

        rows = []

        # special case: no delta in complete group
        if len(comparison) == 1:
            row = {
                'valid_from': temporal_index[0],
                'valid_to': temporal_index[-1],
            }

            for k in group_by:
                row[k] = group.reset_index()[k][0]

            for k in group.columns:
                row[k] = group.reset_index()[k][0]

            rows.append(row)

        else:
            for i, idx in enumerate(comparison.index):
                # special case: first entry
                if i == 0:
                    continue
                else:
                    valid_from = comparison.iloc[i - 1].name[0]
                    valid_to = temporal_index[temporal_index.index(idx[0]) - 1]

                row = {
                    'valid_from': valid_from,
                    'valid_to': valid_to,
                }

                for j, k in enumerate(group_by):
                    row[k] = idx[j + 1]

                for k in group.columns:
                    row[k] = group.shift().loc[idx][k]

                rows.append(row)

            # special case: last entry
            row = {
                'valid_from': idx[0],
                'valid_to': group.index[-1][0],
            }

            for j, k in enumerate(group_by):
                row[k] = idx[j + 1]

            for k in group.columns:
                row[k] = group.loc[idx][k]

            rows.append(row)

        rows_output.extend(rows)

    df_output = pd.DataFrame.from_records(rows_output)
    df_output.reset_index(drop=True, inplace=True)
    # recast to original dtypes from input df
    for col, dtype in df.dtypes.items():
        if col in df_output.columns and col != temporal_column and df_output[col].dtype != dtype:
            df_output[col] = df_output[col].astype(dtype)

    return df_output


# ______________________________________________________________________________________________________________________


def transform_long_wide(
        df: pd.DataFrame,
        direction: Literal['long_to_wide', 'wide_to_long'],
        index_columns: list,
        wtl_columns: list | None,
        measure_names: str | list,
        measure_values: str | list,
) -> pd.DataFrame:
    """
    Transforms a dataframe according to direction long_to_wide or wide_to_long using pivot and melt under the hood.

    Args:
        df:             dataframe
        direction:      whether to go from long to wide (pivot) or from wide to long (melt)
        index_columns:  list of columns to group by
        wtl_columns:    wtl only -> list of columns to use as values to melt from wide to long format
        measure_names:  ltw -> name(s) of column(s) to pivot ;
                        wtl -> name to use for the variable column
        measure_values: ltw -> name(s) of column(s) with values to populate the pivot columns ;
                        wtl -> name to use for the value column

    Returns:
        transformed dataframe
    """
    if direction == 'long_to_wide':
        df_output = pd.pivot(
            df,
            columns=measure_names,
            values=measure_values,
            index=index_columns,
        ).reset_index()
    elif direction == 'wide_to_long':
        df_output = pd.melt(
            df,
            id_vars=index_columns,
            value_vars=wtl_columns,
            var_name=measure_names,
            value_name=measure_values,
            ignore_index=True,
        )
    else:
        raise ValueError(f'direction should be "long_to_wide" or "wide_to_long", you specified {direction}!')

    return df_output


# ______________________________________________________________________________________________________________________
