import datetime
from pathlib import Path
import json
from dotmap import DotMap

# This section is used to report on success or failure of the command
output_format="""{% if failure %}<red> FAIL - </red>{% endif %}<green>OK - </green>{{ title or command }} {% if failure and output %} {{ ('command: ' + command + '\n  ') if title else '' }}ERROR output: \n{{ output|indent(4 * ' ') }}\n  ...{% endif %}"""

# output_format="""{% if success %}<green> ✓</green>
# {% elif nofail %}<yellow>✗</yellow>
# {% else %}<red>ERROR ✗</red>{% endif %} 
# <bold>{{ ex }}</bold>
# {% if failure %} ({{ code }}){% endif %}
# {% if failure and output and not quiet %}\n
# {{ ('  > ' + command + '\n') if title else '' }}
# {{ output|indent(2 * ' ') }}{% endif %}"""

# Read config file, use dot (.) notation for accessing elements
with open("config.json") as file:
    config = DotMap(json.load(file))

""" simpleCommand takes a context, command and directory.
It runs the command and saves the output to the directory.
If expectedOutputs is used, it will search the output for 
the values identified."""
def simpleCommand(ctx, command, dir, expectedOutputs=None):
    content = f"Command: {command}\n"
    content += "Data:\n"
    output = ctx.run(command, fmt=f"custom={output_format}")
    content += f"{output}"
    writeToFile(dir, content)
    
    if not expectedOutputs is None:
        if not verifyOutput(content, expectedOutputs):
            exit(8)

def verifyOutput(data, expectedOutputs):
    for value in expectedOutputs:
        if value not in data:
            print(f"Error finding {value} in {data}")
            return False
    return True

def submitandrety(ctx, dataset, dir, maxRC=0, numRetries=1):
    if numRetries > 0:
        submitJobAndDownloadOutput(ctx, dataset, dir, maxRC)
        numRetries = numRetries - 1
    else:
        print ("Max retries exceeded")
        exit(88)

def submitJobAndDownloadOutput(ctx, dataset, dir, maxRC=0):
    command = f'zowe jobs submit data-set "{dataset}" -d {dir} --rfj'
    content = f"Command: {command}\n"
    content += "Data:\n"
    output = ctx.run(command, capture="both", fmt=f"custom={output_format}")
    # output = ctx.run(command, capture="both")
    data = DotMap(json.loads(output))
    print(data.data.owner, data.data.jobid, data.data.jobname, data.data.retcode)

    content += f"{output}"
    writeToFile(dir, content)
    retcode = int(data.data.retcode.split(" ")[1])
    if retcode > maxRC:
        print("MaxRC exceeded")
        exit(retcode)

"""Creates a directory and a file with the current timestamp.
If the directories don't exist, it makes them.
If they do exist, there's no error.
- replaces : so the file can be written to windows."""
def writeToFile(dir, content):
    filename = datetime.datetime.now().isoformat().replace(":","-")
    filepath = Path(dir + "/" + filename)
    filepath.parent.mkdir(exist_ok=True, parents=True)
    filepath.write_text(content)
