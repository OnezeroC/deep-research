import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import SearchBar from '../components/SearchBar';
import PluginToggle from '../components/PluginToggle';
import { useStartResearch } from '../hooks/useResearch';
import { useI18n } from '../lib/i18n';

export default function HomePage() {
  const navigate = useNavigate();
  const { start, starting } = useStartResearch();
  const { t } = useI18n();
  const [selectedPlugins, setSelectedPlugins] = useState<string[]>([
    'arxiv', 'semantic_scholar', 'reddit', 'web_search',
  ]);

  const handleSearch = async (query: string) => {
    const taskId = await start(query, selectedPlugins, ['md', 'tex', 'pdf']);
    navigate(`/research/${taskId}`);
  };

  return (
    <div className="max-w-3xl mx-auto px-8 py-20">
      <div className="text-center mb-10">
        <h1 className="text-4xl font-bold text-white tracking-tight mb-3">
          {t('home.title')}
        </h1>
        <p className="text-gray-400 text-lg">
          {t('home.subtitle')}
        </p>
      </div>

      <div className="space-y-6">
        <SearchBar onSearch={handleSearch} loading={starting} />

        <div>
          <p className="text-xs text-gray-500 mb-3 uppercase tracking-wider font-medium">{t('home.sources')}</p>
          <PluginToggle selected={selectedPlugins} onChange={setSelectedPlugins} />
        </div>
      </div>

      <div className="mt-16 grid grid-cols-3 gap-4">
        {[
          { t: t('home.feature1.title'), d: t('home.feature1.desc') },
          { t: t('home.feature2.title'), d: t('home.feature2.desc') },
          { t: t('home.feature3.title'), d: t('home.feature3.desc') },
        ].map((f) => (
          <div key={f.t} className="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <h3 className="text-sm font-semibold text-white mb-1">{f.t}</h3>
            <p className="text-xs text-gray-500">{f.d}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
