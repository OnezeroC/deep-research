import { FileText, FileCode, FileArchive } from 'lucide-react';
import { getOutputUrl } from '../lib/api';
import { useI18n } from '../lib/i18n';

interface ExportPanelProps {
  taskId: string;
  formats: string[];
}

export default function ExportPanel({ taskId, formats }: ExportPanelProps) {
  const { t } = useI18n();

  const buttons = [
    { format: 'md', icon: FileText, label: t('export.markdown'), ext: '.md' },
    { format: 'tex', icon: FileCode, label: t('export.latex'), ext: '.tex' },
    { format: 'pdf', icon: FileArchive, label: t('export.pdf'), ext: '.pdf' },
  ].filter((b) => formats.includes(b.format));

  return (
    <div className="flex items-center gap-2">
      <span className="text-xs text-gray-500 mr-1">{t('results.download')}</span>
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
