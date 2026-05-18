interface PaperCardProps {
  title: string;
  source: string;
  authors?: string[];
  summary?: string;
  url?: string;
  publishedDate?: string;
  relevanceScore?: number;
}

const SOURCE_COLORS: Record<string, string> = {
  arxiv: 'bg-red-500/20 text-red-400',
  semantic_scholar: 'bg-blue-500/20 text-blue-400',
  reddit: 'bg-orange-500/20 text-orange-400',
  web_search: 'bg-green-500/20 text-green-400',
};

export default function PaperCard({
  title,
  source,
  authors,
  summary,
  url,
  publishedDate,
  relevanceScore,
}: PaperCardProps) {
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 hover:border-gray-700 transition">
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <a
            href={url || '#'}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm font-medium text-white hover:text-blue-400 transition line-clamp-2"
          >
            {title}
          </a>
          {authors && authors.length > 0 && (
            <p className="text-xs text-gray-500 mt-1">{authors.slice(0, 3).join(', ')}</p>
          )}
          {summary && (
            <p className="text-xs text-gray-400 mt-2 line-clamp-3">{summary}</p>
          )}
        </div>
        <div className="shrink-0 flex flex-col items-end gap-1">
          <span className={`text-[10px] px-2 py-0.5 rounded font-medium ${SOURCE_COLORS[source] || 'bg-gray-800 text-gray-400'}`}>
            {source}
          </span>
          {publishedDate && (
            <span className="text-[10px] text-gray-600">{publishedDate}</span>
          )}
        </div>
      </div>
    </div>
  );
}
