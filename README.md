# LLM HTML Solutions

Compare different methods of preparing web pages for use with an LLM

Some experiments with using raw html vs stripping tags vs converting to markdown
against a 3 axis:

**Formats:**

- `html`: Raw HTML
- `strip_tags`: HTML that has had all tags stripped
- `markdown`: HTML converted to Markdown

**Sections**:

- `all`: the entire web page is processed; everything returned from the `GET`
- `body`: everything within the `<body>` tags
- `content`: the main "content" of the page, as specified by a CSS selector. See the config for specifics on what constitutes the content of a given URL.

**Measurements:**

- `characters`: straight count of all characters, including whitespace TODO: define characters better - emoji = one character but we are counting as more than one for instance
- `words`: count of all words TODO: define words - probably split on whitespace + ":;=" or something?
- `tokens`: count of `cl100k_base` tokens

At this time I'm only concerned with OpenAI's `cl100k_base` tokenizer, as well as the GPT3.5 models. I would also love to test against GPT4, but Sam would need to bless me with a key to do that :'(

## Additional Environmental Information

- we should compare injecting additional info for a given page
- Full URL of page
- stuff in <head> ?
- If only the semantic web took off :(

## Problems

### What Web Pages to Use?

- Wikipedia is obvious, but using Wikipedia in training data with high weights is table stakes at this point
  - Wikipedia pages with dates after the cutoff - this may be easier said than done
    - pages about events - try to stick to non-controversial ones (does such a thing exist)
- Me (the author of this) needs to be familiar enough with the subject matter in question to evaluate the (likely subtle) differences in quality of responses

### How to Evaluate Responses?

- I'm not the first to try to do this, so probably should look into prior art

### What Does it Mean to Convert to Markdown?

- look into prior art
  - pandoc
  - LlamaIndex retrievers (?)
- there is metadata in html that may be lost
  - anything in head
    - what is in head that we might care about?
    - this is lost with `strip-tags` also
- what do we definitely want to retain?
  - headings
  - links
  - lists (ordered and unordered)
  - whitespace (newlines mostly)
  - forms ?

### Extremely Dynamic Pages

- all my homies hate SPA's
- we can take a screenshot of the page and OCR it?
  - pretty sure this is a thing? need to look at prior art

### I Don't Have Access to GPT4

- :(
