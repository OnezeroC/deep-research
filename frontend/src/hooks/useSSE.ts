import { useEffect, useState, useRef } from 'react';
import { getSSEUrl } from '../lib/api';
import type { SSEEvent } from '../lib/types';

export function useSSE(taskId: string | null) {
  const [events, setEvents] = useState<SSEEvent[]>([]);
  const [connected, setConnected] = useState(false);
  const [done, setDone] = useState(false);
  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    if (!taskId) return;

    setEvents([]);
    setDone(false);

    const url = getSSEUrl(taskId);
    const es = new EventSource(url);
    eventSourceRef.current = es;

    es.onopen = () => setConnected(true);

    es.addEventListener('searching', (e) => {
      const data = JSON.parse(e.data) as SSEEvent;
      setEvents((prev) => [...prev, data]);
    });

    es.addEventListener('analyzing', (e) => {
      const data = JSON.parse(e.data) as SSEEvent;
      setEvents((prev) => [...prev, data]);
    });

    es.addEventListener('generating', (e) => {
      const data = JSON.parse(e.data) as SSEEvent;
      setEvents((prev) => [...prev, data]);
    });

    es.addEventListener('done', (e) => {
      const data = JSON.parse(e.data) as SSEEvent;
      setEvents((prev) => [...prev, data]);
      setDone(true);
      es.close();
    });

    es.addEventListener('error', (e: MessageEvent) => {
      try {
        const data = JSON.parse(e.data) as SSEEvent;
        setEvents((prev) => [...prev, data]);
      } catch {
        // Connection error
      }
      setDone(true);
      es.close();
    });

    es.onerror = () => {
      setConnected(false);
    };

    return () => {
      es.close();
      eventSourceRef.current = null;
    };
  }, [taskId]);

  const latestEvent = events.length > 0 ? events[events.length - 1] : null;

  return { events, connected, done, latestEvent };
}
