from ..plugins.web_crawler import RemaxExecutor


class Extract:
    @staticmethod
    def get_listing_data(pages: list, multithreaded: bool) -> list:
        return RemaxExecutor(multithreaded=multithreaded).get_multipage_listing(pages=pages, output=False)

    @staticmethod
    def get_workload() -> int:
        return RemaxExecutor().get_workload(m=3, distribution_type="bin", n=10)
