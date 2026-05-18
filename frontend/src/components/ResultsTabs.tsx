import { useState } from 'react';

interface Tab {
  id: string;
  label: string;
  count?: number;
}

interface ResultsTabsProps {
  tabs: Tab[];
  children: (activeTab: string) => React.ReactNode;
}

export default function ResultsTabs({ tabs, children }: ResultsTabsProps) {
  const [activeTab, setActiveTab] = useState(tabs[0]?.id || '');

  return (
    <div>
      <div className="flex gap-1 border-b border-gray-800 mb-6 overflow-x-auto">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2.5 text-sm font-medium whitespace-nowrap border-b-2 -mb-px transition ${
              activeTab === tab.id
                ? 'border-blue-500 text-white'
                : 'border-transparent text-gray-500 hover:text-gray-300'
            }`}
          >
            {tab.label}
            {tab.count !== undefined && (
              <span className="ml-1.5 text-xs text-gray-500">({tab.count})</span>
            )}
          </button>
        ))}
      </div>
      <div>{children(activeTab)}</div>
    </div>
  );
}
