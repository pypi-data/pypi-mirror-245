from .module_imports import *


@headers({"Ocp-Apim-Subscription-Key": key})
class _TCO(Consumer):
    """Inteface to TCO resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._base_url
        super().__init__(base_url=Resource._base_url, *args, **kw)

    def maintenance(self):
        return self._Maintenance(self)

    @headers({"Ocp-Apim-Subscription-Key": key})
    class _Maintenance(Consumer):
        """Inteface to TCO resource for the RockyRoad API."""

        def __init__(self, Resource, *args, **kw):
            self._base_url = Resource._base_url
            super().__init__(base_url=Resource._base_url, *args, **kw)

        def parts(self):
            return self._Parts(self)

        @headers({"Ocp-Apim-Subscription-Key": key})
        class _Parts(Consumer):
            """Inteface to TCO resource for the RockyRoad API."""

            def __init__(self, Resource, *args, **kw):
                self._base_url = Resource._base_url
                super().__init__(base_url=Resource._base_url, *args, **kw)

            def parts(self):
                return self.TCO(self)

            @returns.json
            @http_get("calculators/tco/maintenance/parts")
            def list(
                self,
            ):
                """This call will return list of TCO Parts."""

            @returns.json
            @http_get("calculators/tco/maintenance/parts/{uid}")
            def get(self, uid: str):
                """This call will return list of TCO Parts."""

            @delete("calculators/tco/maintenance/parts/{uid}")
            def delete(self, uid: str):
                """This call will the TCO Part."""

            @returns.json
            @json
            @post("calculators/tco/maintenance/parts")
            def insert(self, tco_part: Body):
                """This call will create the TCO Part."""

            @json
            @patch("calculators/tco/maintenance/parts/{uid}")
            def update(self, uid: str, tco_part: Body):
                """This call will update the TCO Part."""
