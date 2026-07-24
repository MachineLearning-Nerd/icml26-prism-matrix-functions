# Limitations and deviations

- GPU/A100 execution is forbidden by the campaign's compute authorization.
- The paper archive provides plots but no training code, raw data, seeds, or
  checkpoints.
- The CPU CIFAR models are intentionally smaller lower bounds and omit
  Shampoo. They are never described as reproductions.
- The GPT estimate assumes a tied 50,257-token embedding and leading
  `12 d^2` transformer weights per layer because the remaining architecture is
  unspecified. It is an optimistic feasibility bound, not observed training.
- Missing evidence is not treated as falsification.
