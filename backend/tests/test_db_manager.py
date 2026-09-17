# test url
import requests
from datetime import datetime, timedelta, timezone
from pydantic_settings import BaseSettings, SettingsConfigDict

# test enviroment configuration
class TestSettings(BaseSettings):
    __test__ = False
    
    NEON_API_KEY: str
    NEON_USER: str
    NEON_PASSWORD: str
    NEON_DB_NAME: str
    NEON_PROJECT_ID: str
    NEON_PARENT_BRANCH_ID: str

    model_config = SettingsConfigDict(
        env_file=".env.test",
        env_file_encoding="utf-8",
        extra="ignore"
    )

test_settings = TestSettings()

# enviroment manager for test database
class TestDatabaseManager:
    __test__ = False
    
    def __init__(self, test_settings: TestSettings):
        self.test_settings = test_settings
        self.base_url = f"https://console.neon.tech/api/v2/projects/{test_settings.NEON_PROJECT_ID}/branches"
        self.headers = {
            "Authorization": f"Bearer {test_settings.NEON_API_KEY}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        self.branch_id = None
        self.endpoint_host = None
    
    def _get_payload(self, expires_at: str) -> dict:
        return {
            "branch": {
                "name": f"pytest-run-{int(datetime.now().timestamp())}",
                "parent_id": self.test_settings.NEON_PARENT_BRANCH_ID,
                "init_source": "schema-only", # Traz apenas a estrutura (tabelas, views, etc)
                "expires_at": expires_at
            },
            "endpoints": [{"type": "read_write"}]
        }   
    
    def provide_test_branch(self) -> str:
        expires_at = (datetime.now(timezone.utc) + timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:%SZ')
        payload = self._get_payload(expires_at)
        
        response = requests.post(self.base_url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        self.branch_id = data["branch"]["id"]
        
        # Get the endpoint host for the new branch
        self.endpoint_host = data["endpoints"][0]["host"]
        
        return (
            f"postgresql+psycopg://{self.test_settings.NEON_USER}:{self.test_settings.NEON_PASSWORD}"
            f"@{self.endpoint_host}/{self.test_settings.NEON_DB_NAME}?sslmode=require"
        )
        
    def teardown_test_branch(self):
        if self.branch_id:
            delete_url = f"{self.base_url}/{self.branch_id}"
            response = requests.delete(delete_url, headers=self.headers)
            response.raise_for_status()