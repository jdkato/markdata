# Diagrams Through Ascii Art

ditaa is a small command-line utility written in Java, that can convert diagrams drawn using ascii art ('drawings' that contain characters that resemble lines like | / - ), into proper bitmap graphics. This is best illustrated by the following example -- which also illustrates the benefits of using ditaa in comparison to other methods :)

```text
`document{'path': 'sample.ditaa'}`
```

After conversion using ditaa, the above file becomes:

`ditaa{'path': 'sample.ditaa', 'alt': 'A ditaa diagram'}`

ditaa interprets ASCII art as a series of open and closed shapes, but it also uses special markup syntax to increase the possibilities of shapes and symbols that can be rendered.

ditaa is open source and free software (free as in free speech), since it is released under the GPL license.
