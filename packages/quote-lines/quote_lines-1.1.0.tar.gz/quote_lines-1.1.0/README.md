# quote

A tiny CLI used for quoting input lines

## Example

Consider the directory:
```bash
$ find .
.
./c
./a b
```

Here, `xargs` alone will fail if we do: `find . -type f | xargs cat` with:
```
This file is named: c
cat: ./a: No such file or directory
cat: b: No such file or directory
```

This is because the file 'a b' is not quoted!

Instead we can do: `find . -type f | quote | xargs cat` and we will get:
```
This file is named: c
This file is named: a b
```
