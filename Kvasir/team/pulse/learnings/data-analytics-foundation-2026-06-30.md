# Data Analytics Foundation — 2026-06-30

> PULSE study of top open-source data tools for the JACOB Team ecosystem.

---

## 1. Tool Comparison Table

| Tool | Stars | Language | License | Type | Best For | Steepness |
|------|-------|----------|---------|------|----------|-----------|
| **Polars** | 38.9K | Rust + Python | MIT | DataFrame Engine | Fast ETL, large datasets, streaming | Low-Medium |
| **DuckDB** | 39.1K | C++ | MIT | In-Process OLAP | Ad-hoc SQL analytics, Parquet/CSV queries | Low |
| **Streamlit** | 45.1K | Python + TS | Apache 2.0 | Data App Framework | Rapid internal dashboards, prototypes | Very Low |
| **Apache Superset** | 73.6K | TS + Python | Apache 2.0 | BI Platform | Enterprise BI, multi-source dashboards, teams | Medium |
| **Plotly Dash** | 24.3K | Python + TS | MIT | Dashboard Framework | Complex interactive dashboards, production apps | Medium-High |

### Core Differentiators

| Feature | Polars | DuckDB | Streamlit | Superset | Dash |
|---------|--------|--------|-----------|----------|------|
| UI / Frontend | No | No (CLI) | Yes | Yes | Yes |
| SQL Support | Yes (via sql) | Native | No | Yes (SQL Lab) | No |
| In-Memory Engine | Yes | Yes | No | No | No |
| Larger-than-RAM | Yes (streaming) | Yes (spilling) | N/A | N/A | N/A |
| No-Code Charts | No | No | No | Yes | No |
| Multi-User / Auth | No | No | No (Cloud has) | Yes | Enterprise only |
| REST API | No | No | No | Yes | Enterprise only |
| Embeddable | Yes (library) | Yes (library) | Yes (iframe) | Yes (iframe) | Yes (native/iframe) |

---

## 2. Setup Guide for Each Tool

### 2.1 Polars

```bash
# Install — zero required dependencies
pip install polars

# For >4.2 billion rows (bigidx support)
pip install 'polars[bigidx]'

# For older CPUs without AVX
pip install 'polars[compat]'

# Quick test
python -c "import polars as pl; df = pl.read_csv('data.csv'); print(df.head())"
```

**Key imports:**
```python
import polars as pl

# Lazy API (recommended for performance)
q = pl.scan_csv("sales.csv").filter(pl.col("amount") > 1000).group_by("region").agg(pl.col("amount").sum())
df = q.collect()

# Eager API
df = pl.read_csv("sales.csv")
df.filter(pl.col("amount") > 1000)
```

### 2.2 DuckDB

```bash
# Python install
pip install duckdb

# CLI — download from duckdb.org or:
pip install duckdb-cli
# Then: duckdb

# Quick test
python -c "import duckdb; print(duckdb.sql(\"SELECT 'Hello' AS greeting\").fetchall())"
```

**Use cases — query files directly:**
```sql
-- Query a CSV without loading it
SELECT region, SUM(amount) FROM 'sales_2026.csv' GROUP BY region;

-- Join CSV and Parquet on the fly
SELECT a.*, b.category
FROM 'transactions.parquet' a
JOIN 'product_map.csv' b ON a.product_id = b.id;

-- Export results
COPY (SELECT * FROM 'big_data.parquet' WHERE region = 'TH') TO 'thailand_data.parquet';
```

### 2.3 Streamlit

```bash
pip install streamlit

# Verify
streamlit hello

# Run an app
streamlit run app.py
```

**Minimal app:**
```python
import streamlit as st
import polars as pl

st.title("JACOB Team Sales Dashboard")
df = pl.read_csv("sales.csv")
st.dataframe(df)
st.bar_chart(df.group_by("region").agg(pl.col("revenue").sum()).to_pandas())
```

### 2.4 Apache Superset

```bash
# Docker Compose (fastest path)
git clone https://github.com/apache/superset.git
cd superset
docker compose -f docker-compose-non-dev.yml up -d

# OR pip install
pip install apache-superset
superset db upgrade
superset init
superset load_examples  # optional demo data
superset run -p 8088

# Access at http://localhost:8088 (admin / admin)
```

**After install:**
1. Add a database (Settings > Database Connections) — Postgres, MySQL, DuckDB, BigQuery, etc.
2. Create a dataset from a table or SQL query.
3. Build charts with the no-code chart builder.
4. Compose a dashboard from multiple charts.

### 2.5 Plotly Dash

```bash
pip install dash

# Quick test
python app.py
# Opens at http://localhost:8050
```

**Minimal app:**
```python
import dash
from dash import dcc, html, Input, Output
import polars as pl

df = pl.read_csv("sales.csv")
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(df["region"].unique().to_list(), id="region-dropdown"),
    dcc.Graph(id="sales-graph")
])

@app.callback(Output("sales-graph", "figure"), Input("region-dropdown", "value"))
def update_chart(region):
    filtered = df.filter(pl.col("region") == region)
    return {"data": [{"x": filtered["date"].to_list(), "y": filtered["revenue"].to_list()}]}

if __name__ == "__main__":
    app.run(debug=True)
```

---

## 3. Sample Use Cases for JACOB Team Marketing Data

The JACOB Team manages marketing across Thai market channels: Facebook, LINE, TikTok, Shopee, and Lazada. Here is how each tool applies:

### Use Case 1: Ad Spend Analytics (Polars + DuckDB)

```python
# Polars — crash multiple channel-level CSVs into one analysis
import polars as pl

fb_ads = pl.read_csv("fb_ads_daily.csv")
tiktok_ads = pl.read_csv("tiktok_ads_daily.csv")
shopee_ads = pl.read_csv("shopee_ads_daily.csv")

# Union all channels
all_ads = pl.concat([fb_ads, tiktok_ads, shopee_ads])

# Calculate ROAS per campaign
roas = (all_ads
    .group_by(["campaign", "channel"])
    .agg([
        pl.sum("spend").alias("total_spend"),
        pl.sum("revenue").alias("total_revenue"),
    ])
    .with_columns((pl.col("total_revenue") / pl.col("total_spend")).alias("ROAS"))
)

print(roas.sort("ROAS", descending=True))
```

```sql
-- DuckDB — same job in SQL
SELECT campaign, channel,
       SUM(spend) AS total_spend,
       SUM(revenue) AS total_revenue,
       SUM(revenue) / SUM(spend) AS ROAS
FROM read_csv_auto(['fb_ads_daily.csv', 'tiktok_ads_daily.csv', 'shopee_ads_daily.csv'])
GROUP BY campaign, channel
ORDER BY ROAS DESC;
```

### Use Case 2: GemLogin Profile Performance Dashboard (Streamlit)

Build an internal dashboard that reads GemPhoneFarm workflow logs and shows:
- Active profiles by device
- Success/fail rates per workflow
- Daily OTP arrival counts
- Proxy health status

```python
# streamlit_gemlogin_dashboard.py
import streamlit as st
import polars as pl
import duckdb

st.set_page_config(page_title="GemLogin Ops Dashboard", layout="wide")
st.title("GemPhoneFarm Fleet Dashboard")

logs = pl.read_parquet("workflow_logs.parquet")
con = duckdb.connect()

# Polars-fed DuckDB for SQL convenience
con.execute("CREATE TABLE logs AS SELECT * FROM logs")

active = con.execute("""
    SELECT device_id, COUNT(*) AS workflows_run,
           SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) AS successes
    FROM logs
    WHERE date = CURRENT_DATE
    GROUP BY device_id
""").fetchdf()

st.metric("Active Devices", active.shape[0])
col1, col2 = st.columns(2)
with col1:
    st.subheader("Per-Device Success Rate")
    st.dataframe(active)
with col2:
    st.subheader("Fleet Health")
    st.bar_chart(active.set_index("device_id")["successes"])
```

### Use Case 3: Multi-Source BI with Superset

Connect Superset to:
- **Postgres**: campaign performance, CRM data
- **DuckDB file**: ad-hoc Parquet/CSV exports from GemLogin workflows
- **Google Sheets**: budget tracking (via Shillelagh connector)

Build a **"Marketing Command Center"** dashboard with:
- ROAS trend (line chart, 7-day rolling)
- Spend by channel (pie chart)
- Campaign ranking (table, sortable)
- OTP arrival SLA (gauge chart)
- MAP: Thai province-level lead density (geospatial)

### Use Case 4: Production Interactive Dashboard (Dash)

When the Streamlit prototype needs **multi-user authentication**, **URL-based state sharing**, or **background job processing**:

```python
# dash_marketing_ops.py — enterprise-grade
import dash
from dash import dcc, html, dash_table
import plotly.express as px
import polars as pl

app = dash.Dash(__name__, url_base_pathname="/marketing/")
df = pl.read_parquet("agg_marketing.parquet")
pdf = df.to_pandas()

app.layout = html.Div([
    html.H1("JACOB Team — Marketing Ops Center"),
    dcc.Tabs([
        dcc.Tab(label="ROAS Overview", children=[
            dcc.Graph(figure=px.line(pdf, x="date", y="ROAS", color="channel"))
        ]),
        dcc.Tab(label="Campaign Table", children=[
            dash_table.DataTable(pdf.to_dict("records"), page_size=20)
        ]),
    ])
])
```

---

## 4. Recommended Analytics Stack for JACOB Team

### Tier 1: Daily Analysis (Single machine, ad-hoc)

```
┌─────────────┐     ┌─────────────┐     ┌──────────────┐
│  DuckDB     │────▶│  Polars     │────▶│  Streamlit   │
│  (Raw data) │     │  (Transform)│     │  (Dashboard) │
└─────────────┘     └─────────────┘     └──────────────┘
```

**When to use:** Daily ad spend review, workflow success analysis, quick charting for team standup.

**Why:** DuckDB queries CSVs/Parquet directly — no loading step. Polars does fast group-bys and joins. Streamlit turns results into a shareable app in < 50 lines.

### Tier 2: Team BI (Shared, scheduled, multi-source)

```
┌──────────────┐
│  PostgreSQL  │────┐
│  (CRM data)  │    │
└──────────────┘    │   ┌────────────────┐
                    ├──▶│  Apache Superset│
┌──────────────┐    │   │  (BI Platform)  │
│  DuckDB      │────┘   └────────────────┘
│  (Ad-hoc)    │
└──────────────┘
```

**When to use:** Weekly team reports, cross-channel ROAS, campaign manager self-serve.

**Why:** Superset gives non-technical team members drag-and-drop charts. SQL Lab lets analysts write ad-hoc queries. DuckDB connector brings file-based data into the BI layer.

### Tier 3: Production Apps (Customer-facing, authenticated)

```
┌────────────┐    ┌────────────┐    ┌─────────────┐
│  Polars    │───▶│  Dash      │───▶│  Nginx/Auth │
│  (ETL)     │    │  (App)     │    │  (Proxy)    │
└────────────┘    └────────────┘    └─────────────┘
```

**When to use:** Client-facing reports, automated email PDF exports, multi-user dashboards with roles.

**Why:** Dash supports authentication (LDAP/OAuth), URL state, background job queues, and embedding in existing web apps. Polars handles the data layer with streaming for large exports.

---

## 5. Quick Reference: Install All Tools

```bash
# One-liner for a JACOB Team analytics workstation
pip install polars duckdb streamlit apache-superset dash
```

Docker-based (Superset only needs this):
```bash
# Superset — isolated from Python env
docker pull apache/superset
docker run -d -p 8088:8088 apache/superset
```

---

## 6. Ecosystem Map

```
                   ┌──────────────────┐
                   │   Raw Data       │
                   │  (CSV / Parquet  │
                   │   / Postgres /   │
                   │   API Logs)      │
                   └────────┬─────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
     ┌────────────────┐        ┌──────────────────┐
     │   DuckDB       │        │    Polars        │
     │  (SQL queries) │        │  (DataFrame API) │
     └────────┬───────┘        └────────┬─────────┘
              │                         │
              └──────────┬──────────────┘
                         │
                         ▼
          ┌──────────────────────────────┐
          │  Pick your Presentation Layer │
          └──────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
   ┌──────────┐   ┌──────────┐   ┌──────────┐
   │Streamlit │   │ Superset │   │   Dash   │
   │(Rapid)   │   │  (BI)    │   │(Prod)    │
   └──────────┘   └──────────┘   └──────────┘
```

---

## 7. Learning Path (Suggested Order)

1. **DuckDB** — 1 hour to learn. Query anything from the CLI immediately. Lowest friction.
2. **Polars** — 2-3 hours. If you know pandas, the `.group_by().agg()` pattern clicks fast. The lazy API takes another session.
3. **Streamlit** — 1 hour. Build a working dashboard in your first session.
4. **Apache Superset** — Half-day to set up, 1-2 hours to connect data and build first dashboard.
5. **Plotly Dash** — 2-3 days to go from zero to production-ready app with auth and callbacks.

---

*End of report — PULSE Data Analytics Foundation.*
