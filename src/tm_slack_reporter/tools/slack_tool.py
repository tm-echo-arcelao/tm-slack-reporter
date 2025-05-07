from composio_crewai import ComposioToolSet, Action

slack_toolset = ComposioToolSet()

slack_tools = slack_toolset.get_tools(
    actions=[Action.SLACK_SEARCH_FOR_MESSAGES_WITH_QUERY]
)
