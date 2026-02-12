# FliVideo Architecture Alignment Report

**Date**: 2026-02-10
**Analyzed Projects**: FliDeck, FliGen, FliHub, Storyline App
**System**: Node v22.16.0, npm 10.9.2

---

## Executive Summary

All four projects share a **consistent monorepo architecture** using npm workspaces with client/server/shared structure. They all use React 19+ (or 18+), TypeScript, Vite, TailwindCSS v4, Express 5+, and Socket.io for real-time communication.

**Key Finding**: Despite starting from the same foundation, version drift and dependency misalignment have occurred across projects. Several projects are using outdated or inconsistent dependency versions that should be aligned.

---

## 1. Architectural Commonalities

### 1.1 Monorepo Structure (100% Consistent)

All four projects use **npm workspaces** with the same three-package structure:

```
project-root/
├── package.json              # Root workspace config
├── client/                   # React frontend
│   └── package.json
├── server/                   # Express backend
│   └── package.json
└── shared/                   # TypeScript types
    └── package.json (or types.ts only)
```

**Package Naming Conventions**:
- **FliDeck**: `@flideck/client`, `@flideck/server`, `@flideck/shared`
- **FliGen**: `@fligen/client`, `@fligen/server`, `@fligen/shared`
- **FliHub**: `client`, `server`, `shared` (no scope)
- **Storyline App**: `client-temp`, `server`, `shared` (no scope, temp name)

**Gap**: FliHub and Storyline App don't use scoped package names. Recommend standardizing to `@projectname/workspace` pattern.

### 1.2 Core Tech Stack (Consistent Pattern)

| Layer | Technology | All Projects |
|-------|-----------|-------------|
| **Frontend** | React 19+ | ✅ Yes |
| **Build Tool** | Vite 6+ | ✅ Yes |
| **Styling** | TailwindCSS v4 | ✅ Yes |
| **Backend** | Express 5+ | ✅ Yes |
| **Real-time** | Socket.io 4.8+ | ✅ Yes |
| **Language** | TypeScript 5.6+ | ✅ Yes |
| **Module System** | ESM (`"type": "module"`) | ✅ Yes |

### 1.3 Development Patterns

**Common Scripts** (all projects):
```json
{
  "dev": "concurrently ...",
  "build": "npm run build -w server && npm run build -w client",
  "start": "npm start -w server"
}
```

**Build Tools**:
- **Client**: `tsc -b && vite build`
- **Server**: `tsc` (compile TypeScript)
- **Dev Server**: `tsx` or `nodemon` with `tsx`

### 1.4 Port Allocation (Consistent Pattern)

All projects use a **5X00/5X01** port range:

| Project | Client Port | Server Port |
|---------|------------|------------|
| **FliDeck** | 5200 | 5201 |
| **FliGen** | 5400 | 5401 |
| **FliHub** | Vite dev | 5101 |
| **Storyline App** | 5300 | 5301 |

✅ **No conflicts** - well-organized port allocation.

### 1.5 Real-time Architecture (Socket.io)

All projects use **Socket.io** for:
- File system change notifications
- Real-time data updates
- Client-server synchronization

**Common Patterns**:
- Server emits events on file changes (Chokidar watchers)
- Client uses hooks (`useSocket`, `useSocketInvalidation`)
- Room-based subscriptions for scoped updates

---

## 2. Dependency Version Analysis

### 2.1 Core Frontend Dependencies

| Package | FliDeck | FliGen | FliHub | Storyline App | Status |
|---------|---------|--------|--------|---------------|--------|
| **react** | 19.1.0 | 19.0.0 | 19.0.0 | 19.1.1 | ⚠️ Minor drift |
| **react-dom** | 19.1.0 | 19.0.0 | 19.0.0 | 19.1.1 | ⚠️ Minor drift |
| **@types/react** | 19.0.2 | 19.0.1 | 19.0.0 | 19.1.10 | ⚠️ Drift |
| **@types/react-dom** | 19.0.2 | 19.0.1 | 19.0.0 | 19.1.7 | ⚠️ Drift |
| **vite** | 6.0.6 | 6.0.5 | 6.0.0 | 7.1.5 | 🔴 **Major drift** |
| **@vitejs/plugin-react** | 4.3.4 | 4.3.4 | 4.3.0 | 5.0.0 | ⚠️ Major version gap |
| **typescript** | 5.7.2 | 5.7.2 | ~5.6.0 | ~5.8.3 | ⚠️ Version drift |

**Critical Finding**:
- **Vite 7.1.5** in Storyline App vs **Vite 6.0.x** in others - **major version difference**
- **@vitejs/plugin-react 5.0.0** in Storyline App vs **4.3.x** in others
- TypeScript versions range from 5.6 to 5.8.3

**Recommendation**: Standardize to **Vite 6.0.6** (stable) or **Vite 7.x** (latest) consistently.

### 2.2 TailwindCSS v4

| Package | FliDeck | FliGen | FliHub | Storyline App | Status |
|---------|---------|--------|--------|---------------|--------|
| **tailwindcss** | 4.0.0 | 4.0.0 | 4.0.0 | 4.1.13 | ⚠️ Version drift |
| **@tailwindcss/vite** | 4.0.0 | 4.0.0 | 4.0.0 | N/A | ⚠️ Missing |
| **@tailwindcss/postcss** | N/A | N/A | N/A | 4.1.13 | - |

**Finding**: Storyline App uses **Tailwind 4.1.13** with PostCSS instead of the Vite plugin. Others use **4.0.0** with `@tailwindcss/vite`.

**Recommendation**: Standardize to **Tailwind 4.1.x** with `@tailwindcss/vite` plugin for consistency.

### 2.3 Backend Dependencies

| Package | FliDeck | FliGen | FliHub | Storyline App | Status |
|---------|---------|--------|--------|---------------|--------|
| **express** | 5.1.0 | 5.0.1 | 5.1.0 | 5.1.0 | ⚠️ Minor drift |
| **@types/express** | 5.0.0 | 5.0.0 | 5.0.0 | 5.0.3 | ⚠️ Minor drift |
| **socket.io** | 4.8.1 | 4.8.1 | 4.8.1 | 4.8.1 | ✅ **Perfect** |
| **socket.io-client** | 4.8.1 | 4.8.1 | 4.8.1 | 4.8.1 | ✅ **Perfect** |
| **cors** | 2.8.5 | 2.8.5 | 2.8.5 | 2.8.5 | ✅ **Perfect** |
| **dotenv** | 16.4.7 | 16.4.7 | 16.4.0 | 17.2.2 | 🔴 **Major drift** |
| **chokidar** | 3.6.0 | N/A | 3.6.0 | 3.6.0 | ✅ Good (where used) |

**Critical Finding**:
- **dotenv 17.2.2** in Storyline App vs **16.4.x** in others - **major version difference**
- Express versions slightly inconsistent (5.0.1 vs 5.1.0)

**Recommendation**: Upgrade all to **dotenv ^16.4.7** (or standardize to 17.x if needed).

### 2.4 State Management

| Package | FliDeck | FliGen | FliHub | Storyline App | Status |
|---------|---------|--------|--------|---------------|--------|
| **@tanstack/react-query** | 5.62.11 | N/A | 5.60.0 | 5.87.1 | ⚠️ Drift |
| **@tanstack/react-query-devtools** | N/A | N/A | N/A | 5.87.1 | - |

**Finding**: FliDeck and FliHub use TanStack Query, but different versions. Storyline App uses latest (5.87.1). FliGen doesn't use it.

**Recommendation**: Standardize to **@tanstack/react-query ^5.87.1** for projects that use it.

### 2.5 Development Tools

| Package | FliDeck | FliGen | FliHub | Storyline App | Status |
|---------|---------|--------|--------|---------------|--------|
| **tsx** | 4.19.2 | 4.19.2 | 4.19.0 | 4.20.5 | ⚠️ Minor drift |
| **nodemon** | 3.1.9 | N/A | 3.1.0 | 3.1.10 | ⚠️ Minor drift |
| **concurrently** | 9.1.0 | 9.1.0 | 8.2.0 | 9.0.1 | 🔴 **Major drift** |

**Critical Finding**: FliHub uses **concurrently 8.2.0** while others use **9.x**.

**Recommendation**: Upgrade FliHub to **concurrently ^9.1.0**.

### 2.6 Routing

| Package | FliDeck | FliGen | FliHub | Storyline App | Status |
|---------|---------|--------|--------|---------------|--------|
| **react-router-dom** | 7.1.1 | N/A | N/A | 7.8.2 | ⚠️ Version drift |

**Finding**: Only FliDeck and Storyline App use React Router, but different versions.

**Recommendation**: Align to **react-router-dom ^7.8.2** (latest stable).

### 2.7 UI Libraries

| Package | FliDeck | FliGen | FliHub | Storyline App | Status |
|---------|---------|--------|--------|---------------|--------|
| **sonner** | 1.7.1 | N/A | 1.7.0 | N/A | ⚠️ Minor drift |

**Finding**: FliDeck and FliHub use Sonner (toast notifications), but different versions.

---

## 3. Gap Analysis

### 3.1 Structural Gaps

| Issue | FliDeck | FliGen | FliHub | Storyline App |
|-------|---------|--------|--------|---------------|
| **Scoped package names** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **Shared package.json** | ✅ Yes | ✅ Yes | ❌ No* | ❌ No* |
| **CLAUDE.md docs** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Git hooks (gitleaks)** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |

*FliHub and Storyline App have shared types but not a full package.json.

### 3.2 Configuration Gaps

| Feature | FliDeck | FliGen | FliHub | Storyline App |
|---------|---------|--------|--------|---------------|
| **Config hot-reload** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **External config file** | ✅ config.json | ❌ No | ✅ config.json | ✅ project-config.json |
| **Environment variables** | ✅ .env | ✅ .env | ✅ .env | ✅ .env |

**Finding**: FliDeck has the most advanced configuration system with hot-reload support.

### 3.3 Feature Completeness

| Feature | FliDeck | FliGen | FliHub | Storyline App |
|---------|---------|--------|--------|---------------|
| **File watching (Chokidar)** | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes |
| **Socket.io rooms** | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| **Image processing** | ❌ No | ✅ Yes (Sharp via APIs) | ✅ Yes | ✅ Yes (Sharp) |
| **AI Integration** | ❌ No | ✅ Yes (Claude, FAL, ElevenLabs) | ✅ Yes (Anthropic SDK) | ❌ No |
| **Monaco Editor** | ❌ No | ❌ No | ✅ Yes | ❌ No |

### 3.4 Middleware & Security

| Feature | FliDeck | FliGen | FliHub | Storyline App |
|---------|---------|--------|--------|---------------|
| **Helmet (security headers)** | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| **Compression** | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| **Morgan (logging)** | ❌ No | ❌ No | ❌ No | ✅ Yes |

**Recommendation**: Add **Helmet** and **Compression** to FliGen and FliHub for production readiness.

---

## 4. Outdated Dependencies

### 4.1 Critical Updates Needed

**FliHub**:
- ❌ **concurrently** `8.2.0` → `9.1.0` (major version behind)
- ❌ **vite** `6.0.0` → `6.0.6` (security/bug fixes)
- ❌ **@vitejs/plugin-react** `4.3.0` → `4.3.4`
- ❌ **@tanstack/react-query** `5.60.0` → `5.87.1`
- ❌ **tsx** `4.19.0` → `4.19.2`
- ❌ **nodemon** `3.1.0` → `3.1.9`

**FliGen**:
- ❌ **vite** `6.0.5` → `6.0.6`
- ❌ **react** `19.0.0` → `19.1.0`
- ❌ **react-dom** `19.0.0` → `19.1.0`

**FliDeck**:
- ✅ Most up-to-date (as of late December 2025)

**Storyline App**:
- ⚠️ **Vite 7.1.5** is cutting-edge - may want to wait for stability
- ⚠️ **@vitejs/plugin-react 5.0.0** is latest major version

### 4.2 Node.js Engine Requirements

| Project | Node Requirement | Status |
|---------|-----------------|--------|
| **FliDeck** | `>=20.0.0` | ✅ Specified |
| **FliGen** | Not specified | ❌ Missing |
| **FliHub** | Not specified | ❌ Missing |
| **Storyline App** | Not specified | ❌ Missing |

**Recommendation**: Add `"engines": { "node": ">=20.0.0" }` to all root package.json files.

---

## 5. Recommendations for Alignment

### 5.1 Immediate Actions (High Priority)

1. **Standardize dependency versions**:
   - React 19.1.0 across all projects
   - Vite 6.0.6 (or decide on Vite 7.x for all)
   - TypeScript 5.7.2 (or 5.8.3)
   - TailwindCSS 4.1.13 with `@tailwindcss/vite` plugin

2. **Update critical outdated packages**:
   - FliHub: concurrently 8.2.0 → 9.1.0
   - FliHub: @tanstack/react-query 5.60.0 → 5.87.1
   - All: dotenv standardized (16.4.7 or 17.x)

3. **Add scoped package names**:
   - FliHub: Rename to `@flihub/client`, `@flihub/server`, `@flihub/shared`
   - Storyline App: Rename `client-temp` to `@storyline/client`

4. **Add Node.js engine requirement** to all projects:
   ```json
   "engines": { "node": ">=20.0.0" }
   ```

### 5.2 Medium Priority

5. **Add security middleware to all projects**:
   - Helmet (security headers)
   - Compression (gzip)
   - Morgan (HTTP logging) for debugging

6. **Standardize shared package structure**:
   - FliHub and Storyline App should add `shared/package.json`
   - Use consistent build scripts (`tsc`, `tsc --watch`)

7. **Add gitleaks pre-commit hooks** to FliHub and Storyline App

8. **Standardize concurrently configuration**:
   - Use consistent naming conventions (`-n server,client`)
   - Use consistent color schemes (`-c blue,green`)

### 5.3 Low Priority (Nice to Have)

9. **Align development tooling**:
   - Consistent use of nodemon vs tsx watch
   - Standardize ESLint configurations
   - Add Prettier to all projects

10. **Documentation alignment**:
    - Consistent CLAUDE.md structure
    - Standardized docs/ folder organization
    - Shared architectural patterns document

---

## 6. Proposed Standard Package Versions

### 6.1 Frontend Stack

```json
{
  "dependencies": {
    "react": "^19.1.0",
    "react-dom": "^19.1.0",
    "socket.io-client": "^4.8.1",
    "@tanstack/react-query": "^5.87.1",
    "react-router-dom": "^7.8.2",
    "sonner": "^1.7.1"
  },
  "devDependencies": {
    "@types/react": "^19.1.10",
    "@types/react-dom": "^19.1.7",
    "@vitejs/plugin-react": "^4.3.4",
    "tailwindcss": "^4.1.13",
    "@tailwindcss/vite": "^4.1.13",
    "typescript": "^5.7.2",
    "vite": "^6.0.6"
  }
}
```

### 6.2 Backend Stack

```json
{
  "dependencies": {
    "express": "^5.1.0",
    "socket.io": "^4.8.1",
    "cors": "^2.8.5",
    "dotenv": "^16.4.7",
    "chokidar": "^3.6.0",
    "fs-extra": "^11.3.0",
    "helmet": "^8.0.0",
    "compression": "^1.7.5"
  },
  "devDependencies": {
    "@types/express": "^5.0.0",
    "@types/cors": "^2.8.17",
    "@types/node": "^22.10.2",
    "tsx": "^4.19.2",
    "nodemon": "^3.1.9",
    "typescript": "^5.7.2"
  }
}
```

### 6.3 Root Workspace

```json
{
  "devDependencies": {
    "concurrently": "^9.1.0"
  },
  "engines": {
    "node": ">=20.0.0"
  }
}
```

---

## 7. Migration Strategy

### Phase 1: Critical Updates (Week 1)
1. Update concurrently in FliHub (8.2.0 → 9.1.0)
2. Standardize React to 19.1.0 across all projects
3. Add Node.js engine requirements

### Phase 2: Dependency Alignment (Week 2)
4. Align Vite versions (decide on 6.0.6 or 7.x)
5. Standardize TailwindCSS to 4.1.13
6. Update @tanstack/react-query in FliHub

### Phase 3: Structural Improvements (Week 3)
7. Add scoped package names to FliHub and Storyline App
8. Add shared/package.json to FliHub and Storyline App
9. Add security middleware (Helmet, Compression)

### Phase 4: Tooling & Documentation (Week 4)
10. Add gitleaks hooks to FliHub and Storyline App
11. Standardize CLAUDE.md documentation
12. Add shared architectural patterns document

---

## 8. Conclusion

All four projects demonstrate **strong architectural consistency** in their core structure (monorepo with npm workspaces, React + Express + Socket.io). However, **dependency drift** has occurred over time, particularly in:

- **Vite versions** (6.0.0 to 7.1.5)
- **React versions** (19.0.0 to 19.1.1)
- **TailwindCSS** (4.0.0 to 4.1.13)
- **concurrently** (8.2.0 to 9.1.0)
- **dotenv** (16.4.0 to 17.2.2)

The **primary goal** should be to:
1. **Standardize core dependencies** (React, Vite, TypeScript, TailwindCSS)
2. **Update critical outdated packages** (concurrently, @tanstack/react-query)
3. **Add missing structural elements** (scoped names, shared packages, security middleware)
4. **Establish a maintenance schedule** to prevent future drift

**Overall Architecture Health**: 8/10 - Excellent foundation, minor alignment needed.

---

**Report Generated**: 2026-02-10
**Next Review**: 2026-03-10 (recommended quarterly alignment check)
