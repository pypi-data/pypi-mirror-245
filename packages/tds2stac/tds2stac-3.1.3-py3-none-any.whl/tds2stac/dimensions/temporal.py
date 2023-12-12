import sys
from datetime import datetime

# SPDX-FileCopyrightText: 2023 Karlsruher Institut für Technologie
#
# SPDX-License-Identifier: CC0-1.0
import pytz


class Temporal(object):
    def regulator(self, main_dict, temporal_format_by_dataname, data_name):
        errors = []
        warnings = []
        if (
            main_dict["temporal_extent_start_datetime"] is not None
            and temporal_format_by_dataname is None
        ):
            main_dict["temporal_extent_start_datetime"] = main_dict[
                "temporal_extent_start_datetime"
            ]
        elif (
            main_dict["temporal_extent_start_datetime"] is None
            or main_dict["temporal_extent_start_datetime"] is not None
        ) and temporal_format_by_dataname is not None:
            # print("data_name", data_name)
            # print(
            #     "temporal_format_by_dataname",
            #     datetime.strptime(
            #         str(data_name),
            #         temporal_format_by_dataname,
            #     )
            #     .strftime("%Y-%m-%dT%H:%M:%SZ")
            #     .lstrip("0"),
            # )
            try:
                main_dict["temporal_extent_start_datetime"] = (
                    datetime.strptime(
                        str(data_name),
                        temporal_format_by_dataname,
                    ).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                    # .lstrip("0")
                    # .replace(" 0", " ")
                )
            except Exception:
                if main_dict["temporal_extent_start_datetime"] is not None:
                    main_dict["temporal_extent_start_datetime"] = main_dict[
                        "temporal_extent_start_datetime"
                    ]
                ex_type, ex_value, ex_traceback = sys.exc_info()
                if ex_type is not None and ex_value is not None:
                    warnings.append(
                        "There is a problem with `temporal_format_by_dataname`. Revise your input `temporal_format_by_dataname`. %s : %s"
                        % (
                            ex_type.__name__,
                            ex_value,
                        )
                    )
                else:
                    warnings.append(
                        "There is a problem with `temporal_format_by_dataname`. Revise your input `temporal_format_by_dataname`."
                    )
        elif (
            main_dict["temporal_extent_start_datetime"] is None
            and temporal_format_by_dataname is None
        ):
            errors.append(
                "Start DateTime is None in the given dataset. Please review your `tag_config.json` file or use `temporal_format_by_dataname` attr to the date of your data will be read from file names."
            )
        if (
            main_dict["temporal_extent_end_datetime"] is not None
            and temporal_format_by_dataname is None
        ):
            main_dict["temporal_extent_end_datetime"] = main_dict[
                "temporal_extent_end_datetime"
            ]
        elif (
            main_dict["temporal_extent_end_datetime"] is None
            or main_dict["temporal_extent_end_datetime"] is not None
        ) and temporal_format_by_dataname is not None:
            try:
                main_dict["temporal_extent_end_datetime"] = (
                    datetime.strptime(
                        str(data_name),
                        temporal_format_by_dataname,
                    ).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                    # .lstrip("0")
                    # .replace(" 0", " ")
                )
            except Exception:
                if main_dict["temporal_extent_end_datetime"] is not None:
                    main_dict["temporal_extent_end_datetime"] = main_dict[
                        "temporal_extent_end_datetime"
                    ]
                ex_type, ex_value, ex_traceback = sys.exc_info()
                if ex_type is not None and ex_value is not None:
                    warnings.append(
                        "There is a problem with `temporal_format_by_dataname`. Revise your input `temporal_format_by_dataname`. %s : %s"
                        % (
                            ex_type.__name__,
                            ex_value,
                        )
                    )
                else:
                    warnings.append(
                        "There is a problem with `temporal_format_by_dataname`. Revise your input `temporal_format_by_dataname`."
                    )
        elif (
            main_dict["temporal_extent_end_datetime"] is None
            and temporal_format_by_dataname is None
        ):
            errors.append(
                "End DateTime is None in the given dataset. Please review your `tag_config.json` file or use `temporal_format_by_dataname` attr to the date of your data will be read from file names."
            )

        try:
            main_dict["collection_interval_time"].append(
                datetime.strptime(
                    main_dict["temporal_extent_start_datetime"],
                    "%Y-%m-%dT%H:%M:%S.%fZ",
                ).replace(tzinfo=pytz.utc)
            )
            main_dict["collection_interval_time"].append(
                datetime.strptime(
                    main_dict["temporal_extent_end_datetime"],
                    "%Y-%m-%dT%H:%M:%S.%fZ",
                ).replace(tzinfo=pytz.utc)
            )
        except ValueError:
            main_dict["collection_interval_time"].append(
                datetime.strptime(
                    main_dict["temporal_extent_start_datetime"],
                    "%Y-%m-%dT%H:%M:%SZ",
                ).replace(tzinfo=pytz.utc)
            )
            main_dict["collection_interval_time"].append(
                datetime.strptime(
                    main_dict["temporal_extent_end_datetime"],
                    "%Y-%m-%dT%H:%M:%SZ",
                ).replace(tzinfo=pytz.utc)
            )

        main_dict["collection_interval_time"] = sorted(
            main_dict["collection_interval_time"]
        )

        if errors != [] and warnings != []:
            return errors, warnings
        elif errors != [] and warnings == []:
            return errors, None
        elif errors == [] and warnings != []:
            return None, warnings
        else:
            return None, None
