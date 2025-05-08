from composio_crewai import ComposioToolSet, Action, App

from src.tm_slack_reporter.utils.env import config


class SlackToolSet:
    def __init__(self):
        self.slack_toolset = ComposioToolSet(api_key=config.get("COMPOSIO_API_KEY"))
        self.entity_id = self._init_auth()
        self.actions = [
            Action.SLACK_CONVERSATIONS_HISTORY,
            Action.SLACK_CONVERSATIONS_LIST,
            Action.SLACK_USERS_LIST,
        ]

    def _init_auth(self):
        print("Initializing Slack connection...")

        user_id = config.get("COMPOSIO_SLACK_USER_ID")
        integration_id = config.get("COMPOSIO_SLACK_INTEGRATION_ID")

        entity = self.slack_toolset.get_entity(id=user_id)

        try:
            active_connection = entity.get_connection(App.SLACK)

            if active_connection:
                print(
                    "Slack connection is already active. Proceeding with tool initialization..."
                )
                return active_connection.entityId

            connection_request = self.slack_toolset.initiate_connection(
                integration_id=integration_id,
                entity_id=entity.id,
            )

            if connection_request.redirectUrl:
                print(
                    f"Please visit the following URL to authorize the Slack integration: {connection_request.redirectUrl}"
                )
            else:
                raise Exception(
                    "Error: Expected a redirectUrl for OAuth flow but didn't receive one."
                )

            print("Waiting for Slack connection to be active...")

            active_connection = connection_request.wait_until_active(
                client=self.slack_toolset.client, timeout=300
            )

            print("Slack connection is active. Proceeding with tool initialization...")
            return active_connection.entityId

        except Exception as e:
            raise Exception(f"Error initiating Slack connection: {e}")

    def get_tools(self):
        return self.slack_toolset.get_tools(
            actions=self.actions, entity_id=self.entity_id
        )
