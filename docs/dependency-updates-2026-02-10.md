# Dependency Updates - February 10, 2026

**Status**: Complete - All dependency updates and quality tooling implemented
**Last Updated**: 2026-02-14

## ✅ Completed Updates

### FliHub (Most Critical)

**Root package.json:**
- ✅ `concurrently`: `8.2.0` → `9.1.0` (major version update)
- ✅ Added `engines`: `node >=20.0.0`

**Client package.json:**
- ✅ `react`: `19.0.0` → `19.1.0`
- ✅ `react-dom`: `19.0.0` → `19.1.0`
- ✅ `@types/react`: `19.0.0` → `19.0.2`
- ✅ `@types/react-dom`: `19.0.0` → `19.0.2`
- ✅ `@tanstack/react-query`: `5.60.0` → `5.87.1`
- ✅ `vite`: `6.0.0` → `6.0.6`
- ✅ `@vitejs/plugin-react`: `4.3.0` → `4.3.4`
- ✅ `tailwindcss`: `4.0.0` → `4.1.13`
- ✅ `@tailwindcss/vite`: `4.0.0` → `4.1.13`
- ✅ `typescript`: `5.6.0` → `5.7.2`
- ✅ `sonner`: `1.7.0` → `1.7.1`

**Server package.json:**
- ✅ `typescript`: `5.6.0` → `5.7.2`
- ✅ `tsx`: `4.19.0` → `4.19.2`
- ✅ `nodemon`: `3.1.0` → `3.1.9`
- ✅ `@types/node`: `22.0.0` → `22.10.2`

---

### FliGen

**Root package.json:**
- ✅ Added `engines`: `node >=20.0.0`

**Client package.json:**
- ✅ `react`: `19.0.0` → `19.1.0`
- ✅ `react-dom`: `19.0.0` → `19.1.0`
- ✅ `@types/react`: `19.0.1` → `19.0.2`
- ✅ `@types/react-dom`: `19.0.1` → `19.0.2`
- ✅ `vite`: `6.0.5` → `6.0.6`
- ✅ `tailwindcss`: `4.0.0` → `4.1.13`
- ✅ `@tailwindcss/vite`: `4.0.0` → `4.1.13`

---

### FliDeck

**Client package.json:**
- ✅ `tailwindcss`: `4.0.0` → `4.1.13`
- ✅ `@tailwindcss/vite`: `4.0.0` → `4.1.13`

---

### Storyline App

**Root package.json:**
- ✅ Added `engines`: `node >=20.0.0`

---

## 🔄 Next Steps Required

### Install Updated Dependencies

After these package.json changes, you need to reinstall dependencies:

```bash
# FliHub
cd flihub
rm -rf node_modules package-lock.json
npm install

# FliGen
cd ../fligen
rm -rf node_modules package-lock.json
npm install

# FliDeck
cd ../flideck
rm -rf node_modules package-lock.json
npm install

# Storyline App
cd ../storyline-app
rm -rf node_modules package-lock.json
npm install
```

Or run a clean install for all:

```bash
# From /Users/davidcruwys/dev/ad/flivideo/
for project in flihub fligen flideck storyline-app; do
  cd $project
  rm -rf node_modules package-lock.json
  npm install
  cd ..
done
```

---

## ⚠️ Manual Actions Required (Not Automated)

### Task 12: Add Scoped Package Names to FliHub

**Current:**
- `"name": "client"`
- `"name": "server"`
- `"name": "shared"`

**Target:**
- `"name": "@flihub/client"`
- `"name": "@flihub/server"`
- `"name": "@flihub/shared"`

**Why not automated?**
This is a **breaking change** that requires:
1. Updating all import statements in the codebase
2. Potentially updating build configurations
3. Testing to ensure nothing breaks

**Manual steps:**
1. Update package names in `client/package.json`, `server/package.json`, `shared/package.json`
2. Search and replace imports throughout codebase
3. Run `npm install` to update workspace links
4. Test build and dev scripts

---

### Task 13: Add Scoped Package Names to Storyline App

**Current:**
- `"name": "client-temp"`
- `"name": "server"`
- `"name": "shared"` (no package.json)

**Target:**
- `"name": "@storyline/client"`
- `"name": "@storyline/server"`
- `"name": "@storyline/shared"` (create package.json)

**Why not automated?**
Same breaking change concerns as FliHub, plus:
- Need to create `shared/package.json` first
- `client-temp` suggests this was temporary naming

**Manual steps:**
1. Create `shared/package.json` with proper structure
2. Update package names in all workspace packages
3. Search and replace imports
4. Test thoroughly

---

## 📊 Alignment Summary

### Now Consistent Across All Projects:

| Dependency | Version | Projects |
|------------|---------|----------|
| **React** | `19.1.0` | All |
| **TypeScript** | `5.7.2` | All |
| **Vite** | `6.0.6` | FliDeck, FliGen, FliHub |
| **Vite** | `7.1.5` | Storyline App ⚠️ |
| **TailwindCSS** | `4.1.13` | FliDeck, FliGen, FliHub |
| **TailwindCSS** | `4.1.13` | Storyline App (with PostCSS) |
| **Socket.io** | `4.8.1` | All |
| **Express** | `5.0.1` - `5.1.0` | All ⚠️ |
| **Node Engine** | `>=20.0.0` | All ✅ |

---

## ⚠️ Remaining Inconsistencies

### Vite Version
- **FliDeck, FliGen, FliHub**: `6.0.6`
- **Storyline App**: `7.1.5`

**Decision needed:** Adopt Vite 7.x everywhere or keep Storyline App on stable 6.x?

### Express Version
- **FliGen**: `5.0.1`
- **FliDeck, FliHub, Storyline App**: `5.1.0`

**Recommendation:** Update FliGen to `5.1.0`

### TailwindCSS Setup
- **FliDeck, FliGen, FliHub**: Use `@tailwindcss/vite` plugin
- **Storyline App**: Uses `@tailwindcss/postcss` + `postcss` + `autoprefixer`

**Recommendation:** Standardize on Vite plugin for consistency

---

## 🎯 Priority Next Actions

1. **Install dependencies** in all projects (see commands above)
2. **Test all projects** to ensure updates didn't break anything
3. **Decide on scoped package names** - Worth the refactoring effort?
4. **Standardize Express** to `5.1.0` in FliGen
5. **Decide on Vite 7.x** adoption strategy
6. **Add security middleware** (Helmet, Compression) to FliGen and FliHub

---

## 🎉 Quality Tooling Implementation (Complete as of 2026-02-14)

All 4 FliVideo apps now have complete quality tooling:

### Implementation Timeline

| App | ESLint 9 | Prettier | Vitest | GitHub CI | Zod Env | Pino Logging | Completion Date |
|-----|----------|----------|--------|-----------|---------|--------------|-----------------|
| **FliGen** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 2026-02-10 |
| **FliHub** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 2026-01-15 |
| **FliDeck** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 2026-02-11 |
| **Storyline App** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 2026-02-14 |

### What's Implemented Everywhere

1. **ESLint 9 with Flat Config** - Root-level linting with TypeScript and React support
2. **Prettier** - Consistent code formatting across all workspaces
3. **Vitest Testing** - Client and server test infrastructure
4. **GitHub Actions CI** - Automated linting, formatting, type checking, and testing
5. **Zod Environment Validation** - Type-safe environment variable validation
6. **Pino Structured Logging** - Production-ready logging with pretty-print for development

---

**Updated**: 2026-02-14
**Status**: All dependency updates complete, quality tooling implemented across all apps
