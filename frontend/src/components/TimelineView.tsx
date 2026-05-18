interface TimelineEntry {
  year: number;
  event: string;
  significance: string;
}

interface TimelineViewProps {
  entries: TimelineEntry[];
}

export default function TimelineView({ entries }: TimelineViewProps) {
  const sorted = [...entries].sort((a, b) => a.year - b.year);

  return (
    <div className="relative pl-8">
      <div className="absolute left-[11px] top-2 bottom-2 w-px bg-gray-800" />
      {sorted.map((entry, i) => (
        <div key={i} className="relative pb-6 last:pb-0">
          <div className="absolute -left-[29px] top-1 w-3 h-3 rounded-full border-2 border-blue-500 bg-gray-950" />
          <span className="text-xs font-mono text-blue-400 font-medium">{entry.year}</span>
          <h4 className="text-sm font-medium text-white mt-0.5">{entry.event}</h4>
          <p className="text-xs text-gray-400 mt-0.5">{entry.significance}</p>
        </div>
      ))}
    </div>
  );
}
