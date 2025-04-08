# Crew With Local Llm
## Execution
- Make sure you are running ollama locally: 
    - `ollama run llama3`
    - `ollama ps`

      ```
          NAME             ID              SIZE      PROCESSOR          UNTIL
          llama3:latest    365c0bd3c000    5.9 GB    14%/86% CPU/GPU    4 minutes from now
        ```
- .env file should contain the following: 
    ```
    MODEL=ollama/llama3
    API_BASE=http://localhost:11434

    ```
  - Finally Run. `crewai run` 

## Installation
- Step 0: CrewAI requires Python >=3.10 and <3.13. Here’s how to check your version:
    `python --version`
    ```
        Python 3.12.4
    ```
- Step 1: UV installation on Windows. 
  `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

  ```
  Downloading uv 0.6.13 (x86_64-pc-windows-msvc)
  Installing to C:\Users\gulam\.local\bin
    uv.exe
    uvx.exe
  everything's installed!
  To add C:\Users\gulam\.local\bin to your PATH, either restart your shell or run:

      set Path=C:\Users\gulam\.local\bin;%Path%   (cmd)
      $env:Path = "C:\Users\gulam\.local\bin;$env:Path"   (powershell)
  ```
- Step 2: Run the following command to install crewai CLI
    `uv tool install crewai`. If you 
    encounter a PATH warning, run this command to update your shell: `uv tool update-shell`
- Step 3: `uv tool list`. Something like below should show up. 
    ```
    crewai v0.102.0
    - crewai
    ```
- Step 4: `uv tool install crewai --upgrade` Upgrade to ensure we have latest package. 
- Step 5: Create a new project `crewai create crew crew-with-local-llm`
- Step 6: Run `cd crew-with-local-llm` & run `crew install`
- Step 7: Choose the newly create .venv in your vs code. 

