# MCP Local Development Test Demo

A practical demonstration of how to build, test, and iterate on Model Context Protocol (MCP) servers using Amazon Q Developer Pro in a dual-terminal setup.

## What is This Demo?

This repository showcases a complete workflow for developing MCP servers locally using Amazon Q Developer Pro. It demonstrates how you can use two terminal sessions to create a seamless development experience:

- **Terminal 1**: Development environment for building the MCP server
- **Terminal 2**: Testing environment with Amazon Q Developer Pro configured to use your local MCP server

## Why This Approach Matters

Building MCP servers can be complex, but this demo shows how Amazon Q Developer Pro can help you:

- **Rapid Prototyping**: Quickly build and modify MCP server functionality
- **Real-time Testing**: Immediately test your changes without complex deployment
- **Iterative Development**: Make changes and see results instantly
- **Best Practices**: Learn proper MCP server structure and implementation

## Repository Structure

```
├── terminal1/
│   ├── seans_tools_mcp_server.py  # The MCP server implementation
│   └── prompt.txt                 # Original requirements/prompt
├── terminal2/
│   └── .amazonq/
│       └── mcp.json              # MCP configuration for Amazon Q
└── README.md                     # This file
```

## The MCP Server

The demo includes a fully functional MCP server (`seans_tools_mcp_server.py`) with these tools:

### Mathematical Operations
- `math_add` - Add two numbers
- `math_subtract` - Subtract two numbers  
- `math_multiply` - Multiply two numbers
- `math_divide` - Divide two numbers (with zero-division protection)

### Random Number Generation
- `get_random_number` - Generate a single random number within a range
- `get_random_number_list` - Generate multiple random numbers

### Random Selection
- `get_random_choice` - Pick random items from a list with options for:
  - Multiple selections
  - Duplicate allowance
  - Various data types (strings, numbers, booleans)

## How to Use This Demo

### Prerequisites

- Python 3.8 or higher
- Amazon Q Developer Pro CLI (`q` command)
- Basic understanding of MCP concepts

### Step 1: Set Up Terminal 1 (Development)

1. Clone this repository:
   ```bash
   git clone https://github.com/seandkendall/mcp-local-dev-test-demo.git
   cd mcp-local-dev-test-demo
   ```

2. Navigate to the development directory:
   ```bash
   cd terminal1
   ```

3. Make the MCP server executable:
   ```bash
   chmod +x seans_tools_mcp_server.py
   ```

4. Test the server directly:
   ```bash
   python seans_tools_mcp_server.py
   ```

### Step 2: Set Up Terminal 2 (Testing)

1. Open a new terminal and navigate to the testing directory:
   ```bash
   cd terminal2
   ```

2. Start Amazon Q Developer Pro with MCP configuration:
   ```bash
   q chat
   ```

3. The MCP server will be automatically loaded based on the configuration in `.amazonq/mcp.json`

### Step 3: Test Your MCP Server

In Terminal 2 (Amazon Q session), try these commands:

```
# Test mathematical operations
Can you add 15 and 27 using the math tools?

# Test random number generation  
Generate 5 random numbers between 1 and 100

# Test random selection
Pick 3 random items from this list: ["apple", "banana", "cherry", "date", "elderberry"]
```

### Step 4: Iterate and Improve

1. **Modify the server** in Terminal 1 (`seans_tools_mcp_server.py`)
2. **Restart Amazon Q** in Terminal 2 to load changes
3. **Test your modifications** immediately
4. **Repeat** until satisfied

## Key Learning Points

### MCP Server Structure
- **Protocol Implementation**: Uses the official MCP Python SDK
- **Tool Definition**: Clear schema definitions for each tool
- **Error Handling**: Robust validation and error messages
- **Async Operations**: Proper async/await patterns

### Development Workflow
- **Local Testing**: No need for complex deployment pipelines
- **Rapid Iteration**: Make changes and test immediately
- **Real Integration**: Test with actual AI assistant (Amazon Q)
- **Version Control**: Track changes and improvements over time

### Best Practices Demonstrated
- **Input Validation**: All tools validate their parameters
- **Error Messages**: Clear, helpful error responses
- **Type Safety**: Proper type definitions and checking
- **Documentation**: Well-documented tool descriptions

## Configuration Details

The MCP configuration (`terminal2/.amazonq/mcp.json`) connects Amazon Q to your local server:

```json
{
  "mcpServers": {
    "seans-tools": {
      "command": "python",
      "args": ["../terminal1/seans_tools_mcp_server.py"],
      "env": {}
    }
  }
}
```

This tells Amazon Q to:
- Run your Python MCP server
- Use the relative path to find your server file
- Load it as "seans-tools" in the MCP ecosystem

## Extending the Demo

Want to add more functionality? Here's how:

1. **Add New Tools**: Extend the `handle_list_tools()` function
2. **Implement Logic**: Add corresponding logic in `handle_call_tool()`
3. **Test Immediately**: Use Amazon Q to test your new tools
4. **Iterate**: Refine based on real usage

## Common Use Cases

This development pattern is perfect for:

- **Custom Business Logic**: Build tools specific to your organization
- **API Integrations**: Create MCP tools that interact with external services  
- **Data Processing**: Build specialized data manipulation tools
- **Automation**: Create tools for common development tasks
- **Prototyping**: Quickly test ideas before full implementation

## Troubleshooting

### Server Won't Start
- Check Python version compatibility
- Verify file permissions (`chmod +x`)
- Review error messages in Terminal 1

### Amazon Q Can't Find Tools
- Restart Amazon Q after server changes
- Verify MCP configuration path
- Check server is running without errors

### Tools Not Working as Expected
- Test server directly in Terminal 1
- Check parameter validation
- Review error messages in Amazon Q

## Contributing

This demo is designed to be educational and extensible. Feel free to:

- Add new tools and functionality
- Improve error handling
- Enhance documentation
- Share your own MCP server examples

## Next Steps

After mastering this demo:

1. **Build Production Servers**: Deploy MCP servers for real applications
2. **Integrate with CI/CD**: Automate testing and deployment
3. **Create Complex Tools**: Build more sophisticated functionality
4. **Share with Community**: Contribute to the MCP ecosystem

## Resources

- [MCP Official Documentation](https://modelcontextprotocol.io/)
- [Amazon Q Developer Pro](https://aws.amazon.com/q/developer/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

**Happy MCP Development!** 🚀

This demo shows that building powerful AI integrations doesn't have to be complicated. With the right tools and workflow, you can rapidly prototype, test, and deploy MCP servers that extend AI capabilities in meaningful ways.
