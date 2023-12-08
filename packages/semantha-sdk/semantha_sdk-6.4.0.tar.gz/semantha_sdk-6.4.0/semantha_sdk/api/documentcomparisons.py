from semantha_sdk.rest.rest_client import RestClient, RestEndpoint

class DocumentcomparisonsEndpoint(RestEndpoint):
    """ author semantha, this is a generated class do not change manually! 
    
    """

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/documentcomparisons"

    def __init__(
        self,
        session: RestClient,
        parent_endpoint: str,
    ) -> None:
        super().__init__(session, parent_endpoint)

    
    
    
    
    