#!/usr/bin/env python3
"""
Sean's Tools Cloud MCP Proxy Server
A proxy MCP server that connects to the cloud-deployed REST API endpoints.
"""

import asyncio
import json
import sys
import httpx
from typing import Any, Sequence
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    TextContent,
    Tool,
)
import mcp.server.stdio


# Get API URL from command line argument
if len(sys.argv) != 2:
    print("Usage: python3 cloud_mcp_proxy.py <API_GATEWAY_URL>", file=sys.stderr)
    sys.exit(1)

API_BASE_URL = sys.argv[1].rstrip('/')

# Create server instance
server = Server("seans-tools-cloud")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="get_random_number",
            description="Generate a random number within a specified range (Cloud)",
            inputSchema={
                "type": "object",
                "properties": {
                    "min": {
                        "type": "number",
                        "description": "Minimum value (default: 0)",
                        "default": 0
                    },
                    "max": {
                        "type": "number", 
                        "description": "Maximum value (default: 100)",
                        "default": 100
                    }
                },
                "additionalProperties": False
            }
        ),
        Tool(
            name="get_random_number_list",
            description="Generate a list of random numbers (Cloud)",
            inputSchema={
                "type": "object",
                "properties": {
                    "count": {
                        "type": "integer",
                        "description": "Number of random numbers to generate (default: 5)",
                        "default": 5,
                        "minimum": 1,
                        "maximum": 1000
                    },
                    "min": {
                        "type": "number",
                        "description": "Minimum value for each number (default: 0)",
                        "default": 0
                    },
                    "max": {
                        "type": "number",
                        "description": "Maximum value for each number (default: 100)", 
                        "default": 100
                    }
                },
                "additionalProperties": False
            }
        ),
        Tool(
            name="get_random_choice",
            description="Pick random item(s) from a provided list of choices (Cloud)",
            inputSchema={
                "type": "object",
                "properties": {
                    "choices": {
                        "type": "array",
                        "description": "List of items to choose from",
                        "items": {
                            "type": ["string", "number", "boolean"]
                        },
                        "minItems": 1
                    },
                    "count": {
                        "type": "integer",
                        "description": "Number of items to select (default: 1)",
                        "default": 1,
                        "minimum": 1
                    },
                    "allow_duplicates": {
                        "type": "boolean",
                        "description": "Allow selecting the same item multiple times (default: false)",
                        "default": False
                    }
                },
                "required": ["choices"],
                "additionalProperties": False
            }
        ),
        Tool(
            name="math_add",
            description="Add two numbers together (Cloud)",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number", 
                        "description": "Second number"
                    }
                },
                "required": ["a", "b"],
                "additionalProperties": False
            }
        ),
        Tool(
            name="math_subtract",
            description="Subtract second number from first number (Cloud)",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number (minuend)"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number (subtrahend)"
                    }
                },
                "required": ["a", "b"],
                "additionalProperties": False
            }
        ),
        Tool(
            name="math_multiply",
            description="Multiply two numbers together (Cloud)",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    }
                },
                "required": ["a", "b"],
                "additionalProperties": False
            }
        ),
        Tool(
            name="math_divide",
            description="Divide first number by second number (Cloud)",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "Dividend (number to be divided)"
                    },
                    "b": {
                        "type": "number",
                        "description": "Divisor (number to divide by)"
                    }
                },
                "required": ["a", "b"],
                "additionalProperties": False
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[TextContent]:
    """Handle tool calls by proxying to cloud API."""
    
    # Map tool names to API endpoints
    endpoint_map = {
        "get_random_number": "/random/number",
        "get_random_number_list": "/random/list", 
        "get_random_choice": "/random/choice",
        "math_add": "/math/add",
        "math_subtract": "/math/subtract",
        "math_multiply": "/math/multiply",
        "math_divide": "/math/divide"
    }
    
    if name not in endpoint_map:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    endpoint = endpoint_map[name]
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                url,
                json=arguments or {},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'expression' in result:
                    return [TextContent(type="text", text=result['expression'])]
                elif 'result' in result:
                    return [TextContent(type="text", text=f"Result: {result['result']}")]
                else:
                    return [TextContent(type="text", text=f"Success: {json.dumps(result)}")]
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {"error": response.text}
                return [TextContent(type="text", text=f"Error: {error_data.get('error', 'Unknown error')}")]
                
    except httpx.TimeoutException:
        return [TextContent(type="text", text="Error: Request timed out")]
    except httpx.RequestError as e:
        return [TextContent(type="text", text=f"Error: Network request failed - {str(e)}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Main entry point for the server."""
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="seans-tools-cloud",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
