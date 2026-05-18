import { useState } from 'react';
import { Search, Loader2 } from 'lucide-react';

interface SearchBarProps {
  onSearch: (query: string) => void;
  loading: boolean;
}

export default function SearchBar({ onSearch, loading }: SearchBarProps) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim().length >= 3) {
      onSearch(query.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="relative">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter a research topic (e.g., diffusion models for protein design)..."
          className="w-full px-5 py-4 pl-12 bg-gray-900 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-lg"
          disabled={loading}
        />
        <Search size={20} className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" />
        <button
          type="submit"
          disabled={loading || query.trim().length < 3}
          className="absolute right-2 top-1/2 -translate-y-1/2 px-5 py-2 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 disabled:text-gray-500 text-white rounded-lg transition text-sm font-medium"
        >
          {loading ? <Loader2 size={16} className="animate-spin" /> : 'Analyze'}
        </button>
      </div>
    </form>
  );
}
