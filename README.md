# W3Schools Tutorials to Markdown 

A lightweight Python scraper that converts W3Schools tutorials into clean, organized Markdown files optimized for **Obsidian**.

## Features
- **Targeted Scraping:** Only grabs the DSA portion (Arrays, Stacks, Queues, Linked Lists, Sorting, etc.).
- **Obsidian Optimized:** - Adds YAML frontmatter (tags, source URL).
  - Converts HTML to ATX-style headers (`#`, `##`).
  - Preserves code blocks for syntax highlighting.
- **Auto-Cleanup:** Removes website navigation, ads, and "Try it Yourself" buttons for a distraction-free note-taking experience.
- **Slugified Filenames:** Saves files with clean names (e.g., `Linked_Lists.md`).
- 
### Prerequisites
Make sure you have Python 3.x installed and the following libraries:
```bash
pip install requests beautifulsoup4 markdownify
