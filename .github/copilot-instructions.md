# Copilot Instructions

## MD-100: Markdown Line Limit

**Every generated Markdown file MUST NOT exceed 100 lines.**

If more content would be needed, produce a version that fits within 100 lines and add this frontmatter at the top:

```yaml
---
capped_at_100_lines: true
instruction: MD-100
trimmed_for_conciseness: |
  If more size is granted, this document would additionally cover:
  - [A] [brief description of first trimmed point]
  - [B] [brief description of second trimmed point]
  - [C] [brief description of third trimmed point]
---
```

List only the highest-priority trimmed points (A, B, C). Omit the frontmatter block entirely when the document is under 100 lines.
