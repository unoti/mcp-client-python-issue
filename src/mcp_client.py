import asyncio
import sys

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# From https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#writing-mcp-clients


# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command=sys.executable, # Leverage the parent python environment so the child also uses python 3.10 with the same libraries.
    args=["mcp_echo_server.py"],  # Optional command line arguments
    env=None,  # Optional environment variables
)

# Removed the optional sampling callback for simplicity.

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            print("Initializing session...") # This is the last thing we will see.
            await session.initialize()
            print("Session initialized successfully.") # If it's broken we won't see this.

            # List available prompts
            prompts = await session.list_prompts()

            # Get a prompt
            prompt = await session.get_prompt(
                "example-prompt", arguments={"arg1": "value"}
            )

            # List available resources
            resources = await session.list_resources()

            # List available tools
            tools = await session.list_tools()

            # Read a resource
            content, mime_type = await session.read_resource("file://some/path")

            # Call a tool
            result = await session.call_tool("tool-name", arguments={"arg1": "value"})


def main():
    print('Ultra Basic MCP Client')
    print(f'{sys.executable=}')
    print(f'Python version {sys.version}')

    asyncio.run(run())


if __name__ == "__main__":
    main()