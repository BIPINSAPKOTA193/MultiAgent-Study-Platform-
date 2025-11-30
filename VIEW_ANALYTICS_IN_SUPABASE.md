# How to View Analytics Data in Supabase UI

## ✅ Correct: There Are Only 2 Tables

When you look at your Supabase dashboard, you should see:
1. **`users`** - User accounts
2. **`rl_state`** - Contains ALL analytics data

**There is NO separate "analytics" table** - and that's correct! The analytics are stored **inside** the `rl_state` table.

---

## 📊 Where Analytics Are Stored

### Table: `rl_state`
### Column: `chunk_performance` (JSONB type)

This JSONB column contains **all your analytics data**:
- Quiz answers
- Accuracy percentages
- Attempt counts
- Timestamps
- File information
- Everything the dashboard displays

---

## 🔍 How to View Analytics in Supabase UI

### Method 1: View in Table Editor

1. Go to your Supabase dashboard
2. Click **"Table Editor"** in the sidebar
3. Click on the **`rl_state`** table
4. Find a row (e.g., username = "Bipin")
5. Click on the **`chunk_performance`** column
6. You'll see a JSON editor showing all analytics data!

### Method 2: Use SQL Editor

1. Go to **"SQL Editor"** in Supabase
2. Run this query to see analytics:

```sql
-- View analytics for a specific user
SELECT 
    username,
    jsonb_pretty(chunk_performance) as analytics,
    jsonb_pretty(file_mapping) as files
FROM rl_state
WHERE username = 'Bipin';
```

### Method 3: Query Specific Analytics

```sql
-- Count chunks with analytics data
SELECT 
    username,
    jsonb_object_keys(chunk_performance) as chunk_id,
    chunk_performance->jsonb_object_keys(chunk_performance)->>'attempts' as attempts,
    chunk_performance->jsonb_object_keys(chunk_performance)->>'correct' as correct
FROM rl_state
WHERE username = 'Bipin';
```

---

## 📋 Example: What's Inside `chunk_performance`

The `chunk_performance` JSONB column looks like this:

```json
{
  "7cc23ea4_chunk_1": {
    "correct": 5,
    "incorrect": 2,
    "attempts": 7,
    "last_attempt": "2025-11-29T13:22:29",
    "source_reference": "Chunk 1 - EXACT quote: '...'",
    "filename": "example.pdf",
    "questions": [...]
  },
  "7cc23ea4_chunk_2": {
    "correct": 3,
    "incorrect": 1,
    "attempts": 4,
    ...
  }
}
```

**This is ALL your analytics data!**

---

## ✅ Why This Design?

1. **Efficient**: One row per user, all analytics in one place
2. **Flexible**: JSONB allows any structure without schema changes
3. **Fast**: PostgreSQL JSONB is optimized for this
4. **Simple**: Dashboard loads all analytics in one query

---

## 🎯 Summary

- ✅ **2 tables is correct**: `users` and `rl_state`
- ✅ **Analytics are in**: `rl_state.chunk_performance` (JSONB column)
- ✅ **No separate table needed**: This is the right design
- ✅ **Your dashboard reads from**: `rl_state.chunk_performance`

**Everything is working correctly!** The analytics are there, just stored as JSON within the `rl_state` table.

