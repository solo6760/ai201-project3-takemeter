# NBA Discourse Classification — planning.md

This document outlines the planning, data collection, labeling schema, evaluation metrics, and AI assistance strategy for classifying post titles from the **r/nba** subreddit.

---

## 1. Community Selection

### Choice & Rationale
We chose **r/nba** (Reddit's primary NBA community) as our target online community. With over 10 million subscribers, it is one of the most active, text-heavy, and discourse-dense communities on the internet. 

### Why r/nba is a Fit for Classification
The community is defined by a sharp contrast in discourse quality and intent:
*   **Tactical and Statistical Depth**: The subreddit has a dedicated group of users who post detailed, data-driven analytical write-ups (known as "Original Content" or `[OC]`) and serious tactical game analyses.
*   **Reactionary "Hot Takes"**: A massive volume of posts consists of hyperbolic, narrative-driven opinion pieces, player comparisons, emotional fan reactions, and trade speculations.
*   **Objective/Transactional Updates**: The subreddit serves as a news aggregator, with posts consisting of tweet links from NBA insiders (e.g., Wojnarowski, Charania), injury reports, official game results, and highlight video links.

This natural division makes the community a perfect fit for a text classification task, as the vocabulary, tone, and formatting of posts vary wildly based on these intentions.

---

## 2. Label Definitions

We define three mutually exclusive labels for the classification task:

### Label 1: `ANALYSIS` (Deep Analytical & Tactical Content)
*   **Definition**: Posts that provide deep, data-driven statistical analysis, salary cap/contract breakdowns, film study, or serious tactical breakdowns of players, teams, or games, often marked with `[OC]` or `[Serious]`.
*   **Example 1**: `"[OC] The Most Consistent 3-Point Shooters in the NBA - Volatility and Streakiness Analysis"`
*   **Example 2**: `"[SERIOUS NEXT DAY THREAD] Post-Game Discussion (May 05, 2026) - A tactical breakdown of the defensive schemes in the third quarter"`
*   **Uncertain Case**: `"Player X is shooting 20% from three over the last 5 games, showing he's completely washed and the team should trade him immediately."` (This contains a statistic but uses it to drive a subjective narrative. It belongs to `HOT_TAKE` because the primary intent is a reactionary opinion, not a deep analytical breakdown.)

### Label 2: `HOT_TAKE` (Subjective Fan Narrative & Opinion)
*   **Definition**: Posts focused on subjective opinions, player ranking debates, hyperbolic claims, rumors/gossip, emotional reactions, or community meta-discussions about players, teams, and the league.
*   **Example 1**: `"Adrian Wojnarowski also leaked MVP winners before they were officially announced. Notice the lack of outrage."`
*   **Example 2**: `"Write an r/NBA headline that might happen 5 to 10 years from now (2015 Classic)"`
*   **Uncertain Case**: `"If the Lakers sign Player Y to a $30M/year contract under the new CBA tax apron, is their championship window officially closed?"` (This blends transactional facts and cap terminology with a subjective question. It belongs to `HOT_TAKE` because the core of the post is inviting opinion/speculation rather than providing an objective update or deep analysis.)

### Label 3: `NEWS` (Transactional Updates & Objective Highlights)
*   **Definition**: Posts that report objective updates, official transactions, trade/signing announcements from verified reporters, official player/coach quotes, game scores (Post-Game Threads), or highlight video clips.
*   **Example 1**: `"[Wojnarowski] Thrilled to announce the hiring of @ShamsCharania, best young basketball reporter on the planet, to our NBA coverage team at Yahoo Sports"`
*   **Example 2**: `"[Highlight] Jaylen Brunson Finals Game 4, 2026 Full Play Highlights"`
*   **Uncertain Case**: `"[Highlight] Stephen Curry dances on the defender and hits a ridiculous, impossible circus shot to save the Warriors' season."` (Although the title uses highly subjective and sensationalized language, the post itself is a highlight clip. It belongs to `NEWS` because the primary content is an objective game play highlight.)

---

## 3. Hard Edge Cases & Annotation Rules

During annotation, we will resolve boundary conflicts using the following priority rules:

1.  **The Primary Intent Rule**: If a post contains statistical figures but its primary purpose is to make a hyperbolic point, stir debate, or complain about a player, it is labeled `HOT_TAKE`, not `ANALYSIS`. `ANALYSIS` is reserved for posts showing systemic investigation, multi-step statistics, or deep tactical breakdown.
2.  **The Content Format Rule**: Any post that is fundamentally sharing a media clip (`[Highlight]`), a journalist's tweet, or a standard match score (`[Post Game Thread]`) is labeled `NEWS`, even if the title uses colorful, subjective, or sensationalized language.
3.  **The Speculation vs. Transaction Rule**: Unconfirmed rumors and fan trade proposals are labeled `HOT_TAKE`. Confirmed transactions, official signings, and reporter announcements of finalised deals are labeled `NEWS`.

---

## 4. Data Collection Plan

### Source & Quantity
*   **Source**: Live and historical posts from `r/nba` using our custom Reddit API scraper (`reddit_post_collector.py`) and the interactive index dashboard (`nba_discourse_dashboard.html`).
*   **Target Count**: Exactly 200 labeled examples (approximately 65-70 posts per label).

### Underrepresentation Strategy
If a label (specifically `ANALYSIS`, which is less frequent in raw feeds than news or opinion) has fewer than 45 examples after collecting the initial 200 posts:
1.  We will run targeted keyword queries using Reddit's search API or search filters on `r/nba` (e.g., searching specifically for `"[OC]"`, `"[SERIOUS]"`, `"statistical breakdown"`, or `"film study"`).
2.  We will collect additional posts from those search results to balance the underrepresented label while maintaining the overall high-quality validation set.

---

## 5. Evaluation Metrics

To evaluate our classifier's performance, we will use the following metrics:

*   **Macro F1-Score (Primary Metric)**: Because the class distribution in a live feed is naturally imbalanced (high volume of `NEWS` and `HOT_TAKE`, low volume of `ANALYSIS`), accuracy alone would paint an overly optimistic picture. Macro F1-score averages the F1-score of each class equally, ensuring the model performs well on all three labels.
*   **Precision (specifically for `ANALYSIS`)**: For a community filter tool, false positives in the `ANALYSIS` category are highly disruptive. A user wanting to read high-quality analyses does not want their feed cluttered with misclassified hot takes. We want a high precision score for this label.
*   **Recall (specifically for `NEWS`)**: For users using the tool as a news reader, missing a major trade or game highlight (false negative in `NEWS`) is a bad user experience. Thus, high recall on `NEWS` is critical.
*   **Confusion Matrix**: We will analyze the confusion matrix to identify specific directional failures (e.g., how often `ANALYSIS` is misclassified as `HOT_TAKE`).

---

## 6. Definition of Success

We establish the following objective criteria to determine whether the classifier is ready for deployment in a real-world community filtering tool:

1.  **Macro F1-Score >= 0.82** across all three classes.
2.  **Precision for `ANALYSIS` >= 0.85**, ensuring that less than 15% of posts recommended as deep analysis are actually hot takes or news.
3.  **Accuracy >= 82%** overall.

These success criteria are specific and measurable, allowing us to objectively decide whether the model is ready for integration into a community dashboard or browser extension.

---

## 7. AI Tool Plan

This project uses AI tools at three key checkpoints to improve quality, efficiency, and depth of analysis:

### Part A: Label Stress-Testing
*   **AI Tool**: Gemini / Claude
*   **Input**: The three label definitions and current edge case rules listed in this document.
*   **Expected Output**: 8 generated synthetic post titles that lie on the boundaries between `ANALYSIS` vs. `HOT_TAKE` and `NEWS` vs. `HOT_TAKE`.
*   **Verification**: We will attempt to classify the AI-generated posts using our current definitions. If any post exposes a loophole or remains ambiguous, we will refine our label definitions and add explicit handling instructions to Section 3 before starting annotation.

### Part B: Annotation Assistance
*   **AI Tool**: LLM API (e.g., Gemini 3.5 Flash or Claude 3.5 Sonnet) via a script.
*   **Input**: The 200 collected post titles along with the label definitions.
*   **Expected Output**: A pre-labeled dataset containing predicted categories.
*   **Verification & Tracking**: To ensure absolute transparency and disclosure:
    *   We will add two metadata columns to our dataset: `is_prelabeled` (boolean) and `prelabeled_by` (string).
    *   A human annotator (ourselves) will manually review every single pre-labeled row, correcting any errors to create the final `gold_standard_label` column.
    *   Only the human-verified labels will be used for final training and evaluation.

### Part C: Failure Analysis
*   **AI Tool**: Gemini / Claude
*   **Input**: A list of all misclassified examples (Title, Gold Standard Label, Predicted Label) from our test set.
*   **Expected Output**: An identification of the top 3-4 semantic or structural patterns causing model failures (e.g., "model struggles with sarcasm", "numerical figures confuse opinion for analysis", "short titles default to news").
*   **Verification**: We will manually query our evaluation dataset to verify the frequency of the patterns identified by the AI tool, ensuring we can substantiate these claims in our final evaluation report.
