class DeepResearchError(Exception):
    pass


class PluginError(DeepResearchError):
    pass


class AnalysisError(DeepResearchError):
    pass


class OutputError(DeepResearchError):
    pass
