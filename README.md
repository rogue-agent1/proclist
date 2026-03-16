# proclist
List and filter running processes with sorting, regex matching, and kill support.

## Usage
```bash
python proclist.py              # All processes, sorted by CPU
python proclist.py python       # Filter by name
python proclist.py -u root --sort mem --top 10
python proclist.py node --kill  # Kill matching processes
```
## Zero dependencies. Python 3.6+.
