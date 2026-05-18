import { NavLink, Outlet } from 'react-router-dom';
import { Search, Clock, Settings } from 'lucide-react';

export default function Layout() {
  return (
    <div className="flex h-screen bg-gray-950">
      <aside className="w-56 border-r border-gray-800 flex flex-col shrink-0">
        <div className="p-4 border-b border-gray-800">
          <h1 className="text-lg font-bold text-white tracking-tight">Deep Research</h1>
          <p className="text-xs text-gray-500 mt-0.5">AI-powered research assistant</p>
        </div>
        <nav className="flex-1 p-3 space-y-1">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition ${
                isActive ? 'bg-gray-800 text-white' : 'text-gray-400 hover:text-white hover:bg-gray-800/50'
              }`
            }
          >
            <Search size={16} />
            New Research
          </NavLink>
          <NavLink
            to="/history"
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition ${
                isActive ? 'bg-gray-800 text-white' : 'text-gray-400 hover:text-white hover:bg-gray-800/50'
              }`
            }
          >
            <Clock size={16} />
            History
          </NavLink>
          <NavLink
            to="/settings"
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition ${
                isActive ? 'bg-gray-800 text-white' : 'text-gray-400 hover:text-white hover:bg-gray-800/50'
              }`
            }
          >
            <Settings size={16} />
            Settings
          </NavLink>
        </nav>
        <div className="p-4 border-t border-gray-800 text-xs text-gray-600">
          v0.1.0
        </div>
      </aside>
      <main className="flex-1 overflow-auto">
        <Outlet />
      </main>
    </div>
  );
}
