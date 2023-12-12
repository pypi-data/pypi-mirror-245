import io
import json
from functools import wraps
from time import time
from typing import Callable

import attrs
import click
from openai import OpenAI
from tqdm import tqdm

from .run import _run
from .suite import _update, pull_

in_tokens = 0
out_tokens = 0


@attrs.define()
class RunEvaluationResults:
    results_link: str


def parse_test_suite_id_from_url(test_suite_url: str) -> str:
    start_index = test_suite_url.find("test_suite_id=") + len("test_suite_id=")
    return test_suite_url[start_index:]


def run_evaluations(
    test_suite_url: str,
    generate_fn: Callable[[str], str],
    description="Ran automatically using the PRL SDK",
    maximum_threads=4,
    verbosity=1,
):
    test_suite_id = parse_test_suite_id_from_url(test_suite_url)
    in_mem_file = io.StringIO()

    pull_(in_mem_file, test_suite_id, include_id=True)

    in_mem_file.seek(0)
    suite_data = json.load(in_mem_file)

    if verbosity == 0:
        iterator = suite_data["tests"]
    else:
        iterator = tqdm(suite_data["tests"])

    global in_tokens, out_tokens
    metadata = {}
    for test in iterator:
        start = time()
        test["fixed_output"] = generate_fn(test["input_under_test"])
        end = time()
        metadata[test["id"]] = {
            "in_tokens": in_tokens,
            "out_tokens": out_tokens,
            "duration_seconds": end - start,
        }
        print("METADATA", metadata)
        in_tokens = 0
        out_tokens = 0

    # TODO: Going back and forth between files, strings, json etc. too much right now
    _update(test_suite_id, False, io.StringIO(json.dumps(suite_data)), True)
    run_url = _run(
        {
            "use_fixed_output": True,
            "description": description,
            "maximum_threads": maximum_threads,
        },
        test_suite_id,
        metadata_map=metadata,
    )

    if verbosity >= 1:
        click.secho(
            "Successfully updated test suite with new fixed outputs and started a new run.",
            fg="green",
        )
        click.secho(run_url, bold=True)

    return run_url


def wrap_chatcompletion(func: Callable):
    @wraps(func)
    def wrapper(**kwargs):
        response = func(**kwargs)
        global in_tokens, out_tokens

        in_tokens += response.usage.prompt_tokens
        out_tokens += response.usage.completion_tokens

        return response

    return wrapper


# External Facing
def patch(client: OpenAI):
    client.chat.completions.create = wrap_chatcompletion(client.chat.completions.create)
    return client
