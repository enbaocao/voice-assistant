#!/usr/bin/env python3
"""
Check FastMCP version and available transports
"""

import fastmcp
import inspect

# Print version info
print(f"FastMCP version: {fastmcp.__version__ if hasattr(fastmcp, '__version__') else 'unknown'}")

# Check available modules
print("\nAvailable FastMCP modules:")
for module_name in dir(fastmcp):
    if not module_name.startswith('_'):  # Skip private modules
        print(f"- {module_name}")

# Check available transports
print("\nLooking for transport-related attributes:")
for item in dir(fastmcp):
    if 'transport' in item.lower():
        print(f"- {item}")

# Try to import common transports
print("\nTrying to import potential transport modules:")
try:
    from fastmcp.server.transports import get_transport
    print("- get_transport function is available")
    # Try to see what transports are registered
    print("\nAvailable transports:")
    try:
        # This might not work, but worth trying
        for name in get_transport():
            print(f"- {name}")
    except:
        print("Unable to list available transports")
except ImportError:
    print("- get_transport function is not available")

# Print FastMCP.run method signature
print("\nFastMCP.run method signature:")
try:
    sig = inspect.signature(fastmcp.FastMCP.run)
    print(sig)
    print("Parameters:")
    for param_name, param in sig.parameters.items():
        print(f"- {param_name}: {param.default if param.default is not inspect.Parameter.empty else 'required'}")
except Exception as e:
    print(f"Error examining run method: {e}")
