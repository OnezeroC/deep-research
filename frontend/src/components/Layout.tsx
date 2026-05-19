import { NavLink, Outlet } from 'react-router-dom';
import { Search, Clock, Settings, Globe } from 'lucide-react';
import { useI18n } from '../lib/i18n';

export default function Layout() {
  const { t, lang, setLang } = useI18n();

  return (
    <div className="flex h-screen bg-gray-950">
      <aside className="w-56 border-r border-gray-800 flex flex-col shrink-0">
        <div className="p-4 border-b border-gray-800">
          <h1 className="text-lg font-bold text-white tracking-tight">{t('app.title')}</h1>
          <p className="text-xs text-gray-500 mt-0.5">{t('app.subtitle')}</p>
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
            {t('nav.new')}
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
            {t('nav.history')}
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
            {t('nav.settings')}
          </NavLink>
        </nav>
        <div className="p-3 border-t border-gray-800">
          <button
            onClick={() => setLang(lang === 'en' ? 'zh' : 'en')}
            className="flex items-center gap-2 w-full px-3 py-2 rounded-lg text-xs text-gray-400 hover:text-white hover:bg-gray-800/50 transition"
          >
            <Globe size={14} />
            {lang === 'en' ? '中文' : 'English'}
          </button>
        </div>
        <div className="px-4 pb-3 text-xs text-gray-600">
          v0.1.0
        </div>
      </aside>
      <main className="flex-1 overflow-auto">
        <Outlet />
      </main>
    </div>
  );
}
