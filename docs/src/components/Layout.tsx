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
        `block border-l-2 px-4 py-1.5 text-[13px] transition-all duration-150 ${
          isActive
            ? "sidebar-link-active border-l-lavender-grey font-semibold"
            : "border-l-transparent text-lavender-grey/70 hover:border-l-dusk-blue hover:text-alabaster"
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
      <aside className="sticky top-0 flex h-screen w-60 shrink-0 flex-col border-r border-dusk-blue/20 bg-prussian-blue/40">
        <div className="border-b border-dusk-blue/20 px-5 py-5">
          <NavLink to="/" className="glow typewriter-heading text-xl font-bold tracking-widest">
            EPSTEIN<span className="text-lavender-grey">EXPOSED</span>
          </NavLink>
          <p className="mt-1 text-[11px] uppercase tracking-wider text-dusk-blue">
            Python Client Docs
          </p>
        </div>

        <nav className="flex-1 overflow-y-auto px-2 py-4">
          {NAV_SECTIONS.map((section) => (
            <div key={section.title} className="mb-5">
              <h3 className="mb-1.5 px-4 text-[10px] font-bold uppercase tracking-[0.15em] text-dusk-blue">
                {section.title}
              </h3>
              {section.links.map((link) => (
                <SidebarLink key={link.to} to={link.to} label={link.label} />
              ))}
            </div>
          ))}
        </nav>

        <div className="border-t border-dusk-blue/20 px-5 py-3">
          <div className="flex items-center justify-between">
            <a
              href="https://github.com/guilyx/epsteinexposed"
              target="_blank"
              rel="noopener noreferrer"
              className="text-[11px] text-dusk-blue transition hover:text-lavender-grey"
            >
              GitHub &rarr;
            </a>
            <a
              href="https://pypi.org/project/epsteinexposed/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-[11px] text-dusk-blue transition hover:text-lavender-grey"
            >
              PyPI &rarr;
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
