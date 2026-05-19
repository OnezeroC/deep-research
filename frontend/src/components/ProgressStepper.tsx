import type { SSEEvent } from '../lib/types';

const PHASES = [
  { key: 'searching', label: 'Searching', icon: '🔍' },
  { key: 'analyzing', label: 'Analyzing', icon: '🧠' },
  { key: 'generating', label: 'Generating', icon: '📄' },
  { key: 'done', label: 'Complete', icon: '✅' },
];

interface ProgressStepperProps {
  events: SSEEvent[];
  status?: string;
}

export default function ProgressStepper({ events, status }: ProgressStepperProps) {
  const currentPhase = status === 'done' ? 3
    : status === 'generating' ? 2
    : status === 'analyzing' ? 1
    : status === 'searching' ? 0
    : -1;

  const latestEvent = events.length > 0 ? events[events.length - 1] : null;

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        {PHASES.map((phase, i) => (
          <div key={phase.key} className="flex-1 flex items-center">
            <div className={`flex items-center gap-2 ${i <= currentPhase ? 'text-white' : 'text-gray-600'}`}>
              <span className="text-lg">{phase.icon}</span>
              <span className="text-xs font-medium">{phase.label}</span>
            </div>
            {i < PHASES.length - 1 && (
              <div className={`flex-1 h-0.5 mx-2 rounded ${i < currentPhase ? 'bg-blue-500' : 'bg-gray-800'}`} />
            )}
          </div>
        ))}
      </div>
      {latestEvent && latestEvent.phase !== 'done' && (
        <div className="flex items-center gap-2 text-sm text-gray-400">
          <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse" />
          {latestEvent.message}
        </div>
      )}
    </div>
  );
}
