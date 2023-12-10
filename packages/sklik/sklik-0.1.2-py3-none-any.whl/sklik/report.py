from datetime import datetime, timedelta

from sklik.api import SklikApi
from sklik.object import Account
from sklik.util import SKLIK_DATE_FORMAT


def _restriction_filter_validator(
        since: str | None,
        until: str | None,
        restriction_filter: dict | None) -> dict[str, any]:
    since = since if since else (datetime.today() - timedelta(days=29)).strftime(SKLIK_DATE_FORMAT)
    until = until if until else (datetime.today() - timedelta(days=1)).strftime(SKLIK_DATE_FORMAT)

    restriction_filter = restriction_filter or {}
    restriction_filter.setdefault('dateFrom', since)
    restriction_filter.setdefault('dateTo', until)

    return restriction_filter


def _display_option_validator(granularity: str | None) -> dict[str, any]:
    granularity = granularity if granularity else 'daily'
    return {'statGranularity': granularity}


class Report:
    """
    The `Report` class is used to represent a report in the Sklik API.

    Attributes:
        account_id (int): The ID of the Sklik account.
        report_id (str): The ID of the report.
        service (str): The service name.
        fields (list[str]): The list of fields to be included in the report.
        total_count (int, optional): The total number of items in the report. Defaults to 0.
        api (SklikApi | None, optional): The Sklik API instance. Defaults to None.

    Methods:
        __init__(account_id: int, report_id: str, service: str, fields: list[str], total_count: int = 0, api: SklikApi | None = None)
            Constructs a new Report object.

        __repr__()
            Returns a string representation of the Report object.

        __len__()
            Returns the total number of items in the report.

        __iter__()
            Returns an iterator object.

        __next__()
            Returns the next item in the report.

        load_page(offset: int, limit: int) -> list[dict[str, any]]
            Loads a page of items from the Sklik API.

    Examples:
        report = Report(account_id=123, report_id='abc', service='report', fields=['field1', 'field2'])
        print(report)  # Output: Report(account_id=123, report_id=abc, total_count=0)
        print(len(report))  # Output: 0

        for item in report:
            print(item)

        page = report.load_page(0, 100)
        print(page)  # Output: [{'field1': value1, 'field2': value2}, {'field1': value3, 'field2': value4}]
    """
    def __init__(
            self,
            account_id: int,
            report_id: str,
            service: str,
            fields: list[str],
            total_count: int = 0,
            api: SklikApi | None = None):
        self.account_id = account_id
        self.report_id = report_id
        self.fields = fields
        self.service = service

        self._total_count = total_count
        self._api = api or SklikApi.get_default_api()

        self._current_offset = 0
        self._current_limit = 100
        self._current_page = self.load_page(self._current_offset, self._current_limit)
        self._current_index = 0

    def __repr__(self):
        return f"Report(account_id= {self.account_id},report_id={self.report_id}, total_count={self._total_count})"

    def __len__(self):
        return self._total_count

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_index >= len(self._current_page):
            self._current_offset += self._current_limit
            self._current_page = self.load_page(self._current_offset, self._current_limit)
            self._current_index = 0

        if not self._current_page or self._current_index >= len(self._current_page):
            raise StopIteration()

        item = self._current_page[self._current_index]
        self._current_index += 1
        return item

    def load_page(self, offset: int, limit: int) -> list[dict[str, any]]:
        """
        :param offset: The starting index of the page, indicating the position of the first item to be included in the output.
        :param limit: The maximum number of items to be included in the page.
        :return: A list of dictionaries representing the requested page of data.

        """
        args = [
            {'userId': self.account_id},
            self.report_id,
            {'offset': offset, 'limit': limit, 'displayColumns': self.fields}
        ]

        report = self._api.call(self.service, 'readReport', args=args)['report']
        output = [dict(**stat,
                       **{key: value for key, value in item.items() if key != 'stats'})
                  for item in report for stat in item.get('stats', [])]

        return output


def create_report(
        account: Account,
        service: str,
        fields: list[str],
        since: str | None = None,
        until: str | None = None,
        granularity: str | None = None,
        restriction_filter: dict | None = None) -> Report:
    """
    :param account: The account object representing the user account.
    :type account: Account
    :param service: The name of the service for which the report is being created.
    :type service: str
    :param fields: The list of fields to include in the report. (optional)
    :type fields: list
    :param since: The date from which the report data is being fetched. (optional)
    :type since: str | None
    :param until: The date until which the report data is being fetched. (optional)
    :type until: str | None
    :param granularity: The granularity of the report data. (optional)
    :type granularity: str | None
    :param restriction_filter: The filter to apply to the report data. (optional)
    :type restriction_filter: dict | None
    :return: The created Report object.
    :rtype: Report
    """
    args = [
        _restriction_filter_validator(since, until, restriction_filter),
        _display_option_validator(granularity)
    ]

    response = account.call(service, 'createReport', args)
    return Report(account.account_id, response['reportId'], service=service, fields=fields,
                  total_count=response['totalCount'], api=account.api)
