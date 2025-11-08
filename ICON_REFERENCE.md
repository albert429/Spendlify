# Lucide Icon Reference Guide

## Icon Mappings (Emoji → Lucide)

### Login Page
| Old Emoji | New Lucide Icon | Usage |
|-----------|----------------|-------|
| 🔐 | `lock` | Login tab |
| ✨ | `sparkles` | Register tab, Spendlify logo |
| 👤 | `user` | Username fields |
| 🔒 | `lock` | Password fields |
| 👁️ | `eye` / `eye-off` | Password toggle (show/hide) |
| → | `arrow-right` | Submit buttons |
| 💰 | `dollar-sign` | Currency selector |
| 👨‍💼 | `user-circle` | Full name field |
| 🔐 | `shield-check` | Confirm password |
| 📊 | `bar-chart-3` | Smart Tracking feature |
| 🤖 | `brain` | AI Insights feature |
| 💱 | `coins` | Multi-Currency feature |
| 🔐 | `shield-check` | Secure & Private feature |

### Dashboard - Sidebar Navigation
| Old Emoji | New Lucide Icon | Usage |
|-----------|----------------|-------|
| ✨ | `sparkles` | Spendlify logo |
| 📊 | `layout-dashboard` | Dashboard nav link |
| 💳 | `credit-card` | Transactions nav link |
| 🎯 | `target` | Goals nav link |
| 🔔 | `bell` | Reminders nav link |
| 🤖 | `bot` | AI Assistant nav link |

### Dashboard - Stats Cards
| Old Emoji | New Lucide Icon | Usage |
|-----------|----------------|-------|
| 💰 | `trending-up` | Total Income card |
| 💸 | `trending-down` | Total Expenses card |
| 📈 | `wallet` | Net Balance card |

### Dashboard - Section Headers
| Old Emoji | New Lucide Icon | Usage |
|-----------|----------------|-------|
| 📅 | `calendar` | Upcoming Bills |
| 📊 | `pie-chart` | Spending by Category chart |
| 📈 | `trending-up` | Monthly Trend chart |
| 🏷️ | `tag` | Top Spending Categories |
| 🕐 | `clock` | Recent Transactions |

### Topbar
| Old Emoji | New Lucide Icon | Usage |
|-----------|----------------|-------|
| ☰ | `menu` | Mobile menu toggle |

---

## How to Use Lucide Icons

### Basic Usage
```html
<i data-lucide="icon-name"></i>
```

### With Custom Styling
```html
<i data-lucide="icon-name" style="width: 20px; height: 20px;"></i>
```

### Initialize Icons (JavaScript)
```javascript
// After DOM manipulation or dynamic content
lucide.createIcons();
```

---

## Common Icon Sizes

| Context | Size | CSS |
|---------|------|-----|
| Tab icons | 20px | `.tab-icon { width: 20px; height: 20px; }` |
| Label icons | 18px | `.label-icon { width: 18px; height: 18px; }` |
| Button icons | 20px | `.btn-icon { width: 20px; height: 20px; }` |
| Nav icons | 20px | `.nav-link .icon { width: 20px; height: 20px; }` |
| Stat icons | 64px | `.stat-icon { width: 64px; height: 64px; }` |
| Menu toggle | 24px | `.menu-toggle i { width: 24px; height: 24px; }` |
| Feature icons | 20px | `.feature-icon { width: 20px; height: 20px; }` |

---

## Available Lucide Icons (Commonly Used)

### Financial
- `dollar-sign`, `euro`, `pound-sterling`, `yen`
- `coins`, `wallet`, `credit-card`, `banknote`
- `trending-up`, `trending-down`, `arrow-up-right`, `arrow-down-right`

### Navigation
- `home`, `layout-dashboard`, `menu`, `x`
- `chevron-left`, `chevron-right`, `arrow-left`, `arrow-right`

### Actions
- `plus`, `minus`, `edit`, `trash-2`, `save`
- `check`, `x`, `refresh-cw`, `download`, `upload`

### Data & Analytics
- `bar-chart`, `bar-chart-2`, `bar-chart-3`, `bar-chart-4`
- `pie-chart`, `line-chart`, `trending-up`, `activity`

### User & Account
- `user`, `user-circle`, `users`, `user-plus`
- `lock`, `unlock`, `shield`, `shield-check`
- `eye`, `eye-off`, `key`

### Time & Calendar
- `calendar`, `clock`, `timer`, `alarm-clock`
- `calendar-days`, `calendar-check`

### Communication
- `bell`, `bell-off`, `message-circle`, `mail`
- `send`, `inbox`, `archive`

### General
- `sparkles`, `star`, `heart`, `bookmark`
- `target`, `flag`, `tag`, `tags`
- `search`, `filter`, `settings`, `help-circle`
- `info`, `alert-circle`, `alert-triangle`, `check-circle`

---

## Resources
- **Lucide Icons Website:** https://lucide.dev/icons/
- **CDN Link:** https://unpkg.com/lucide@latest
- **Documentation:** https://lucide.dev/guide/

---

## Notes
- Icons are loaded from CDN (requires internet connection)
- All icons are SVG-based for crisp rendering at any size
- Icons automatically adapt to parent text color
- Use `lucide.createIcons()` after dynamically adding icons to the DOM
