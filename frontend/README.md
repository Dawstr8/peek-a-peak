# 🏔️ Peek-a-Peak - Frontend Application

> **Modern Next.js 15 App Router client with TypeScript, TanStack Query, and interactive geospatial features**

A production-ready frontend application designed for performance and developer experience. This project showcases modern React patterns, strict type safety, and intelligent UI/UX for a summit diary application.

## 🚀 Quick Start

> **Tip:** The recommended way to run this project is using the VS Code Dev Container, which comes with all dependencies pre-installed. See the [Dev Container README](../.devcontainer/README.md) for details.

1. **Install Dependencies**

   ```bash
   cd frontend
   npm install
   ```

2. **Configure Environment**

   ```bash
   cp .env.example .env.local
   # Update NEXT_PUBLIC_API_URL if backend is not on localhost:8000
   ```

3. **Start Development Server**

   ```bash
   npm run dev
   ```

   Visit **http://localhost:3000**

## 🧱 Tech Stack

| Category             | Technologies                                      |
| :------------------- | :------------------------------------------------ |
| **Core**             | Next.js 15.5 (App Router), React 19, TypeScript   |
| **State Management** | TanStack Query v5 (Server State), React Hook Form |
| **Styling**          | Tailwind CSS v4, shadcn/ui, Radix UI              |
| **Geospatial**       | Leaflet, React Leaflet, Marker Clustering         |
| **Validation**       | Zod Schemas (Shared with Backend)                 |
| **Build Tooling**    | Turbopack, ESLint, Prettier                       |

## ✨ Engineering Highlights

### 🏗️ Modern Architecture

- **App Router & Server Components**: Leveraging React 19 features for efficient rendering and reduced client bundle size.
- **Route Groups**: Organized structure with `/(guest)` and `/(logged-in-user)` for clean separation of concerns and auth logic.
- **Strict TypeScript**: Full type safety across the application, including API responses and component props.

### ⚡ Performance & UX

- **Optimistic UI**: Immediate interface updates during data mutations (e.g., uploading photos) for a snappy feel.
- **Dynamic Imports**: Lazy loading heavy components like Maps and Charts to improve Initial Load Time (FCP).
- **Infinite Scrolling**: Implemented with `useInfiniteQuery` and Intersection Observer for seamless content consumption.
- **Skeleton Loading**: Polished loading states using Suspense boundaries to prevent layout shift.

### 🛡️ Data Integrity

- **Zod Validation**: Runtime schema validation for all form inputs and API responses, ensuring data consistency.
- **Smart Upload Flow**: Client-side EXIF extraction to pre-fill location data before the file even hits the server.

## 📁 Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages & layouts
│   │   ├── (guest)/           # Public authentication routes
│   │   ├── (logged-in-user)/  # Protected application routes
│   │   └── api/               # Route Handlers (Proxy)
│   ├── components/            # Reusable UI components
│   │   ├── ui/               # shadcn/ui primitives
│   │   ├── forms/            # Complex form logic
│   │   └── maps/             # Leaflet integrations
│   ├── hooks/                # Custom React hooks
│   ├── lib/                  # Utilities, API clients, Zod schemas
│   └── types/                # Global TypeScript definitions
├── public/                    # Static assets
└── package.json
```

## 🛠️ Available Scripts

| Script          | Description                             |
| :-------------- | :-------------------------------------- |
| `npm run dev`   | Start development server with Turbopack |
| `npm run build` | Create production build                 |
| `npm start`     | Serve production build                  |
| `npm run lint`  | Run static analysis                     |

## �� Common Issues

**Map markers not showing?**
Ensure the backend is running and has seeded data. The map relies on valid coordinates from the API.

**Upload failing?**
Check if the backend `uploads/` directory is writable and the `NEXT_PUBLIC_API_URL` is correctly set in `.env.local`.

---

_Part of the Peek-a-Peak project._
