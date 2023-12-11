# Some PantUML sample

```plantuml
Alice -> Bob: Authentication Request
Bob --> Alice: Authentication Response

Alice -> Bob: Another authentication Request
Alice <-- Bob: another authentication Response
```

Nice, huh?

# Another example which referenced later
This tests relative path w/ subdirectory

```{ .plantuml width=60% plantuml-filename=images/example.png }
[producer] -> [consumer]: data streaming
```

This tests relative path w/o subdirectories

```{ .plantuml width=60% plantuml-filename=example.png }
[producer] -> [consumer]: data streaming
```

Here's a UML

# Reference
![And here's the reference](images/example.png)
