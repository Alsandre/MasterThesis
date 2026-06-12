# Master's Thesis — English Master Draft

**Title:** "Conversational AI: The Evolution from Assistant to Interlocutor"
(„სასაუბრო ხელოვნური ინტელექტი: ასისტენტიდან თანამოსაუბრემდე ევოლუცია")

**This is the source-of-truth working text.** Claude drafts and reviews here; Lekso translates each approved section into Georgian (`draft.md`) manually — the translation pass is the authorship/learning step. Terminology is governed by `glossary.md`. Bibliography numbering [N] is shared across both languages.

**Status:** §1 at v3-equivalent (English master of the reviewed Georgian v3, 2026-06-13). §2 onward will be drafted here first.

---

## §1. Introduction

### 1.1 Research problem

Conversational systems built on large language models (LLMs) have in recent years demonstrated human-comparable linguistic competence within a single dialogue session, yet one of their fundamental limitations persists: such systems fail to maintain a continuous, evolving context of interaction over the long term. Empirical evidence renders this deficit precisely: on LoCoMo, a benchmark comprising long conversations distributed across up to 35 sessions, long-context models and RAG approaches trail human performance by 56% overall and by 73% on temporal reasoning [1]. The LongMemEval benchmark confirms a 30% drop in information-recall accuracy for commercial conversational assistants under sustained interaction [2].

This technical deficit translates directly into user experience. In the context of so-called "companion" applications (Replika, Character.AI), a qualitative study of Replika users shows that memory failure — forgetting names, preferences, and life events — is among the principal factors that break the user's sense of relationship [3]. At the same time, when a system's behavior changes abruptly, users exhibit reactions that are statistically mediated by the agent's perceived identity discontinuity [4]. Taken together, these two independent findings give grounds to hypothesize that memory continuity underlies perceived identity and, by extension, the continuity of the relationship — a hypothesis whose experimental examination is among the objectives of the present work.

The research problem is therefore two-dimensional: (a) technical — how relevant information should be represented, stored, and retrieved across multi-session interaction; and (b) perceptual — which memory behaviors users experience as natural and relationship-reinforcing. The existing literature treats these two dimensions largely in isolation: memory architectures are evaluated with factual-accuracy (QA) metrics, while perception studies treat memory as an isolated manipulation on a single system. The intersection of these two dimensions constitutes the research space of the present work.

The object of research is LLM-based voice conversational systems. The subject of research is the effect of long-term memory architecture on user-perceived social constructs.

### 1.2 Research aim

The aim of this work is to develop a long-term memory architecture for a voice conversational system, grounded in cognitive theories of human memory, and to evaluate experimentally its effect on user-perceived social constructs — social presence, user–agent alliance, and perceived humanlikeness — through a controlled comparative study.

To achieve this aim, the following objectives are set:
1. a systematic analysis of existing approaches to long-term conversational memory and of their cognitive-theoretical foundations;
2. formalization of the behavioral signatures of the selected theories (the multi-store model, the Ebbinghaus forgetting curve, the episodic/semantic memory distinction, gist-based recall) and their transformation into architectural components;
3. implementation of the architecture in a working voice system (Voice Companion) as mutually comparable experimental profiles: (A) no long-term memory, (B) RAG based on verbatim retrieval, (C) a profile modeled on human memory;
4. a user study employing a repeated-measures (within-subject) design with validated instruments [14];
5. analysis of the results and formulation of memory-design recommendations for interlocutor systems.

Primary research question and hypotheses:
- **RQ1:** Does a memory architecture grounded in theories of human memory strengthen perceived social constructs — social presence, user–agent alliance, and perceived humanlikeness — relative to an approach based on verbatim retrieval?
- **H1:** the theory-grounded profile (C) outperforms verbatim RAG (B) on the social-presence and user–agent-alliance scales;
- **H2a:** verbatim RAG (B) scores highest on the perceived-intelligence dimension;
- **H2b:** the same profile (B) scores lowest on trust and privacy-related comfort — a conjecture extrapolated from text-modality results [11] to the voice modality.

Linguistic scope of the study: the system and the experiments are conducted in English, a choice dictated by the current level of maturity of Georgian speech-recognition technology; accordingly, the perceptual conclusions apply directly to the tested language condition, while a Georgian-language demonstration is discussed in the future-work section.

### 1.3 Relevance of the problem

The relevance of the problem is determined by three mutually independent factors. First — industrial: in 2025–2026, leading vendors (OpenAI, Anthropic) either deployed background memory-consolidation mechanisms in commercial products or presented them as public research previews [18, 19], which suggests that long-term memory is regarded by the field itself as a central unsolved problem. It is notable, moreover, that no peer-reviewed publications accompany these systems — which makes the need for academic study all the more acute. Second — social: prolonged, personal interaction with conversational systems has become a widespread practice [5], which turns the perceptual effects of memory into a socially significant question. Third — methodological: every major long-term-memory benchmark known to us (LoCoMo, LongMemEval, MSC) is designed for the text modality [1, 2]; under voice interaction — where response latency is strictly bounded in real time — the behavior of memory architectures and their perceptual effects remain practically unstudied.

### 1.4 Practical value of the research

The research will produce:
- a working voice interlocutor system with a long-term memory module — built on the Voice Companion platform developed by us;
- empirically grounded design recommendations on which memory mechanisms strengthen, and which weaken, user trust and the sense of relationship — a useful guide for builders of conversational products;
- a reproducible experimental environment for comparing memory profiles.

The results are relevant to the development of personal assistants as well as of conversational systems for educational and medical purposes.

### 1.5 Theoretical value of the research

The theoretical contribution of the work is threefold. First, it connects the memory theories of cognitive psychology with the engineering of LLM systems not at the level of metaphor but at the level of measurable behavioral signatures. Second, in the literature available to us no controlled study could be found that compares architectures grounded in different theories of human memory with respect to user-perceived social constructs — existing comparisons are confined to factual-accuracy metrics [1, 2], while perception studies treat memory as an isolated manipulation on a single system [11]; the present work aims precisely at filling this gap by means of a controlled experiment. Third, the work proposes an operationalization of the distinction between an "assistant" and an "interlocutor" on the basis of three measurable properties — context persistence, identity continuity, and initiative — thereby transforming these notions from loosely defined terms into measurable categories.

### 1.6 Structure of the work

The work consists of five chapters: introduction, literature review, research methods, results and discussion, and conclusion. The literature review analyzes existing approaches to long-term conversational memory, their cognitive-theoretical foundations, and the limitations of evaluation methodology. The methods chapter describes the developed architecture, the experimental profiles, and the design of the user study. The results chapter presents the quantitative and qualitative analysis, and the conclusion summarizes the findings and outlines directions for future research.

---

*Bibliography: shared [N] numbering — see the list at the end of `draft.md` (all entries verified against primary sources 2026-06-12; [18]/[19] vendor-announcement URLs still TODO).*
