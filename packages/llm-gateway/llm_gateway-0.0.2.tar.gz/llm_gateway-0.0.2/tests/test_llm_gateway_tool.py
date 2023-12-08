import pytest
import unittest

from promptflow.connections import CustomConnection
from llm_gateway.tools.llm_gateway_tool import llm_gateway


@pytest.fixture
def my_custom_connection() -> CustomConnection:
    my_custom_connection = CustomConnection(
        {
            "api-key" : "my-api-key",
            "api-secret" : "my-api-secret",
            "api-url" : "my-api-url"
        }
    )
    return my_custom_connection


class TestTool:
    def test_llm_gateway(self, my_custom_connection):
        result = llm_gateway(my_custom_connection, input_text="Microsoft")
        assert result == "Hello Microsoft"


# Run the unit tests
if __name__ == "__main__":
    unittest.main()