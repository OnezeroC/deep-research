interface PluginToggleProps {
  selected: string[];
  onChange: (selected: string[]) => void;
}

const PLUGIN_META: Record<string, { name: string; description: string; category: string }> = {
  arxiv: { name: 'arXiv', description: 'Academic preprints in physics, math, CS', category: 'academic' },
  semantic_scholar: { name: 'Semantic Scholar', description: 'Peer-reviewed papers with citations', category: 'academic' },
  reddit: { name: 'Reddit', description: 'Research discussions and communities', category: 'social' },
  web_search: { name: 'Web Search', description: 'Articles, blogs, and news', category: 'web' },
  twitter: { name: 'Twitter / X', description: 'Real-time research chatter', category: 'social' },
  xiaohongshu: { name: 'Xiaohongshu', description: 'Chinese social platform discussions', category: 'social' },
};

const CATEGORY_COLORS: Record<string, string> = {
  academic: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
  social: 'bg-orange-500/20 text-orange-400 border-orange-500/30',
  web: 'bg-green-500/20 text-green-400 border-green-500/30',
};

export default function PluginToggle({ selected, onChange }: PluginToggleProps) {
  const toggle = (name: string) => {
    if (selected.includes(name)) {
      onChange(selected.filter((s) => s !== name));
    } else {
      onChange([...selected, name]);
    }
  };

  return (
    <div className="flex flex-wrap gap-3">
      {Object.entries(PLUGIN_META).map(([key, meta]) => {
        const isActive = selected.includes(key);
        return (
          <button
            key={key}
            onClick={() => toggle(key)}
            className={`flex items-center gap-2 px-4 py-2.5 rounded-xl border text-sm transition-all ${
              isActive
                ? 'bg-gray-800 border-gray-600 text-white'
                : 'bg-gray-900 border-gray-800 text-gray-500 hover:border-gray-700 hover:text-gray-300'
            }`}
          >
            <span className={`text-[10px] uppercase tracking-wider px-1.5 py-0.5 rounded font-medium ${CATEGORY_COLORS[meta.category]}`}>
              {meta.category}
            </span>
            <span className="font-medium">{meta.name}</span>
            <span className="text-gray-600 text-xs hidden sm:inline">{meta.description.slice(0, 20)}...</span>
          </button>
        );
      })}
    </div>
  );
}
