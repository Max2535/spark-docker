import React, { useEffect, useRef, useState } from "react";
import "./App.css";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

// Modern color palette and styles
const styles = {
  app: {
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    fontFamily: "'Inter', sans-serif",
    padding: '20px 0',
  },
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '0 20px',
  },
  header: {
    textAlign: 'center',
    marginBottom: '40px',
    color: 'white',
  },
  title: {
    fontSize: '3rem',
    fontWeight: '700',
    marginBottom: '10px',
    textShadow: '0 2px 4px rgba(0,0,0,0.3)',
  },
  subtitle: {
    fontSize: '1.2rem',
    fontWeight: '300',
    opacity: '0.9',
  },
  card: {
    background: 'white',
    borderRadius: '16px',
    padding: '32px',
    marginBottom: '24px',
    boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
    border: '1px solid rgba(255, 255, 255, 0.1)',
  },
  sectionTitle: {
    fontSize: '1.5rem',
    fontWeight: '600',
    color: '#1f2937',
    marginBottom: '16px',
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
  },
  icon: {
    width: '24px',
    height: '24px',
    color: '#4f46e5',
  },
  fileInput: {
    display: 'none',
  },
  fileInputLabel: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: '8px',
    padding: '12px 24px',
    background: '#f8fafc',
    border: '2px dashed #cbd5e1',
    borderRadius: '12px',
    cursor: 'pointer',
    transition: 'all 0.2s',
    fontSize: '14px',
    fontWeight: '500',
    color: '#64748b',
    ':hover': {
      borderColor: '#4f46e5',
      background: '#f1f5f9',
    }
  },
  button: {
    background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)',
    color: 'white',
    border: 'none',
    padding: '12px 24px',
    borderRadius: '12px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '600',
    transition: 'all 0.2s',
    display: 'inline-flex',
    alignItems: 'center',
    gap: '8px',
    ':hover': {
      transform: 'translateY(-2px)',
      boxShadow: '0 10px 20px rgba(79, 70, 229, 0.3)',
    },
    ':disabled': {
      opacity: '0.6',
      cursor: 'not-allowed',
      transform: 'none',
    }
  },
  textarea: {
    width: '100%',
    minHeight: '120px',
    padding: '16px',
    border: '2px solid #e2e8f0',
    borderRadius: '12px',
    fontSize: '14px',
    fontFamily: "'Monaco', 'Menlo', 'Ubuntu Mono', monospace",
    resize: 'vertical',
    transition: 'border-color 0.2s',
    ':focus': {
      outline: 'none',
      borderColor: '#4f46e5',
      boxShadow: '0 0 0 3px rgba(79, 70, 229, 0.1)',
    }
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    marginTop: '20px',
    background: 'white',
    borderRadius: '12px',
    overflow: 'hidden',
    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
  },
  tableHeader: {
    background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)',
    color: 'white',
  },
  tableHeaderCell: {
    padding: '16px',
    textAlign: 'left',
    fontWeight: '600',
    fontSize: '14px',
  },
  tableRow: {
    ':hover': {
      background: '#f8fafc',
    }
  },
  tableCell: {
    padding: '12px 16px',
    borderBottom: '1px solid #e2e8f0',
    fontSize: '14px',
  },
  alert: {
    padding: '16px',
    borderRadius: '12px',
    marginBottom: '20px',
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    fontSize: '14px',
    fontWeight: '500',
  },
  alertSuccess: {
    background: '#ecfdf5',
    color: '#065f46',
    border: '1px solid #a7f3d0',
  },
  alertError: {
    background: '#fef2f2',
    color: '#991b1b',
    border: '1px solid #fecaca',
  },
  spinner: {
    animation: 'spin 1s linear infinite',
  },
  preview: {
    background: '#f8fafc',
    padding: '20px',
    borderRadius: '12px',
    marginTop: '20px',
  },
  previewTitle: {
    fontSize: '1.1rem',
    fontWeight: '600',
    color: '#374151',
    marginBottom: '12px',
  }
};

function App() {
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState("");
  const [queryResult, setQueryResult] = useState(null);
  const [lastUpload, setLastUpload] = useState(null);
  const [error, setError] = useState(null);
  const [statusMessage, setStatusMessage] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isQuerying, setIsQuerying] = useState(false);

  // Autocomplete: catalog, suggestions, and editor refs
  const [tables, setTables] = useState([]);
  const [columnsByTable, setColumnsByTable] = useState({});
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [selectedSuggestion, setSelectedSuggestion] = useState(0);
  const textareaRef = useRef(null);

  const KEYWORDS = [
    'SELECT', 'FROM', 'WHERE', 'GROUP BY', 'ORDER BY', 'JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'INNER JOIN', 'FULL JOIN',
    'ON', 'AS', 'LIMIT', 'OFFSET', 'AND', 'OR', 'NOT', 'BETWEEN', 'LIKE', 'IN', 'IS NULL', 'IS NOT NULL',
    'HAVING', 'DISTINCT', 'COUNT', 'SUM', 'AVG', 'MIN', 'MAX', 'CAST', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END',
    'UNION', 'UNION ALL', 'DESC', 'ASC'
  ];

  // Load tables/columns from backend once
  useEffect(() => {
    const loadCatalog = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/tables`);
        const data = await res.json();
        if (res.ok && data.tables) {
          setTables(data.tables);
          data.tables.forEach(async (t) => {
            try {
              const cr = await fetch(`${API_BASE_URL}/columns?table=${encodeURIComponent(t.name)}`);
              const cd = await cr.json();
              if (cr.ok && cd.columns) {
                setColumnsByTable(prev => ({ ...prev, [t.name]: cd.columns.map(c => c.name) }));
              }
            } catch {}
          });
        }
      } catch {}
    };
    loadCatalog();
  }, []);

  const uploadFile = async () => {
    if (!file) {
      setError("Please choose a CSV file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setError(null);
      setStatusMessage(null);
      setIsUploading(true);
      const response = await fetch(`${API_BASE_URL}/upload`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || data.error || "Failed to upload file");
      }
      setLastUpload(data);
      setStatusMessage(data.message);
      setQueryResult(null);
      // Update catalog with the newly registered temp view
      if (data?.tableName && Array.isArray(data?.columns)) {
        setTables((prev) => {
          const exists = prev.some((t) => t.name === data.tableName);
          return exists ? prev : [...prev, { name: data.tableName, isTemporary: true }];
        });
        setColumnsByTable((prev) => ({ ...prev, [data.tableName]: data.columns }));
      }
    } catch (err) {
      console.error("Upload failed", err);
      setError(err.message || "An unexpected error occurred while uploading");
    } finally {
      setIsUploading(false);
    }
  };

  const runQuery = async () => {
    if (!query.trim()) {
      setError("Please enter a SQL query to run");
      return;
    }

    const formData = new FormData();
    formData.append("query", query);

    try {
      setError(null);
      setStatusMessage(null);
      setIsQuerying(true);
      const response = await fetch(`${API_BASE_URL}/query`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || data.error || "Failed to run query");
      }
      setQueryResult(data);
      if (!data.data?.length) {
        setStatusMessage("Query executed successfully but returned no rows");
      }
    } catch (err) {
      console.error("Query failed", err);
      setError(err.message || "An unexpected error occurred while running the query");
      setQueryResult(null);
    } finally {
      setIsQuerying(false);
    }
  };

  // ===== Autocomplete helpers =====
  const getTokenBounds = (text, cursor) => {
    const isToken = (ch) => /[A-Za-z0-9_\.]/.test(ch);
    let start = cursor;
    let end = cursor;
    while (start > 0 && isToken(text[start - 1])) start--;
    while (end < text.length && isToken(text[end])) end++;
    return { start, end, token: text.slice(start, end) };
  };

  const buildSuggestions = (text, cursor) => {
    const { start, end, token } = getTokenBounds(text, cursor);
    const before = text.slice(0, start);
    const prevWordMatch = before.match(/([A-Za-z_]+)\s*$/i);
    const prevWord = prevWordMatch ? prevWordMatch[1].toUpperCase() : "";

    const items = [];
    const add = (type, value, detail) => items.push({ type, value, detail });
    const tableNames = tables.map(t => t.name);
    const allColumns = Object.values(columnsByTable).flat();

    if (token.includes('.')) {
      const [tbl, prefix = ""] = token.split('.', 2);
      const cols = columnsByTable[tbl] || [];
      cols.filter(c => c.toLowerCase().startsWith(prefix.toLowerCase()))
          .slice(0, 50)
          .forEach(c => add('column', `${tbl}.${c}`, tbl));
    } else {
      if (["FROM", "JOIN", "UPDATE", "INTO"].includes(prevWord)) {
        tableNames.filter(n => n.toLowerCase().startsWith(token.toLowerCase()))
                  .slice(0, 50)
                  .forEach(n => add('table', n));
      } else {
        KEYWORDS.filter(k => k.toLowerCase().startsWith(token.toLowerCase()))
                .slice(0, 50)
                .forEach(k => add('keyword', k));
        tableNames.filter(n => n.toLowerCase().startsWith(token.toLowerCase()))
                  .slice(0, 50)
                  .forEach(n => add('table', n));
        allColumns.filter(c => c.toLowerCase().startsWith(token.toLowerCase()))
                  .slice(0, 50)
                  .forEach(c => add('column', c));
      }
    }
    return { list: items, range: { start, end } };
  };

  const openSuggestions = () => {
    if (!textareaRef.current) return;
    const cursor = textareaRef.current.selectionStart;
    const { list } = buildSuggestions(query, cursor);
    setSuggestions(list);
    setSelectedSuggestion(0);
    setShowSuggestions(list.length > 0);
  };

  const applySuggestion = (sugg, range) => {
    const before = query.slice(0, range.start);
    const after = query.slice(range.end);
    const insert = sugg.value;
    const next = before + insert + after;
    setQuery(next);
    setShowSuggestions(false);
    setSuggestions([]);
    // restore caret
    requestAnimationFrame(() => {
      if (textareaRef.current) {
        const pos = before.length + insert.length;
        textareaRef.current.focus();
        textareaRef.current.setSelectionRange(pos, pos);
      }
    });
  };

  const onTextareaKeyDown = (e) => {
    if (e.ctrlKey && e.code === 'Space') {
      e.preventDefault();
      openSuggestions();
      return;
    }
    if (showSuggestions && suggestions.length) {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        setSelectedSuggestion((p) => (p + 1) % suggestions.length);
        return;
      }
      if (e.key === 'ArrowUp') {
        e.preventDefault();
        setSelectedSuggestion((p) => (p - 1 + suggestions.length) % suggestions.length);
        return;
      }
      if (e.key === 'Enter' || e.key === 'Tab') {
        e.preventDefault();
        const cursor = textareaRef.current ? textareaRef.current.selectionStart : query.length;
        const { range } = buildSuggestions(query, cursor);
        applySuggestion(suggestions[selectedSuggestion], range);
        return;
      }
      if (e.key === 'Escape') {
        e.preventDefault();
        setShowSuggestions(false);
        return;
      }
    }
    const isChar = e.key.length === 1 && /[A-Za-z0-9_.]/.test(e.key);
    if (isChar || e.key === 'Backspace' || e.key === 'Delete') {
      setTimeout(() => openSuggestions(), 0);
    }
  };

  const renderTable = (columns, rows) => {
    if (!rows || !rows.length) {
      return (
        <div className="text-center" style={{
          padding: '40px',
          color: '#6b7280',
          background: '#f9fafb',
          borderRadius: '12px',
          border: '2px dashed #d1d5db'
        }}>
          <i className="fas fa-table" style={{ fontSize: '2rem', marginBottom: '12px', display: 'block' }}></i>
          <p>No data to display</p>
        </div>
      );
    }

    return (
      <table className="table" style={styles.table}>
        <thead className="table-header" style={styles.tableHeader}>
          <tr>
            {columns.map((col) => (
              <th key={col} className="table-header-cell" style={styles.tableHeaderCell}>
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, rowIndex) => (
            <tr key={rowIndex} className="table-row" style={styles.tableRow}>
              {columns.map((col) => (
                <td key={col} className="table-cell" style={styles.tableCell}>
                  {row[col] ?? ""}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  return (
    <div className="app" style={styles.app}>
      <div className="container" style={styles.container}>
        {/* Header */}
        <div style={styles.header}>
          <h1 className="title" style={styles.title}>
            <i className="fas fa-fire" style={{ marginRight: '16px', color: '#fbbf24' }}></i>
            Spark SQL Analytics
          </h1>
          <p className="subtitle" style={styles.subtitle}>
            Upload your data and run powerful SQL queries with Apache Spark
          </p>
        </div>

        {/* Status Messages */}
        {statusMessage && (
          <div className="alert-enter" style={{...styles.alert, ...styles.alertSuccess}}>
            <i className="fas fa-check-circle"></i>
            {statusMessage}
          </div>
        )}

        {error && (
          <div className="alert-enter" style={{...styles.alert, ...styles.alertError}}>
            <i className="fas fa-exclamation-circle"></i>
            {error}
          </div>
        )}

        {/* Upload Section */}
        <div className="card card-enter" style={styles.card}>
          <h2 className="section-title" style={styles.sectionTitle}>
            <i className="fas fa-cloud-upload-alt" style={styles.icon}></i>
            Upload CSV File
          </h2>
          <p style={{ color: '#6b7280', marginBottom: '20px', fontSize: '14px' }}>
            Select a CSV file to register it as a temporary Spark table for querying
          </p>

          <div className="button-group flex items-center gap-4 flex-wrap">
            <label className="file-input-label" style={styles.fileInputLabel}>
              <input
                type="file"
                accept=".csv"
                onChange={(e) => setFile(e.target.files[0] ?? null)}
                style={styles.fileInput}
              />
              <i className="fas fa-file-csv"></i>
              {file ? file.name : 'Choose CSV file'}
            </label>

            <button
              className="button"
              onClick={uploadFile}
              disabled={!file || isUploading}
              style={{
                ...styles.button,
                opacity: (!file || isUploading) ? 0.6 : 1,
                cursor: (!file || isUploading) ? 'not-allowed' : 'pointer'
              }}
            >
              {isUploading ? (
                <>
                  <i className="fas fa-spinner" style={styles.spinner}></i>
                  Uploading...
                </>
              ) : (
                <>
                  <i className="fas fa-upload"></i>
                  Upload File
                </>
              )}
            </button>
          </div>
        </div>

        {/* Preview Section */}
        {lastUpload && lastUpload.preview?.length ? (
          <div className="card card-enter" style={styles.card}>
            <h3 className="section-title" style={styles.sectionTitle}>
              <i className="fas fa-table" style={styles.icon}></i>
              Data Preview
            </h3>
            <div style={styles.preview}>
              <p style={styles.previewTitle}>
                Table: <code>{lastUpload.tableName}</code>
                <span style={{ color: '#6b7280', fontWeight: 'normal', marginLeft: '8px' }}>
                  (showing first {lastUpload.preview.length} rows)
                </span>
              </p>
              <div className="table-container" style={{ overflowX: 'auto' }}>
                {renderTable(lastUpload.columns, lastUpload.preview)}
              </div>
            </div>
          </div>
        ) : null}

        {/* Query Section */}
        <div className="card card-enter" style={styles.card}>
          <h2 className="section-title" style={styles.sectionTitle}>
            <i className="fas fa-code" style={styles.icon}></i>
            SQL Query
          </h2>
          <p style={{ color: '#6b7280', marginBottom: '20px', fontSize: '14px' }}>
            Write your SQL query to analyze the uploaded data
          </p>
          <p style={{ color: '#9ca3af', marginTop: '-12px', marginBottom: '16px', fontSize: '12px', fontStyle: 'italic' }}>
            Tip: Press Ctrl+Space for autocomplete (keywords, tables, columns)
          </p>

          <textarea
            className="textarea"
            style={styles.textarea}
            placeholder="SELECT * FROM your_table LIMIT 10;"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={onTextareaKeyDown}
            ref={textareaRef}
          />

          {showSuggestions && suggestions.length ? (
            <div style={{
              marginTop: '8px',
              background: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)',
              maxHeight: '220px',
              overflowY: 'auto'
            }}>
              {suggestions.map((s, idx) => (
                <div
                  key={idx}
                  onMouseDown={(e) => {
                    e.preventDefault();
                    const cursor = textareaRef.current ? textareaRef.current.selectionStart : query.length;
                    const { range } = buildSuggestions(query, cursor);
                    applySuggestion(s, range);
                  }}
                  onMouseEnter={() => setSelectedSuggestion(idx)}
                  style={{
                    padding: '8px 12px',
                    cursor: 'pointer',
                    background: idx === selectedSuggestion ? '#eef2ff' : 'transparent',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    fontFamily: "'Monaco', 'Menlo', 'Ubuntu Mono', monospace",
                    fontSize: '13px'
                  }}
                >
                  <span style={{ display: 'inline-block', minWidth: '56px', color: '#6b7280' }}>{s.type}</span>
                  <span style={{ color: '#111827' }}>{s.value}</span>
                  {s.detail ? (
                    <span style={{ color: '#9ca3af', marginLeft: 'auto' }}>{s.detail}</span>
                  ) : null}
                </div>
              ))}
            </div>
          ) : null}

          <button
            className="button"
            onClick={runQuery}
            disabled={!query.trim() || isQuerying}
            style={{
              ...styles.button,
              marginTop: '16px',
              opacity: (!query.trim() || isQuerying) ? 0.6 : 1,
              cursor: (!query.trim() || isQuerying) ? 'not-allowed' : 'pointer'
            }}
          >
            {isQuerying ? (
              <>
                <i className="fas fa-spinner" style={styles.spinner}></i>
                Running Query...
              </>
            ) : (
              <>
                <i className="fas fa-play"></i>
                Execute Query
              </>
            )}
          </button>
        </div>

        {/* Results Section */}
        {queryResult && queryResult.columns ? (
          <div className="card card-enter" style={styles.card}>
            <h2 className="section-title" style={styles.sectionTitle}>
              <i className="fas fa-chart-bar" style={styles.icon}></i>
              Query Results
            </h2>
            {queryResult.data?.length ? (
              <>
                <div className="table-container" style={{ overflowX: 'auto' }}>
                  {renderTable(queryResult.columns, queryResult.data)}
                </div>
                {queryResult.limit && (
                  <p className="text-center" style={{
                    marginTop: '16px',
                    color: '#6b7280',
                    fontSize: '14px',
                    fontStyle: 'italic'
                  }}>
                    <i className="fas fa-info-circle" style={{ marginRight: '6px' }}></i>
                    Showing up to {queryResult.limit} rows
                  </p>
                )}
              </>
            ) : (
              <div className="text-center" style={{
                padding: '40px',
                color: '#6b7280',
                background: '#f9fafb',
                borderRadius: '12px'
              }}>
                <i className="fas fa-search" style={{ fontSize: '2rem', marginBottom: '12px', display: 'block' }}></i>
                <p>Query executed successfully but returned no results</p>
              </div>
            )}
          </div>
        ) : null}
      </div>
    </div>
  );
}

export default App;
