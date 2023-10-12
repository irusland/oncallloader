from prometheus_client import Summary, Counter, Histogram


class MetricsCollector:
    def __init__(self):
        self.search_teams_requests_total = Counter('search_teams_requests_total', 'Total number of teams searches')
        self.search_teams_requests_success = Counter('search_teams_requests_success', 'Number of successful teams searches')
        self.get_team_schedule_requests = Histogram('get_team_schedule_requests', 'Histogram of search events request times')
        self.api_request_statuses = Counter('api_request_statuses', 'Api request statuses', labelnames=('path', 'status'))
