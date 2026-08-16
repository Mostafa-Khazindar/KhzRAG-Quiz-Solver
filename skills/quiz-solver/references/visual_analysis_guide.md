# Visual Analysis Guide

When the `advanced-quiz-solver` encounters PDFs or images, it must follow these rules to avoid missing critical data:

## 1. The "Invisible" Image Strategy
Sometimes a PDF contains diagrams that are drawn using vector lines rather than embedded images, or images that contain zero text. The Python search script (BM25) might fail to find these because it relies on text.
**If a question asks about an image/figure, and the search script finds nothing, you must:**
- Search the text for the *caption* or reference (e.g., search for "Figure 4", "Table 2", or "Diagram").
- Find the page where the text *talks* about the concept, and use `view_file` to look at that page AND the page immediately after it.
- **Note:** Your `view_file` tool renders the entire PDF page visually. You will be able to see vector graphics, embedded JPEGs, and scanned photos perfectly, even if the text-extractor missed them.

## 2. Do Not Hallucinate Graphs
If a chart is provided (e.g., a bar chart or scatter plot), read the X and Y axes carefully. Note the units of measurement before extracting data points.

## 3. Cross-Reference Text and Images
Often, a diagram is explained in the paragraph immediately preceding or following it. Always read the surrounding text to contextualize the image.

## 4. Handling Blurry/Unreadable Text
If a diagram is too low-resolution for you to confidently read the labels, state this explicitly in your answer: *"The diagram on page X is too blurry to confidently read the specific values for the Y-axis."* Do not guess.

## 5. Diagram Labels
Pay special attention to arrows, legends, and footnotes within the image. They often hold the key to the quiz answer.
