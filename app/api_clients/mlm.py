from app.api_clients.client import ApiClient
from app.configs.configs import settings
from app.utils.logs import get_logger

logger = get_logger(__name__)

class MLMApiEndPoints:
    ADD_USER = "/user/register"
    DOWNLINE = "/user/downline/{user_id}"
    TRIGGER_BONUS = "/bonus/"
    USER_BONUS_HISTORY = "/bonus/user/{user_id}"
    ALL_BONUS = "/bonus/"
    MARK_BONUS_PAID = "/bonus/{bonus_id}/mark-paid"
    PAY_ALL_BONUSES = "/bonus/mark-paid/all"
    USER_RANK = "/ranks/evaluate/{user_id}"
    USER_WEEKLY_BONUS_REPORT = "/reports/weekly/{user_id}"


class MLMApiClient:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    @staticmethod
    def prepare() -> "MLMApiClient":
        base_url = settings.MLM_SERVICE_BASE_URL
        api_key = settings.MLM_SERVICE_API_KEY
        api_secret = settings.MLM_SERVICE_API_SECRET

        if not base_url:
            logger.error("Environment variables for MLM API are missing")
            raise EnvironmentError("Required environment variables are not set.")

        headers = {
            "X-Api-Key": api_key,
            "X-Api-Secret": api_secret
        }

        return MLMApiClient(ApiClient(base_url, headers))

    def add_user(self, user_data: dict):
        return self.api_client.post(MLMApiEndPoints.ADD_USER, body=user_data)
    
    def get_downline(self, user_id: str):
        return self.api_client.get(MLMApiEndPoints.DOWNLINE.format(user_id=user_id))
    
    def trigger_bonus(self, body: dict):
        return self.api_client.post(MLMApiEndPoints.TRIGGER_BONUS, body=body)
    
    def get_user_bonus_history(self, user_id: str):
        return self.api_client.get(MLMApiEndPoints.USER_BONUS_HISTORY.format(user_id=user_id))
    
    def get_all_bonus(self):
        return self.api_client.get(MLMApiEndPoints.ALL_BONUS)
    
    def mark_bonus_paid(self, bonus_id: str):
        return self.api_client.patch(MLMApiEndPoints.MARK_BONUS_PAID.format(bonus_id=bonus_id))
    
    def pay_all_bonuses(self):
        return self.api_client.get(MLMApiEndPoints.PAY_ALL_BONUSES)
    
    def get_user_rank(self, user_id: str):
        return self.api_client.post(MLMApiEndPoints.USER_RANK.format(user_id=user_id))
    
    def get_user_weekly_bonus_report(self, user_id: str):
        return self.api_client.get(MLMApiEndPoints.USER_WEEKLY_BONUS_REPORT.format(user_id=user_id))
    