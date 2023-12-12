<div align="center">
   <img alt="logo" height="100px" src="https://gitlab.com/uploads/-/system/project/avatar/51880384/llama-prompt2.png">
</div>

# llama-prompter
llama-prompter is a Python library designed to facilitate the crafting of prompts for Large Language Models (LLMs) and the retrieval of structured responses.
It transcribes prompt templates into llama_cpp grammars, guiding the LLM to produce more structured and relevant outputs.

## Features

- **Prompt Templates to llama_cpp Grammar**: Transcribe templates into grammars that guide the LLM output, ensuring more structured and relevant responses.
- **Support for Pydantic Types**: Define complex variables using Pydantic classes for more detailed and specific model outputs.
- **Decode LLM output to populate predefined variables**: Variables defined in prompt templates will be automatically populated by decoding the LLM output.

## Installation

```
pip install llama-prompter
```

## How it works

### Prompt template
A prompt template allows user to structure the LLM output.
A template may contain typed variables, defined as `{<variable-name>:<type>}` which, once compiled into a grammar, will guide the model's output.

Example
```
from llama_prompter import Prompter

prompter = Prompter("""USER: How far is the Moon from Earth in miles?
ASSISTANT: {var:int}""")
```

### Template variables
llama-prompter supports most basic types for variable types (str, int, float, list, tuple, dict) as well as pydantic models.
The type notation follows python's standard type declaration.

Example with list
```
prompter = Prompter(
    """USER: Write a comma separated list of the first 10 digits of pi
ASSISTANT: {digits:list[int]}"""
)
```

### Compiled grammar
The template will be transcribed into llama_cpp grammar (from llama-cpp-python).
The initialized prompter will contain 2 useful properties:
1. `prompter.prompt` which contains the model prompt
2. `prompter.grammar` which contains the compiled grammar

In our previous example, the template will be transcribed into the following grammar:
```
listInteger ::= "[" (integer ("," integer)*)? "]"
integer ::= ("-"? ([0-9]+))
root ::= listInteger
```

`prompter.prompt` contains:
```
USER: Write a comma separated list of the first 10 digits of pi
ASSISTANT:
```
`prompter.grammar` contains a LlamaGrammar object that can be passed to a llama-cpp-python model:
```
<llama_cpp.llama_grammar.LlamaGrammar object at 0x100e9d7f0
```

### Call llama-cpp-python

```
model = Llama(model_path="<path_to_your_model>", verbose=False)
response = model(prompter.prompt, grammar=prompter.grammar)
```

## Usage

### Basic example
```
import json
from llama_cpp import Llama
from llama_prompter import Prompter

model = Llama(model_path="<path_to_your_model>", verbose=False)
prompter = Prompter(
    """[INST] Describe the moon[/INST]
Short description: {description:str}
Distance from Earth in miles: {distance:int}
Diameter in miles: {diameter:int}
Gravity in Gs: {gravity:float}"""
)

response = model(
    prompter.prompt,
    grammar=prompter.grammar,
    stop=["[INST]", "[/INST]"],
    temperature=0,
    max_tokens=2048
)
completion = response['choices'][0]['text']
variables = prompter.decode_response(completion)

print(prompter.prompt)
print(completion)
print('\nVariables:')
print(json.dumps(variables, indent=4))
```
Output:
```
[INST] Describe the moon[/INST]
Short description:
"The Moon is Earth's only permanent natural satellite, orbiting our planet at an average distance of about 384,400 kilometers. It is roughly spherical in shape with a diameter of about 3,474 kilometers and has no atmosphere or magnetic field. The surface of the Moon is rocky and dusty, and it is covered in impact craters, mountains, and vast, flat plains called maria."
Distance from Earth in miles: 238855
Diameter in miles: 2159
Gravity in Gs: 0.1655

Variables:
{
    "description": "The Moon is Earth's only permanent natural satellite, orbiting our planet at an average distance of about 384,400 kilometers. It is roughly spherical in shape with a diameter of about 3,474 kilometers and has no atmosphere or magnetic field. The surface of the Moon is rocky and dusty, and it is covered in impact craters, mountains, and vast, flat plains called maria.",
    "distance": 238855,
    "diameter": 2159,
    "gravity": 0.1655
}
```
### Advanced example with pydantic

```import json
from pydantic import BaseModel
from llama_cpp import Llama
from llama_prompter import Prompter

class Planet(BaseModel):
    name: str
    short_description: str
    diameter_miles: int
    distance_from_earth_miles: int
    gravity: float

model = Llama(model_path="<path_to_your_model>", verbose=False)
prompter = Prompter(
    """[INST] Describe the moon[/INST]
{moon:Planet}"""
)

response = model(
    prompter.prompt,
    grammar=prompter.grammar,
    stop=["[INST]", "[/INST]"],
    temperature=0,
    max_tokens=2048
)
completion = response['choices'][0]['text']
variables = prompter.decode_response(completion)
planet = variables['moon']

print(prompter.prompt)
print(completion)

print('\nPlanet model:')
print(planet.model_dump_json(indent=4))
```
Output:
```
[INST] Describe the moon[/INST]

{"name":"Moon","short_description":"The Moon is Earth's only permanent natural satellite and is about one-quarter the size of our planet. It orbits around Earth at an average distance of about 238,900 miles (384,400 kilometers) and takes approximately 27.3 days to complete one orbit.","diameter_miles":2159,"distance_from_earth_miles":238900,"gravity":0.165}

Planet model:
{
    "name": "Moon",
    "short_description": "The Moon is Earth's only permanent natural satellite and is about one-quarter the size of our planet. It orbits around Earth at an average distance of about 238,900 miles (384,400 kilometers) and takes approximately 27.3 days to complete one orbit.",
    "diameter_miles": 2159,
    "distance_from_earth_miles": 238900,
    "gravity": 0.165
}
```

## Development

### Dependencies
```
python -m pip install poetry poethepoet
```

### Running tests, linters, mypy
```
poe check
```


## License

llama-prompter is released under the MIT License.
