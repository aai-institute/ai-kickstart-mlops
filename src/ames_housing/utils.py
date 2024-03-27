"""Utilities."""

from typing import Union

from dagster import InputContext, OutputContext


def get_metadata(context: Union[OutputContext, InputContext]) -> dict:
    if isinstance(context, OutputContext):
        return context.metadata
    else:  # type is InputContext
        return context.upstream_output.metadata
