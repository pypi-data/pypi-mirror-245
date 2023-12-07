from typing import Dict, Optional

from orkg.out import OrkgResponse
from orkg.utils import NamespacedClient, dict_to_url_params, query_params


class ResearchProblemsClient(NamespacedClient):
    @query_params("page", "size", "sort", "desc")
    def in_research_field(
        self, research_field_id: str, params: Optional[Dict] = None
    ) -> OrkgResponse:
        """
        Get all problems in a research field
        :param research_field_id: the id of the research field
        :param page: the page number (optional)
        :param size: number of items per page (optional)
        :param sort: key to sort on (optional)
        :param desc: true/false to sort desc (optional)
        :return: OrkgResponse object
        """
        if len(params) > 0:
            self.client.backend._append_slash = False
            response = self.client.backend("research-fields")(
                research_field_id
            ).problems.GET(dict_to_url_params(params))
        else:
            self.client.backend._append_slash = True
            response = self.client.backend("research-fields")(
                research_field_id
            ).problems.GET()
        return self.client.wrap_response(response)
