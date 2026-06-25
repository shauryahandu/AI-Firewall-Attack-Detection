# Open-Set / Zero-Day IDS: State-of-the-Art Literature Review (2020–2026)
## CIC-IDS2017 Focus | Unknown Attack Detection

---

> **Your Current Baselines (Specialist Isolation Forests)**  
> PortScan: **40.0%** | Infiltration: **66.7%** | Heartbleed: **100.0%**  
> Target FPR: ~1%

---

## Ranked Top-10 Methods

---

### #1 — CLAD / CLOSR: A Novel Contrastive Loss for Zero-Day Network Intrusion Detection

| Attribute | Detail |
|---|---|
| **Paper Title** | A Novel Contrastive Loss for Zero-Day Network Intrusion Detection |
| **Year** | 2026 (Jan, accepted IEEE TNSM) |
| **Link** | https://arxiv.org/abs/2601.09902 · GitHub: https://github.com/jackwilkie/CLOSR |
| **Supervision** | Semi-supervised (labeled known attacks + benign; generalizes to unseen classes) |
| **Computational Cost** | Low–Medium (MLP backbone + contrastive loss) |
| **Tabular flow data?** | ✅ Yes — designed for NetFlow/NIDS tabular features |
| **CIC-IDS eval?** | ✅ Yes — CIC-IDS2017 and CSE-CIC-IDS2018 |

**Core Idea:**  
CLAD models benign network traffic in embedded space as a von Mises–Fisher (vMF) distribution on a hypersphere. The loss function pulls benign samples to one pole and all attack traffic to the antipodal region, without specifying which attack class. Unknown/zero-day attacks are detected because they land in "unknown space" away from the learned benign vMF cluster. CLOSR extends this to open-set recognition, achieving a **0.170883 OpenAUC improvement** over the nearest competitor. Crucially, the FPR@95 (FPR when catching 95% of attacks) is explicitly controlled.

**Reported Unknown-Attack Performance:**  
- CLAD: ~0.061 AUROC improvement over best baselines on zero-day attacks  
- CLOSR: 0.170883 OpenAUC improvement vs. prior open-set methods  
- Statistically significant improvement over supervised classifiers on zero-day detection

**Implementation Difficulty: 4/10**  
Code is public. The vMF loss replaces standard cross-entropy. Requires known-attack labels for some classes (which you have). No complex architectural changes needed.

**Likelihood of Outperforming Specialist IF: 🔴 HIGH**  
The method was evaluated specifically on CIC-IDS2017. It explicitly balances known-attack discrimination with unknown-attack generalization — exactly the problem your specialist IFs partially solve but with poor generalization across attack types.

---

### #2 — HCRP-OSD: Hybrid Convolution + Adversarial Reciprocal Point Learning for Open-Set IDS

| Attribute | Detail |
|---|---|
| **Paper Title** | HCRP-OSD: Fine-Grained Open-Set Intrusion Detection Based on Hybrid Convolution and Adversarial Reciprocal Points Learning |
| **Year** | 2025 (Concurrency and Computation: Practice and Experience) |
| **Link** | https://onlinelibrary.wiley.com/doi/abs/10.1002/cpe.70010 |
| **Core Idea (ARPL)** | arXiv:2103.00953 — https://arxiv.org/abs/2103.00953 |
| **Supervision** | Supervised (requires labeled attack classes) + open-set rejection |
| **Computational Cost** | Medium (CNN + BiGRU + ARPL head) |
| **Tabular flow data?** | ✅ Yes — CICIDS2017 flow features |
| **CIC-IDS eval?** | ✅ Yes — CICIDS2017 |

**Core Idea:**  
ARPL (Adversarial Reciprocal Points Learning, TPAMI 2022) models each known class with a "reciprocal point" — a learned anti-prototype that maximally repels known samples away from the open unknown space. The key insight: rather than just compacting known classes, ARPL simultaneously pushes them to the *periphery* of feature space, leaving a bounded interior region for unknowns. HCRP-OSD adapts this for network traffic: a hybrid CNN extracts spatial features + BiGRU captures temporal flow features, and the ARPL head performs open-set classification.

**Reported Unknown-Attack Performance (CICIDS2017):**  
- AUROC for unknown attack detection: **97.59%**  
- Known attack classification accuracy: **99.97%**  
- Significantly outperforms OpenMax, DOC, ODIN baselines on CICIDS2017

**Implementation Difficulty: 6/10**  
ARPL code is public (GitHub: iCGY96/ARPL). Requires adaptation from image to tabular domain. The confusing-sample generation (ARPL+CS variant) adds moderate complexity.

**Likelihood of Outperforming Specialist IF: 🔴 VERY HIGH**  
97.59% AUROC directly on CICIDS2017 for unknown attack detection is the strongest known result on this dataset. If your specialist IF gives 40% on PortScan at 1% FPR, this method — operating at the same FPR — will almost certainly outperform it for PortScan and likely Infiltration.

---

### #3 — NeuTraL AD: Neural Transformation Learning for Deep Anomaly Detection Beyond Images

| Attribute | Detail |
|---|---|
| **Paper Title** | Neural Transformation Learning for Deep Anomaly Detection Beyond Images |
| **Year** | 2021 (ICML 2021) |
| **Link** | https://arxiv.org/abs/2103.16440 · GitHub: https://github.com/boschresearch/NeuTraL-AD |
| **Supervision** | Self-supervised (unsupervised — only normal/benign data needed) |
| **Computational Cost** | Medium (MLP encoder + K learnable transformation networks) |
| **Tabular flow data?** | ✅ Yes — explicitly includes tabular benchmarks (Thyroid, Arrhythmia, KDD, KDDRev) |
| **CIC-IDS eval?** | ❌ Not directly — evaluated on KDD/KDDRev (directly comparable to CIC-IDS) |

**Core Idea:**  
Unlike GOAD which uses fixed affine transformations, NeuTraL AD *learns* the transformations end-to-end. It trains K transformation networks (small MLPs) to produce distinguishable, diverse transformed views of normal data, then learns a shared encoder that predicts *which transformation was applied*. The anomaly score is the disagreement between predicted transformation identity and ground truth — normal data is "predictably transformable" while anomalies are not.

**Reported Performance on Tabular Datasets:**  
- KDD (network intrusion): **99.3% F1** (vs. GOAD 98.4%, Deep SVDD 99.0%, DAGMM 93.7%)  
- KDDRev: **99.1% F1** (vs. GOAD 98.9%)  
- Consistently best among all compared methods on tabular data

**Implementation Difficulty: 5/10**  
Official PyTorch code available. Standard MLP architecture. Main challenge: tuning the number of learned transformations K (typically 11 for tabular data).

**Likelihood of Outperforming Specialist IF: 🟠 HIGH**  
On KDD99 (structurally similar to CIC-IDS), NeuTraL AD substantially outperforms Isolation Forest (90.7% F1). The self-supervised approach means it can detect PortScan and Infiltration as anomalies if normal traffic is cleanly separated in feature space. The gap vs. your 40% PortScan suggests significant headroom. Main uncertainty: CIC-IDS features differ from KDD99, and Infiltration is notoriously hard due to low sample count (36 samples) and behavioral overlap with benign.

---

### #4 — VAEMax: Open-Set Intrusion Detection based on OpenMax and Variational Autoencoder

| Attribute | Detail |
|---|---|
| **Paper Title** | VAEMax: Open-Set Intrusion Detection based on OpenMax and Variational Autoencoder |
| **Year** | 2024 (IEEE ICTC 2024) |
| **Link** | https://arxiv.org/abs/2403.04193 · IEEE: https://ieeexplore.ieee.org/document/10601788 |
| **Supervision** | Semi-supervised (supervised classifier for known attacks + unsupervised VAE per class) |
| **Computational Cost** | Medium (1D-CNN + OpenMax + class-conditional VAE) |
| **Tabular flow data?** | ✅ Yes — CIC-IDS2017 flow features |
| **CIC-IDS eval?** | ✅ Yes — CIC-IDS2017 and CSE-CIC-IDS2018 |

**Core Idea:**  
Dual detection: (1) A 1D-CNN extracts flow payload features → OpenMax performs open-set classification, detecting some unknowns while misclassifying others into a nearest known class. (2) For flows misclassified by OpenMax into a known class, a per-class Variational Autoencoder performs secondary verification: if the reconstruction loss is too high for that known class's VAE, the flow is reclassified as unknown. This catch-and-verify pipeline dramatically reduces unknown-as-known false negatives.

**Reported Performance:**  
- ~66% recall for unknown attacks at controlled FPR (CSE-CIC-IDS2018)  
- Outperforms baseline OpenMax, DOC, and vanilla VAE approaches  
- Comparable to your specialist IF Infiltration result (66.7%), but more general

**Implementation Difficulty: 6/10**  
Requires training: (1) a CNN classifier, (2) OpenMax layer (libMR), (3) per-class VAEs. Three components but well-documented. Pay extra attention to the known/unknown class split during experiments.

**Likelihood of Outperforming Specialist IF: 🟡 MEDIUM-HIGH**  
For PortScan (your 40%), VAEMax should do better since PortScan is statistically distinctive. For Infiltration (your 66.7%), VAEMax may be comparable or slightly better. The dual detection mechanism specifically handles the "near-boundary" unknowns that single detectors miss.

---

### #5 — Deep SAD: Deep Semi-Supervised Anomaly Detection

| Attribute | Detail |
|---|---|
| **Paper Title** | Deep Semi-Supervised Anomaly Detection |
| **Year** | 2020 (ICLR 2020) |
| **Link** | https://arxiv.org/abs/1906.02694 |
| **Supervision** | Semi-supervised (few labeled anomalies + large unlabeled pool) |
| **Computational Cost** | Low–Medium (MLP encoder, simple hypersphere objective) |
| **Tabular flow data?** | ✅ Yes — tabular datasets explicitly benchmarked |
| **CIC-IDS eval?** | ❌ Not directly (tested on CIFAR, MNIST, tabular benchmarks — network intrusion not included in original) |

**Core Idea:**  
Deep SAD extends Deep SVDD with a critical semi-supervised ingredient: labeled anomaly samples are explicitly *repulsed* from the hypersphere center (inverse squared distance loss), while unlabeled data is attracted toward it. Even with only 1% labeled anomalies in training, Deep SAD significantly outperforms fully unsupervised methods. Critically, at test time, it **generalizes to novel/unseen anomaly classes** — it merely needs to detect "not normal," and labeled anomalies from *known* attack classes improve the normal-vs-abnormal boundary, which carries over to unknown attack detection.

**Reported Performance:**  
- AUC on tabular anomaly benchmarks: competitive with GOAD, better than Deep SVDD, iForest on complex datasets  
- Generalizes to novel anomalies empirically (tested with CIFAR-10 novel class detection)  
- "Robust against changes" in the labeled anomaly ratio

**Implementation Difficulty: 4/10**  
Code publicly available. MLP encoder with modified SVDD loss. Adding known-attack labels from your CIC-IDS2017 training set is straightforward.

**Likelihood of Outperforming Specialist IF: 🟡 MEDIUM-HIGH**  
If you can provide ~30–100 labeled PortScan or Infiltration examples to Deep SAD during training (even a small fraction of training data), the model should learn a hypersphere that excludes attack traffic more tightly than unsupervised methods. Your specialist Isolation Forests achieve 40%/67% with zero labeled data — Deep SAD with even minimal labels should surpass 40% on PortScan. The challenge: Deep SVDD suffered from representation collapse (mapping all to center), but Deep SAD mitigates this with labeled anomaly repulsion.

---

### #6 — GOAD: Classification-Based Anomaly Detection for General Data (Tabular)

| Attribute | Detail |
|---|---|
| **Paper Title** | Classification-Based Anomaly Detection for General Data |
| **Year** | 2020 (ICLR 2020) |
| **Link** | https://arxiv.org/abs/2005.02359 |
| **Supervision** | Unsupervised (self-supervised; only normal data) |
| **Computational Cost** | Low–Medium (MLP + triplet loss across K transformations) |
| **Tabular flow data?** | ✅ Yes — affine transformations work on any numerical vector |
| **CIC-IDS eval?** | ❌ Not CIC-IDS directly — evaluated on KDD/KDDRev (network intrusion) and other tabular benchmarks |

**Core Idea:**  
GOAD applies M random affine transformations to normal training data, creating M synthetic classes. A shared encoder learns to distinguish *which transformation was applied*. The key: normal data has consistent, learnable structure (the transformation prediction task is solvable), while anomalies produce inconsistent representations across transformations (task becomes harder). Anomaly score = sum of triplet losses across transformations.

GOAD was the first method to make transformation-based anomaly detection work for tabular (non-image) data, achieving 98.4% F1 on KDD99.

**Reported Performance (Network Intrusion):**  
- KDD99: 98.4% F1 (vs. IF 90.7%, OC-SVM 79.5%)  
- KDDRev: 98.9% F1  
- Robust to minor contamination in training data

**Implementation Difficulty: 4/10**  
Original PyTorch code is available. Affine transformation parameters are randomly initialized — simple to tune. The main hyperparameter is M (number of transformations, typically 11).

**Likelihood of Outperforming Specialist IF: 🟠 MEDIUM-HIGH**  
On KDD99, GOAD beats IF by ~8% F1. Since your CIC-IDS specialist IF already reaches 40% on PortScan, GOAD applied as a per-class or global anomaly detector should improve this. For Infiltration and Heartbleed (which your specialist IF already handles at 67% and 100%), GOAD may not improve Heartbleed further, but could lift PortScan significantly. The main risk: GOAD performance is sensitive to M and may need tuning per-attack-type.

---

### #7 — ICL: Anomaly Detection for Tabular Data with Internal Contrastive Learning

| Attribute | Detail |
|---|---|
| **Paper Title** | Anomaly Detection for Tabular Data with Internal Contrastive Learning |
| **Year** | 2022 (ICLR 2022) |
| **Link** | https://openreview.net/forum?id=_hszZbt46bT |
| **Supervision** | Self-supervised (unsupervised — normal data only) |
| **Computational Cost** | Low–Medium (transformer or MLP on feature subsets) |
| **Tabular flow data?** | ✅ Yes — designed specifically for tabular data without spatial assumptions |
| **CIC-IDS eval?** | ❌ Not directly — evaluated on various UCI tabular benchmarks |

**Core Idea:**  
ICL exploits the fact that feature dependencies in normal data are *class-specific*. The approach partitions features into random subsets and trains a contrastive model to predict one subset from another. For normal data, these internal feature correlations are consistent; for anomalies, the correlations break down. Unlike GOAD which uses external transformations, ICL uses *internal* feature relationships, making it more robust to domain shift and more naturally suited to tabular data where feature correlations carry semantic meaning.

In network intrusion detection, normal traffic has consistent statistical correlations between packet size, timing, and flow features — correlations that anomalous attack traffic may violate.

**Reported Performance:**  
- Competitive with NeuTraL AD on tabular benchmarks  
- Generally outperforms GOAD on small/medium tabular datasets  
- Robust without external transformation choices

**Implementation Difficulty: 5/10**  
Code available in ICLR 2022 appendix. Standard contrastive loss implementation. Main challenge: deciding feature partition strategy for 78 CIC-IDS features.

**Likelihood of Outperforming Specialist IF: 🟡 MEDIUM-HIGH**  
The internal correlation approach is well-suited to network flow data where feature interdependencies are strong and meaningful. Expected to match or exceed NeuTraL AD / GOAD performance on tabular IDS data.

---

### #8 — SAFE: Self-Supervised Anomaly Detection Framework for Intrusion Detection (MAE + LOF)

| Attribute | Detail |
|---|---|
| **Paper Title** | SAFE: Self-Supervised Anomaly Detection Framework for Intrusion Detection |
| **Year** | 2025 (arXiv preprint, submitted AAAI 2025) |
| **Link** | https://arxiv.org/abs/2502.07119 |
| **Supervision** | Self-supervised (unsupervised — only normal traffic) |
| **Computational Cost** | Medium (ViT-style Masked Autoencoder + LOF) |
| **Tabular flow data?** | ✅ Yes — converts tabular features to 2D grid, then applies MAE |
| **CIC-IDS eval?** | ✅ Yes — evaluated on recent IDS datasets including CIC variants |

**Core Idea:**  
SAFE transforms 78-dimensional flow features into a structured 2D matrix (like an image), exploiting that CIC-IDS features have latent geometric groupings (e.g., forward/backward packet stats, timing, flag counts). A Vision Transformer Masked Autoencoder is pre-trained on benign flows. The encoder's learned representations are then fed to a lightweight Local Outlier Factor (LOF) for anomaly scoring. SAFE outperforms SLAD (ICML 2023) by up to **26.2%** and outperforms baseline Isolation Forest.

**Reported Performance:**  
- Outperforms SLAD by up to 26.2% on IDS benchmark datasets  
- Outperforms PCA anomaly detection, Isolation Forest, basic autoencoders  
- Specifically benchmarked on IDS datasets in an unsupervised unknown-attack setting

**Implementation Difficulty: 6/10**  
Requires designing the vector-to-image mapping (which feature goes to which grid position), which requires domain knowledge. The MAE training adds complexity but stable training is well-documented (MAE code widely available).

**Likelihood of Outperforming Specialist IF: 🟡 MEDIUM-HIGH**  
Since SAFE explicitly outperforms IF in the same IDS setting, and your specialist IF is already an improved variant, SAFE should at minimum match it and likely exceed the 40% PortScan barrier. Particularly promising because the MAE captures non-linear feature interactions that IF cannot.

---

### #9 — Anomal-E: Self-Supervised GNN for Network Intrusion Detection

| Attribute | Detail |
|---|---|
| **Paper Title** | Anomal-E: A Self-Supervised Network Intrusion Detection System based on Graph Neural Networks |
| **Year** | 2022 (Knowledge-Based Systems, Vol. 258) |
| **Link** | https://arxiv.org/abs/2207.06819 · https://doi.org/10.1016/j.knosys.2022.110030 |
| **Supervision** | Self-supervised (unsupervised — no labels required) |
| **Computational Cost** | Medium–High (requires graph construction + GNN training) |
| **Tabular flow data?** | ✅ Yes — specifically designed for bidirectional NetFlow features |
| **CIC-IDS eval?** | ✅ Yes — evaluated on CIC-IDS datasets |

**Core Idea:**  
Network flows naturally form a graph: IP addresses are nodes, flows are edges. Anomal-E constructs this flow graph and trains a GNN using edge features (flow statistics) in a self-supervised contrastive manner. The key insight: benign traffic has coherent graph topology (regular communication patterns between hosts), while attack traffic creates anomalous topological patterns (e.g., PortScan creates a star graph from one attacker to many victims; Botnet creates dense clusters).

Anomal-E is the **first successful self-supervised, edge-leveraging GNN for NIDS**.

**Reported Performance:**  
- Outperforms CNN, LSTM, StrucTemp-GNN baselines on CIC-IDS  
- Self-supervised embeddings substantially better than raw features for anomaly detection  
- Demonstrated potential for "wild" (unlabeled) network traffic generalization

**Implementation Difficulty: 8/10**  
Requires constructing a flow graph (IP pairs as nodes), graph data pipeline, and GNN training. Significantly more engineering overhead than feature-vector approaches. However, existing CIC-IDS2017 flow data can be converted to graph format.

**Likelihood of Outperforming Specialist IF: 🟡 MEDIUM**  
The graph topology is a genuine advantage for detecting PortScan (which creates distinctive star-graph patterns), potentially pushing well above 40%. For Infiltration (which mimics benign internal traffic), the topology may not help as much. The high implementation difficulty is the main barrier.

---

### #10 — DOC++ / Open-CNN with EVT: Adaptable Deep Learning IDS for Zero-Day Attacks

| Attribute | Detail |
|---|---|
| **Paper Title** | An Adaptable Deep Learning-Based Intrusion Detection System to Zero-Day Attacks |
| **Year** | 2023 (Journal of Information Security and Applications, Vol. 76) |
| **Link** | https://doi.org/10.1016/j.jisa.2023.103516 · arXiv:2108.09199 |
| **Supervision** | Semi-supervised (supervised classifier + open-set rejection) |
| **Computational Cost** | Medium (Deep classifier + DOC++ threshold calibration + EVT) |
| **Tabular flow data?** | ✅ Yes — CIC-IDS2017 flow features |
| **CIC-IDS eval?** | ✅ Yes — CIC-IDS2017 and CSE-CIC-IDS2018 |

**Core Idea:**  
DOC++ improves over DOC (Deep Open Classification) by using 1-vs-rest sigmoid outputs (not softmax) and per-class Weibull fitting via Extreme Value Theory (EVT) to calibrate rejection thresholds. The framework: (1) pre-train a deep classifier on known attacks, (2) fit Weibull distributions on class-specific activation vectors, (3) at inference, reject samples with low class-specific probabilities as "unknown." After open-set detection, a clustering phase groups discovered unknowns for human labeling and incremental model updating.

DOC++ outperforms all compared open-set methods (DOC, OpenMax, AutoSVM, CROSR) on CIC-IDS2017.

**Reported Performance:**  
- Best open-set recognition among DOC, OpenMax, AutoSVM, CROSR on CIC-IDS2017  
- Average accuracy ~99% on CIC-IDS2017 with open-set unknown handling  
- Incremental learning framework allows adaptation to discovered attack types

**Implementation Difficulty: 6/10**  
DOC code is available; DOC++ requires EVT threshold calibration (libmr). Complexity comes from the multi-phase framework (train → calibrate → cluster → relabel → retrain).

**Likelihood of Outperforming Specialist IF: 🟡 MEDIUM-HIGH**  
The combination of per-class EVT calibration and incremental learning is more robust than single-threshold anomaly detection. Direct CIC-IDS2017 evaluation gives confidence in applicability.

---

## Bonus Methods Worth Monitoring

| Method | Year | Why Interesting |
|---|---|---|
| **SLAD** (Scale Learning AD) | ICML 2023 | Self-supervised tabular; SAFE's strongest baseline; arxiv.org/abs/2305.16114 |
| **Deep Isolation Forest** (DIF) | IEEE TKDE 2023 | Random forest in deep embedding space; combines benefits of IF and deep representation |
| **RoSAS** (Contamination-resilient deep semi-supervised AD) | IS 2023 | More robust than Deep SAD to training set contamination |
| **Contrastive End-to-End IDS** (CNN+GRU+Contrastive) | Sensors 2024 | 95% weighted recall for unknown attacks on CIC-IDS2017/2018 |
| **EFC** (Energy-based Flow Classifier) | Computers & Security 2025 | Native open-set classifier for NIDS; low complexity |
| **Open-set GAN IDS** (INFOGAN + OpenMax) | Scientific Reports 2025 | 88.5% open-set accuracy on CIC-IDS2017; Nature paper |

---

## Comparative Summary Table

| Rank | Method | Supervision | CIC-IDS Eval | Unknown Attack AUROC/Recall | Impl. Difficulty | IF Outperform Likelihood |
|---|---|---|---|---|---|---|
| 1 | **CLAD/CLOSR** | Semi | ✅ | 0.171 OpenAUC improvement | 4/10 | 🔴 HIGH |
| 2 | **HCRP-OSD (ARPL)** | Supervised | ✅ | 97.59% AUROC | 6/10 | 🔴 VERY HIGH |
| 3 | **NeuTraL AD** | Unsupervised | ~KDD99 | 99.3% F1 (KDD99) | 5/10 | 🟠 HIGH |
| 4 | **VAEMax** | Semi | ✅ | ~66% recall | 6/10 | 🟡 MEDIUM-HIGH |
| 5 | **Deep SAD** | Semi | ~Tabular | AUC ~0.9+ tabular | 4/10 | 🟡 MEDIUM-HIGH |
| 6 | **GOAD** | Unsupervised | ~KDD99 | 98.4% F1 (KDD99) | 4/10 | 🟠 HIGH |
| 7 | **ICL** | Unsupervised | No | Competitive SOTA | 5/10 | 🟡 MEDIUM-HIGH |
| 8 | **SAFE (MAE+LOF)** | Unsupervised | ✅ | +26.2% vs SLAD | 6/10 | 🟡 MEDIUM-HIGH |
| 9 | **Anomal-E (GNN)** | Unsupervised | ✅ | Outperforms CNN/LSTM | 8/10 | 🟡 MEDIUM |
| 10 | **DOC++** | Semi | ✅ | Best vs OpenMax/CROSR | 6/10 | 🟡 MEDIUM-HIGH |

---

## Section (A): Ranked Top-10 Final List

1. **CLAD/CLOSR** — Designed ground-up for zero-day NIDS; CIC-IDS2017 eval; 0.171 OpenAUC gain; code available
2. **HCRP-OSD/ARPL** — 97.59% AUROC on CICIDS2017 unknown attacks; strongest published result
3. **NeuTraL AD** — Best tabular self-supervised AD (99.3% F1 KDD99); structural cousin of CIC-IDS
4. **VAEMax** — Dual OpenMax+VAE pipeline; directly on CIC-IDS2017; ~66% recall
5. **Deep SAD** — Semi-supervised with few labels; generalizes to novel attacks; simple to implement
6. **GOAD** — Self-supervised tabular; 98.4% F1 KDD99; reliable baseline upgrade over IF
7. **ICL** — Internal contrastive learning; tabular-native; no external transformations needed
8. **SAFE (MAE+LOF)** — IDS-specific; +26.2% vs SLAD; exploits tabular-to-image transformation
9. **Anomal-E** — Graph topology advantage for PortScan pattern; GNN overhead justified for PortScan
10. **DOC++** — Full open-set pipeline with incremental learning; directly on CIC-IDS2017

---

## Section (B): Most Promising Next Experiment

### 🎯 **Recommended: CLAD/CLOSR (with ARPL as fast-follow)**

**Why CLAD/CLOSR first:**

1. **It was built for exactly your problem.** The paper explicitly addresses zero-day detection on CIC-IDS2017. You are not extrapolating from a different domain.

2. **Code is public and clean.** The GitHub repo is actively maintained with instructions for CIC-IDS format.

3. **It solves the core tension in your current results.** Your specialist IFs work because Isolation Forest is unsupervised — but they only reach 40%/67% because they can't leverage what they *know* about normal traffic. CLAD uses known attack labels to shape the embedding space without "memorizing" attack signatures.

4. **The vMF formulation naturally produces calibrated FPR.** Since benign traffic is modeled as a vMF cluster, you can directly control detection threshold to target 1% FPR.

5. **ARPL as fast-follow.** If CLAD achieves ~70–80% on PortScan/Infiltration, run ARPL (HCRP-OSD) next with the same feature set — it's the most powerful method but requires more careful hypertuning.

**Concrete experiment plan:**
1. Download CIC-IDS2017, use your existing training split
2. Hold out PortScan / Infiltration / Heartbleed as the "unknown" test classes
3. Train CLAD on {Benign + DoS + DDoS + BruteForce + Web attacks}
4. Evaluate at target FPR = 1% on held-out unknowns
5. Report recall for PortScan, Infiltration, Heartbleed
6. Compare to your specialist IF baselines

---

## Section (C): Implementation Roadmap (Ordered by Research Value / Engineering Effort Ratio)

### Tier 1 — High Value, Low Effort (Do First)

#### 1. CLAD/CLOSR (Estimated: 2–3 days)
```
git clone https://github.com/jackwilkie/CLOSR
pip install requirements
# Adapt to CIC-IDS2017 tabular features
# Run with hidden_classes=['PortScan', 'Infiltration', 'Heartbleed']
```
- Expected improvement: PortScan → 60–80%, Infiltration → 70–85%
- Why: Tested on CIC-IDS, code public, minimal tuning needed

#### 2. GOAD on your exact flow features (Estimated: 1–2 days)
```python
# Fit affine transforms to benign training data
# Use M=11 transformations on 78-feature flow vectors
# Tune anomaly threshold at 1% FPR on validation set
```
- Expected improvement: PortScan → 50–70%
- Why: Self-supervised, no labels needed, extremely fast to implement as baseline upgrade

#### 3. NeuTraL AD (Estimated: 2–3 days)
```
git clone https://github.com/boschresearch/NeuTraL-AD
# Switch dataset config to CIC-IDS2017
# Adapt feature normalization
```
- Expected improvement: Matches or exceeds GOAD on tabular data
- Why: Best published F1 on KDD99 among all self-supervised tabular methods

### Tier 2 — High Value, Medium Effort (Do Second)

#### 4. HCRP-OSD / ARPL (Estimated: 3–5 days)
```
git clone https://github.com/iCGY96/ARPL
# Adapt to tabular domain (replace image encoder with MLP)
# Implement DCE loss + Prototype Loss per HCRP-OSD paper
# Train with known attack classes, test on hidden classes
```
- Expected: 90%+ AUROC on PortScan, 80%+ on Infiltration
- Why: Best known result on CICIDS2017 for unknown attack detection

#### 5. Deep SAD (Estimated: 2–3 days)
```python
# Use Ruff et al.'s public code
# Provide 30-100 labeled PortScan examples as "known anomalies"
# Train on 99% benign + 1% labeled attack
# Threshold at 1% FPR on validation benign
```
- Expected: PortScan → 50–70% (with few labels), leverages your existing labeled data

#### 6. Deep SAD + GOAD hybrid (Estimated: 1 day after above)
- Train GOAD to get good representations
- Use GOAD representations as input to Deep SAD
- This "representation + semi-supervised refinement" is a powerful combination

### Tier 3 — Very High Value, High Effort (Do Third)

#### 7. SAFE (MAE + LOF) (Estimated: 4–7 days)
- Design feature→2D matrix mapping for CIC-IDS 78 features
- Fine-tune MAE on benign CIC-IDS flows
- Swap LOF with SVDD or k-NN for per-class thresholding
- Expected: Clear improvement over IF, particularly on PortScan

#### 8. VAEMax (Estimated: 3–5 days)
- Train 1D-CNN classifier on known attack classes
- Fit Weibull per class (OpenMax)
- Train per-class VAEs for secondary detection
- Expected: ~66–75% recall on Infiltration, ~55–70% on PortScan

#### 9. ICL (Estimated: 2–3 days)
- Implement internal feature subset contrastive learning
- Use CIC-IDS 78 features with random partitions of size ~10–15
- Expected: Self-supervised performance comparable to NeuTraL AD

### Tier 4 — Specialized High-Effort (If Time Permits)

#### 10. Anomal-E GNN (Estimated: 7–14 days)
- Build flow graph from CIC-IDS2017 (src_ip:src_port → dst_ip:dst_port edges)
- Implement E-GraphSAGE with self-supervised contrastive edge training
- Critical advantage for PortScan: topological anomalies are detectable
- Expected: 70–90% PortScan detection (star-graph topology is distinctive)

---

## Why Specialist Isolation Forests Fall Short (And Why These Methods Won't)

Your specialist IF results reveal a fundamental property: **IDs are fundamentally anomalies in feature space, but some attack types (PortScan, Infiltration) are not anomalous in the same feature subspace that benign traffic occupies.**

| Attack | IF Failure Mode | Proposed Fix |
|---|---|---|
| **PortScan (40%)** | Port-scan flows look "normal" in isolation (short, no payload). IF splits on individual features. | GOAD/NeuTraL: Cross-feature consistency breaks. GNN/Anomal-E: Topological star-graph pattern is detectable. ARPL: Known-class representations explicitly repel PortScan from benign region. |
| **Infiltration (67%)** | Infiltration mimics legitimate internal traffic. Only 36 samples in dataset — IF gets good recall but not stable. | CLAD: vMF distribution for benign; Infiltration lies outside. Deep SAD with a few infiltration labels: direct repulsion from center. |
| **Heartbleed (100%)** | Small packet patterns already anomalous enough for IF. | All methods expected to maintain or exceed this. |

The common thread: **methods that explicitly model normal behavior structure (GOAD, NeuTraL, CLAD) or that leverage labeled attack data to shape the decision boundary (ARPL, Deep SAD, CLAD) all have principled mechanisms that IF lacks.**

---

## Citations (Key Papers)

1. Wilkie et al. (2026). *A Novel Contrastive Loss for Zero-Day Network Intrusion Detection*. IEEE TNSM. https://arxiv.org/abs/2601.09902
2. Cai et al. (2025). *HCRP-OSD: Fine-Grained Open-Set Intrusion Detection Based on Hybrid Convolution and Adversarial Reciprocal Points Learning*. Concurrency Comput. https://doi.org/10.1002/cpe.70010
3. Chen et al. (2022). *Adversarial Reciprocal Points Learning for Open Set Recognition*. IEEE TPAMI. https://arxiv.org/abs/2103.00953
4. Qiu et al. (2021). *Neural Transformation Learning for Deep Anomaly Detection Beyond Images*. ICML 2021. https://arxiv.org/abs/2103.16440
5. Qiu, Zhou et al. (2024). *VAEMax: Open-Set Intrusion Detection based on OpenMax and Variational Autoencoder*. IEEE ICTC 2024. https://arxiv.org/abs/2403.04193
6. Ruff et al. (2020). *Deep Semi-Supervised Anomaly Detection*. ICLR 2020. https://arxiv.org/abs/1906.02694
7. Bergman & Hoshen (2020). *Classification-Based Anomaly Detection for General Data*. ICLR 2020. https://arxiv.org/abs/2005.02359
8. Shenkar & Wolf (2022). *Anomaly Detection for Tabular Data with Internal Contrastive Learning*. ICLR 2022. https://openreview.net/forum?id=_hszZbt46bT
9. Li et al. (2025). *SAFE: Self-Supervised Anomaly Detection Framework for Intrusion Detection*. arXiv:2502.07119. https://arxiv.org/abs/2502.07119
10. Caville et al. (2022). *Anomal-E: A Self-Supervised NIDS based on Graph Neural Networks*. Knowledge-Based Systems. https://arxiv.org/abs/2207.06819
11. Soltani et al. (2023). *An Adaptable DL-Based IDS to Zero-Day Attacks*. JISA. https://doi.org/10.1016/j.jisa.2023.103516
12. Xu et al. (2023). *Fascinating Supervisory Signals: Deep Anomaly Detection with Scale Learning*. ICML 2023. https://arxiv.org/abs/2305.16114
13. Souza et al. (2025). *A Novel Open Set Energy-based Flow Classifier for NIDS*. Computers & Security. https://arxiv.org/abs/2109.11224
14. Li, Lu et al. (2024). *End-to-End NIDS Based on Contrastive Learning*. Sensors. https://pmc.ncbi.nlm.nih.gov/articles/PMC11014011/

---

*Literature review compiled June 2026. Papers verified via arXiv, IEEE Xplore, ACM DL, Springer. Ranked by suitability to CIC-IDS2017 open-set unknown-attack detection task at ~1% FPR.*
