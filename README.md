## Data quality assistant for Athena data lake

Data quality is the most important aspect when building any reports or machine learning models based on data available in an enterprise data lake. When managing an Athena data lake professionally I would like to see an agent which can answer common questions like:

 - how do I get this piece of information (understanding data catalog)
 - When was this dataset last updated (data quality)
 - How is this particular column derived (lineage)
 - When I use this dataset can I make this assumption (provenance)


## Why are agents the right solution to this problem
Modern enterprise data lakes—such as those built on Amazon Athena—could contain hundreds of tables, tens of thousands of columns, and a constantly evolving set of ingestion pipelines, ETL jobs, and business rules.

While organizations typically maintain metadata systems such as Glue Data Catalog, lineage tools, dashboards, and wikis, the knowledge about data quality, provenance, and usage patterns is fragmented across many systems and often locked in tribal knowledge.

An LLM-agent–based solution is uniquely suited to this problem for several reasons:

### 1. Natural-language querying of complex metadata
A large language model can interpret ambiguous or conversational questions like:

 - “Where do I find customer churn metrics?”
 - “What table contains the canonical definition of a transaction?”
  
Instead of requiring the user to navigate Glue Catalog, query logs, lineage tools, application source code and documentation separately, an LLM agent can integrate these sources and provide intuitive, plain-English answers. This removes friction for analysts, engineers, and product managers who may not know the structure of the data lake.

### 2. Reasoning across structured and unstructured metadata
Data quality signals exist across multiple layers:

 - Technical metadata (Glue/Athena table definitions)
 - Operational metadata (update timestamps, job logs, job statuses, pipeline failures)
 - Business metadata (wiki pages, Confluence docs, slack threads)
 - Lineage graphs (ETL tools, event logs)
 - Data quality rules and monitoring outputs (e.g., Great Expectations, Soda)

An LLM agent can reason across all of these by synthesizing information rather than requiring rigid schemas or brittle rule-based systems. This makes it well-suited for answering questions like:

 - “When was this dataset last refreshed?”
 - “What upstream sources does this column depend on?”

Such questions typically require joining information across multiple systems—something LLMs excel at when combined with retrieval tools.

### 3. Explaining derivation and lineage in human terms
Lineage tools often represent relationships as graphs or JSON blobs. They are technically correct but not human-friendly.

An LLM agent can translate technical lineage (“column X is produced by Spark job Y reading from S3 prefix Z…”) into crisp, concise explanations:

“This column comes from the Finance ETL pipeline and is derived from daily trades data aggregated by order ID.”

This supports onboarding, data literacy, and reduces reliance on subject-matter experts.

### 4. Providing judgment and guidance on assumptions (provenance)
One of the hardest problems in data engineering is helping users understand whether a dataset is fit for purpose.

Questions like:

 - “Can I assume this field is unique?”
 - “Is it safe to use this column for customer segmentation?”
require a combination of rule interpretation, historical patterns, data quality metrics, domain context and provenance. LLM agents can give context-aware, probabilistic advice based on available metadata, plus point users toward authoritative documentation or warn them if information is incomplete.

### 5. Reducing operational overhead and democratizing data access
Without such a system, data lake teams spend a huge amount of time answering questions on Slack:

 - “What does account_id mean here?”
 - “Is this table still maintained?”
 - "How often is this table used?"
 - “Why does the date only update once a week?”
  
An LLM agent acts as an always-available first responder, reducing load on data engineering teams while making data  - knowledge accessible to the entire organization (data democratisation).


### 6. Future-proof, adaptive, and incrementally improvable
Unlike rule-based chatbots or static documentation, an LLM agent:

 - Improves as more metadata becomes available
 - Adapts to schema changes automatically
 - Scales with the size and complexity of the data environment
 - Can learn organizational domain model language and conventions
  
This makes it a long-term strategic asset rather than a static tool.

