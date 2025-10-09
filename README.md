# BigFile Inspector

BigFile Inspector is a memory-efficient Python tool for browsing and searching extremely large text files (10+ GB+) on Linux without loading the entire file into memory. It supports interactive paging, substring and regex searches, field-specific searches for colon-delimited files, and exporting matches to a separate file. Designed for safe and fast exploration of huge datasets.

## Installation

Clone the repository or download the script:

```bash
git clone https://github.com/deadeye/bigfileinspector.git
cd bigfileinspector

python3 bigfile_inspector.py /path/to/largefile.txt -i

python3 bigfile_inspector.py /path/to/largefile.txt -i -s mysearchterm

python3 bigfile_inspector.py /path/to/largefile.txt -s mysearchterm -l 100

python3 bigfile_inspector.py /path/to/largefile.txt -f 1 --field-substring "@hotmail.com"

python3 bigfile_inspector.py /path/to/largefile.txt -r "\b[a-f0-9]{32}\b"

python3 bigfile_inspector.py /path/to/largefile.txt -s mysearchterm -e matches.txt

# Interactive browsing
python3 bigfile_inspector.py ~/Downloads/hugefile.txt -i

# Find first 50 matches of 'testuser'
python3 bigfile_inspector.py ~/Downloads/hugefile.txt -s testuser -l 50

# Search 2nd field for '@example.com' and export
python3 bigfile_inspector.py ~/Downloads/hugefile.txt -f 1 --field-substring "@example.com" -e results.txt

# Regex search for MD5-like fields
python3 bigfile_inspector.py ~/Downloads/hugefile.txt -r "\b[a-f0-9]{32}\b"
