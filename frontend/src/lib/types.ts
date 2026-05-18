export interface PluginInfo {
  name: string;
  display_name: string;
  description: string;
  category: string;
  requires_auth: boolean;
  default_enabled: boolean;
}

export interface PluginConfig {
  name: string;
  enabled: boolean;
  config: Record<string, unknown>;
}

export interface SearchResult {
  source: string;
  source_url: string;
  title: string;
  summary: string;
  authors: string[];
  published_date: string | null;
  url: string | null;
  metadata: Record<string, unknown>;
  relevance_score: number;
}

export interface ResearchHotspot {
  topic: string;
  intensity: 'high' | 'medium' | 'low';
  description: string;
  key_sources: number[];
}

export interface Innovation {
  innovation: string;
  year: number;
  significance: string;
  source_indices: number[];
}

export interface TimelineEntry {
  year: number;
  event: string;
  significance: string;
}

export interface HistoricalContext {
  timeline: TimelineEntry[];
  narrative: string;
}

export interface KeyPaper {
  title: string;
  source: string;
  url: string;
  why_important: string;
}

export interface Methodology {
  name: string;
  description: string;
  maturity: 'established' | 'emerging' | 'experimental';
}

export interface Debate {
  topic: string;
  summary: string;
  source_indices: number[];
}

export interface EmergingTrend {
  trend: string;
  confidence: 'high' | 'medium' | 'low';
  evidence: string;
}

export interface GapOpportunity {
  gap: string;
  opportunity: string;
}

export interface RecommendedReading {
  title: string;
  url: string;
  priority: number;
}

export interface StructuredAnalysis {
  executive_summary: string;
  research_hotspots: ResearchHotspot[];
  key_innovations: Innovation[];
  historical_context: HistoricalContext;
  key_papers_and_discussions: KeyPaper[];
  methodologies_and_approaches: Methodology[];
  controversies_and_debates: Debate[];
  emerging_trends: EmergingTrend[];
  gaps_and_opportunities: GapOpportunity[];
  recommended_reading: RecommendedReading[];
  search_quality_assessment: string;
}

export interface ResearchTask {
  task_id: string;
  query: string;
  status: 'pending' | 'searching' | 'analyzing' | 'generating' | 'done' | 'failed';
  progress: number;
  progress_message: string | null;
  plugins_used: string[];
  search_results: SearchResult[] | null;
  analysis_raw: string | null;
  analysis_structured: StructuredAnalysis | null;
  error: string | null;
  created_at: string;
  updated_at: string;
  completed_at: string | null;
}

export interface HistoryTask {
  task_id: string;
  query: string;
  status: string;
  progress: number;
  progress_message: string | null;
  plugins_used: string[];
  created_at: string;
  updated_at: string;
  completed_at: string | null;
  error: string | null;
}

export interface SSEEvent {
  phase: string;
  progress: number;
  message: string;
}
