import { useParams, Link } from 'react-router-dom';
import { useResearch } from '../hooks/useResearch';
import { useSSE } from '../hooks/useSSE';
import { useI18n } from '../lib/i18n';
import ProgressStepper from '../components/ProgressStepper';
import ResultsTabs from '../components/ResultsTabs';
import PaperCard from '../components/PaperCard';
import TimelineView from '../components/TimelineView';
import ExportPanel from '../components/ExportPanel';
import MarkdownView from '../components/MarkdownView';
import { PlusCircle, ArrowLeft } from 'lucide-react';
import { useEffect } from 'react';

export default function ResultsPage() {
  const { taskId } = useParams<{ taskId: string }>();
  const { task, refetch } = useResearch(taskId || null);
  const { events, done } = useSSE(taskId || null);
  const { t } = useI18n();

  useEffect(() => {
    if (done && task?.status !== 'done') {
      refetch();
    }
  }, [done]);

  if (!taskId) {
    return (
      <div className="flex items-center justify-center h-full text-gray-400">
        {t('results.noTask')}
      </div>
    );
  }

  const isRunning = task?.status && !['done', 'failed'].includes(task?.status);

  return (
    <div className="max-w-5xl mx-auto px-8 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <Link to="/" className="text-gray-400 hover:text-white">
            <ArrowLeft size={20} />
          </Link>
          <div>
            <h1 className="text-xl font-bold text-white">{task?.query || t('results.loading')}</h1>
            <p className="text-xs text-gray-400">
              {task?.status === 'done' ? t('results.complete')
                : task?.status === 'failed' ? t('results.failed')
                : task?.status ? `${t('results.processing')} — ${task.progress_message || t('results.starting')}` : t('results.loading')}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          {task?.status === 'done' && (
            <ExportPanel taskId={taskId} formats={['md', 'tex', 'pdf']} />
          )}
          <Link
            to="/"
            className="flex items-center gap-1.5 px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-xs"
          >
            <PlusCircle size={14} />
            {t('results.new')}
          </Link>
        </div>
      </div>

      {/* Progress (when running) */}
      {isRunning && (
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 mb-6">
          <ProgressStepper events={events} status={task?.status} />
        </div>
      )}

      {/* Error */}
      {task?.status === 'failed' && (
        <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-6 mb-6">
          <h3 className="text-red-400 font-medium text-lg">{t('results.failedTitle')}</h3>
          <p className="text-red-300/80 text-sm mt-1">{task?.error || t('results.failedErr')}</p>
          {task.search_results && task.search_results.length > 0 && (
            <div className="mt-4 pt-4 border-t border-red-500/20">
              <p className="text-sm text-gray-300 mb-2">
                {t('results.searchCompleted', { n: task.search_results.length })}
              </p>
            </div>
          )}
          <Link to="/" className="inline-block mt-4 text-sm text-blue-400 hover:text-blue-300">
            {t('results.tryAgain')}
          </Link>
        </div>
      )}

      {/* Results */}
      {task?.status === 'done' && task.analysis_structured && (
        <ResultsTabs
          tabs={[
            { id: 'summary', label: t('results.tab.summary') },
            { id: 'hotspots', label: t('results.tab.hotspots'), count: task.analysis_structured.research_hotspots.length },
            { id: 'timeline', label: t('results.tab.timeline') },
            { id: 'innovations', label: t('results.tab.innovations'), count: task.analysis_structured.key_innovations.length },
            { id: 'papers', label: t('results.tab.papers'), count: task.analysis_structured.key_papers_and_discussions.length },
            { id: 'debates', label: t('results.tab.debates'), count: task.analysis_structured.controversies_and_debates.length },
            { id: 'raw', label: t('results.tab.raw'), count: task.search_results?.length },
          ]}
        >
          {(activeTab) => {
            const a = task.analysis_structured!;
            switch (activeTab) {
              case 'summary':
                return (
                  <div className="space-y-6">
                    <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
                      <MarkdownView content={a.executive_summary} />
                    </div>
                    {a.emerging_trends.length > 0 && (
                      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
                        <h3 className="text-sm font-semibold text-white mb-3">{t('results.emerging')}</h3>
                        <div className="space-y-3">
                          {a.emerging_trends.map((tr, i) => (
                            <div key={i} className="flex items-start gap-3">
                              <span className={`text-[10px] px-1.5 py-0.5 rounded font-medium shrink-0 mt-0.5 ${
                                tr.confidence === 'high' ? 'bg-green-500/20 text-green-400'
                                : tr.confidence === 'medium' ? 'bg-yellow-500/20 text-yellow-400'
                                : 'bg-gray-500/20 text-gray-400'
                              }`}>
                                {tr.confidence}
                              </span>
                              <div>
                                <p className="text-sm font-medium text-white">{tr.trend}</p>
                                <p className="text-xs text-gray-400 mt-0.5">{tr.evidence}</p>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    {a.gaps_and_opportunities.length > 0 && (
                      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
                        <h3 className="text-sm font-semibold text-white mb-3">{t('results.gaps')}</h3>
                        <div className="space-y-3">
                          {a.gaps_and_opportunities.map((g, i) => (
                            <div key={i} className="border-l-2 border-blue-500/50 pl-3">
                              <p className="text-sm text-white">{g.gap}</p>
                              <p className="text-xs text-gray-400 mt-0.5">{g.opportunity}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
                      <p className="text-xs text-gray-400">{a.search_quality_assessment}</p>
                    </div>
                  </div>
                );
              case 'hotspots':
                return (
                  <div className="space-y-4">
                    {a.research_hotspots.map((h, i) => (
                      <div key={i} className="bg-gray-900 border border-gray-800 rounded-xl p-5">
                        <div className="flex items-center gap-2 mb-2">
                          <h3 className="text-sm font-semibold text-white">{h.topic}</h3>
                          <span className={`text-[10px] px-1.5 py-0.5 rounded font-medium ${
                            h.intensity === 'high' ? 'bg-red-500/20 text-red-400'
                            : h.intensity === 'medium' ? 'bg-yellow-500/20 text-yellow-400'
                            : 'bg-gray-500/20 text-gray-400'
                          }`}>{h.intensity}</span>
                        </div>
                        <p className="text-sm text-gray-300">{h.description}</p>
                      </div>
                    ))}
                  </div>
                );
              case 'timeline':
                return (
                  <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
                    <TimelineView entries={a.historical_context.timeline} />
                    {a.historical_context.narrative && (
                      <div className="mt-6 pt-4 border-t border-gray-800">
                        <MarkdownView content={a.historical_context.narrative} />
                      </div>
                    )}
                  </div>
                );
              case 'innovations':
                return (
                  <div className="space-y-4">
                    {a.key_innovations.map((inv, i) => (
                      <div key={i} className="bg-gray-900 border border-gray-800 rounded-xl p-5">
                        <div className="flex items-center gap-2 mb-1">
                          <h3 className="text-sm font-semibold text-white">{inv.innovation}</h3>
                          <span className="text-xs text-gray-400 font-mono">{inv.year}</span>
                        </div>
                        <p className="text-sm text-gray-300">{inv.significance}</p>
                      </div>
                    ))}
                  </div>
                );
              case 'papers':
                return (
                  <div className="space-y-3">
                    {a.key_papers_and_discussions.map((p, i) => (
                      <PaperCard key={i} title={p.title} source={p.source} summary={p.why_important} url={p.url} />
                    ))}
                  </div>
                );
              case 'debates':
                return (
                  <div className="space-y-4">
                    {a.controversies_and_debates.map((d, i) => (
                      <div key={i} className="bg-gray-900 border border-gray-800 rounded-xl p-5">
                        <h3 className="text-sm font-semibold text-orange-400 mb-2">{d.topic}</h3>
                        <p className="text-sm text-gray-300">{d.summary}</p>
                      </div>
                    ))}
                  </div>
                );
              case 'raw':
                return (
                  <div className="space-y-3">
                    {task.search_results?.map((r, i) => (
                      <PaperCard
                        key={i}
                        title={r.title}
                        source={r.source}
                        authors={r.authors}
                        summary={r.summary}
                        url={r.url || undefined}
                        publishedDate={r.published_date || undefined}
                        relevanceScore={r.relevance_score}
                      />
                    ))}
                  </div>
                );
              default:
                return null;
            }
          }}
        </ResultsTabs>
      )}
    </div>
  );
}
