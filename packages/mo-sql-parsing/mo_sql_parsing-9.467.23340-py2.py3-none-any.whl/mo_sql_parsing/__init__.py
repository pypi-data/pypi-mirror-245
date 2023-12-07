# encoding: utf-8
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Contact: Kyle Lahnakoski (kyle@lahnakoski.com)
#


import json
from threading import Lock

from mo_parsing import debug

from mo_sql_parsing.sql_parser import scrub
from mo_sql_parsing.utils import ansi_string, simple_op, normal_op, n_string

parse_locker = Lock()  # ENSURE ONLY ONE PARSING AT A TIME
common_parser = None
mysql_parser = None
sqlserver_parser = None
bigquery_parser = None

SQL_NULL = {"null": {}}


def parse(sql, null=SQL_NULL, calls=simple_op):
    """
    :param sql: String of SQL
    :param null: What value to use as NULL (default is the null function `{"null":{}}`)
    :param calls: What to do with function calls (default is the simple_op function `{"op":{}}`)
    :return: parse tree
    """
    global common_parser

    with parse_locker:
        if not common_parser:
            common_parser = sql_parser.common_parser()
        result = _parse(common_parser, sql, null, calls)
        return result


def parse_mysql(sql, null=SQL_NULL, calls=simple_op):
    """
    PARSE MySQL ASSUME DOUBLE QUOTED STRINGS ARE LITERALS
    :param sql: String of SQL
    :param null: What value to use as NULL (default is the null function `{"null":{}}`)
    :return: parse tree
    """
    global mysql_parser

    with parse_locker:
        if not mysql_parser:
            mysql_parser = sql_parser.mysql_parser()
        return _parse(mysql_parser, sql, null, calls)


def parse_sqlserver(sql, null=SQL_NULL, calls=simple_op):
    """
    PARSE MySQL ASSUME DOUBLE QUOTED STRINGS ARE LITERALS
    :param sql: String of SQL
    :param null: What value to use as NULL (default is the null function `{"null":{}}`)
    :return: parse tree
    """
    global sqlserver_parser

    with parse_locker:
        if not sqlserver_parser:
            sqlserver_parser = sql_parser.sqlserver_parser()
        return _parse(sqlserver_parser, sql, null, calls)


def parse_bigquery(sql, null=SQL_NULL, calls=simple_op):
    """
    PARSE BigQuery ASSUME DOUBLE QUOTED STRINGS ARE LITERALS
    :param sql: String of SQL
    :param null: What value to use as NULL (default is the null function `{"null":{}}`)
    :return: parse tree
    """
    global bigquery_parser

    with parse_locker:
        if not bigquery_parser:
            bigquery_parser = sql_parser.bigquery_parser()
        return _parse(bigquery_parser, sql, null, calls)


def _parse(parser, sql, null, calls):
    utils.null_locations = []
    utils.scrub_op = calls
    sql = sql.rstrip().rstrip(";")
    parse_result = parser.parse_string(sql, parse_all=True)
    output = scrub(parse_result)
    for o, n in utils.null_locations:
        o[n] = null
    return output


def format(json, ansi_quotes=True, should_quote=None):
    """
    :param json:  Parsed SQL as json
    :param ansi_quotes: True if identifiers can be put in double quotes
    :param should_quote: Function that returns True if a string should be quoted (because contains spaces, etc)
    :return: SQL string
    """
    from mo_sql_parsing.formatting import Formatter

    return Formatter(ansi_quotes, should_quote).dispatch(json)


_ = json.dumps

__all__ = ["parse", "format", "parse_mysql", "parse_bigquery", "normal_op", "simple_op"]
