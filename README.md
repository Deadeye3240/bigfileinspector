# BigFile Inspector

BigFile Inspector is a **memory-efficient Python tool** for browsing and searching extremely large text files (10GB+).
It reads files **line-by-line instead of loading them into memory**, making it safe and fast for exploring massive datasets on Linux systems.

---

## Features

* Memory-safe streaming (no full file load)
* Interactive browsing mode
* Substring and regex search
* Field-specific searching for colon-delimited files
* Progress tracking while scanning large files
* Export matches to a separate file
* Designed for very large datasets (10GB+)

---

## Installation

Clone the repository:

```bash
git clone https://github.com/deadeye/bigfileinspector.git
```

Enter the project directory:

```bash
cd bigfileinspector
```

Run the script:

```bash
python3 bigfile_inspector.py /path/to/largefile.txt
```

---

## Basic Usage

### Interactive Browsing

```bash
python3 bigfile_inspector.py /path/to/largefile.txt -i
```

### Search for a Substring

```bash
python3 bigfile_inspector.py /path/to/largefile.txt -s mysearchterm
```

### Limit Number of Matches

```bash
python3 bigfile_inspector.py /path/to/largefile.txt -s mysearchterm -l 100
```

---

## Field-Specific Searching

For colon-delimited files, search inside a specific field.

Example: search the **second field** for `@hotmail.com`

```bash
python3 bigfile_inspector.py /path/to/largefile.txt -f 1 --field-substring "@hotmail.com"
```

---

## Regex Searching

Example: search for MD5-style hashes.

```bash
python3 bigfile_inspector.py /path/to/largefile.txt -r "\b[a-f0-9]{32}\b"
```

---

## Export Matches

Save matching results to a file.

```bash
python3 bigfile_inspector.py /path/to/largefile.txt -s mysearchterm -e matches.txt
```

---

## Example Commands

### Interactive browsing of a huge dataset

```bash
python3 bigfile_inspector.py ~/Downloads/hugefile.txt -i
```

### Find first 50 matches of `testuser`

```bash
python3 bigfile_inspector.py ~/Downloads/hugefile.txt -s testuser -l 50
```

### Search second field for `@example.com` and export results

```bash
python3 bigfile_inspector.py ~/Downloads/hugefile.txt -f 1 --field-substring "@example.com" -e results.txt
```

### Regex search for MD5-like hashes

```bash
python3 bigfile_inspector.py ~/Downloads/hugefile.txt -r "\b[a-f0-9]{32}\b"
```

---

## Requirements

* Python 3.7+
* Linux recommended for extremely large files

---

## License

MIT License
