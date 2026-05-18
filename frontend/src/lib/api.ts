import axios from 'axios';

const BASE_URL = 'http://localhost:8765/api';

export const api = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
});

export async function createResearch(query: string, plugins?: string[], outputFormats?: string[]) {
  const { data } = await api.post('/research', {
    query,
    plugins,
    output_formats: outputFormats || ['md', 'tex', 'pdf'],
  });
  return data;
}

export async function getResearch(taskId: string) {
  const { data } = await api.get(`/research/${taskId}`);
  return data;
}

export async function getHistory(limit = 20, offset = 0) {
  const { data } = await api.get('/research/history', { params: { limit, offset } });
  return data;
}

export async function deleteResearch(taskId: string) {
  await api.delete(`/research/${taskId}`);
}

export async function getPlugins() {
  const { data } = await api.get('/plugins');
  return data.plugins;
}

export async function configurePlugin(name: string, enabled: boolean, config?: Record<string, unknown>) {
  const { data } = await api.put(`/plugins/${name}/config`, { enabled, config: config || {} });
  return data;
}

export function getSSEUrl(taskId: string): string {
  return `${BASE_URL}/research/${taskId}/stream`;
}

export function getOutputUrl(taskId: string, format: 'md' | 'tex' | 'pdf'): string {
  return `${BASE_URL}/research/${taskId}/output.${format}`;
}

export async function getConfig() {
  const { data } = await api.get('/config');
  return data;
}
