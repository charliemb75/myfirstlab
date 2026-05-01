# News Summarizer

A Python command-line app that fetches top headlines from NewsAPI, summarizes each article with OpenAI, analyzes sentiment with Cohere, and prints a cost-aware news summary report.

## Features

- Fetches top headlines by category.
- Supports synchronous and concurrent article processing.
- Uses OpenAI for article summaries.
- Uses Cohere for sentiment analysis.
- Falls back to Cohere if OpenAI summarization fails.
- Tracks estimated token usage and API cost.
- Includes unit tests with mocked API calls.

## Project Structure

```text
.
+-- config.py           # Environment and application configuration
+-- llm_providers.py    # OpenAI/Cohere clients, fallback logic, and cost tracking
+-- main.py             # CLI entry point
+-- news_api.py         # NewsAPI integration
+-- summarizer.py       # Article summarization workflow
+-- test_summarizer.py  # Unit tests
+-- requirements.txt    # Python dependencies
```

## Requirements

- Python 3.10+
- NewsAPI API key
- OpenAI API key
- Cohere API key

## Setup

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
COHERE_API_KEY=your_cohere_api_key
NEWS_API_KEY=your_newsapi_key

# Optional settings
ENVIRONMENT=development
MAX_RETRIES=3
REQUEST_TIMEOUT=30
DAILY_BUDGET=5.00
```

## Usage

Run the app:

```powershell
python main.py
```

The CLI will ask for:

- A news category, such as `technology`, `business`, `health`, or `general`.
- The number of articles to process, from 1 to 10.
- Whether to use async processing.

Example interaction:

```text
Enter news category (technology/business/health/general): technology
How many articles to process? (1-10): 3
Use async processing? (y/n): y
```

After processing, the app prints a report with each article's title, source, URL, summary, sentiment, and estimated API cost summary.

## Running Tests

```powershell
pytest -v
```

The tests mock external API calls, so they can validate the core behavior without making real requests.

## Notes

- The `.env` file is ignored by Git and should not be committed.
- API usage may incur costs depending on your OpenAI, Cohere, and NewsAPI plans.
- The default models are configured in `config.py`.


# Example Output

✓ Configuration validated for development environment
================================================================================
NEWS SUMMARIZER - Multi-Provider Edition
================================================================================

Enter news category (technology/business/health/general): sports
How many articles to process? (1-10): 3
Use async processing? (y/n): y

Fetching 3 articles from category: sports
✓ Fetched 3 articles from News API

Processing 3 articles concurrently...

Processing: 4 takeaways: Cade Cunningham, Paolo Banchero engage in duel ...
  → Summarizing with OpenAI...

Processing: Braves To Activate Spencer Strider On Sunday - MLB Trade Rum...
  → Summarizing with OpenAI...

Processing: LIV Golf reportedly loses Saudi funding as tour's future loo...
  → Summarizing with OpenAI...
  ✓ Summary generated
  → Analyzing sentiment with Cohere...
  ✓ Summary generated
  → Analyzing sentiment with Cohere...
  ✓ Sentiment analyzed
  ✓ Summary generated
  → Analyzing sentiment with Cohere...
  ✓ Sentiment analyzed
  ✓ Sentiment analyzed

================================================================================
NEWS SUMMARY REPORT
================================================================================

1. 4 takeaways: Cade Cunningham, Paolo Banchero engage in duel for the ages in Game 5 - NBA
   Source: Google News | Published: 2026-04-30T04:54:06Z
   URL: https://news.google.com/rss/articles/CBMieEFVX3lxTE1BZl9VZzBXNmZHU25HM1BmTWtIVThwdXpGakMtc0VuMHpWQTh3TWZleUZhZVRXQ0hKNnp4YUxWMFljMmFocnZXcUw0RGhvckdCWENsNk4xR0lmOWl5V3pMMDZMY0ZJeDZEbUZjVjcwU2dPcE45V0kzNg?oc=5

   SUMMARY:
   In a thrilling Game 5, Cade Cunningham and Paolo Banchero showcased their exceptional skills in a high-scoring duel, captivating fans and setting the stage for an intense playoff series. Both players delivered standout performances, with Cunningham's playmaking and Banchero's scoring prowess adding drama to the matchup. The game highlighted their potential as future stars in the league and left fans eager for what’s next in the postseason.

   SENTIMENT:
   **Overall Sentiment:** Positive

**Confidence:** 95%

**Key Emotional Tone:** Enthusiastic and hopeful. The text conveys excitement and anticipation for the players' future success, emphasizing their standout performances and the thrilling nature of the game.

   ----------------------------------------------------------------------------

2. Braves To Activate Spencer Strider On Sunday - MLB Trade Rumors
   Source: Google News | Published: 2026-04-30T03:56:01Z
   URL: https://news.google.com/rss/articles/CBMikgFBVV95cUxOaTFyTFNnYTJETzZkaUtGUDdpdjg3VlZPYXF0Y0dadkZadjVZY1RuLUpNRmRIRHRPTXo1TlBjMkhLTnFtNk1mWW05NGFQRjlXT0FxNEdFOFlMellTWXRJMWhSNEJEVDdKTHpwMWppNzQxRTRocmNrSFF1VUI2bkZ2RWZYeVZGS2Z2cjFuM1VTM1hGQQ?oc=5

   SUMMARY:
   The Atlanta Braves are set to activate pitcher Spencer Strider from the injured list on Sunday. Strider has been recovering from an injury and is expected to bolster the Braves' pitching rotation as they approach the postseason. His return is seen as a significant boost for the team's playoff aspirations.

   SENTIMENT:
   **Overall Sentiment:** Positive
**Confidence:** 95%
**Key Emotional Tone:** Enthusiasm and optimism.

The text conveys a positive sentiment, indicating excitement and anticipation for the Braves' upcoming success in the postseason with the return of Spencer Strider. The language used suggests a confident expectation of a positive impact on the team's performance.

   ----------------------------------------------------------------------------

3. LIV Golf reportedly loses Saudi funding as tour's future looks murky - Axios
   Source: Google News | Published: 2026-04-30T03:38:20Z
   URL: https://news.google.com/rss/articles/CBMiY0FVX3lxTE9JLXMybE81VGp4U1lUQ0RTTE14YnhCUjR2b3ctVkgxSS1aa3RBSjJZaVlKMlR5cDNVamhjMFNVZllsdUZVSU1XMTVaRldPekxId2NVaENBUE5ZcFQ0NU9VYUtwZw?oc=5

   SUMMARY:
   LIV Golf is reportedly losing financial backing from Saudi sources, raising concerns about the tour's future viability. This development adds to the uncertainty surrounding the league's long-term prospects and its ability to attract top players. As the situation evolves, stakeholders are closely monitoring the implications for competitive golf.

   SENTIMENT:
   **Overall Sentiment:** Negative
**Confidence:** 85%
**Key Emotional Tone:** Concern and Uncertainty

The text conveys a negative sentiment due to the mention of financial backing issues and concerns about the tour's future, which are described as "raising concerns" and adding to "uncertainty." The language suggests a sense of worry and doubt about LIV Golf's stability and ability to sustain itself, which is further emphasized by the focus on the implications for competitive golf.

   ----------------------------------------------------------------------------

================================================================================
COST SUMMARY
================================================================================
Total requests: 6
Total cost: $0.0055
Total tokens: 995
  Input: 522
  Output: 473
Average cost per request: $0.000913
================================================================================

✓ Processing complete!