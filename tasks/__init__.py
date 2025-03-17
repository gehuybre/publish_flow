"""
Package initialization for tasks module.
"""
from .strategy_task import StrategyTask
from .writing_task import WritingTask
from .fact_checking_task import FactCheckingTask
from .editing_task import EditingTask
from .copywriting_task import CopywritingTask
from .quality_assessment_task import QualityAssessmentTask
from .html_formatting_task import HTMLFormattingTask

__all__ = [
    'StrategyTask',
    'WritingTask',
    'FactCheckingTask',
    'EditingTask',
    'CopywritingTask',
    'QualityAssessmentTask',
    'HTMLFormattingTask'
]