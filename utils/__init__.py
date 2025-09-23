"""Utility package exports.

This module implements lazy attribute access so importing `utils`
doesn't immediately import heavy optional dependencies (audio,
PDF parsing, TTS, etc.). Attributes are loaded on demand.
"""
from typing import Any
import importlib
import types

_EXPORTS = {
    "analyze_candidate_response_and_generate_new_question": (
        "analyze_candidate", "analyze_candidate_response_and_generate_new_question"
    ),
    "get_feedback_of_candidate_response": ("analyze_candidate", "get_feedback_of_candidate_response"),
    "load_content": ("load_content", "load_content"),
    "load_content_streamlit": ("load_content", "load_content_streamlit"),
    "validate_audio_file": ("record_utils", "validate_audio_file"),
    "record_audio_with_interrupt": ("record_utils", "record_audio_with_interrupt"),
    "reduce_noise": ("record_utils", "reduce_noise"),
    "save_interview_data": ("save_interview_data", "save_interview_data"),
    "speak_text": ("text_to_speech", "speak_text"),
    "transcribe_with_speechmatics": ("transcript_audio", "transcribe_with_speechmatics"),
    "get_ai_greeting_message": ("basic_details", "get_ai_greeting_message"),
    "extract_resume_info_using_llm": ("basic_details", "extract_resume_info_using_llm"),
    "get_final_thanks_message": ("basic_details", "get_final_thanks_message"),
    "get_overall_evaluation_score": ("evaluation", "get_overall_evaluation_score"),
    "basic_details": ("prompts", "basic_details"),
    "next_question_generation": ("prompts", "next_question_generation"),
    "feedback_generation": ("prompts", "feedback_generation"),
}


def __getattr__(name: str) -> Any:
    """Lazily import the requested attribute from the appropriate submodule."""
    if name in _EXPORTS:
        module_name, attr_name = _EXPORTS[name]
        module = importlib.import_module(f"utils.{module_name}")
        return getattr(module, attr_name)
    raise AttributeError(f"module 'utils' has no attribute '{name}'")


def __dir__() -> list[str]:
    return sorted(list(_EXPORTS.keys()))

