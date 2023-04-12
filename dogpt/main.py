import ast
import logging
import os

import openai
import typer

from dogpt.constants import ROUTINES_SPEC, SUPERPROMT_PATTERN
from dogpt.validators import ProgramValidator, SyntaxSafetyValidator


logger = logging.getLogger(__name__)


def main(prompt: str):
    superprompt = SUPERPROMT_PATTERN.format(prompt=prompt)
    logger.info(superprompt)

    # Set up your OpenAI API key
    openai.api_key = os.environ["OPENAI_API_KEY"]

    # Use the OpenAI API to generate text from ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": superprompt}],
    )

    # Print the generated text
    code = response.choices[0].message.content
    logger.info(code)

    code = code.strip("`")

    program_validator = ProgramValidator()
    program_validator.validate(code)

    syntax_tree = ast.parse(code)
    syntax_validator = SyntaxSafetyValidator(safe_func_ids=set(ROUTINES_SPEC))
    syntax_validator.validate(syntax_tree)

    locals = {
        routine_alias: routine_spec["callable"]
        for routine_alias, routine_spec in ROUTINES_SPEC.items()
    }
    exec(code, locals, {})


if __name__ == "__main__":
    typer.run(main)
