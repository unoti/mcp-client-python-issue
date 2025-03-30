**Describe the bug**
Python MCP client cannot successfully initialize an MCP Stdio server.

## To Reproduce
I have two reproduction steps.  One for windows, and one for Linux.  Additional notes and details are here in my [reproduction notes](https://github.com/unoti/mcp-client-python-issue/tree/main) but I will reproduce them here as well.

### Windows Reproduction Steps
Create a new empty directory and cd to it, then:
1. Save this file as [mcp_echo_server.py](https://github.com/unoti/mcp-client-python-issue/blob/main/src/mcp_echo_server.py). This is intended to be the same as the [sdk docs  for echo server](https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#echo-server).
2. Save this file as [mcp_client.py](https://github.com/unoti/mcp-client-python-issue/blob/main/src/mcp_client.py). This is intended to be as close as practical to the [sdk docs for writing mcp clients](https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#writing-mcp-clients).
Install `mcp` and run:
```Powershell
uv venv --python=3.10 venv
.\venv\Scripts\activate.ps1
uv pip install mcp
python mcp_client.py
```
The output I get is this:
```
(venv) PS C:\Users\rilack\code\mcp-client-python-issue\src> python mcp_client.py
Ultra Basic MCP Client
sys.executable='C:\\Users\\rilack\\code\\mcp-client-python-issue\\venv\\Scripts\\python.exe'
Python version 3.10.16 (main, Mar 17 2025, 20:54:03) [MSC v.1943 64 bit (AMD64)]
Initializing session...
```
Note that we never see the message indicating that it finished initializing the session.
```python
    print("Initializing session...") # This is the last thing we will see.
    await session.initialize()
    print("Session initialized successfully.") # If it's broken we won't see this.
```

### Linux Container Reproduction Steps
There is a [repo with these files](https://github.com/unoti/mcp-client-python-issue/blob/main/README.md) but I am placing the info here as well.

Make an empty directy and go to it, then:
1. Save this as [DOCKERFILE](https://github.com/unoti/mcp-client-python-issue/blob/main/DOCKERFILE)
2. Save this as [src/mcp_client.py](https://github.com/unoti/mcp-client-python-issue/blob/main/src/mcp_client.py)
3. Save this as [src/mcp_echo_server.py](https://github.com/unoti/mcp-client-python-issue/blob/main/src/mcp_echo_server.py)
4. Build the dockerfile, from the root of the project use the following. I used `podman` but you can use `docker`:
    ```
    podman build --tag mcp-lab-08c --file DOCKERFILE .
    ```
5. Run the container.  Replace `your-src-path` with the full pathname of the root above `src`:
    ```
    podman run -it --rm -v "your-src-path:/usr/code" mcp-lab-08c bash
    ```
    So for me, I used this to replace the path:
    ```
    podman run -it --rm -v "c:\Users\rilack\code\mcp-client-python-issue:/usr/code" mcp-lab-08c bash
    ```
6. Then from within the container:
    ```bash
    pip install mcp
    cd src
    python mcp_client.py
    ```
Observed output:
```
root@85b6bb0ac0e8:/usr/code/src# python mcp_client.py
Ultra Basic MCP Client
sys.executable='/usr/bin/python'
Python version 3.10.12 (main, Feb  4 2025, 14:57:36) [GCC 11.4.0]
Initializing session...
```
Note that we do not see further output indicating a successful initialization.

**Expected behavior**
We expect to see the message `Session initialized successfully.`
```python
    print("Initializing session...") # This is the last thing we will see.
    await session.initialize()
    print("Session initialized successfully.") # If it's broken we won't see this.
```

**Desktop (please complete the following information):**
 - OS: Windows 11, for container we used Ubuntu 22.04.

**Additional context**
I have tried this in many configurations, including Python 3.10 windows, Python 3.12 windows, Python 3.12 under WSL, and running Linux in a container, using the latest main branch and also the latest releases, and various forms of UV and global Python installations. I have also tried it using asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) in various Windows configurations. Under some configurations this leads to a new NotImplementedError, but under no circumstances was I able to make it work.

I haven't been able to make a Python client work yet. I can get node client and server working without difficulties, though.

It's possible that [issue 382](https://github.com/modelcontextprotocol/python-sdk/issues/382) is similar, although its
code for the repro is much more complex.  I have endeavored to strip this down to the bare minimum of what is shown
in the sdk documentation.  In fact the only difference in these repros versus the [sdk documentation on clients](https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#writing-mcp-clients) is the example there shows something about `handle_sampling_message` and indicates it is optional. I was unable to figure out what that's for either by reading the docs or
studying the source for a while, so I removed that, but it doesn't help either way.

I am able to make node clients work without difficulty, but I really need a Python client, so I'm sticking with this.
I have not yet tried an HTTP/SSE client and will do so next, but I already have a stdio-only server that works
well for my use case in Claude desktop that I am trying to get working from a Python client.


