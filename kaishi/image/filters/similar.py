"""Filters for image datasets."""
import os
from kaishi.core.pipeline_component import PipelineComponent
from kaishi.core.misc import trim_list_by_inds
from kaishi.core.misc import find_similar_by_value


class FilterSimilar(PipelineComponent):
    """Filter near duplicate files, detected via perceptual hashing ('imagehash' library)."""

    def __init__(self, dataset):
        super().__init__(dataset)
        self.configure()

    def __call__(self):
        hashlist = [
            f.perceptual_hash
            if f.perceptual_hash is not None
            else f.compute_perceptual_hash()
            for f in self.dataset.files
        ]

        duplicate_ind, parent_ind = find_similar_by_value(
            hashlist, self.perceptual_hash_threshold
        )
        for di, pi in zip(duplicate_ind, parent_ind):
            self.dataset.files[pi].children["similar"].append(self.dataset.files[di])
        self.dataset.files, trimmed = trim_list_by_inds(
            self.dataset.files, duplicate_ind
        )
        self.dataset.filtered["similar"] = trimmed

        return trimmed

    def configure(self, perceptual_hash_threshold=3):
        self.perceptual_hash_threshold = perceptual_hash_threshold