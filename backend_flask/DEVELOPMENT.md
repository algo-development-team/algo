# Development Guide

- `# DEBUG` comment for print statements solely for debugging, should be removed at production code.
- `# FOR TESTING ONLY` comment for variables used for testing, should be removed at production code.
- `# TEST` with comment block contain code that are used for temporary, manual testing, should be migrated to proper testing at production code.
- `# FUTURE CHANGES` comment is for changes that are not necessary, but can be done in the future for runtime efficiency.
- `# helper function` are functions with specific inputs and outputs that are designed for only one function, thus they should not be used beyond their intended use.
- ARRAY data types and references from database schemas must be called using their getter functions.
- Normal objects are deep copied within the called function if they are modified within the function.
