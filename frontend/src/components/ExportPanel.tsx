import { FileText, FileCode, FileArchive } from 'lucide-react';
import { getOutputUrl } from '../lib/api';

interface ExportPanelProps {
  taskId: string;
  formats: string[];
}

export default function ExportPanel({ taskId, formats }: ExportPanelProps) {
  const buttons = [
    { format: 'md', icon: FileText, label: 'Markdown', ext: '.md' },
    { format: 'tex', icon: FileCode, label: 'LaTeX', ext: '.tex' },
    { format: 'pdf', icon: FileArchive, label: 'PDF', ext: '.pdf' },
  ].filter((b) => formats.includes(b.format));

  return (
    <div className="flex items-center gap-2">
      <span className="text-xs text-gray-500 mr-1">Download:</span>
      {buttons.map((btn) => (
        <a
          key={btn.format}
          href={getOutputUrl(taskId, btn.format as 'md' | 'tex' | 'pdf')}
          download
          className="flex items-center gap-1.5 px-3 py-1.5 bg-gray-800 hover:bg-gray-700 text-gray-300 hover:text-white rounded-lg text-xs transition"
        >
          <btn.icon size={14} />
          {btn.label}
        </a>
      ))}
    </div>
  );
}
