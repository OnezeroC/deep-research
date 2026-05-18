import { useState, useCallback, useEffect } from 'react';
import { createResearch, getResearch, getHistory, deleteResearch } from '../lib/api';
import type { ResearchTask, HistoryTask } from '../lib/types';

export function useResearch(taskId: string | null) {
  const [task, setTask] = useState<ResearchTask | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchTask = useCallback(async () => {
    if (!taskId) return;
    setLoading(true);
    try {
      const data = await getResearch(taskId);
      setTask(data);
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to fetch task');
    } finally {
      setLoading(false);
    }
  }, [taskId]);

  useEffect(() => {
    fetchTask();
  }, [fetchTask]);

  return { task, loading, error, refetch: fetchTask };
}

export function useStartResearch() {
  const [starting, setStarting] = useState(false);

  const start = useCallback(async (query: string, plugins?: string[], outputFormats?: string[]) => {
    setStarting(true);
    try {
      const data = await createResearch(query, plugins, outputFormats);
      return data.task_id as string;
    } finally {
      setStarting(false);
    }
  }, []);

  return { start, starting };
}

export function useHistory() {
  const [tasks, setTasks] = useState<HistoryTask[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);

  const fetchHistory = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getHistory(50, 0);
      setTasks(data.tasks);
      setTotal(data.total);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  const remove = useCallback(async (id: string) => {
    await deleteResearch(id);
    setTasks((prev) => prev.filter((t) => t.task_id !== id));
    setTotal((prev) => prev - 1);
  }, []);

  return { tasks, total, loading, refetch: fetchHistory, remove };
}
