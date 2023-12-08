import warnings

from enfobench import Model, ModelInfo


def assert_model_provides_info(model: Model) -> None:
    """Raises an assertion error if the not correct ModelInfo is provided."""
    try:
        model_info = model.info()
    except NameError as e:
        msg = f"Model {model} does not provide an info() method."
        raise AssertionError(msg) from e

    if not isinstance(model_info, ModelInfo):
        msg = f"Model {model} does not provide a ModelInfo object."
        raise AssertionError(msg)

    if not isinstance(model_info.name, str) or not model_info.name:
        msg = f"Model {model} does not provide a valid name."
        raise AssertionError(msg)

    if not model_info.authors:
        warnings.warn(f"Model {model} does not provide any authors.", UserWarning, stacklevel=2)


def assert_model_forecasts(model: Model, horizon: int) -> bool:
    ...
