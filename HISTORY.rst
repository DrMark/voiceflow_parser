=======
History
=======

0.3.0 (2025-05-01)
------------------

* Enhanced prompt handling and extraction:
  * Improved extraction of system prompts from programResources section
  * Added support for extracting message content from complex nested data structures
  * Created comprehensive prompt output files including complete_prompt.txt
  * Properly preserved role-specific content (system, user, assistant)
  * Added support for variable placeholders in prompts
* New detailed prompt output organization:
  * Added prompts_detailed.json with extracted content
  * Created role-specific message files (system_messages.txt, user_messages.txt)
  * Added complete_prompt.txt with full prompt specification
* Enhanced folder structure:
  * Implemented voiceflow_exports/ for original VF files
  * Created voiceflow_projects/ for generated project files

0.2.0 (2025-04-30)
------------------

* Added support for additional Voiceflow component types:
  * Buttons
  * Captures
  * APIs
  * Knowledge Base Searches
  * Choices
  * Cards
* Enhanced the parser service to extract and generate files for all component types
* Improved project structure generation with better organization
* Added progress tracking for file generation
* Updated README with comprehensive component information

0.1.0 (2025-04-28)
------------------

* First release.
