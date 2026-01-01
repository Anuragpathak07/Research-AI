import { Link, useLocation } from "react-router-dom";
import { cn } from "@/lib/utils";

const navItems = [
  { label: "Home", path: "/" },
  { label: "Discover", path: "/discover" },
  { label: "Clusters", path: "/clusters" },
  { label: "Synthesis", path: "/synthesis" },
  { label: "Gaps", path: "/gaps" },
  { label: "Code", path: "/code" },
  { label: "About", path: "/about" },
];

export function Navigation() {
  const location = useLocation();

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-xl border-b border-border/50">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link 
            to="/" 
            className="text-lg font-semibold text-foreground tracking-tight hover:opacity-70 transition-opacity"
          >
            ResearchAI
          </Link>

          {/* Center Navigation */}
          <div className="hidden md:flex items-center gap-1">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={cn(
                  "px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200",
                  location.pathname === item.path
                    ? "text-foreground bg-secondary"
                    : "text-muted-foreground hover:text-foreground hover:bg-secondary/50"
                )}
              >
                {item.label}
              </Link>
            ))}
          </div>

          {/* Right side - could be used for auth later */}
          <div className="w-24" />
        </div>
      </div>
    </nav>
  );
}
