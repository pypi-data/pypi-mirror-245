"""
Module: string_expected_result_evaluator.py

This module defines the StringExpectedResultEvaluator class, which is used for
evaluating string expected results.

Classes:
    StringExpectedResultEvaluator: Class for evaluating string expected
    results.

"""

import json

from ..schemas.evaluator_config import (
    EvaluatorOutput,
    EvaluatorType,
    ExpectedResultEvaluatorConfig,
    MatchingTechnique,
    MethodCalculationMethod,
    MetricCalculatorConfig,
)
from ..schemas.experiment_config import ExperimentResult
from .base_evaluator import BaseEvaluator
from .utils import fuzzy_match_util


def is_valid_json(s: str) -> bool:
    """
    Check if the given string is a valid JSON.

    Args:
        s (str): The input string to check.

    Returns:
        bool: True if the input string is a valid JSON, False otherwise.

    """

    try:
        json.loads(s)
        return True
    except ValueError:
        return False


class StringExpectedResultEvaluator(BaseEvaluator):
    """
    Class for evaluating string expected results.

    This class extends the BaseEvaluator and provides specific implementation
    for evaluating string expected results using different matching techniques.

    Attributes:
        config (ExpectedResultEvaluatorConfig): Configuration object for the
                                                evaluator.

    """
    default_config = ExpectedResultEvaluatorConfig(
        matching_technique=MatchingTechnique.INCLUDES,
        evaluator_type=EvaluatorType.INDIVIDUAL,
        name="string_expected_result",
        metric_calculators=[
            MetricCalculatorConfig(
                MethodCalculationMethod(MethodCalculationMethod.AVERAGE)
            )
        ]
    )

    def __init__(self, config: ExpectedResultEvaluatorConfig):
        """
        Initialize the StringExpectedResultEvaluator with the provided
        configuration.

        Args:
            config (ExpectedResultEvaluatorConfig): Configuration object for
            the evaluator.

        """
        super().__init__(config)
        self.config: ExpectedResultEvaluatorConfig = config

    def evaluate(self, experiment_result: ExperimentResult) -> EvaluatorOutput:
        """
        Evaluate the expected result against the actual result using the
        specified matching technique.

        Returns:
            EvaluatorOutput: An EvaluatorOutput object containing the
            evaluation result.

        """
        input_data = experiment_result.input_data
        raw_output = experiment_result.raw_output.text_output
        expected_result = input_data.expected_result
        is_match = False
        technique = MatchingTechnique(self.config.matching_technique)
        # Default to empty strings if the values are None
        output_text = raw_output if raw_output is not None else ""
        expected_text = expected_result if expected_result is not None else ""
        if technique == MatchingTechnique.FUZZY_MATCH:
            if not expected_result:
                is_match = True
            else:
                is_match = fuzzy_match_util(output_text, expected_text)
        elif technique == MatchingTechnique.JSON_VALIDATOR:
            is_match = is_valid_json(output_text)
        elif technique == MatchingTechnique.MATCH:
            if not expected_result:
                is_match = True
            else:
                is_match = expected_result == output_text
        elif technique == MatchingTechnique.INCLUDES:
            if not expected_result:
                is_match = True
            else:
                is_match = expected_result in output_text

        result = 1 if is_match else 0
        return EvaluatorOutput(
            name=self.config.name,
            display_name="matching",
            result=result,
            metric_calculators=self.config.metric_calculators
        )


BaseEvaluator.register_evaluator(
    "string_expected_result", StringExpectedResultEvaluator,
    ExpectedResultEvaluatorConfig
)
