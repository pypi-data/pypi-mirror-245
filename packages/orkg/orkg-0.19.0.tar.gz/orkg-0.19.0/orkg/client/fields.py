from typing import Dict, Optional

from orkg.out import OrkgResponse
from orkg.utils import NamespacedClient, dict_to_url_params, query_params


class ResearchFieldsClient(NamespacedClient):
    @query_params("page", "size", "sort", "desc")
    def with_benchmarks(self, params: Optional[Dict] = None) -> OrkgResponse:
        """
        Get all the research fields with benchmarks
        :param page: the page number (optional)
        :param size: number of items per page (optional)
        :param sort: key to sort on (optional)
        :param desc: true/false to sort desc (optional)
        :return: OrkgResponse object
        """
        if len(params) > 0:
            self.client.backend._append_slash = False
            response = self.client.backend("research-fields").benchmarks.GET(
                dict_to_url_params(params)
            )
        else:
            self.client.backend._append_slash = True
            response = self.client.backend("research-fields").benchmarks.GET()
        return self.client.wrap_response(response)
