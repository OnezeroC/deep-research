import { Link } from 'react-router-dom';
import { useHistory } from '../hooks/useResearch';
import { Clock, Trash2, ArrowRight, Loader2 } from 'lucide-react';

const STATUS_COLORS: Record<string, string> = {
  pending: 'bg-gray-500/20 text-gray-400',
  searching: 'bg-blue-500/20 text-blue-400',
  analyzing: 'bg-purple-500/20 text-purple-400',
  generating: 'bg-yellow-500/20 text-yellow-400',
  done: 'bg-green-500/20 text-green-400',
  failed: 'bg-red-500/20 text-red-400',
};

export default function HistoryPage() {
  const { tasks, loading, remove } = useHistory();

  return (
    <div className="max-w-4xl mx-auto px-8 py-8">
      <h1 className="text-2xl font-bold text-white mb-6">Research History</h1>

      {loading && tasks.length === 0 && (
        <div className="flex items-center justify-center py-20 text-gray-500">
          <Loader2 size={24} className="animate-spin" />
        </div>
      )}

      {!loading && tasks.length === 0 && (
        <div className="text-center py-20">
          <Clock size={48} className="mx-auto text-gray-700 mb-4" />
          <p className="text-gray-500">No research history yet.</p>
          <Link to="/" className="text-sm text-blue-400 hover:text-blue-300 mt-2 inline-block">
            Start your first research
          </Link>
        </div>
      )}

      <div className="space-y-3">
        {tasks.map((task) => (
          <div
            key={task.task_id}
            className="bg-gray-900 border border-gray-800 rounded-xl p-4 hover:border-gray-700 transition group"
          >
            <div className="flex items-center justify-between">
              <div className="flex-1 min-w-0">
                <Link
                  to={`/research/${task.task_id}`}
                  className="text-sm font-medium text-white hover:text-blue-400 transition line-clamp-1"
                >
                  {task.query}
                </Link>
                <div className="flex items-center gap-2 mt-1.5">
                  <span className={`text-[10px] px-1.5 py-0.5 rounded font-medium ${STATUS_COLORS[task.status] || STATUS_COLORS.pending}`}>
                    {task.status}
                  </span>
                  <span className="text-[10px] text-gray-600">
                    {task.created_at ? new Date(task.created_at).toLocaleDateString() : ''}
                  </span>
                  {task.plugins_used && task.plugins_used.length > 0 && (
                    <span className="text-[10px] text-gray-600">
                      {task.plugins_used.map((p) => p.replace('_', ' ')).join(', ')}
                    </span>
                  )}
                </div>
                {task.error && (
                  <p className="text-xs text-red-400 mt-1">{task.error}</p>
                )}
              </div>
              <div className="flex items-center gap-2 ml-4">
                <Link
                  to={`/research/${task.task_id}`}
                  className="p-2 text-gray-600 hover:text-white transition"
                >
                  <ArrowRight size={16} />
                </Link>
                <button
                  onClick={() => remove(task.task_id)}
                  className="p-2 text-gray-600 hover:text-red-400 transition opacity-0 group-hover:opacity-100"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
