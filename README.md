# Boask

Pure Python website engine.  
Zero external dependencies.  
Real JSX-style templates without React.

```bash
pip install boask
```

## Quick Start

```python
from boask import route, use, run_server, html_templates

@route("/")
def home(handler):
    return html_templates.render("home.html", title="Boask")

if __name__ == "__main__":
    run_server()
```

