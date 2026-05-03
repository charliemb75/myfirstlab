# Lab 7: Python Low-Code - Lab Summary

## Path Chosen
I chose **Path 1** - refactored my own existing code from Lab 4.

## Improvements Made
See [refactoring_checklist.txt](refactoring_checklist.txt) to review the improvements made between the original code and the refactored version.

## Key Learnings
1. **Importance of Single-Action Functions**: Functions that perform one single action are more reusable and maintainable, rather than functions that try to do everything at once. Then, multiple chained functions perform all required steps in the code, creating a more modular and flexible architecture.

2. **Error Handling and User Experience**: The ability to predict possible errors in the code and handle them in a useful way for the user is critical for creating robust applications.

## Main Challenge Beyond Lab Purpose
**API Error 429 (Rate Limiting)**: Encountered rate limiting issues when using the OpenAI API, changed to **Cohere** as the alternative LLM provider.

## Results
The refactored code produced **comparable results** with both versions:
- Original code (Lab 4) / Refactored code (Lab 7)
- New LLM (Cohere)