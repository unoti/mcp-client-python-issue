# MCP SDK Client Python Issue

Created [Issue 395 on MCP Python Github](https://github.com/modelcontextprotocol/python-sdk/issues/395)

This repo is to demonstrate and diagnose an issue we're having with the Python MCP stdio
client. What happens is it never finishes initializes the server. What I expect to
happen is for it to initialize the server successfully so that we can start
communicating with it.

I have tried this in many configurations, including Python 3.10 windows,
Python 3.12 windows, Python 3.12 under WSL, and running Linux in a container,
using the latest main branch and also the latest releases,
and various forms of UV and global Python installations.  I have also tried
it using `asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())`
in various Windows configurations.  Under some configurations this leads
to a new `NotImplementedError`, but under no circumstances was I able to make
it work.

I haven't been able to make a Python client work yet.  I can get node client
and server working without difficulties, though.

## Repro steps, Windows and UV
From the root directory of the project (above src):
```Powershell
uv venv --python=3.10 venv
.\venv\Scripts\activate.ps1
uv pip install mcp
```

Output under windows:
```
(venv) PS C:\Users\rilack\code\mcp-client-python-issue\src> python mcp_client.py
Ultra Basic MCP Client
sys.executable='C:\\Users\\rilack\\code\\mcp-client-python-issue\\venv\\Scripts\\python.exe'
Python version 3.10.16 (main, Mar 17 2025, 20:54:03) [MSC v.1943 64 bit (AMD64)]
Initializing session...
```
And that is the last thing that we see.

## Repro steps, Docker, Ubuntu
To eliminate the variables that this could be an issue with Windows or UV,
I also tested this with Linux.  I have tried this both with Python 3.12 and 3.10
with the same results.

### Build container
I used `podman` to build and run my containers, but you can use `docker` instead.

From the root of the project:
```bash
podman build --tag mcp-lab-08c --file DOCKERFILE .
```

### Run container
Replace `your-src-path` to the directory of your local machine where this project is installed.
```bash
podman run -it --rm -v "your-src-path:/usr/code" mcp-lab-08c bash
```
So for me, I used:
```bash
podman run -it --rm -v "c:\Users\rilack\code\mcp-client-python-issue:/usr/code" mcp-lab-08c bash
```

Then from the container:
```bash
pip install mcp
cd src
python mcp_client.py
```

Output:
```
root@85b6bb0ac0e8:/usr/code/src# python mcp_client.py
Ultra Basic MCP Client
sys.executable='/usr/bin/python'
Python version 3.10.12 (main, Feb  4 2025, 14:57:36) [GCC 11.4.0]
Initializing session...
```
