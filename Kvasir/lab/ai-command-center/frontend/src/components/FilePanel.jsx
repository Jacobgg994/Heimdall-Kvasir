import { useState, useEffect } from 'react';
import useStore from '../stores/useStore';
import { fetchFiles } from '../api';

function FileTree({ items, path = '', depth = 0, onSelect }) {
  const [expanded, setExpanded] = useState({});
  const [children, setChildren] = useState({});
  const [loading, setLoading] = useState({});

  const toggleExpand = async (item) => {
    const itemPath = path ? `${path}/${item.name}` : item.name;
    if (expanded[itemPath]) {
      setExpanded((prev) => ({ ...prev, [itemPath]: false }));
      return;
    }
    setExpanded((prev) => ({ ...prev, [itemPath]: true }));
    if (children[itemPath]) return;

    setLoading((prev) => ({ ...prev, [itemPath]: true }));
    try {
      const data = await fetchFiles(itemPath);
      setChildren((prev) => ({ ...prev, [itemPath]: data || [] }));
    } catch {
      setChildren((prev) => ({ ...prev, [itemPath]: [] }));
    } finally {
      setLoading((prev) => ({ ...prev, [itemPath]: false }));
    }
  };

  if (!items || items.length === 0) {
    return depth === 0 ? (
      <div style={{ padding: 16, color: 'var(--text-secondary)', textAlign: 'center' }}>no files</div>
    ) : null;
  }

  return (
    <div>
      {items.map((item, idx) => {
        const itemPath = path ? `${path}/${item.name}` : item.name;
        const isDir = item.type === 'directory' || item.is_dir;
        const isExpanded = expanded[itemPath];
        const childItems = children[itemPath];
        const isLoading = loading[itemPath];
        const isLast = idx === items.length - 1;

        const connector = isLast ? '└── ' : '├── ';
        const childConnector = isLast ? '    ' : '│   ';

        return (
          <div key={itemPath}>
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 4,
                padding: '2px 0',
                paddingLeft: depth * 14,
                cursor: 'pointer',
                color: isDir ? '#3b82f6' : 'var(--text)',
                fontFamily: 'JetBrains Mono, monospace',
                fontSize: 13,
              }}
              onClick={() => {
                if (isDir) {
                  toggleExpand(item);
                } else {
                  onSelect(itemPath);
                }
              }}
            >
              <span style={{ color: 'var(--text-secondary)', whiteSpace: 'pre' }}>
                {depth > 0 ? childConnector : ''}{connector}
              </span>
              {isDir && (
                <span style={{ color: isExpanded ? '#eab308' : '#3b82f6', marginRight: 4 }}>
                  {isExpanded ? '▾' : '▸'}
                </span>
              )}
              {!isDir && <span style={{ color: 'var(--text-secondary)', marginRight: 4 }}>📄</span>}
              <span>{item.name}</span>
              {isLoading && <span style={{ color: 'var(--text-secondary)', fontSize: 11 }}> ...</span>}
              {isDir && !isLoading && isExpanded && childItems && childItems.length === 0 && (
                <span style={{ color: '#555', fontSize: 11 }}> (empty)</span>
              )}
            </div>
            {isDir && isExpanded && childItems && (
              <FileTree
                items={childItems}
                path={itemPath}
                depth={depth + 1}
                onSelect={onSelect}
              />
            )}
          </div>
        );
      })}
    </div>
  );
}

export default function FilePanel() {
  const [rootItems, setRootItems] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileContent, setFileContent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [editContent, setEditContent] = useState('');

  useEffect(() => {
    loadRoot();
  }, []);

  const loadRoot = async () => {
    setLoading(true);
    try {
      const data = await fetchFiles();
      const items = data?.files || data || [];
      setRootItems(Array.isArray(items) ? items : []);
    } catch (err) {
      setRootItems([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectFile = async (filePath) => {
    setSelectedFile(filePath);
    setEditing(false);
    setFileContent(null);
    try {
      const data = await fetchFiles(filePath);
      if (typeof data === 'object' && data.content) {
        setFileContent(data.content);
      } else if (typeof data === 'string') {
        setFileContent(data);
      } else {
        setFileContent(JSON.stringify(data, null, 2));
      }
    } catch {
      setFileContent('// Error loading file');
    }
  };

  return (
    <div style={{
      display: 'flex',
      height: '100%',
      background: 'var(--bg)',
      fontFamily: 'JetBrains Mono, monospace',
      fontSize: 13,
    }}>
      {/* File tree panel */}
      <div style={{
        width: 280,
        borderRight: '1px solid var(--border)',
        display: 'flex',
        flexDirection: 'column',
        flexShrink: 0,
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '8px 12px',
          borderBottom: '1px solid var(--border)',
        }}>
          <span style={{ color: 'var(--accent)', fontWeight: 500 }}>$ tree</span>
          <button
            onClick={loadRoot}
            style={{
              background: 'transparent',
              color: 'var(--text-secondary)',
              border: '1px solid #333',
              padding: '1px 6px',
              fontSize: 11,
              fontFamily: 'JetBrains Mono, monospace',
              cursor: 'pointer',
            }}
          >
            ↻
          </button>
        </div>
        <div style={{ flex: 1, overflowY: 'auto', padding: '6px 8px' }}>
          {loading ? (
            <div style={{ color: 'var(--text-secondary)', textAlign: 'center', padding: 16 }}>loading...</div>
          ) : (
            <FileTree items={rootItems} onSelect={handleSelectFile} />
          )}
        </div>
      </div>

      {/* File content panel */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '8px 16px',
          borderBottom: '1px solid var(--border)',
        }}>
          <span style={{ color: selectedFile ? 'var(--text)' : 'var(--text-secondary)' }}>
            {selectedFile ? `$ cat ${selectedFile}` : '$ cat <file>'}
          </span>
          {selectedFile && !editing && (
            <button
              onClick={() => { setEditContent(fileContent || ''); setEditing(true); }}
              style={{
                background: 'transparent',
                color: 'var(--text-secondary)',
                border: '1px solid #333',
                padding: '1px 6px',
                fontSize: 11,
                fontFamily: 'JetBrains Mono, monospace',
                cursor: 'pointer',
              }}
            >
              edit
            </button>
          )}
          {editing && (
            <div style={{ display: 'flex', gap: 4 }}>
              <button
                onClick={() => { setFileContent(editContent); setEditing(false); }}
                style={{
                  background: 'transparent',
                  color: 'var(--accent)',
                  border: '1px solid #22c55e',
                  padding: '1px 6px',
                  fontSize: 11,
                  fontFamily: 'JetBrains Mono, monospace',
                  cursor: 'pointer',
                }}
              >
                :wq
              </button>
              <button
                onClick={() => setEditing(false)}
                style={{
                  background: 'transparent',
                  color: 'var(--text-secondary)',
                  border: '1px solid #333',
                  padding: '1px 6px',
                  fontSize: 11,
                  fontFamily: 'JetBrains Mono, monospace',
                  cursor: 'pointer',
                }}
              >
                :q!
              </button>
            </div>
          )}
        </div>
        <div style={{ flex: 1, overflowY: 'auto' }}>
          {fileContent !== null ? (
            editing ? (
              <textarea
                value={editContent}
                onChange={(e) => setEditContent(e.target.value)}
                style={{
                  width: '100%',
                  height: '100%',
                  background: 'var(--bg)',
                  color: 'var(--text)',
                  fontFamily: 'JetBrains Mono, monospace',
                  fontSize: 13,
                  padding: 16,
                  border: 'none',
                  outline: 'none',
                  resize: 'none',
                  lineHeight: 1.6,
                }}
                spellCheck={false}
              />
            ) : (
              <pre style={{
                padding: 16,
                color: 'var(--text)',
                fontFamily: 'JetBrains Mono, monospace',
                fontSize: 13,
                whiteSpace: 'pre-wrap',
                wordBreak: 'break-word',
                lineHeight: 1.6,
                margin: 0,
              }}>
                {fileContent}
              </pre>
            )
          ) : (
            <div style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              height: '100%',
              color: '#555',
            }}>
              <span style={{ fontSize: 24, marginBottom: 8 }}>📂</span>
              <span>select a file to view</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
