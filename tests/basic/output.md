# Markdata: Keep your data out of your markup!

<table class="table">
<caption>My data</caption>
<thead>
<tr><th>age</th><th>first_name</th><th>last_name</th></tr>
</thead>
<tbody>
<tr><td>90</td><td>John</td><td>Adams</td></tr>
<tr><td>83</td><td>Henry</td><td>Ford</td></tr>
</tbody>
</table>

## New section

> This is a blockquote.


```python
nlp = spacy.load("en")
nlp.add_pipe(my_component, name="print_info", first=True)
print(nlp.pipe_names)  # ['print_info', 'tagger', 'parser', 'ner']
doc = nlp("This is a sentence.")
```
