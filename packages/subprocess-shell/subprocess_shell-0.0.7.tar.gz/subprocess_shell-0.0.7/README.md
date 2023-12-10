# *subprocess_shell*

is a Python package providing an alternative interface to sub processes. The aim is simplicity comparable to shell scripting and transparency for more complex use cases.

[[_TOC_]]

![`videos/aperitif.mp4`](videos/aperitif.mp4)

## Features

- Simple
    - e.g. 4 functions (`start`, `write`, `wait`, `read`) and 3 operators (`>>`, `+`, `-`)
- Transparent
    - usability layer for [*subprocess*](https://docs.python.org/3/library/subprocess.html) except streams
- Separates streams
    - no interleaving of stdout and stderr and from different processes of a chain
- Avoids deadlocks due to OS pipe buffer limits by using queues
- Uses [*Rich*](https://github.com/Textualize/rich) if available

<details>
  <summary>

`images/rich_output.png`

</summary>

![](images/rich_output.png)

</details>

## Examples

<table>
<thead>
  <tr>
    <th></th>
    <th>

`bash -e`

</th>
    <th>

*subprocess_shell*

</th>
    <th>

*subprocess*

</th>
    <th>

[*Plumbum*](https://github.com/tomerfiliba/plumbum)[^e1]

</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>initialization</td>
    <td></td>
    <td>

```python
from subprocess_shell import *
```

</td>
    <td>

```python
import subprocess
```

</td>
    <td>

```python
from plumbum import local
```

</td>
  </tr>
  <tr>
    <td>run command</td>
    <td>

```bash
echo this
```

</td>
    <td>

```python
["echo", "this"] >> start() >> wait()
```

</td>
    <td>

```python
assert subprocess.Popen(["echo", "this"]).wait() == 0
```

</td>
    <td>

```python
local["echo"]["this"].run_fg()
```

</td>
  </tr>
  <tr>
    <td>redirect stream</td>
    <td>

```bash
echo this > /path/to/file
```

</td>
    <td>

```python
["echo", "this"] >> start(stdout="/path/to/file") >> wait()
```

</td>
    <td>

```python
with open("/path/to/file", "wb") as stdout:
    assert subprocess.Popen(["echo", "this"], stdout=stdout).wait() == 0
```

</td>
    <td>

```python
(local["echo"]["this"] > "/path/to/file").run_fg()
```

</td>
  </tr>
  <tr>
    <td>read stream</td>
    <td>

```bash
a=$(echo this)
```

</td>
    <td>

```python
a = ["echo", "this"] >> start() >> read()
```

</td>
    <td>

```python
process = subprocess.Popen(["echo", "this"], stdout=subprocess.PIPE)
a, _ = process.communicate()
assert process.wait() == 0
```

</td>
    <td>

```python
a = local["echo"]("this")
```

</td>
  </tr>
  <tr>
    <td>write stream</td>
    <td>

```bash
cat - <<EOF
this
EOF
```

</td>
    <td>

```python
["cat", "-"] >> start() >> write("this") >> wait()
```

</td>
    <td>

```python
process = subprocess.Popen(["cat", "-"], stdin=subprocess.PIPE)
process.communicate(b"this")
assert process.wait() == 0
```

</td>
    <td>

```python
(local["cat"]["-"] << "this").run_fg()
```

</td>
  </tr>
  <tr>
    <td>chain commands</td>
    <td>

```bash
echo this | cat -
```

</td>
    <td>

```python
["echo", "this"] >> start() + ["cat", "-"] >> start() >> wait()
```

</td>
    <td>

```python
process = subprocess.Popen(["echo", "this"], stdout=subprocess.PIPE)
assert subprocess.Popen(["cat", "-"], stdin=process.stdout).wait() == 0
assert process.wait() == 0
```

</td>
    <td>

```python
(local["echo"]["this"] | local["cat"]["-"]).run_fg()
```

</td>
  </tr>
  <tr>
    <td>branch out</td>
    <td>?</td>
    <td>

```python
import sys

_v_ = "import sys; print('stdout'); print('stderr', file=sys.stderr)"
arguments = [sys.executable, "-c", _v_]

process = arguments >> start(pass_stdout=True, pass_stderr=True)
process + ["cat", "-"] >> start() >> wait()
process - ["cat", "-"] >> start() >> wait()
```

</td>
    <td>

```python
import sys

_v_ = "import sys; print('stdout'); print('stderr', file=sys.stderr)"
arguments = [sys.executable, "-c", _v_]

process = subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
assert subprocess.Popen(["cat", "-"], stdin=process.stdout).wait() == 0
assert subprocess.Popen(["cat", "-"], stdin=process.stderr).wait() == 0
assert process.wait() == 0
```

</td>
    <td>

not supported[^e2]

</td>
  </tr>
  <tr>
    <td>errors in chains</td>
    <td>?</td>
    <td>

```python
_v_ = ["echo", "this"] >> start(return_codes=(0, 1)) - ["cat", "-"] >> start()
_v_ >> wait(return_codes=(0, 2))
```

</td>
    <td>

```python
first_process = subprocess.Popen(["echo", "this"], stderr=subprocess.PIPE)
second_process = subprocess.Popen(["cat", "-"], stdin=first_process.stderr)
assert first_process.wait() in (0, 1) and second_process.wait() in (0, 2)
```

</td>
    <td>

not supported[^e2]

</td>
  </tr>
  <tr>
    <td>callbacks</td>
    <td></td>
    <td>

```python
["echo", "this"] >> start(stdout=print) >> wait()
```

</td>
    <td>

```python
process = subprocess.Popen(["echo", "this"], stdout=subprocess.PIPE)

for bytes in process.stdout:
    print(bytes)

assert process.wait() == 0
```
!![^e3]

</td>
    <td></td>
  </tr>
</tbody>
</table>

[^e1]: Mostly adapted versions from https://www.reddit.com/r/Python/comments/16byt8j/comment/jzhh21f/?utm_source=share&utm_medium=web2x&context=3
[^e2]: Has been requested years ago
[^e3]: This is very limited and has several issues with potential for deadlocks. An exact equivalent would be too long for this table.

**Notes**
- `bash -e` because errors can have serious consequences
    - e.g.
```bash
a=$(failing command)
sudo chown -R root:root "$a/"
```
- `assert process.wait() == 0` is the shortest (readable) code waiting for a process to stop and asserting the return code
- complexity of code for *Plumbum* can be misleading because it has a much wider scope (e.g. remote execution and files)

## Quickstart

- Prepare virtual environment (optional but recommended)
    - e.g. [*Pipenv*](https://github.com/pypa/pipenv): `python -m pip install -U pipenv`
- Install *subprocess_shell*
    - e.g. `python -m pipenv run pip install subprocess_shell`
- Import and use it
    - e.g. `from subprocess_shell import *` and `python -m pipenv run python ...`

- Prepare tests
    - e.g. `python -m pipenv run pip install subprocess_shell[test]`
- Run tests
    - e.g. `python -m pipenv run pytest ./tests`

## Documentation

```python
from subprocess_shell import *
```

### Start process

```python
process = arguments >> start(
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    pass_stdout=False,
    stderr=subprocess.PIPE,
    pass_stderr=False,
    queue_size=0,
    return_codes=(0,),
    **{},
)
```

<table>
  <tbody>
    <tr>
      <td>

`arguments`

</td>
      <td>

iterable

</td>
      <td>

arguments are converted to string using `str(...)` and passed to `subprocess.Popen(...)`

</td>
    </tr>
    <tr>
      <td>

`stdin`

</td>
      <td>

`subprocess.PIPE`

</td>
      <td>provide stdin</td>
    </tr>
    <tr>
      <td></td>
      <td>

any `object`

</td>
      <td>

same as `subprocess.Popen(..., stdin=object)`

</td>
    </tr>
    <tr>
      <td>

`stdout`

</td>
      <td>

`subprocess.PIPE`

</td>
      <td>provide stdout</td>
    </tr>
    <tr>
      <td></td>
      <td>

string or `pathlib.Path`

</td>
      <td>

redirect stdout to file

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`function(argument: bytes | str) -> typing.Any`

</td>
      <td>call function for each chunk from stdout</td>
    </tr>
    <tr>
      <td></td>
      <td>

any `object`

</td>
      <td>

same as `subprocess.Popen(..., stdout=object)`

</td>
    </tr>
    <tr>
      <td>

`pass_stdout`

</td>
      <td>

`False`

</td>
      <td>

if `stdout=subprocess.PIPE`: queue chunks from stdout

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`True`

</td>
      <td>don't use stdout</td>
    </tr>
    <tr>
      <td>

`stderr`

</td>
      <td>

`subprocess.PIPE`

</td>
      <td>provide stderr</td>
    </tr>
    <tr>
      <td></td>
      <td>

string or `pathlib.Path`

</td>
      <td>

redirect stderr to file

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`function(argument: bytes | str) -> typing.Any`

</td>
      <td>call function for each chunk from stderr</td>
    </tr>
    <tr>
      <td></td>
      <td>

any `object`

</td>
      <td>

same as `subprocess.Popen(..., stderr=object)`

</td>
    </tr>
    <tr>
      <td>

`pass_stderr`

</td>
      <td>

`False`

</td>
      <td>

if `stderr=subprocess.PIPE`: queue chunks from stderr

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`True`

</td>
      <td>don't use stderr</td>
    </tr>
    <tr>
      <td>

`queue_size`

</td>
      <td>

`0`

</td>
      <td>no limit on size of queues</td>
    </tr>
    <tr>
      <td></td>
      <td>

`int > 0`

</td>
      <td>

wait for other threads to process queues if full; **!! can lead to deadlocks !!**

</td>
    </tr>
    <tr>
      <td>

`return_codes`

</td>
      <td>

`(0,)`

</td>
      <td>

if in a chain: analog of `wait(return_code=(0,))`

</td>
    </tr>
    <tr>
      <td></td>
      <td>

collection `object`

</td>
      <td>

if in a chain: analog of `wait(return_code=object)`

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`None`

</td>
      <td>

if in a chain: analog of `wait(return_code=None)`

</td>
    </tr>
    <tr>
      <td>

`**`

</td>
      <td>

`{}`

</td>
      <td>

passed to `subprocess.Popen(...)`

</td>
    </tr>
  </tbody>
</table>

### Write to stdin

```python
process = process >> write(argument)
```

<table>
  <tbody>
    <tr>
      <td>

`argument`

</td>
      <td>

string or `bytes`

</td>
      <td>en/decoded if necessary, written to stdin and flushed</td>
    </tr>
  </tbody>
</table>

**requires** `start(stdin=subprocess.PIPE)`

### Wait for process

```python
return_code = process >> wait(
    stdout=True,
    stderr=True,
    return_codes=(0,),
)
```

<table>
  <tbody>
    <tr>
      <td>

`stdout`

</td>
      <td>

`True`

</td>
      <td>

if stdout is queued: collect stdout, format and print to stdout

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`False`

</td>
      <td>don't use stdout</td>
    </tr>
    <tr>
      <td></td>
      <td>

any `object`

</td>
      <td>

if stdout is queued: collect stdout, format and print with `print(..., file=object)`

</td>
    </tr>
    <tr>
      <td>

`stderr`

</td>
      <td>

`True`

</td>
      <td>

if stderr is queued: collect stderr, format and print to stderr

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`False`

</td>
      <td>don't use stderr</td>
    </tr>
    <tr>
      <td></td>
      <td>

any `object`

</td>
      <td>

if stderr is queued: collect stderr, format and print with `print(..., file=object)`

</td>
    </tr>
    <tr>
      <td>

`return_codes`

</td>
      <td>

`(0,)`

</td>
      <td>assert the return code is 0</td>
    </tr>
    <tr>
      <td></td>
      <td>collection</td>
      <td>assert the return code is in the collection</td>
    </tr>
    <tr>
      <td></td>
      <td>

`None`

</td>
      <td>don't assert the return code</td>
    </tr>
  </tbody>
</table>

### Read from stdout/stderr

```python
string = process >> read(
    stdout=True,
    stderr=False,
    bytes=False,
    return_codes=(0,),
)
```

<table>
  <tbody>
    <tr>
      <td>

`stdout`

</td>
      <td>

`True`

</td>
      <td>

execute `process >> wait(..., stdout=False)`, collect stdout, join and return; **requires** queued stdout

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`False`

</td>
      <td>

execute `process >> wait(..., stdout=True)`

</td>
    </tr>
    <tr>
      <td></td>
      <td>

any `object`

</td>
      <td>

execute `process >> wait(..., stdout=object)`

</td>
    </tr>
    <tr>
      <td>

`stderr`

</td>
      <td>

`False`

</td>
      <td>

execute `process >> wait(..., stderr=True)`

</td>
    </tr>
    <tr>
      <td></td>
      <td>

`True`

</td>
      <td>

execute `process >> wait(..., stderr=False)`, collect stderr, join and return; **requires** queued stderr

</td>
    </tr>
    <tr>
      <td></td>
      <td>

any `object`

</td>
      <td>

execute `process >> wait(..., stderr=object)`

</td>
    </tr>
    <tr>
      <td>

`bytes`

</td>
      <td>

`False`

</td>
      <td>return a string or tuple of strings</td>
    </tr>
    <tr>
      <td></td>
      <td>

`True`

</td>
      <td>

return `bytes` or tuple of `bytes`

</td>
    </tr>
    <tr>
      <td>

`return_codes`

</td>
      <td>

`(0,)`

</td>
      <td>

execute `process >> wait(..., return_codes=(0,))`

</td>
    </tr>
    <tr>
      <td></td>
      <td>

any `object`

</td>
      <td>

execute `process >> wait(..., return_codes=object)`

</td>
    </tr>
  </tbody>
</table>

```python
process.get_stdout_lines(bytes=False)
process.get_stderr_lines(bytes=False)
process.get_stdout_strings()
process.get_stderr_strings()
process.get_stdout_bytes()
process.get_stderr_bytes()
process.get_stdout_objects()
process.get_stderr_objects()
```

<table>
  <tbody>
    <tr>
      <td>

`bytes`

</td>
      <td>

`False`

</td>
      <td>return iterable of strings</td>
    </tr>
    <tr>
      <td></td>
      <td>

`True`

</td>
      <td>

return iterable of `bytes`

</td>
    </tr>
  </tbody>
</table>

**requires** queued stdout/stderr

### Chain processes / pass streams

```python
process = source_arguments >> start(...) + arguments >> start(...)
# or
source_process = source_arguments >> start(..., pass_stdout=True)
process = source_process + arguments >> start(...)
```

```python
process = source_arguments >> start(...) - arguments >> start(...)
# or
source_process = source_arguments >> start(..., pass_stderr=True)
process = source_process - arguments >> start(...)
```

```python
source_process = process.get_source_process()
```

- `process >> wait(...)` waits for the processes from left/source to right/target

### Other

#### LineStream

If you want to use `wait` and process the streams line by line at the same time, you can use `LineStream`.

Example:

```python
import subprocess_shell
import sys

def function(line_string):
    pass

process >> wait(stdout=subprocess_shell.LineStream(function, sys.stdout))
```

## Limitations

- Linux only

## Motivation

Shell scripting is great for simple tasks.
When tasks become more complex, e.g. hard to chain or require non-trivial processing, I always switch to Python.
The interface provided by *subprocess* is rather verbose and parts that would look trivial in a shell script end up a repetitive mess.
After refactoring up the mess once too often, it was time for a change.

## See also

- [*Plumbum*](https://github.com/tomerfiliba/plumbum)
- [*sh*](https://github.com/amoffat/sh)

## Why the name subprocess\_shell

Simply because I like the picture of *subprocess* with a sturdy layer that is easy and safe to handle.
Also, while writing `import subprocess` it is easy to remember to add `_shell`.

Before subprocess\_shell I chose to call it shell.
This was a bad name for several reasons, but most notably because the term shell is commonly used for applications providing an interface to the operating system.

---
