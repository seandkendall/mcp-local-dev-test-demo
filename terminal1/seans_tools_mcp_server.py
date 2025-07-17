#!/usr/bin/env python3
"""
Sean's Tools MCP Server
A local MCP server providing mathematical operations and random number generation tools.
"""

import asyncio
import random
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
from pydantic import AnyUrl
import mcp.server.stdio


# Create server instance
server = Server("seans-tools")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="get_random_number",
            description="Generate a random number within a specified range",
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
            description="Generate a list of random numbers",
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
            description="Pick random item(s) from a provided list of choices",
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
            description="Add two numbers together",
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
            description="Subtract second number from first number",
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
            description="Multiply two numbers together",
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
            description="Divide first number by second number",
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
    """Handle tool calls."""
    
    if name == "get_random_number":
        min_val = arguments.get("min", 0) if arguments else 0
        max_val = arguments.get("max", 100) if arguments else 100
        
        if min_val > max_val:
            return [TextContent(type="text", text=f"Error: min value ({min_val}) cannot be greater than max value ({max_val})")]
        
        result = random.uniform(min_val, max_val)
        return [TextContent(type="text", text=f"Random number: {result}")]
    
    elif name == "get_random_number_list":
        count = arguments.get("count", 5) if arguments else 5
        min_val = arguments.get("min", 0) if arguments else 0
        max_val = arguments.get("max", 100) if arguments else 100
        
        if min_val > max_val:
            return [TextContent(type="text", text=f"Error: min value ({min_val}) cannot be greater than max value ({max_val})")]
        
        if count < 1 or count > 1000:
            return [TextContent(type="text", text=f"Error: count must be between 1 and 1000, got {count}")]
        
        numbers = [random.uniform(min_val, max_val) for _ in range(count)]
        return [TextContent(type="text", text=f"Random numbers: {numbers}")]
    
    elif name == "get_random_choice":
        if not arguments or "choices" not in arguments:
            return [TextContent(type="text", text="Error: 'choices' parameter is required")]
        
        choices = arguments["choices"]
        count = arguments.get("count", 1)
        allow_duplicates = arguments.get("allow_duplicates", False)
        
        if not choices:
            return [TextContent(type="text", text="Error: choices list cannot be empty")]
        
        if count > len(choices) and not allow_duplicates:
            return [TextContent(type="text", text=f"Error: cannot select {count} unique items from {len(choices)} choices. Set allow_duplicates=true or reduce count.")]
        
        if count == 1:
            result = random.choice(choices)
            return [TextContent(type="text", text=f"Random choice: {result}")]
        else:
            if allow_duplicates:
                result = [random.choice(choices) for _ in range(count)]
            else:
                result = random.sample(choices, count)
            return [TextContent(type="text", text=f"Random choices: {result}")]
    
    elif name == "math_add":
        if not arguments or "a" not in arguments or "b" not in arguments:
            return [TextContent(type="text", text="Error: Both 'a' and 'b' parameters are required")]
        
        a = arguments["a"]
        b = arguments["b"]
        result = a + b
        return [TextContent(type="text", text=f"{a} + {b} = {result}")]
    
    elif name == "math_subtract":
        if not arguments or "a" not in arguments or "b" not in arguments:
            return [TextContent(type="text", text="Error: Both 'a' and 'b' parameters are required")]
        
        a = arguments["a"]
        b = arguments["b"]
        result = a - b
        return [TextContent(type="text", text=f"{a} - {b} = {result}")]
    
    elif name == "math_multiply":
        if not arguments or "a" not in arguments or "b" not in arguments:
            return [TextContent(type="text", text="Error: Both 'a' and 'b' parameters are required")]
        
        a = arguments["a"]
        b = arguments["b"]
        result = a * b
        return [TextContent(type="text", text=f"{a} × {b} = {result}")]
    
    elif name == "math_divide":
        if not arguments or "a" not in arguments or "b" not in arguments:
            return [TextContent(type="text", text="Error: Both 'a' and 'b' parameters are required")]
        
        a = arguments["a"]
        b = arguments["b"]
        
        if b == 0:
            return [TextContent(type="text", text="Error: Division by zero is not allowed")]
        
        result = a / b
        return [TextContent(type="text", text=f"{a} ÷ {b} = {result}")]
    
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Main entry point for the server."""
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="seans-tools",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
