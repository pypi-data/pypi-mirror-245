# PokeAPI SDK for Python

The PokeAPI SDK for Python provides a scoped demo of using Python to create an SDK for a REST api.

## Preamble

This is a small demo of a Pokeapi SDK written in python which covers the `Pokemon`, `Nature` and `Stat` endpoints of PokeAPI only.

The main packages/tools used are:

- `requests` - to ensure code readability and maintainability when interacting with the PokeAPI
- `pytest` - for testing
- GitHub Actions - for automated testing and deployment
- Pypi - for hosting the built pip package

The first versions I came up with for this project were returning JSON objects which, while easy to work with in Python, did not feel native enough.

I therefore restructured the project to use classes for a better object-orientated experience. Code generation via ChatGPT was helpful for filling gaps, particularly as PokeAPI has a lot of nested types in the responses to the `pokemon` endpoint - writing this out manually would have cost a lot of time and would be prone to errors.

While the main 3 methods mirror PokeAPI, I decided to add a fourth method `get_pokemon_full_details` which helps to amalgamate the other methods together. As previously mentioned, PokeAPI has a lot of nested types, but it does not retrieve the full details on the request for a Pokemon. This method therefore also resolves any Nature and Stat information and provides this alongside the normal `Pokemon` object.

The basic premise of the way this repo is set up is that on each push, the package is tested then published, via GitHub Actions, to Pypi, ready to be installed via Pip. Of course, as this is only a demo it simply runs this in a dumb fashion on each push (in the real world this would be configured differently).

As a little stretch goal, I did get ChatGPT to generate an OpenAPI spec based on my SDK and than ran this through SpeakEasy. The result is [here](https://github.com/speakeasy-sdks/bytesguy-sample-sdk), however I have not had chance to test this yet! It would be interesting to see how this compares to my "source" SDK.

## Installation

The SDK demo can be installed into your Python environment via Pip:

```
pip install pokeapi-sdk-demo
```

Full details can be found on the [Pypi project page](https://pypi.org/project/pokeapi-sdk-demo/).

## Usage

After installation, you can import the package into your project with `import pokeapi_sdk` at the top of your file.

You can then instantiate an SDK client with `client = pokeapi_sdk.PokeAPISDK()`. See below examples for how to get started with the SDK. 

Note that the SDK demo only covers the `Pokemon`, `Nature` and `Stat` endpoints of PokeAPI. 

An additional method, `get_pokemon_full_details()`, has been provided which combines nested retrieval of details. For example, if a Pokemon has a Nature, rather than just returning the Pokeapi URL for that Nature, this method will resolve the Nature into a Nature object.

### Examples

Retrieving Pokemon details from the ID number:

```
pokemon = client.get_pokemon(1)
print (pokemon.name)

>>> bulbasaur
```

Retrieving Pokemon ability from the name:

```
pokemon = client.get_pokemon('bulbasaur')
print (pokemon.abilities[0].ability.name)

>>> overgrow
```

Retrieving Nature details from an ID number:

```
nature = client.get_nature(1)
print (nature.name)

>>> 'hardy'
```

Retrieving Stat information from name:

```
stat = client.get_stat('hp')
stat.game_index

>>> 1
```

## Testing

Testing is done via Pytest, which needs to be installed prior to running `pip install pytest` or via the requirements file `pip install -r requirements.txt`.

Then run `pytest` to run all the tests in the [test](tests/) directory. Sample output:

```
========================= test session starts ==========================
platform darwin -- Python 3.10.13, pytest-7.1.3, pluggy-1.0.0
rootdir: /Users/adam/GitHub/pokeapisdkdemo
plugins: testinfra-6.8.0
collected 8 items                                                      

tests/nature_test.py ..                                          [ 25%]
tests/pokemon_test.py ....                                       [ 75%]
tests/stat_test.py ..                                            [100%]

========================== 8 passed in 1.72s ===========================
```

Testing is also automated via GitHub Actions on each push to the repo ([example pipeline](https://github.com/BytesGuy/pokeapisdkdemo/actions/runs/7133047284/job/19424902120))