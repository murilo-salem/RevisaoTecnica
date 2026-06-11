"""
Flags de composição do pipeline para benchmarks e ablation.
"""

from dataclasses import dataclass


@dataclass
class PipelineFeatures:
    """Toggles para comparar variantes do pipeline."""

    require_evidence: bool = True
    enable_thematic_clusters: bool = True
    enable_structural_roles: bool = True
    enable_screening_rerank: bool = True
    enable_prisma: bool = True
    enable_snapshot: bool = True
    enable_comparative_analysis: bool = True
    enable_whitespace_analysis: bool = True
    enable_manual_review_queue: bool = True

    def to_dict(self) -> dict:
        return {
            "require_evidence": self.require_evidence,
            "enable_thematic_clusters": self.enable_thematic_clusters,
            "enable_structural_roles": self.enable_structural_roles,
            "enable_screening_rerank": self.enable_screening_rerank,
            "enable_prisma": self.enable_prisma,
            "enable_snapshot": self.enable_snapshot,
            "enable_comparative_analysis": self.enable_comparative_analysis,
            "enable_whitespace_analysis": self.enable_whitespace_analysis,
            "enable_manual_review_queue": self.enable_manual_review_queue,
        }
