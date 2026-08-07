// Credits: Erwin Lejeune — 2026-02-22
import { NavLink, Outlet, useLocation } from "react-router-dom";

const NAV_SECTIONS = [
  {
    title: "Overview",
    links: [
      { to: "/", label: "Home" },
      { to: "/getting-started", label: "Getting Started" },
    ],
  },
  {
    title: "API Reference",
    links: [
      { to: "/api/client", label: "Sync Client" },
      { to: "/api/async-client", label: "Async Client" },
      { to: "/api/models", label: "Models" },
      { to: "/api/exceptions", label: "Exceptions" },
    ],
  },
  {
    title: "Operations",
    links: [{ to: "/deployment", label: "Deployment" }],
  },
];

function SidebarLink({ to, label }: { to: string; label: string }) {
  return (
    <NavLink
      to={to}
      end={to === "/"}
      className={({ isActive }) =>
        `block border-l-2 px-4 py-1.5 font-mono text-[13px] transition-colors duration-150 ${
          isActive
            ? "sidebar-link-active font-medium"
            : "border-l-transparent text-subtle hover:border-l-muted hover:text-text"
        }`
      }
    >
      {label}
    </NavLink>
  );
}

export default function Layout() {
  const { pathname } = useLocation();

  return (
    <div className="flex min-h-screen">
      <aside className="sticky top-0 flex h-screen w-60 shrink-0 flex-col border-r border-line bg-deep">
        <div className="border-b border-line px-5 py-5">
          <NavLink
            to="/"
            className="font-mono text-base font-bold tracking-tight text-bright"
          >
            epstein<span className="text-ember">exposed</span>
          </NavLink>
          <p className="mt-1 font-mono text-[11px] uppercase tracking-[0.12em] text-muted">
            Python Client Docs
          </p>
        </div>

        <nav className="flex-1 overflow-y-auto px-2 py-4">
          {NAV_SECTIONS.map((section) => (
            <div key={section.title} className="mb-5">
              <h3 className="mb-1.5 px-4 font-mono text-[11px] font-semibold uppercase tracking-[0.12em] text-muted">
                {section.title}
              </h3>
              {section.links.map((link) => (
                <SidebarLink key={link.to} to={link.to} label={link.label} />
              ))}
            </div>
          ))}
        </nav>

        <div className="border-t border-line px-5 py-3">
          <div className="flex items-center gap-4">
            <a
              href="https://github.com/guilyx/epsteinexposed"
              target="_blank"
              rel="noopener noreferrer"
              className="font-mono text-xs text-subtle transition-colors duration-150 hover:text-ember"
            >
              GitHub
            </a>
            <a
              href="https://pypi.org/project/epsteinexposed/"
              target="_blank"
              rel="noopener noreferrer"
              className="font-mono text-xs text-subtle transition-colors duration-150 hover:text-ember"
            >
              PyPI
            </a>
          </div>
        </div>
      </aside>

      <main key={pathname} className="flex-1 overflow-y-auto px-10 py-10 lg:px-16">
        <div className="mx-auto max-w-4xl">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
