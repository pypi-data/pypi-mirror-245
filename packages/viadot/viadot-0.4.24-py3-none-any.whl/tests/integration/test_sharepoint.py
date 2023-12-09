import os
import re
from copy import deepcopy

import pandas as pd
import pytest
from prefect.tasks.secrets import PrefectSecret

from viadot.config import local_config
from viadot.exceptions import CredentialError
from viadot.sources import Sharepoint, SharepointList
from viadot.task_utils import df_get_data_types_task
from viadot.tasks.sharepoint import SharepointToDF


def get_url() -> str:
    """
    Function to get file URL.

    Returns:
        str: File URL.
    """
    return local_config["SHAREPOINT"].get("file_url")


@pytest.fixture(scope="session")
def sharepoint():
    """
    Fixture for creating a Sharepoint class instance.
    The class instance can be used within a test functions to interact with Sharepoint.
    """
    s = Sharepoint()
    yield s


@pytest.fixture(scope="session")
def file_name(sharepoint):
    """
    A function built to get the path to a file.

    Args:
        sharepoint (Sharepoint): Sharepoint class instance.
    """
    path = "Questionnaires.xlsx"
    sharepoint.download_file(download_to_path=path, download_from_path=get_url())
    yield path
    os.remove(path)


def test_credentials_not_found():
    """
    Testing if a VauleError is thrown when none of credentials are given.

    Args:
        sharepoint (Sharepoint): Sharepoint class instance.
    """
    none_credentials = None
    with pytest.raises(CredentialError, match=r"Credentials not found."):
        Sharepoint(credentials=none_credentials)


def test_get_connection_credentials():
    """
    Testing if a CredentialError is thrown when credentials doesn't contain required keys.

    Args:
        sharepoint (Sharepoint): Sharepoint class instance.
    """
    credentials = {"site": "tenant.sharepoint.com", "username": "User"}
    s = Sharepoint(credentials=credentials)
    with pytest.raises(CredentialError, match="Missing credentials."):
        s.get_connection()


def test_connection(sharepoint):
    """
    Testing if connection is succesfull with given credentials.

    Args:
        sharepoint (Sharepoint): Sharepoint class instance.
    """
    credentials = local_config.get("SHAREPOINT")
    site = f'https://{credentials["site"]}'
    conn = sharepoint.get_connection()
    response = conn.get(site)
    assert response.status_code == 200


def test_sharepoint_to_df_task():
    """Testing if result of `SharepointToDF` is a Data Frame."""
    task = SharepointToDF()
    credentials_secret = PrefectSecret("SHAREPOINT_KV").run()
    res = task.run(
        credentials_secret=credentials_secret,
        sheet_number=0,
        path_to_file="Questionnaires.xlsx",
        url_to_file=get_url(),
    )
    assert isinstance(res, pd.DataFrame)
    os.remove("Questionnaires.xlsx")


def test_download_file_missing_patameters(sharepoint):
    """
    Testing if a VauleError is thrown when none of the parameters are given.

    Args:
        sharepoint (Sharepoint): Sharepoint class instance.
    """
    with pytest.raises(ValueError, match=r"Missing required parameter"):
        sharepoint.download_file(download_to_path=None, download_from_path=None)


def test_file_download(file_name):
    """
    Testing if file is downloaded.

    Args:
        file_name (str): File name.
    """
    files = []
    for file in os.listdir():
        if os.path.isfile(os.path.join(file)):
            files.append(file)
    assert file_name in files


def test_autopopulating_download_from(file_name):
    """
    Testing if file name is correct.

    Args:
        file_name (str): File name.
    """
    assert os.path.basename(get_url()) == file_name


def test_file_extension():
    """Testing if file has correct extension."""
    file_ext = (".xlsm", ".xlsx")
    assert get_url().endswith(file_ext)


def test_file_to_df(file_name):
    """
    Testing if downloaded file contains data and if first sheet can be build as a Data frame.

    Args:
        file_name (str): File name.
    """
    df = pd.read_excel(file_name, sheet_name=0)
    df_test = pd.DataFrame(data={"col1": [1, 2]})
    assert type(df) == type(df_test)


def test_get_data_types(file_name):
    """
    Testing if downloaded file contains data and columns have `String` type.

    Args:
        file_name (str): File name.
    """
    df = pd.read_excel(file_name, sheet_name=0)
    dtypes_map = df_get_data_types_task.run(df)
    dtypes = dtypes_map.values()

    assert "String" in dtypes


### SECTION FOR TESTING SHAREPOINT LIST CONNECTOR ###
@pytest.fixture(scope="session")
def sharepoint_list():
    """
    Fixture for creating a SharepointList class instance.
    The class instance can be used within a test functions to interact with Sharepoint.
    """
    spl = SharepointList()
    yield spl


def test_valid_filters(sharepoint_list):
    filters = {
        "filter1": {"dtype": "int", "operator1": "<", "value1": 10},
        "filter2": {"dtype": "str", "operator1": "==", "value1": "value"},
    }
    result = sharepoint_list.check_filters(filters)
    assert result is True


def test_filters_missing_dtype(sharepoint_list):
    filters = {
        "filter1": {"operator1": ">", "value1": 10},
    }
    with pytest.raises(
        ValueError,
        match=re.escape("dtype for filter1 is missing!"),
    ):
        sharepoint_list.check_filters(filters)


def test_filters_invalid_dtype(sharepoint_list):
    filters = {
        "filter1": {"dtype": "list", "operator1": ">", "value1": 10},
    }
    with pytest.raises(
        ValueError,
        match=re.escape(
            "dtype not allowed! Expected: ['datetime', 'date', 'bool', 'int', 'float', 'complex', 'str'] got: list ."
        ),
    ):
        sharepoint_list.check_filters(filters)


def test_filters_missing_operator1(sharepoint_list):
    filters = {
        "filter1": {"dtype": "int", "value1": 10},
    }
    with pytest.raises(ValueError, match="Operator1 is missing!"):
        sharepoint_list.check_filters(filters)


def test_filters_invalid_operator1(sharepoint_list):
    filters = {
        "filter1": {"dtype": "int", "operator1": "*", "value1": 10},
    }
    with pytest.raises(
        ValueError,
        match=re.escape(
            "Operator1 type not allowed! Expected: ['<', '>', '<=', '>=', '==', '!='] got: * ."
        ),
    ):
        sharepoint_list.check_filters(filters)


def test_filters_missing_value1(sharepoint_list):
    filters = {
        "filter1": {"dtype": "int", "operator1": ">", "value1": None},
    }
    with pytest.raises(ValueError, match="Value1 for operator1 is missing!"):
        sharepoint_list.check_filters(filters)


def test_filters_missing_operators_conjunction(sharepoint_list):
    filters = {
        "filter1": {
            "dtype": "int",
            "operator1": ">",
            "value1": 10,
            "operator2": "<",
            "value2": 20,
        },
    }
    with pytest.raises(
        ValueError,
        match=re.escape(
            "Operator for conjunction is missing! Expected: ['&', '|'] got empty."
        ),
    ):
        sharepoint_list.check_filters(filters)


def test_filters_invalid_operators_conjunction(sharepoint_list):
    filters = {
        "filter1": {
            "dtype": "int",
            "operator1": ">",
            "value1": 10,
            "operator2": "<",
            "value2": 20,
            "operators_conjunction": "!",
        },
    }
    with pytest.raises(
        ValueError,
        match=re.escape(
            "Operator for conjunction not allowed! Expected: ['&', '|'] got ! ."
        ),
    ):
        sharepoint_list.check_filters(filters)


def test_filters_conjunction_not_allowed(sharepoint_list):
    filters = {
        "filter1": {
            "dtype": "int",
            "operator1": ">",
            "value1": 10,
            "filters_conjunction": "!",
        },
    }
    with pytest.raises(
        ValueError,
        match=re.escape(
            "Filters conjunction allowed only when more then one filter provided!"
        ),
    ):
        sharepoint_list.check_filters(filters)


def test_filters_invalid_conjunction(sharepoint_list):
    filters = {
        "filter1": {
            "dtype": "int",
            "value1": 10,
            "operator1": ">",
            "filters_conjunction": "!",
        },
        "filter2": {
            "dtype": "int",
            "operator1": "==",
        },
    }
    with pytest.raises(
        ValueError,
        match=re.escape(
            "Filter operator for conjunction not allowed! Expected: ['&', '|'] got ! ."
        ),
    ):
        sharepoint_list.check_filters(filters)


def test_valid_mapping(sharepoint_list):
    filters = {
        "filter1": {
            "dtype": "int",
            "value1": 10,
            "value2": 20,
            "operator1": ">",
            "operator2": "<=",
            "operators_conjunction": "&",
            "filters_conjunction": "|",
        },
        "filter2": {
            "dtype": "int",
            "value1": 30,
            "value2": 0,
            "operator1": "==",
            "operator2": "!=",
            "operators_conjunction": "|",
        },
    }
    expected_result = {
        "filter1": {
            "dtype": "int",
            "value1": 10,
            "value2": 20,
            "operator1": "gt",
            "operator2": "le",
            "operators_conjunction": "and",
            "filters_conjunction": "or",
        },
        "filter2": {
            "dtype": "int",
            "value1": 30,
            "value2": 0,
            "operator1": "eq",
            "operator2": "ne",
            "operators_conjunction": "or",
        },
    }
    result = sharepoint_list.operators_mapping(filters)
    assert result == expected_result


def test_operators_mapping_invalid_comparison_operator(sharepoint_list):
    filters = {
        "filter1": {
            "operator1": "*",
            "operator2": "<=",
            "operators_conjunction": "&",
            "filters_conjunction": "|",
        },
    }
    error_message = "This comparison operator: * is not allowed. Please read the function documentation for details!"
    with pytest.raises(ValueError, match=re.escape(error_message)):
        sharepoint_list.operators_mapping(filters)


def test_operators_mapping_invalid_logical_operator(sharepoint_list):
    filters = {
        "filter1": {
            "operator1": ">",
            "operator2": "<=",
            "operators_conjunction": "!",
            "filters_conjunction": "|",
        },
    }
    error_message = "This conjunction (logical) operator: ! is not allowed. Please read the function documentation for details!"
    with pytest.raises(ValueError, match=re.escape(error_message)):
        sharepoint_list.operators_mapping(filters)


def test_operators_mapping_invalid_filters_logical_operator(sharepoint_list):
    filters = {
        "filter1": {
            "operator1": ">",
            "operator2": "<=",
            "operators_conjunction": "&",
            "filters_conjunction": "!",
        },
    }
    error_message = "This filters conjunction (logical) operator: ! is not allowed. Please read the function documentation for details!"
    with pytest.raises(ValueError, match=re.escape(error_message)):
        sharepoint_list.operators_mapping(filters)


def test_single_filter_datetime_api(sharepoint_list):
    filters = {
        "date_column": {"dtype": "datetime", "operator1": ">", "value1": "2023-01-01"}
    }
    result = sharepoint_list.make_filter_for_api(filters)
    expected_result = "date_column gt datetime'2023-01-01T00:00:00' "
    assert result == expected_result


def test_multiple_filters_api(sharepoint_list):
    filters = {
        "int_column": {
            "dtype": "int",
            "operator1": ">=",
            "value1": 10,
            "operator2": "<",
            "value2": 20,
        },
        "str_column": {"dtype": "str", "operator1": "==", "value1": "example"},
    }
    result = sharepoint_list.make_filter_for_api(filters)
    expected_result = "int_column ge '10'int_column lt '20'str_column eq 'example'"
    assert result == expected_result


def test_single_df_filter(sharepoint_list):
    filters = {"column1": {"operator1": ">", "value1": 10}}
    result = sharepoint_list.make_filter_for_df(filters)
    expected_result = "df.loc[(df.column1 > '10')]"
    assert result == expected_result


def test_multiple_df_filters(sharepoint_list):
    filters = {
        "column1": {"operator1": ">", "value1": 10, "filters_conjunction": "&"},
        "column2": {"operator1": "<", "value1": 20},
    }
    result = sharepoint_list.make_filter_for_df(filters)
    expected_result = "df.loc[(df.column1 > '10')&(df.column2 < '20')]"
    assert result == expected_result
