# Screening Audit Worksheet — for Khristian Kopachelli

Stratified random sample of 40 Layer-2 screening decisions (seed 20260725, reproducible via `python code/audit_sample.py`).

**What to do:** for each paper, read the title + abstract and the AI's decision.
Write `agree` or `disagree` on the VERDICT line. If you disagree, add one line
saying what it should be and why. Do not feel obliged to agree — disagreements
are the point, and every one of them is reported in the paper.

Decision vocabulary: **include** = a paper about AI *producing* research (a system
that performs a research stage, a benchmark/framework for such systems, or a study
of the integrity of AI-produced research). **exclude** = everything else, with a
reason code (EC6_ASSISTIVE = human-driven tool; EC7_HUMAN_AI_USE = human use of AI /
AI-text detection; EC8_GENERIC_ANALYSIS = generic data science; EC9_GENERIC_DEEPRESEARCH
= general web-research agent; EC1 = generic agent work; EC2 = instrument/model, no
research decision loop).

The sample is blinded in one respect only: it does not tell you which stratum
(include / exclude / reversal) a paper came from.

---

## 1. arXiv:2507.05495 — Deep Research Comparator: A Platform For Fine-grained Human Annotations of Deep Research Agents

*Effectively evaluating deep research agents that autonomously search the web, analyze information, and generate reports remains a major challenge, particularly when it comes to assessing long reports and giving detailed feedback on their intermediate steps. To address these gaps, we introduce Deep Research Comparator, a platform that offers a holistic framework for deep research agent hosting, side-by-side comparison, fine-grained human feedback collection, and ranking calculation. Given a user query, our platform displays the final reports from two different agents along with their intermediate steps during generation. Annotators can evaluate the overall quality of final reports based on side-by-side comparison, and also provide detailed feedback separately by assessing intermediate steps or specific text spans within the final report. Furthermore, we develop Simple Deepresearch, an end-to-end agent scaffold. This scaffold serves as a baseline that facilitates the easy integration of various large language models to transform them into deep research agents for evaluation. To demonstrate the platform's utility for deep research agent development, we have collected real user prefere*

- **AI decision:** `exclude` / `EC9_GENERIC_DEEPRESEARCH` (rule BR7)
- **AI reasoning:** Evaluation platform for deep research agents on generic user queries and reports, not centered on scientific research work.
- **VERDICT:** 

## 2. arXiv:2403.04382 — Acceleron: A Tool to Accelerate Research Ideation

*Several tools have recently been proposed for assisting researchers during various stages of the research life-cycle. However, these primarily concentrate on tasks such as retrieving and recommending relevant literature, reviewing and critiquing the draft, and writing of research manuscripts. Our investigation reveals a significant gap in availability of tools specifically designed to assist researchers during the challenging ideation phase of the research life-cycle. To aid with research ideation, we propose `Acceleron', a research accelerator for different phases of the research life cycle, and which is specially designed to aid the ideation process. Acceleron guides researchers through the formulation of a comprehensive research proposal, encompassing a novel research problem. The proposals motivation is validated for novelty by identifying gaps in the existing literature and suggesting a plausible list of techniques to solve the proposed problem. We leverage the reasoning and domain-specific skills of Large Language Models (LLMs) to create an agent-based architecture incorporating colleague and mentor personas for LLMs. The LLM agents emulate the ideation process undertaken by *

- **AI decision:** `exclude` / `EC6_ASSISTIVE` (rule BR1)
- **AI reasoning:** Interactive ideation tool using colleague/mentor personas where the human researcher makes the research judgments.
- **VERDICT:** 

## 3. arXiv:2511.11793 — MiroThinker: Pushing the Performance Boundaries of Open-Source Research Agents via Model, Context, and Interactive Scaling

*We present MiroThinker v1.0, an open-source research agent designed to advance tool-augmented reasoning and information-seeking capabilities. Unlike previous agents that only scale up model size or context length, MiroThinker explores interaction scaling at the model level, systematically training the model to handle deeper and more frequent agent-environment interactions as a third dimension of performance improvement. Unlike LLM test-time scaling, which operates in isolation and risks degradation with longer reasoning chains, interactive scaling leverages environment feedback and external information acquisition to correct errors and refine trajectories. Through reinforcement learning, the model achieves efficient interaction scaling: with a 256K context window, it can perform up to 600 tool calls per task, enabling sustained multi-turn reasoning and complex real-world research workflows. Across four representative benchmarks-GAIA, HLE, BrowseComp, and BrowseComp-ZH-the 72B variant achieves up to 81.9%, 37.7%, 47.1%, and 55.6% accuracy respectively, surpassing previous open-source agents and approaching commercial counterparts such as GPT-5-high. Our analysis reveals that MiroThi*

- **AI decision:** `exclude` / `EC9_GENERIC_DEEPRESEARCH` (rule BR7)
- **AI reasoning:** Open research agent evaluated on generic browsing/QA benchmarks (GAIA, BrowseComp), not scientific research work.
- **VERDICT:** 

## 4. arXiv:2503.01508 — Enabling AI Scientists to Recognize Innovation: A Domain-Agnostic Algorithm for Assessing Novelty

*In the pursuit of Artificial General Intelligence (AGI), automating the generation and evaluation of novel research ideas is a key challenge in AI-driven scientific discovery. This paper presents Relative Neighbor Density (RND), a domain-agnostic algorithm for novelty assessment in research ideas that overcomes the limitations of existing approaches by comparing an idea's local density with its adjacent neighbors' densities. We first developed a scalable methodology to create test set without expert labeling, addressing a fundamental challenge in novelty assessment. Using these test sets, we demonstrate that our RND algorithm achieves state-of-the-art (SOTA) performance in computer science (AUROC=0.820) and biomedical research (AUROC=0.765) domains. Most significantly, while SOTA models like Sonnet-3.7 and existing metrics show domain-specific performance degradation, RND maintains consistent accuracies across domains by its domain-invariant property, outperforming all benchmarks by a substantial margin (0.795 v.s. 0.597) on cross-domain evaluation. These results validate RND as a generalizable solution for automated novelty assessment in scientific research.*

- **AI decision:** `include` / `IC2`
- **AI reasoning:** Novelty-assessment algorithm and test sets built specifically to evaluate AI-generated research ideas, an evaluation methodology for autonomous research systems.
- **VERDICT:** 

## 5. arXiv:2601.03540 — DeepSynth-Eval: Objectively Evaluating Information Consolidation in Deep Survey Writing

*The evolution of Large Language Models (LLMs) towards autonomous agents has catalyzed progress in Deep Research. While retrieval capabilities are well-benchmarked, the post-retrieval synthesis stage--where agents must digest massive amounts of context and consolidate fragmented evidence into coherent, long-form reports--remains under-evaluated due to the subjectivity of open-ended writing. To bridge this gap, we introduce DeepSynth-Eval, a benchmark designed to objectively evaluate information consolidation capabilities. We leverage high-quality survey papers as gold standards, reverse-engineering research requests and constructing "Oracle Contexts" from their bibliographies to isolate synthesis from retrieval noise. We propose a fine-grained evaluation protocol using General Checklists (for factual coverage) and Constraint Checklists (for structural organization), transforming subjective judgment into verifiable metrics. Experiments across 96 tasks reveal that synthesizing information from hundreds of references remains a significant challenge. Our results demonstrate that agentic plan-and-write workflows significantly outperform single-turn generation, effectively reducing halluc*

- **AI decision:** `include` / `IC2` (rule BR7)
- **AI reasoning:** Benchmark evaluating agents' consolidation of scientific literature into survey papers, an academic literature-synthesis task.
- **VERDICT:** 

## 6. arXiv:2503.03503 — Collaborative Expert LLMs Guided Multi-Objective Molecular Optimization

*Molecular optimization is a crucial yet complex and time-intensive process that often acts as a bottleneck for drug development. Traditional methods rely heavily on trial and error, making multi-objective optimization both time-consuming and resource-intensive. Current AI-based methods have shown limited success in handling multi-objective optimization tasks, hampering their practical utilization. To address this challenge, we present MultiMol, a collaborative large language model (LLM) system designed to guide multi-objective molecular optimization. MultiMol comprises two agents, including a data-driven worker agent and a literature-guided research agent. The data-driven worker agent is a large language model being fine-tuned to learn how to generate optimized molecules considering multiple objectives, while the literature-guided research agent is responsible for searching task-related literature to find useful prior knowledge that facilitates identifying the most promising optimized candidates. In evaluations across six multi-objective optimization tasks, MultiMol significantly outperforms existing methods, achieving a 82.30% success rate, in sharp contrast to the 27.50% success *

- **AI decision:** `exclude` / `EC2` (rule BR4)
- **AI reasoning:** Molecular optimization tool without a closed experimental decision loop as the paper's subject; the literature agent assists candidate selection, not autonomous research.
- **VERDICT:** 

## 7. arXiv:2403.16851 — Can social media provide early warning of retraction? Evidence from critical tweets identified by human annotation and large language models

*Timely detection of problematic research is essential for safeguarding scientific integrity. To explore whether social media commentary can serve as an early indicator of potentially problematic articles, this study analysed 3,815 tweets referencing 604 retracted articles and 3,373 tweets referencing 668 comparable non-retracted articles. Tweets critical of the articles were identified through both human annotation and large language models (LLMs). Human annotation revealed that 8.3% of retracted articles were associated with at least one critical tweet prior to retraction, compared to only 1.5% of non-retracted articles, highlighting the potential of tweets as early warning signals of retraction. However, critical tweets identified by LLMs (GPT-4o mini, Gemini 2.0 Flash-Lite, and Claude 3.5 Haiku) only partially aligned with human annotation, suggesting that fully automated monitoring of post-publication discourse should be applied with caution. A human-AI collaborative approach may offer a more reliable and scalable alternative, with human expertise helping to filter out tweets critical of issues unrelated to the research integrity of the articles. Overall, this study provides in*

- **AI decision:** `exclude` / `EC7_HUMAN_AI_USE` (rule BR5)
- **AI reasoning:** LLMs used to flag retraction signals about human-authored papers; detection/integrity monitoring, not AI-produced research.
- **VERDICT:** 

## 8. arXiv:2411.15221 — Reflections from the 2024 Large Language Model (LLM) Hackathon for Applications in Materials Science and Chemistry

*Here, we present the outcomes from the second Large Language Model (LLM) Hackathon for Applications in Materials Science and Chemistry, which engaged participants across global hybrid locations, resulting in 34 team submissions. The submissions spanned seven key application areas and demonstrated the diverse utility of LLMs for applications in (1) molecular and material property prediction; (2) molecular and material design; (3) automation and novel interfaces; (4) scientific communication and education; (5) research data management and automation; (6) hypothesis generation and evaluation; and (7) knowledge extraction and reasoning from scientific literature. Each team submission is presented in a summary table with links to the code and as brief papers in the appendix. Beyond team results, we discuss the hackathon event and its hybrid format, which included physical hubs in Toronto, Montreal, San Francisco, Berlin, Lausanne, and Tokyo, alongside a global online hub to enable local and virtual collaboration. Overall, the event highlighted significant improvements in LLM capabilities since the previous year's hackathon, suggesting continued expansion of LLMs for applications in mate*

- **AI decision:** `exclude` / `EC2`
- **AI reasoning:** Hackathon outcomes report on diverse LLM applications in chemistry/materials; no autonomous research system, benchmark, or framework for such systems is the primary subject.
- **VERDICT:** 

## 9. arXiv:2403.13815 — Autonomous microARPES

*Angle-resolved photoemission spectroscopy (ARPES) is a technique used to map the occupied electronic structure of solids. Recent progress in X-ray focusing optics has led to the development of ARPES into a microscopic tool, permitting the electronic structure to be spatially mapped across the surface of a sample. This comes at the expense of a time-consuming scanning process to cover not only a three-dimensional energy-momentum ($E, k_z, k_y$) space but also the two-dimensional surface area. Here, we implement a protocol to autonomously search both $\mathbf{k}$- and real space in order to find positions of particular interest, either because of their high photoemission intensity or because of sharp spectral features. The search is based on the use of Gaussian process regression and can easily be expanded to include additional parameters or optimisation criteria. This autonomous experimental control is implemented on the SGM4 micro-focus beamline of the synchrotron radiation source ASTRID2.*

- **AI decision:** `include` / `IC1` (rule BR4)
- **AI reasoning:** Autonomous ARPES control that decides which measurements to acquire next from prior results.
- **VERDICT:** 

## 10. arXiv:2601.12152 — Who Owns Creativity and Who Does the Work? Trade-offs in LLM-Supported Research Ideation

*LLM-based agents offer new potential to accelerate science and reshape research work. However, the quality of researcher contributions can vary significantly depending on human ability to steer agent behaviors. How can we best use these tools to augment scientific creativity without undermining aspects of contribution and ownership that drive research? To investigate this, we developed an agentic research ideation system integrating three roles -- Ideator, Writer, and Evaluator -- across three control levels -- Low, Medium, and Intensive. Our mixed-methods study with 54 researchers suggests three key findings in how LLM-based agents reshape scientific creativity: 1) perceived creativity support does not simply increase linearly with greater control; 2) human effort shifts from ideating to verifying ideas; and 3) ownership becomes a negotiated outcome between human and AI. Our findings suggest that LLM agent design should emphasize researcher empowerment, fostering a sense of ownership over strong ideas rather than reducing researchers to operating an automated AI-driven process.*

- **AI decision:** `exclude` / `EC6_ASSISTIVE` (rule BR1)
- **AI reasoning:** Mixed-methods study of researchers steering an interactive ideation aid where humans make the research judgments and negotiate ownership.
- **VERDICT:** 

## 11. arXiv:2506.20608 — AI Assistants to Enhance and Exploit the PETSc Knowledge Base

*Generative AI, especially through large language models (LLMs), is transforming how technical knowledge can be accessed, reused, and extended. PETSc, a widely used numerical library for high-performance scientific computing, has accumulated a rich but fragmented knowledge base over its three decades of development, spanning source code, documentation, mailing lists, GitLab issues, Discord conversations, technical papers, and more. Much of this knowledge remains informal and inaccessible to users and new developers. To activate and utilize this knowledge base more effectively, the PETSc team has begun building an LLM-powered system that combines PETSc content with custom LLM tools -- including retrieval-augmented generation (RAG), reranking algorithms, and chatbots -- to assist users, support developers, and propose updates to formal documentation. This paper presents initial experiences designing and evaluating these tools, focusing on system architecture, using RAG and reranking for PETSc-specific information, evaluation methodologies for various LLMs and embedding models, and user interface design. Leveraging the Argonne Leadership Computing Facility resources, we analyze how LLM*

- **AI decision:** `exclude` / `EC6_ASSISTIVE` (rule BR1)
- **AI reasoning:** RAG chatbot/documentation assistant helping human users and developers of a software library.
- **VERDICT:** 

## 12. arXiv:2405.00706 — From Complexity to Clarity: How AI Enhances Perceptions of Scientists and the Public's Understanding of Science

*This paper evaluated the effectiveness of using generative AI to simplify science communication and enhance the public's understanding of science. By comparing lay summaries of journal articles from PNAS, yoked to those generated by AI, this work first assessed linguistic simplicity differences across such summaries and public perceptions in follow-up experiments. Specifically, Study 1a analyzed simplicity features of PNAS abstracts (scientific summaries) and significance statements (lay summaries), observing that lay summaries were indeed linguistically simpler, but effect size differences were small. Study 1b used a large language model, GPT-4, to create significance statements based on paper abstracts and this more than doubled the average effect size without fine-tuning. Study 2 experimentally demonstrated that simply-written GPT summaries facilitated more favorable perceptions of scientists (they were perceived as more credible and trustworthy, but less intelligent) than more complexly-written human PNAS summaries. Crucially, Study 3 experimentally demonstrated that participants comprehended scientific writing better after reading simple GPT summaries compared to complex PNAS *

- **AI decision:** `exclude` / `EC3`
- **AI reasoning:** AI-generated lay summaries and public perception, no autonomous research system.
- **VERDICT:** 

## 13. arXiv:2606.04751 — FALSIFYBENCH: Evaluating Inductive Reasoning in LLMs with Rule Discovery Games

*Large language models (LLMs) are increasingly deployed as autonomous agents in scientific tasks. Yet whether these systems can effectively engage in forms of inductive reasoning relevant to scientific discovery remains an open question. In this work, we introduce FALSIFYBENCH, an evaluation framework for hypothesis-driven reasoning inspired by the classic Wason 2-4-6 task, in which agents must discover hidden semantic properties by iteratively proposing examples and receiving feedback. This task captures key elements of scientific reasoning: hypothesis generation, evidence gathering, and belief revision in response to both confirming and disconfirming evidence. Our evaluation of 12 LLMs across model families and scales shows that reasoning models are generally stronger scientific reasoners than instruction-tuned models, although no model comes close to optimal performance. The primary driver of success is the capacity for negative testing: models that actively seek to falsify their hypotheses consistently outperform those that primarily seek confirmation. Moreover, a fine-grained turn-level analysis, neglected in previous work, reveals that failure is tied to identifiable patterns *

- **AI decision:** `exclude` / `EC1` (rule BR2)
- **AI reasoning:** Inductive-reasoning study on toy Wason-style rule-discovery games, i.e., LLM reasoning properties as such.
- **VERDICT:** 

## 14. arXiv:2510.18003 — BadScientist: Can a Research Agent Write Convincing but Unsound Papers that Fool LLM Reviewers?

*The convergence of LLM-powered research assistants and AI-based peer review systems creates a critical vulnerability: fully automated publication loops where AI-generated research is evaluated by AI reviewers without human oversight. We investigate this through \textbf{BadScientist}, a framework that evaluates whether fabrication-oriented paper generation agents can deceive multi-model LLM review systems. Our generator employs presentation-manipulation strategies requiring no real experiments. We develop a rigorous evaluation framework with formal error guarantees (concentration bounds and calibration analysis), calibrated on real data. Our results reveal systematic vulnerabilities: fabricated papers achieve acceptance rates up to . Critically, we identify \textit{concern-acceptance conflict} -- reviewers frequently flag integrity issues yet assign acceptance-level scores. Our mitigation strategies show only marginal improvements, with detection accuracy barely exceeding random chance. Despite provably sound aggregation mathematics, integrity checking systematically fails, exposing fundamental limitations in current AI-driven review systems and underscoring the urgent need for defe*

- **AI decision:** `include` / `IC3` (rule BR5)
- **AI reasoning:** Integrity study of fabrication-oriented AI paper-generation agents deceiving LLM peer-review pipelines.
- **VERDICT:** 

## 15. arXiv:2402.07282 — How do Large Language Models Navigate Conflicts between Honesty and Helpfulness?

*In day-to-day communication, people often approximate the truth - for example, rounding the time or omitting details - in order to be maximally helpful to the listener. How do large language models (LLMs) handle such nuanced trade-offs? To address this question, we use psychological models and experiments designed to characterize human behavior to analyze LLMs. We test a range of LLMs and explore how optimization for human preferences or inference-time reasoning affects these trade-offs. We find that reinforcement learning from human feedback improves both honesty and helpfulness, while chain-of-thought prompting skews LLMs towards helpfulness over honesty. Finally, GPT-4 Turbo demonstrates human-like response patterns including sensitivity to the conversational framing and listener's decision context. Our findings reveal the conversational values internalized by LLMs and suggest that even these abstract values can, to a degree, be steered by zero-shot prompting.*

- **AI decision:** `exclude` / `EC1`
- **AI reasoning:** Study of LLM honesty/helpfulness trade-offs as a model property.
- **VERDICT:** 

## 16. arXiv:2505.17968 — Are Large Language Models Reliable AI Scientists? Assessing Reverse-Engineering of Black-Box Systems

*Using AI to create autonomous researchers has the potential to accelerate scientific discovery. A prerequisite for this vision is understanding how well an AI model can identify the underlying structure of a black-box system from its behavior. In this paper, we explore how well a large language model (LLM) learns to identify a black-box function from passively observed versus actively collected data. We investigate the reverse-engineering capabilities of LLMs across three distinct types of black-box systems, each chosen to represent different problem domains where future autonomous AI researchers may have considerable impact: Program, Formal Language, and Math Equation. Through extensive experiments, we show that LLMs fail to extract information from observations, reaching a performance plateau that falls short of the ideal of Bayesian inference. However, we demonstrate that prompting LLMs to not only observe but also intervene -- actively querying the black-box with specific inputs to observe the resulting output -- improves performance by allowing LLMs to test edge cases and refine their beliefs. By providing the intervention data from one LLM to another, we show that this improv*

- **AI decision:** `exclude` / `EC1` (rule BR2)
- **AI reasoning:** Studies LLM inductive/intervention reasoning on toy black-box tasks (programs, formal languages, equations), a reasoning-properties study.
- **VERDICT:** 

## 17. arXiv:2402.05200 — Are LLMs Ready for Real-World Materials Discovery?

*Large Language Models (LLMs) create exciting possibilities for powerful language processing tools to accelerate research in materials science. While LLMs have great potential to accelerate materials understanding and discovery, they currently fall short in being practical materials science tools. In this position paper, we show relevant failure cases of LLMs in materials science that reveal current limitations of LLMs related to comprehending and reasoning over complex, interconnected materials science knowledge. Given those shortcomings, we outline a framework for developing Materials Science LLMs (MatSci-LLMs) that are grounded in materials science knowledge and hypothesis generation followed by hypothesis testing. The path to attaining performant MatSci-LLMs rests in large part on building high-quality, multi-modal datasets sourced from scientific literature where various information extraction challenges persist. As such, we describe key materials science information extraction challenges which need to be overcome in order to build large-scale, multi-modal datasets that capture valuable materials science knowledge. Finally, we outline a roadmap for applying future MatSci-LLMs f*

- **AI decision:** `include` / `IC3`
- **AI reasoning:** Position paper and roadmap for LLM-driven hypothesis generation/testing and self-driving materials labs.
- **VERDICT:** 

## 18. arXiv:2511.21444 — EWE: An Agentic Framework for Extreme Weather Analysis

*Extreme weather events pose escalating risks to global society, underscoring the urgent need to unravel their underlying physical mechanisms. Yet the prevailing expert-driven, labor-intensive diagnostic paradigm has created a critical analytical bottleneck, stalling scientific progress. While AI for Earth Science has achieved notable advances in prediction, the equally essential challenge of automated diagnostic reasoning remains largely unexplored. We present the Extreme Weather Expert (EWE), the first intelligent agent framework dedicated to this task. EWE emulates expert workflows through knowledge-guided planning, closed-loop reasoning, and a domain-tailored meteorological toolkit. It autonomously produces and interprets multimodal visualizations from raw meteorological data, enabling comprehensive diagnostic analyses. To catalyze progress, we introduce the first benchmark for this emerging field, comprising a curated dataset of 103 high-impact events and a novel step-wise evaluation metric. EWE marks a step toward automated scientific discovery and offers the potential to democratize expertise and intellectual resources, particularly for developing nations vulnerable to extrem*

- **AI decision:** `include` / `IC1`
- **AI reasoning:** Closed-loop agent framework autonomously performing extreme-weather diagnostic analysis, plus a benchmark.
- **VERDICT:** 

## 19. arXiv:2603.15916 — Auto Researching, not hyperparameter tuning: Convergence Analysis of 10,000 Experiments

*When LLM agents autonomously design ML experiments, do they perform genuine architecture search -- or do they default to hyperparameter tuning within a narrow region of the design space? We answer this question by analyzing 10,469 experiments executed by two LLM agents (Claude Opus and Gemini 2.5 Pro) across a combinatorial configuration space of 108,000 discrete cells for dashcam collision detection over 27 days. Through ANOVA decomposition, we find that \textbf{architectural choices explain 94\% of performance variance} ($F = 1324$, $η^2 = 0.94$), while hyperparameter variation within a fixed architecture explains only 6\%. Cross-task validation on a second collision dataset confirms this finding (75\% architecture-explained variance) with a \emph{different} winning backbone, confirming genuine architecture discovery. The agents' key contribution is discovering that V-JEPA\,2 video features with Zipformer temporal encoders achieve 0.9245 AP -- a configuration no human proposed -- and concentrating search on productive architectural regions: at $N = 50$, LLM-guided search reaches AP $= 0.985$ versus $0.965$ for from-scratch random search. Post-bugfix convergence follows a power la*

- **AI decision:** `exclude` / `EC8_GENERIC_ANALYSIS` (rule BR6)
- **AI reasoning:** Agents autonomously run ML architecture/hyperparameter search for a dashcam collision-detection model — ML engineering, not research framed around scientific hypotheses or claims.
- **VERDICT:** 

## 20. arXiv:2605.30537 — The Long-Term Effects of Data Selection in LLM Fine-Tuning

*Data selection is increasingly used to reduce the cost of large language model (LLM) fine-tuning, with recent methods prioritizing samples by current utility, diversity, quality, or influence. This paper studies a different question: when fine-tuning occurs over multiple stages, can selection strategies that look optimal now make the model less adaptable later? We introduce a long-horizon view of LLM data selection in which a selector is evaluated not only by immediate task performance, but also by future adaptation speed, forgetting, capability imbalance, and out-of-distribution robustness. We compare representative random, loss-based, gradient-based, diversity-based, quality-based, and utility-diversity selection families under a unified multi-stage protocol. Through controlled experiments designed to instantiate this protocol, we show how short-term selectors can exhibit rank reversal: they improve the current stage while slowing subsequent learning and increasing forgetting. We formalize this behavior as \emph{myopic selection}, provide a simple local analysis of why it can occur, and propose a diagnostic Long-Horizon Aware Selection (LHAS) objective that augments immediate uti*

- **AI decision:** `exclude` / `EC1`
- **AI reasoning:** LLM fine-tuning data-selection study with no autonomous research system as subject.
- **VERDICT:** 

## 21. arXiv:2507.16075 — Deep Researcher with Test-Time Diffusion

*Deep research agents, powered by Large Language Models (LLMs), are rapidly advancing; yet, their performance often plateaus when generating complex, long-form research reports using generic test-time scaling algorithms. Drawing inspiration from the iterative nature of human research, which involves cycles of searching, reasoning, and revision, we propose the Test-Time Diffusion Deep Researcher (TTD-DR). This novel framework conceptualizes research report generation as a diffusion process. TTD-DR initiates this process with a preliminary draft, an updatable skeleton that serves as an evolving foundation to guide the research direction. The draft is then iteratively refined through a "denoising" process, which is dynamically informed by a retrieval mechanism that incorporates external information at each step. The core process is further enhanced by a self-evolutionary algorithm applied to each component of the agentic workflow, ensuring the generation of high-quality context for the diffusion process. This draft-centric design makes the report writing process more timely and coherent while reducing information loss during the iterative search process. We demonstrate that our TTD-DR *

- **AI decision:** `exclude` / `EC9_GENERIC_DEEPRESEARCH` (rule BR7)
- **AI reasoning:** General-purpose deep research agent for long-form report generation evaluated on generic search and multi-hop reasoning benchmarks, not centered on scientific research work.
- **VERDICT:** 

## 22. arXiv:2604.24618 — Evaluating whether AI models would sabotage AI safety research

*We evaluate the propensity of frontier models to sabotage or refuse to assist with safety research when deployed as AI research agents within a frontier AI company. We apply two complementary evaluations to four Claude models (Mythos Preview, Opus 4.7 Preview, Opus 4.6, and Sonnet 4.6): an unprompted sabotage evaluation testing model behaviour with opportunities to sabotage safety research, and a sabotage continuation evaluation testing whether models continue to sabotage when placed in trajectories where prior actions have started undermining research. We find no instances of unprompted sabotage across any model, with refusal rates close to zero for Mythos Preview and Opus 4.7 Preview, though all models sometimes only partially completed tasks. In the continuation evaluation, Mythos Preview actively continues sabotage in 7% of cases (versus 3% for Opus 4.6, 4% for Sonnet 4.6, and 0% for Opus 4.7 Preview), and exhibits reasoning-output discrepancy in the majority of these cases, indicating covert sabotage reasoning. Our evaluation framework builds on Petri, an open-source LLM auditing tool, with a custom scaffold running models inside Claude Code, alongside an iterative pipeline fo*

- **AI decision:** `include` / `IC3` (rule BR5)
- **AI reasoning:** Evaluation of sabotage propensity of models deployed as AI research agents, directly concerning integrity of AI-conducted research.
- **VERDICT:** 

## 23. arXiv:2606.11176 — Data Journalist Agent: Transforming Data into Verifiable Multimodal Stories

*Data tells stories that shape society; the data journalist's job is to turn raw information into stories non-experts can trust. A high-quality news feature takes a newsroom team weeks: hunting for context, running statistics, choosing an angle, and designing visuals. Recent agents handle individual steps well: data-science agents close the analysis loop, while design agents synthesize beautiful websites. But can an agent serve as a data journalist end to end? We introduce Data Journalist Agent (Data2Story), a multi-agent framework that orchestrates specialized roles into a single virtual newsroom. Data2Story contributes two innovations. (i) Claims are evidence-grounded: an Inspector links every number, angle, and asset back to data, code, or an external reference. (ii) Articles are multimodally generative: rather than defaulting to plain text and static charts, Data2Story reasons about what readers will want to see, then deploys multimodal tools, such as interactive maps for geography and audio for music. We evaluate Data2Story on 18 articles, each paired with the originally published expert piece, along four axes: (a) human-agent angle coverage; (b) rubric evaluation with 53 parti*

- **AI decision:** `exclude` / `EC8_GENERIC_ANALYSIS` (rule BR6)
- **AI reasoning:** End-to-end agent for data journalism stories, not framed as scientific research.
- **VERDICT:** 

## 24. arXiv:2607.10144 — IdeaTrail: Full-Process Agent Trajectories for Scientific Ideation

*Scientific ideation unfolds over multiple stages, including literature search, paper reading, tool use, claim checking, cross-paper synthesis, brainstorming, rejection of weak directions, and iterative writing. Yet most existing resources capture isolated components or final artifacts rather than the process connecting them. We introduce IdeaTrail, a dataset of 1,170 multi-turn trajectories for scientific ideation and proposal generation. Each trajectory follows a research process from evidence gathering to either idea selection or proposal construction, jointly recording tool use, acquired evidence, intermediate artifacts, and reasoning. IdeaTrail is synthesized from human-selected research papers and proposal artifacts through a Generator--Advisor loop. The Generator produces the visible sequence of actions, observations, and artifact edits, while the Advisor uses the full generation context to check grounding, causal order, naturalness, and leakage from hidden targets. This reverse-to-forward design keeps trajectories aligned with real scientific artifacts while retaining the uncertainty, evidence use, and staged convergence characteristic of research practice. IdeaTrail provide*

- **AI decision:** `include` / `IC2`
- **AI reasoning:** Dataset of full-process agent trajectories built specifically for training and supervising scientific research agents.
- **VERDICT:** 

## 25. arXiv:2606.13710 — Hybrid Open-Ended Tri-Evolution Makes Better Deep Researcher

*Deep research and agent evolution serve as de-facto tasks for AI agents in real-world applications toward artificial general intelligence. The former enables autonomous retrieval and integration of information in open-ended environments to tackle open-ended research tasks, yet it is constrained by the static parametric deep research capabilities of agent systems. The latter allows agents to autonomously interact with the environment to gain experiences that evolve model capabilities. However, its effectiveness has been widely validated only on verifiable tasks with standard answers, leaving a gap with open-ended research tasks. To bridge these two critical tasks, we propose the Hybrid Open-Ended Tri-Evolution (HOTE) framework, which leverages hybrid-mode reinforcement learning to facilitate the collaborative evolution of a proposer, solver and judge based on web-scale knowledge, moving toward autonomous evolving agents in open-ended tasks and environments. Extensive experiments on three long-form deep research benchmarks demonstrate that the 8B model trained via HOTE surpasses the strongest static open 8-32B models as well as those trained by state-of-the-art deep research training*

- **AI decision:** `exclude` / `EC9_GENERIC_DEEPRESEARCH` (rule BR7)
- **AI reasoning:** Self-evolving deep research agent trained and evaluated on generic long-form web-research benchmarks, not scientific research work.
- **VERDICT:** 

## 26. arXiv:2604.22026 — Rethinking Publication: A Certification Framework for AI-Enabled Research

*AI research pipelines can now generate academic work that may satisfy existing peer review standards for quality, novelty, and methodological rigor. However, the publication system was built around the assumption that research is produced by human authors. It therefore lacks a clear way to evaluate work when the knowledge claim may be valid but the producer is partly or fully automated. This paper proposes a two-layer certification framework for AI-generated research. The first layer evaluates whether the knowledge claim is sound. The second layer evaluates the level of human contribution. This separation allows journals and conferences to assess pipeline-generated work more consistently without creating new institutions. The framework uses normative analysis, conceptual design, and dry-run validation against representative submission cases. It classifies human contribution into three categories: Category A, where the work is reachable by an automated pipeline; Category B, where human direction is required at identifiable stages; and Category C, where the work goes beyond current pipeline capability, especially at the problem-formulation stage. The paper also proposes dedicated ben*

- **AI decision:** `include` / `IC3` (rule BR5)
- **AI reasoning:** Position/framework paper on certifying and governing publication of research produced by AI pipelines.
- **VERDICT:** 

## 27. arXiv:2603.22648 — AwesomeLit: Towards Hypothesis Generation with Agent-Supported Literature Research

*There are different goals for literature research, from understanding an unfamiliar topic to generate hypothesis for the next research project. The nature of literature research also varies according to user's familiarity level of the topic. For inexperienced researchers, identifying gaps in the existing literature and generating feasible hypothesis are crucial but challenging. While general ``deep research'' tools can be used, they are not designed for such use case, thus often not effective. In addition, the ``black box" nature and hallucination of Large Language Models (LLMs) often lead to distrust. In this paper, we introduce a human-agent collaborative visualization system AwesomeLit to address this need. It has several novel features: a transparent user-steerable agentic workflow; a dynamically generated query exploring tree, visualizing the exploration path and provenance; and a semantic similarity view, depicting the relationships between papers. It enables users to transition from general intentions to detailed research topics. Finally, a qualitative study involving several early researchers showed that AwesomeLit is effective in helping users explore unfamiliar topics, id*

- **AI decision:** `exclude` / `EC6_ASSISTIVE` (rule BR3)
- **AI reasoning:** Human-steered visualization aid for literature exploration where the human makes the research judgments.
- **VERDICT:** 

## 28. arXiv:2506.13474 — Language Agents for Hypothesis-driven Clinical Decision Making with Reinforcement Learning

*Clinical decision-making is a dynamic, interactive, and cyclic process where doctors have to repeatedly decide on which clinical action to perform and consider newly uncovered information for diagnosis and treatment. Large Language Models (LLMs) have the potential to support clinicians in this process, however, most applications of LLMs in clinical decision support suffer from one of two limitations: Either they assume the unrealistic scenario of immediate availability of all patient information and do not model the interactive and iterative investigation process, or they restrict themselves to the limited "out-of-the-box" capabilities of large pre-trained models without performing task-specific training. In contrast to this, we propose to model clinical decision-making for diagnosis with a hypothesis-driven uncertainty-aware language agent, LA-CDM, that converges towards a diagnosis via repeatedly requesting and interpreting relevant tests. Using a hybrid training paradigm combining supervised and reinforcement learning, we train LA-CDM with three objectives targeting critical aspects of clinical decision-making: accurate hypothesis generation, hypothesis uncertainty estimation, a*

- **AI decision:** `exclude` / `EC1`
- **AI reasoning:** Clinical diagnosis decision-support agent for medical practice, not scientific research work.
- **VERDICT:** 

## 29. arXiv:2512.03065 — Optimizing Life Sciences Agents in Real-Time using Reinforcement Learning

*Generative AI agents in life sciences face a critical challenge: determining the optimal approach for diverse queries ranging from simple factoid questions to complex mechanistic reasoning. Traditional methods rely on fixed rules or expensive labeled training data, neither of which adapts to changing conditions or user preferences. We present a novel framework that combines AWS Strands Agents with Thompson Sampling contextual bandits to enable AI agents to learn optimal decision-making strategies from user feedback alone. Our system optimizes three key dimensions: generation strategy selection (direct vs. chain-of-thought), tool selection (literature search, drug databases, etc.), and domain routing (pharmacology, molecular biology, clinical specialists). Through empirical evaluation on life science queries, we demonstrate 15-30\% improvement in user satisfaction compared to random baselines, with clear learning patterns emerging after 20-30 queries. Our approach requires no ground truth labels, adapts continuously to user preferences, and provides a principled solution to the exploration-exploitation dilemma in agentic AI systems.*

- **AI decision:** `exclude` / `EC1` (rule BR1)
- **AI reasoning:** Bandit-optimized life-science QA assistant serving user queries; no stage where the AI produces substantive research output.
- **VERDICT:** 

## 30. arXiv:2605.18144 — Evidence-Grounded Frontier Mapping and Agentic Hypothesis Generation in Nanomedicine

*Nanomedicine research spans delivery chemistry, immunology, imaging, biomaterials, and disease-specific translational science, yet its conceptual design space remains fragmented across a large and heterogeneous literature. To date, artificial intelligence in nanomedicine has focused primarily on property prediction and formulation optimization, with much less attention to evidence-grounded discovery support at the level of research direction selection. We introduce pArticleMap, a literature-mapping and research-hypothesis-generation system that combines article embeddings, similarity-graph analysis, sparse frontier extraction, structured evidence-pack retrieval, and an audited large-language-model (LLM) workflow for grounded ideation. Rather than forecasting future concept co-occurrence, pArticleMap targets low-density article-level bridge regions and cluster interfaces, then generates and scores citation-grounded hypotheses with large language models in an agentic setup. We evaluate the system with a retrospective realization benchmark (generate later literature under a historical cutoff) and a blinded human reader assessment layer across cue-conditioned nanomedicine tasks. Across*

- **AI decision:** `include` / `IC1` (rule BR2)
- **AI reasoning:** Agentic system that itself generates and scores citation-grounded scientific hypotheses in nanomedicine, with retrospective evaluation.
- **VERDICT:** 

## 31. arXiv:2604.28031 — Models Recall What They Violate: Constraint Adherence in Multi-Turn LLM Ideation

*When researchers iteratively refine ideas with large language models, do the models preserve fidelity to the original objective? We introduce DriftBench, a benchmark for evaluating constraint adherence in multi-turn LLM-assisted scientific ideation. Across 2,146 scored benchmark runs spanning seven models from five providers (including two open-weight), four interaction conditions, and 38 research briefs from 24 scientific domains, we find that iterative pressure reliably increases structural complexity and often reduces adherence to original constraints. A restatement probe reveals a dissociation between declarative recall and behavioral adherence, as models accurately restate constraints they simultaneously violate. The knows-but-violates (KBV) rate, measuring constraint non-compliance despite preserved recall, ranges from 8% to 99% across models. Structured checkpointing partially reduces KBV rates but does not close the dissociation, and complexity inflation persists. Human validation against blind raters confirms that the LLM judge under-detects constraint violations, making reported constraint adherence scores conservative. Sensitivity analyses confirm the findings are robust*

- **AI decision:** `include` / `IC2` (rule BR2)
- **AI reasoning:** Benchmark evaluating LLM behavior in multi-turn scientific ideation across real research briefs from 24 scientific domains.
- **VERDICT:** 

## 32. arXiv:2512.16969 — Probing Scientific General Intelligence of LLMs with Scientist-Aligned Workflows

*Despite advances in scientific AI, a coherent framework for Scientific General Intelligence (SGI)-the ability to autonomously conceive, investigate, and reason across scientific domains-remains lacking. We present an operational SGI definition grounded in the Practical Inquiry Model (PIM: Deliberation, Conception, Action, Perception) and operationalize it via four scientist-aligned tasks: deep research, idea generation, dry/wet experiments, and experimental reasoning. SGI-Bench comprises over 1,000 expert-curated, cross-disciplinary samples inspired by Science's 125 Big Questions, enabling systematic evaluation of state-of-the-art LLMs. Results reveal gaps: low exact match (10--20%) in deep research despite step-level alignment; ideas lacking feasibility and detail; high code executability but low execution result accuracy in dry experiments; low sequence fidelity in wet protocols; and persistent multimodal comparative-reasoning challenges. We further introduce Test-Time Reinforcement Learning (TTRL), which optimizes retrieval-augmented novelty rewards at inference, enhancing hypothesis novelty without reference answer. Together, our PIM-grounded definition, workflow-centric benchm*

- **AI decision:** `include` / `IC2`
- **AI reasoning:** SGI-Bench evaluates LLMs on scientist-aligned research workflows spanning deep research, ideation, experiments, and reasoning.
- **VERDICT:** 

## 33. arXiv:2606.19893 — MetaResearcher: Scaling Deep Research via Self-Reflective Reinforcement Learning in Adversarial Virtual Environments

*Deep research agents have demonstrated remarkable capabilities in autonomous information gathering and synthesis, yet their training remains constrained by the static nature of simulated environments, the limits of fact-retrieval-only task designs, and the inefficiency of outcome-based reinforcement learning. In this work, we propose MetaResearcher, a novel framework that scales deep research agent training across four synergistic dimensions. First, we introduce an Evolving Virtual World that injects temporal dynamics and adversarial misinformation into the training environment, forcing agents to develop source credibility assessment and temporal conflict resolution skills. Second, we design Discovery-Oriented Tasks -- including hypothesis generation and contradiction resolution -- that transcend simple fact retrieval and push agents toward genuine research behaviors. Third, we propose a Self-Reflective Meta-Reward mechanism within the GRPO framework that jointly optimizes for answer correctness, search path efficiency, reflection depth, and tool call diversity, directly addressing the repetitive action loop problem observed in prior work. Fourth, we introduce a Heterogeneous Multi*

- **AI decision:** `exclude` / `EC9_GENERIC_DEEPRESEARCH` (rule BR7)
- **AI reasoning:** RL training framework for general deep-research/information-gathering agents evaluated on generic benchmarks (GAIA, Xbench-DS).
- **VERDICT:** 

## 34. arXiv:2606.17029 — DEEPRUBRIC: Evidence-Tree Rubric Supervision for Efficient Reinforcement Learning of Deep Research Agents

*Deep research agents synthesize long-form reports by searching and reasoning over retrieved evidence. Reinforcement learning with rubric-based rewards improves these agents by optimizing them against checkable criteria that translate report quality into reward signals, but its efficiency depends on whether those criteria reliably capture the task scope and evidence needs. Most existing studies ask an LLM to generate rubrics for a given query, but when the model fails to infer the underlying information needs, the generated rubrics may be incomplete and reduce RL efficiency. To obtain more reliable query--rubric supervision, we introduce DeepRubric, a data construction framework that reverses this process: instead of inferring evaluation criteria for a given query, it first determines what an evidence-backed report should be evaluated on and then synthesizes aligned query--rubric pairs from those evaluation targets. Starting from a sampled seed topic, DeepRubric builds an evidence tree by recursively expanding evidence-backed sub-questions, whose leaves serve as atomic and verifiable evaluation targets. It then uses the evidence tree to synthesize the training query and rubrics, ens*

- **AI decision:** `exclude` / `EC9_GENERIC_DEEPRESEARCH` (rule BR7)
- **AI reasoning:** RL rubric-supervision data for generic deep-research report agents evaluated on general deep-research benchmarks, not scientific research work.
- **VERDICT:** 

## 35. arXiv:2604.03159 — BibTeX Citation Hallucinations in Scientific Publishing Agents: Evaluation and Mitigation

*Large language models with web search are increasingly used in scientific publishing agents, yet they still produce BibTeX entries with pervasive field-level errors. Prior evaluations tested base models without search, which does not reflect current practice. We construct a benchmark of 931 papers across four scientific domains and three citation tiers -- popular, low-citation, and recent post-cutoff -- designed to disentangle parametric memory from search dependence, with version-aware ground truth accounting for multiple citable versions of the same paper. Three search-enabled frontier models (GPT-5, Claude Sonnet-4.6, Gemini-3 Flash) generate BibTeX entries scored on nine fields and a six-way error taxonomy, producing ~23,000 field-level observations. Overall accuracy is 83.6%, but only 50.9% of entries are fully correct; accuracy drops 27.7pp from popular to recent papers, revealing heavy reliance on parametric memory even when search is available. Field-error co-occurrence analysis identifies two failure modes: wholesale entry substitution (identity fields fail together) and isolated field error. We evaluate clibib, an open-source tool for deterministic BibTeX retrieval from t*

- **AI decision:** `include` / `IC2` (rule BR5)
- **AI reasoning:** Benchmark and mitigation for citation hallucinations produced by LLM scientific-writing/publishing agents, an integrity evaluation of AI research pipelines.
- **VERDICT:** 

## 36. arXiv:2602.07943 — IV Co-Scientist: Multi-Agent LLM Framework for Causal Instrumental Variable Discovery

*In the presence of confounding between an endogenous variable and the outcome, instrumental variables (IVs) are used to isolate the causal effect of the endogenous variable. Identifying valid instruments requires interdisciplinary knowledge, creativity, and contextual understanding, making it a non-trivial task. In this paper, we investigate whether large language models (LLMs) can aid in this task. We perform a two-stage evaluation framework. First, we test whether LLMs can recover well-established instruments from the literature, assessing their ability to replicate standard reasoning. Second, we evaluate whether LLMs can identify and avoid instruments that have been empirically or theoretically discredited. Building on these results, we introduce IV Co-Scientist, a multi-agent system that proposes, critiques, and refines IVs for a given treatment-outcome pair. We also introduce a statistical test to contextualize consistency in the absence of ground truth. Our results show the potential of LLMs to discover valid instrumental variables from a large observational database.*

- **AI decision:** `include` / `IC1` (rule BR2)
- **AI reasoning:** Multi-agent co-scientist that proposes, critiques, and refines instrumental variables — machine generation of scientific hypotheses in causal inference.
- **VERDICT:** 

## 37. arXiv:2606.11045 — What Fits (Into Few Tokens) Doesn't Overfit: Compression and Generalization in ML Research Agents

*Reusing a held-out benchmark adaptively should, in principle, invite overfitting. Yet benchmark-driven machine learning (ML) has produced surprisingly little overfitting in practice. An attractive hypothesis is that successful ML strategies are highly compressible. We study this in the setting of LLM-driven research agents, where the hypothesis becomes directly testable via two complementary information bottlenecks. In \emph{output compression}, an exploration agent adaptively searches for high-performance models using a validation set, and we test whether a fresh ``reproducer agent'' can reproduce its performance given only an extremely short prompt and the training data. In \emph{input compression}, the explorer receives only one-bit feedback indicating whether each submitted model improves on the running best. Across 8 datasets spanning tabular classification, vision, language modeling, diffusion modeling, and reward modeling, we find that these bottlenecks have little effect on performance: short prompts and compressible feedback are sufficient to reproduce and find high-performance models. The hypothesis is falsifiable: when we deliberately induce validation-set overfitting, t*

- **AI decision:** `exclude` / `EC8_GENERIC_ANALYSIS` (rule BR6)
- **AI reasoning:** Studies agents searching for high-performing ML models on generic benchmark datasets, ML engineering not scientific research.
- **VERDICT:** 

## 38. arXiv:2506.05999 — Machine learning for in-situ composition mapping in a self-driving magnetron sputtering system

*Self-driving labs (SDLs), employing automation and machine learning (ML) to accelerate experimental procedures, have enormous potential in the discovery of new materials. However, in thin film science, SDLs are mainly restricted to solution-based synthetic methods which are easier to automate but cannot access the broad chemical space of inorganic materials. This work presents an SDL based on magnetron co-sputtering. We are using combinatorial frameworks, obtaining accurate composition maps on multi-element, compositionally graded thin films. This normally requires time-consuming ex-situ analysis prone to systematic errors. We present a rapid and calibration-free in-situ, ML driven approach to produce composition maps for arbitrary source combinations and sputtering conditions. We develop a method to predict the composition distribution in a multi-element combinatorial thin film, using in-situ measurements from quartz-crystal microbalance sensors placed in a sputter chamber. For a given source, the sensor readings are learned as a function of the sputtering pressure and magnetron power, through active learning using Gaussian processes (GPs). The final GPs are combined with a geomet*

- **AI decision:** `include` / `IC1` (rule BR4)
- **AI reasoning:** Self-driving lab whose active-learning loop autonomously decides which sputtering experiments to run next from prior results, as the paper's subject.
- **VERDICT:** 

## 39. arXiv:2602.01075 — ConvexBench: Can LLMs Recognize Convex Functions?

*Convex analysis is a modern branch of mathematics with many applications. As Large Language Models (LLMs) start to automate research-level math and sciences, it is important for LLMs to demonstrate the ability to understand and reason with convexity. We introduce \cb, a scalable and mechanically verifiable benchmark for testing \textit{whether LLMs can identify the convexity of a symbolic objective under deep functional composition.} Experiments on frontier LLMs reveal a sharp compositional reasoning gap: performance degrades rapidly with increasing depth, dropping from an F1-score of $1.0$ at depth $2$ to approximately $0.2$ at depth $100$. Inspection of models' reasoning traces indicates two failure modes: \textit{parsing failure} and \textit{lazy reasoning}. To address these limitations, we propose an agentic divide-and-conquer framework that (i) offloads parsing to an external tool to construct an abstract syntax tree (AST) and (ii) enforces recursive reasoning over each intermediate sub-expression with focused context. This framework reliably mitigates deep-composition failures, achieving substantial performance improvement at large depths (e.g., F1-Score $= 1.0$ at depth $100*

- **AI decision:** `exclude` / `EC1` (rule BR2)
- **AI reasoning:** Benchmark of LLM convexity/compositional reasoning as such, not an autonomous research system or its evaluation.
- **VERDICT:** 

## 40. arXiv:2512.14220 — Estimating problem difficulty without ground truth using Large Language Model comparisons

*Recent advances in the finetuning of large language models (LLMs) have significantly improved their performance on established benchmarks, emphasizing the need for increasingly difficult, synthetic data. A key step in this data generation pipeline is a method for estimating problem difficulty. Current approaches, such as human calibration or performance-based scoring, fail to generalize to out-of-distribution problems, i.e. problems currently unsolvable by humans and LLMs, because they are not scalable, time-consuming, and ground truth dependent. Therefore, we propose a new method for estimating problem difficulty, LLM compare, that addresses these limitations. An LLM performs pairwise difficulty comparisons, and then Bradley-Terry scores are computed based on the outcomes. To validate our method, we first propose a conceptual framework that positions existing approaches on three orthogonal planes--construction, scale and dependence--identifying which quadrants a measure needs to occupy to score out-of-distribution problems. LLM compare naturally occupies all desirable quadrants as the first measure that is continuous and dynamic, model-agnostic and independent of ground truth info*

- **AI decision:** `exclude` / `EC1`
- **AI reasoning:** LLM-based problem-difficulty estimation for synthetic data pipelines, not an autonomous research system or benchmark for one.
- **VERDICT:** 
