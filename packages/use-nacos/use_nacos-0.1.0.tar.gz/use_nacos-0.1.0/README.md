# use-nacos

<a href="https://github.com/use-py/use-nacos/actions/workflows/test.yml?query=event%3Apush+branch%3Amain" target="_blank">
    <img src="https://github.com/use-py/use-nacos/workflows/test%20suite/badge.svg?branch=main&event=push" alt="Test">
</a>
<a href="https://pypi.org/project/use-nacos" target="_blank">
    <img src="https://img.shields.io/pypi/v/use-nacos.svg" alt="Package version">
</a>

<a href="https://pypi.org/project/use-nacos" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/use-nacos.svg" alt="Supported Python versions">
</a>

A python nacos client based on the official [open-api](https://nacos.io/zh-cn/docs/open-api.html).

## usage

## Developing

```text
make install             # Run `poetry install`
make lint                # Runs bandit and black in check mode
make format              # Formats you code with Black
make test                # run pytest with coverage
make publish             # run `poetry publish --build` to build source and wheel package and publish to pypi
```