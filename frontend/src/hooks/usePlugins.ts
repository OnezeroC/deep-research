import { useState, useEffect, useCallback } from 'react';
import { getPlugins, configurePlugin } from '../lib/api';
import type { PluginConfig } from '../lib/types';

export function usePlugins() {
  const [plugins, setPlugins] = useState<PluginConfig[]>([]);
  const [loading, setLoading] = useState(false);

  const fetch = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getPlugins();
      setPlugins(data as PluginConfig[]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetch();
  }, [fetch]);

  const toggle = useCallback(async (name: string, enabled: boolean) => {
    await configurePlugin(name, enabled);
    setPlugins((prev) =>
      prev.map((p) => (p.name === name ? { ...p, enabled } : p))
    );
  }, []);

  return { plugins, loading, refetch: fetch, toggle };
}
