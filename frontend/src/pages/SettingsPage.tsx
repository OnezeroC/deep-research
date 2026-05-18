import { useState, useEffect } from 'react';
import { usePlugins } from '../hooks/usePlugins';
import { getConfig } from '../lib/api';
import { Loader2, Brain } from 'lucide-react';

const PLUGIN_META: Record<string, { displayName: string; description: string; category: string; requiresAuth: boolean }> = {
  arxiv: { displayName: 'arXiv', description: 'Search academic preprints', category: 'academic', requiresAuth: false },
  semantic_scholar: { displayName: 'Semantic Scholar', description: 'Search peer-reviewed papers', category: 'academic', requiresAuth: false },
  reddit: { displayName: 'Reddit', description: 'Search research discussions', category: 'social', requiresAuth: false },
  web_search: { displayName: 'Web Search', description: 'Search the web via DuckDuckGo', category: 'web', requiresAuth: false },
  twitter: { displayName: 'Twitter / X', description: 'Search tweets (experimental)', category: 'social', requiresAuth: false },
  xiaohongshu: { displayName: 'Xiaohongshu', description: 'Search Xiaohongshu (experimental)', category: 'social', requiresAuth: false },
};

const PROVIDER_META: Record<string, { name: string; description: string }> = {
  anthropic: { name: 'Anthropic (Claude)', description: 'Claude Sonnet/Opus with extended thinking' },
  openai: { name: 'OpenAI', description: 'GPT-4.1, GPT-4o, and other OpenAI models' },
  deepseek: { name: 'DeepSeek', description: 'DeepSeek-V3 and DeepSeek-R1 models' },
  openai_compatible: { name: 'OpenAI Compatible', description: 'Any OpenAI-compatible API (Ollama, vLLM, LM Studio, etc.)' },
};

interface ProviderConfig {
  model: string;
  max_tokens: number;
  base_url?: string | null;
  has_key: boolean;
}

interface Config {
  ai_provider: string;
  providers: Record<string, ProviderConfig>;
}

export default function SettingsPage() {
  const { plugins, loading, toggle } = usePlugins();
  const [config, setConfig] = useState<Config | null>(null);
  const [configLoading, setConfigLoading] = useState(true);

  useEffect(() => {
    getConfig()
      .then(setConfig)
      .catch(() => {})
      .finally(() => setConfigLoading(false));
  }, []);

  return (
    <div className="max-w-2xl mx-auto px-8 py-8">
      <h1 className="text-2xl font-bold text-white mb-8">Settings</h1>

      {/* AI Provider */}
      <div className="mb-10">
        <div className="flex items-center gap-2 mb-4">
          <Brain size={16} className="text-blue-400" />
          <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">AI Provider</h2>
        </div>

        {configLoading ? (
          <div className="flex items-center justify-center py-6 text-gray-500">
            <Loader2 size={20} className="animate-spin" />
          </div>
        ) : config ? (
          <div className="space-y-4">
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-400 font-medium uppercase">
                  Active
                </span>
                <span className="text-sm font-medium text-white">
                  {PROVIDER_META[config.ai_provider]?.name || config.ai_provider}
                </span>
              </div>
              <p className="text-xs text-gray-500">
                {PROVIDER_META[config.ai_provider]?.description}
              </p>
              {config.providers[config.ai_provider] && (
                <div className="mt-2 flex items-center gap-4 text-[11px] text-gray-600">
                  <span>Model: <code className="text-gray-400">{config.providers[config.ai_provider].model}</code></span>
                  <span>Key: {config.providers[config.ai_provider].has_key ? 'Configured' : 'Not set'}</span>
                </div>
              )}
            </div>

            <p className="text-xs text-gray-600">
              To switch providers, set <code className="text-gray-400">AI_PROVIDER</code> and the corresponding API key
              in your <code className="text-gray-400">backend/.env</code> file, then restart the backend.
            </p>

            <div className="grid grid-cols-2 gap-2">
              {Object.entries(PROVIDER_META).map(([key, meta]) => {
                const isActive = config.ai_provider === key;
                const providerConfig = config.providers[key];
                return (
                  <div
                    key={key}
                    className={`bg-gray-900 border rounded-xl p-3 transition ${
                      isActive ? 'border-blue-500/50' : 'border-gray-800'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-medium text-white">{meta.name}</span>
                      {isActive && (
                        <span className="w-2 h-2 rounded-full bg-blue-400" />
                      )}
                    </div>
                    <p className="text-[10px] text-gray-500 mb-1.5">{meta.description}</p>
                    {providerConfig && (
                      <div className="flex items-center gap-2 text-[10px]">
                        <span className="text-gray-600">{providerConfig.model}</span>
                        <span className={`px-1 py-0.5 rounded ${
                          providerConfig.has_key ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                        }`}>
                          {providerConfig.has_key ? 'key set' : 'no key'}
                        </span>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        ) : (
          <p className="text-xs text-gray-500">Failed to load config. Is the backend running?</p>
        )}
      </div>

      {/* Search Sources */}
      <div className="space-y-2">
        <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">Search Sources</h2>

        {loading && plugins.length === 0 && (
          <div className="flex items-center justify-center py-10 text-gray-500">
            <Loader2 size={20} className="animate-spin" />
          </div>
        )}

        {plugins.map((plugin) => {
          const meta = PLUGIN_META[plugin.name] || {
            displayName: plugin.name,
            description: '',
            category: 'other',
            requiresAuth: false,
          };

          return (
            <div key={plugin.name} className="bg-gray-900 border border-gray-800 rounded-xl p-4 flex items-center justify-between">
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="text-sm font-medium text-white">{meta.displayName}</h3>
                  {meta.requiresAuth && (
                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-yellow-500/20 text-yellow-400">Auth Required</span>
                  )}
                </div>
                <p className="text-xs text-gray-500 mt-0.5">{meta.description}</p>
              </div>
              <button
                onClick={() => toggle(plugin.name, !plugin.enabled)}
                className={`relative w-10 h-6 rounded-full transition-colors ${
                  plugin.enabled ? 'bg-blue-600' : 'bg-gray-700'
                }`}
              >
                <div
                  className={`absolute top-0.5 w-5 h-5 rounded-full bg-white transition-transform ${
                    plugin.enabled ? 'translate-x-[18px]' : 'translate-x-0.5'
                  }`}
                />
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}
