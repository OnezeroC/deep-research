import { createContext, useContext, useState, useCallback, type ReactNode } from 'react';

export type Lang = 'en' | 'zh';

const translations: Record<Lang, Record<string, string>> = {
  en: {
    'app.title': 'Deep Research',
    'app.subtitle': 'AI-powered research assistant',
    'nav.new': 'New Research',
    'nav.history': 'History',
    'nav.settings': 'Settings',
    'home.title': 'Deep Research',
    'home.subtitle': 'Enter a research topic to discover the latest papers, discussions, and insights across multiple platforms.',
    'home.placeholder': 'Enter a research topic (e.g., diffusion models for protein design)...',
    'home.analyze': 'Analyze',
    'home.sources': 'Search Sources',
    'home.feature1.title': 'Multi-Source',
    'home.feature1.desc': 'Searches arXiv, Semantic Scholar, Reddit, and more simultaneously',
    'home.feature2.title': 'AI Analysis',
    'home.feature2.desc': 'Claude synthesizes findings into structured research reports',
    'home.feature3.title': 'Export Ready',
    'home.feature3.desc': 'Download as Markdown, LaTeX, or PDF for your workflow',
    'results.loading': 'Loading...',
    'results.noTask': 'No research task specified.',
    'results.complete': 'Research complete',
    'results.failed': 'Research failed',
    'results.processing': 'Processing',
    'results.starting': 'Starting...',
    'results.new': 'New',
    'results.failedTitle': 'Research Failed',
    'results.failedErr': 'Unknown error',
    'results.searchCompleted': 'Search completed with {n} results before failure.',
    'results.tryAgain': 'Try again',
    'results.tab.summary': 'Summary',
    'results.tab.hotspots': 'Hotspots',
    'results.tab.timeline': 'Timeline',
    'results.tab.innovations': 'Innovations',
    'results.tab.papers': 'Papers',
    'results.tab.debates': 'Debates',
    'results.tab.raw': 'Raw Results',
    'results.emerging': 'Emerging Trends',
    'results.gaps': 'Gaps & Opportunities',
    'results.download': 'Download:',
    'results.error.unknown': 'Unknown error',
    'history.title': 'Research History',
    'history.empty': 'No research history yet.',
    'history.start': 'Start your first research',
    'settings.title': 'Settings',
    'settings.aiProvider': 'AI Provider',
    'settings.active': 'Active',
    'settings.switchHint': 'To switch providers, set AI_PROVIDER and the corresponding API key in your backend/.env file, then restart the backend.',
    'settings.loadFailed': 'Failed to load config. Is the backend running?',
    'settings.sources': 'Search Sources',
    'settings.keySet': 'key set',
    'settings.noKey': 'no key',
    'settings.model': 'Model:',
    'settings.configured': 'Configured',
    'settings.notSet': 'Not set',
    'export.markdown': 'Markdown',
    'export.latex': 'LaTeX',
    'export.pdf': 'PDF',
    'plugin.academic': 'academic',
    'plugin.social': 'social',
    'plugin.web': 'web',
  },
  zh: {
    'app.title': '深度科研',
    'app.subtitle': 'AI 驱动的科研助手',
    'nav.new': '新建研究',
    'nav.history': '历史记录',
    'nav.settings': '设置',
    'home.title': '深度科研',
    'home.subtitle': '输入研究方向，发现最新论文、讨论和洞见。',
    'home.placeholder': '输入研究方向（例如：大语言模型推理能力、蛋白质结构预测）...',
    'home.analyze': '开始分析',
    'home.sources': '搜索来源',
    'home.feature1.title': '多源检索',
    'home.feature1.desc': '同时搜索 arXiv、Semantic Scholar、Reddit 等平台',
    'home.feature2.title': 'AI 分析',
    'home.feature2.desc': 'AI 综合分析生成结构化科研报告',
    'home.feature3.title': '多格式导出',
    'home.feature3.desc': '下载 Markdown、LaTeX 或 PDF 用于研究工作流',
    'results.loading': '加载中...',
    'results.noTask': '未指定研究任务。',
    'results.complete': '研究完成',
    'results.failed': '研究失败',
    'results.processing': '处理中',
    'results.starting': '启动中...',
    'results.new': '新建',
    'results.failedTitle': '研究失败',
    'results.failedErr': '未知错误',
    'results.searchCompleted': '搜索获取了 {n} 条结果后失败。',
    'results.tryAgain': '重试',
    'results.tab.summary': '摘要',
    'results.tab.hotspots': '热点',
    'results.tab.timeline': '时间线',
    'results.tab.innovations': '创新点',
    'results.tab.papers': '论文',
    'results.tab.debates': '争议',
    'results.tab.raw': '原始结果',
    'results.emerging': '新兴趋势',
    'results.gaps': '研究缺口与机会',
    'results.download': '下载：',
    'results.error.unknown': '未知错误',
    'history.title': '研究历史',
    'history.empty': '暂无研究记录。',
    'history.start': '开始第一次研究',
    'settings.title': '设置',
    'settings.aiProvider': 'AI 提供商',
    'settings.active': '当前使用',
    'settings.switchHint': '切换提供商请在 backend/.env 中修改 AI_PROVIDER 和对应的 API Key，然后重启后端。',
    'settings.loadFailed': '加载配置失败。后端是否在运行？',
    'settings.sources': '搜索来源',
    'settings.keySet': '已配置',
    'settings.noKey': '未配置',
    'settings.model': '模型：',
    'settings.configured': '已配置',
    'settings.notSet': '未设置',
    'export.markdown': 'Markdown',
    'export.latex': 'LaTeX',
    'export.pdf': 'PDF',
    'plugin.academic': '学术',
    'plugin.social': '社交',
    'plugin.web': '网页',
  },
};

const I18nContext = createContext<{
  lang: Lang;
  t: (key: string, params?: Record<string, string | number>) => string;
  setLang: (lang: Lang) => void;
}>({
  lang: 'en',
  t: (k) => k,
  setLang: () => {},
});

export function useI18n() {
  return useContext(I18nContext);
}

export function I18nProvider({ children }: { children: ReactNode }) {
  const [lang, setLang] = useState<Lang>(() => {
    const saved = localStorage.getItem('deep-research-lang');
    return (saved === 'zh' ? 'zh' : 'en') as Lang;
  });

  const t = useCallback(
    (key: string, params?: Record<string, string | number>) => {
      const dict = translations[lang];
      let text = dict[key] ?? translations.en[key] ?? key;
      if (params) {
        for (const [k, v] of Object.entries(params)) {
          text = text.replace(`{${k}}`, String(v));
        }
      }
      return text;
    },
    [lang],
  );

  const changeLang = useCallback((newLang: Lang) => {
    setLang(newLang);
    localStorage.setItem('deep-research-lang', newLang);
  }, []);

  return (
    <I18nContext.Provider value={{ lang, t, setLang: changeLang }}>
      {children}
    </I18nContext.Provider>
  );
}
