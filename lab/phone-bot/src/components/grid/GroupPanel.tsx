import { useState, useEffect } from 'react'
import { useDeviceStore } from '../../hooks/useDevices'
import { phoneBot } from '../../api'
import type { DeviceGroup } from '../../types'

export function GroupPanel() {
  const { devices, selectedGroup, setSelectedGroup } = useDeviceStore()
  const [groups, setGroups] = useState<DeviceGroup[]>([])
  const [showCreate, setShowCreate] = useState(false)
  const [newName, setNewName] = useState('')
  const [newColor, setNewColor] = useState('#22c55e')

  useEffect(() => {
    phoneBot.getGroups().then(g => setGroups(g as DeviceGroup[]))
  }, [])

  const allCount = devices.length
  const onlineCount = devices.filter(d => d.state === 'online').length

  const handleCreate = async () => {
    if (!newName.trim()) return
    const group = await phoneBot.createGroup({ name: newName.trim(), color: newColor, deviceSerials: [] })
    setGroups(prev => [...prev, group as DeviceGroup])
    setNewName('')
    setShowCreate(false)
  }

  const handleDelete = async (groupId: string) => {
    await phoneBot.deleteGroup(groupId)
    setGroups(prev => prev.filter(g => g.id !== groupId))
    if (selectedGroup === groupId) setSelectedGroup(null)
  }

  const getGroupCount = (group: DeviceGroup) => {
    return devices.filter(d => d.tags?.includes(group.id)).length
  }

  return (
    <div className="sidebar">
      {/* All Devices */}
      <div
        className={`sidebar-group ${!selectedGroup ? 'active' : ''}`}
        onClick={() => setSelectedGroup(null)}
      >
        📱 All Devices
        <span className="count">
          <span className="status-dot online" style={{ width: 6, height: 6, marginRight: 2 }} />
          {onlineCount}/{allCount}
        </span>
      </div>

      <div style={{ height: 1, background: 'var(--border-color)', margin: '4px 0' }} />

      {/* Groups */}
      {groups.map(group => (
        <div
          key={group.id}
          className={`sidebar-group ${selectedGroup === group.id ? 'active' : ''}`}
          onClick={() => setSelectedGroup(group.id)}
        >
          <span style={{
            width: 10, height: 10, borderRadius: 2,
            background: group.color, flexShrink: 0
          }} />
          {group.name}
          <span className="count">{getGroupCount(group)}</span>
          <span
            style={{ fontSize: 10, opacity: 0.3, cursor: 'pointer', marginLeft: 4 }}
            onClick={(e) => {
              e.stopPropagation()
              handleDelete(group.id)
            }}
            title="Delete group"
          >
            ✕
          </span>
        </div>
      ))}

      {/* Create Group */}
      {showCreate ? (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 4, padding: '4px 0' }}>
          <input
            type="text"
            placeholder="Group name..."
            value={newName}
            onChange={e => setNewName(e.target.value)}
            onKeyDown={e => {
              if (e.key === 'Enter') handleCreate()
              if (e.key === 'Escape') setShowCreate(false)
            }}
            autoFocus
            style={{
              background: 'var(--bg-primary)',
              border: '1px solid var(--border-color)',
              borderRadius: 3,
              padding: '4px 8px',
              color: 'var(--text-primary)',
              fontSize: 11,
              outline: 'none',
              fontFamily: 'inherit'
            }}
          />
          <div style={{ display: 'flex', gap: 4 }}>
            <input
              type="color"
              value={newColor}
              onChange={e => setNewColor(e.target.value)}
              style={{ width: 24, height: 24, border: 'none', cursor: 'pointer', background: 'none' }}
            />
            <button className="action-btn primary" onClick={handleCreate} style={{ flex: 1, fontSize: 11 }}>
              Create
            </button>
          </div>
        </div>
      ) : (
        <div
          className="sidebar-group"
          onClick={() => setShowCreate(true)}
          style={{ color: 'var(--text-muted)' }}
        >
          + New Group
        </div>
      )}
    </div>
  )
}
