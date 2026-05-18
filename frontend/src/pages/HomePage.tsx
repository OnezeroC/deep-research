import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import SearchBar from '../components/SearchBar';
import PluginToggle from '../components/PluginToggle';
import { useStartResearch } from '../hooks/useResearch';

export default function HomePage() {
  const navigate = useNavigate();
  const { start, starting } = useStartResearch();
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
          Deep Research
        </h1>
        <p className="text-gray-400 text-lg">
          Enter a research topic to discover the latest papers, discussions, and insights across multiple platforms.
        </p>
      </div>

      <div className="space-y-6">
        <SearchBar onSearch={handleSearch} loading={starting} />

        <div>
          <p className="text-xs text-gray-500 mb-3 uppercase tracking-wider font-medium">Search Sources</p>
          <PluginToggle selected={selectedPlugins} onChange={setSelectedPlugins} />
        </div>
      </div>

      <div className="mt-16 grid grid-cols-3 gap-4">
        {[
          { title: 'Multi-Source', desc: 'Searches arXiv, Semantic Scholar, Reddit, and more simultaneously' },
          { title: 'AI Analysis', desc: 'Claude synthesizes findings into structured research reports' },
          { title: 'Export Ready', desc: 'Download as Markdown, LaTeX, or PDF for your workflow' },
        ].map((f) => (
          <div key={f.title} className="bg-gray-900 border border-gray-800 rounded-xl p-5">
            <h3 className="text-sm font-semibold text-white mb-1">{f.title}</h3>
            <p className="text-xs text-gray-500">{f.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
